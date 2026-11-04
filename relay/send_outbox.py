#!/usr/bin/env python3
"""empire-alerts relay — deliver Claude's outbox alerts as iMessages.

Runs on the Mac Mini every 2 minutes (launchd com.empire-alerts.relay).

  1. git pull the repo (Claude's scheduled tasks push alerts to outbox/).
  2. For each outbox/*.json not already handled: validate it strictly.
  3. Send the TEXT ONLY, to the ONE recipient in the local config.json.

Safety properties (each enforced below, each tested in tests/test_relay.py):
  * One recipient. The alert file cannot name who gets it.
  * Text only. Nothing from the repo is ever executed, opened, or used as a path.
  * Strict schema. Unknown keys, wrong types, oversize text -> rejected, logged.
  * Dedupe by id AND by identical text within 6 hours.
  * Rate caps (per hour / per day / per run) so a bug can't flood the phone.
  * Quiet hours 11 PM-8 AM ET for normal alerts; urgent ones go through.
  * Expiry: an alert older than its expires_at (default 24 h) is dropped, so a
    Mini that was asleep for two days doesn't wake up and send stale briefs.
  * RELAY_SEND_SINK=1 prints instead of sending (for tests / dry runs).
The handled-ledger lives in state/ (gitignored), not in git, so the Mini never
has to push to mark something sent.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ET, REPO, STATE, RepoLock, git, load_config, log,  # noqa: E402
                    now_utc, read_json, write_json_atomic)

OUTBOX = REPO / "outbox"
LEDGER = STATE / "sent.json"
HEARTBEAT = STATE / "relay_heartbeat.json"
ALLOWED_KEYS = {"id", "created_at", "priority", "text", "source", "expires_at"}
REQUIRED_KEYS = {"id", "created_at", "priority", "text"}
ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
TEXT_DEDUPE_WINDOW = timedelta(hours=6)
PULL_FAIL_ALERT_AFTER = 15  # ~30 min of failed pulls -> one local alert per day


class Reject(Exception):
    pass


def _parse_ts(value, field: str) -> datetime:
    if not isinstance(value, str):
        raise Reject(f"{field} must be an ISO-8601 string")
    try:
        ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Reject(f"{field} is not ISO-8601: {value[:40]!r}")
    if ts.tzinfo is None:
        raise Reject(f"{field} must include a timezone offset")
    return ts


def validate(raw: str, cfg: dict) -> dict:
    """Return a clean alert dict or raise Reject. Never trusts the file."""
    if len(raw) > 20_000:
        raise Reject("file larger than 20 KB")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise Reject(f"not JSON: {e.msg}")
    if not isinstance(data, dict):
        raise Reject("top level must be an object")
    extra = set(data) - ALLOWED_KEYS
    if extra:
        raise Reject(f"unknown keys {sorted(extra)} (recipients/commands are never accepted)")
    missing = REQUIRED_KEYS - set(data)
    if missing:
        raise Reject(f"missing keys {sorted(missing)}")
    if not isinstance(data["id"], str) or not ID_RE.match(data["id"]):
        raise Reject("id must be 1-100 chars of [A-Za-z0-9._-]")
    if data["priority"] not in ("normal", "urgent"):
        raise Reject("priority must be 'normal' or 'urgent'")
    if not isinstance(data["text"], str):
        raise Reject("text must be a string")
    text = CTRL_RE.sub("", data["text"]).strip()
    if not text:
        raise Reject("text is empty")
    if len(text) > cfg["max_text_chars"]:
        raise Reject(f"text longer than {cfg['max_text_chars']} chars")
    source = data.get("source", "")
    if not isinstance(source, str) or len(source) > 40:
        raise Reject("source must be a string of at most 40 chars")
    created = _parse_ts(data["created_at"], "created_at")
    expires = (_parse_ts(data["expires_at"], "expires_at") if "expires_at" in data
               else created + timedelta(hours=cfg["max_age_hours"]))
    return {"id": data["id"], "priority": data["priority"], "text": text,
            "source": CTRL_RE.sub("", source), "created_at": created, "expires_at": expires}


def in_quiet_hours(now_et: datetime, cfg: dict) -> bool:
    start, end = cfg["quiet_start"], cfg["quiet_end"]
    h = now_et.hour
    return (h >= start or h < end) if start > end else (start <= h < end)


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def send_imessage(text: str, recipient: str) -> bool:
    """Send via Messages. Text and recipient are passed as argv, never spliced
    into AppleScript source, so no message content can become script."""
    sink = os.environ.get("RELAY_SEND_SINK", "").strip()
    if sink:
        print(f"[RELAY SEND SINK] would send to recipient:\n{text}")
        return True
    if not recipient:
        raise RuntimeError("no recipient in config.json — refusing to send")
    scripts = [
        # Same form Empire's notify.py uses (works on this Mini today) ...
        ['on run argv', 'tell application "Messages" to send (item 1 of argv) to buddy (item 2 of argv)', 'end run'],
        # ... and the newer form some macOS versions require.
        ['on run argv', 'tell application "Messages"',
         'set svc to 1st account whose service type = iMessage',
         'send (item 1 of argv) to participant (item 2 of argv) of svc', 'end tell', 'end run'],
    ]
    last_err = ""
    for lines in scripts:
        cmd = ["osascript"]
        for line in lines:
            cmd += ["-e", line]
        cmd += [text, recipient]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        except Exception as e:  # pragma: no cover - mac only
            last_err = str(e)
            continue
        if r.returncode == 0:
            return True
        last_err = r.stderr.strip()
    log("relay", f"ERROR osascript failed: {last_err[:300]}")
    return False


def pull() -> tuple[bool, str]:
    r = git("pull", "--rebase", "--quiet", "origin", "main")
    if r.returncode != 0:
        git("rebase", "--abort")
        return False, (r.stderr or r.stdout).strip()[:300]
    return True, ""


def process(cfg: dict, now=None, do_pull: bool = True) -> dict:
    now = now or now_utc()
    now_et = now.astimezone(ET)
    ledger = read_json(LEDGER, {"handled": {}, "sends": [], "pull_failures": 0,
                                "last_pull_alert": ""})
    hb = {"last_poll": now.isoformat(), "pull_ok": None, "pull_error": "",
          "sent_this_run": 0, "deferred": 0, "rejected_this_run": 0, "pending": 0}

    if do_pull:
        ok, err = pull()
        hb["pull_ok"], hb["pull_error"] = ok, err
        ledger["pull_failures"] = 0 if ok else ledger.get("pull_failures", 0) + 1
        if ok:
            hb["last_pull_ok"] = now.isoformat()
        else:
            log("relay", f"WARN git pull failed ({ledger['pull_failures']} in a row): {err}")

    # Keep the ledger bounded: forget handled ids after 30 days, sends after 2.
    cutoff = (now - timedelta(days=30)).isoformat()
    ledger["handled"] = {k: v for k, v in ledger["handled"].items() if v.get("at", "") >= cutoff}
    ledger["sends"] = [s for s in ledger["sends"]
                       if s["at"] >= (now - timedelta(days=2)).isoformat()]

    def sends_since(delta):
        t = (now - delta).isoformat()
        return sum(1 for s in ledger["sends"] if s["at"] >= t)

    def record_send(text, alert_id):
        ledger["sends"].append({"at": now.isoformat(), "hash": text_hash(text), "id": alert_id})
        hb["sent_this_run"] += 1

    # A relay that can't reach GitHub is a relay that silently stops: say so, once a day.
    if (ledger["pull_failures"] >= PULL_FAIL_ALERT_AFTER
            and ledger.get("last_pull_alert") != now_et.date().isoformat()):
        msg = (f"{cfg['prefix']}⚠️ Relay can't reach GitHub ({ledger['pull_failures']} failed "
               "pulls). Claude's alerts are waiting. Check the Mini's network / git auth.")
        if send_imessage(msg, cfg["recipient"]):
            ledger["last_pull_alert"] = now_et.date().isoformat()
            record_send(msg, "relay-pull-failure")

    files = sorted(OUTBOX.glob("*.json")) if OUTBOX.exists() else []
    quiet = in_quiet_hours(now_et, cfg)
    recent_hashes = {s["hash"] for s in ledger["sends"]
                     if s["at"] >= (now - TEXT_DEDUPE_WINDOW).isoformat()}

    for f in files:
        key = f.name
        if key in ledger["handled"]:
            continue
        try:
            alert = validate(f.read_text(errors="replace"), cfg)
        except Reject as e:
            ledger["handled"][key] = {"at": now.isoformat(), "result": f"rejected: {e}"}
            hb["rejected_this_run"] += 1
            log("relay", f"REJECT {key}: {e}")
            continue
        if alert["id"] in {v.get("id") for v in ledger["handled"].values()}:
            ledger["handled"][key] = {"at": now.isoformat(), "id": alert["id"], "result": "duplicate id"}
            continue
        if now > alert["expires_at"]:
            ledger["handled"][key] = {"at": now.isoformat(), "id": alert["id"], "result": "expired"}
            log("relay", f"EXPIRED {key} (created {alert['created_at']:%Y-%m-%d %H:%M})")
            continue
        body = cfg["prefix"] + alert["text"]
        if text_hash(body) in recent_hashes:
            ledger["handled"][key] = {"at": now.isoformat(), "id": alert["id"],
                                      "result": "duplicate text within 6h"}
            continue
        urgent = alert["priority"] == "urgent"
        if quiet and not urgent:
            hb["deferred"] += 1
            continue
        if (hb["sent_this_run"] >= cfg["max_per_run"]
                or sends_since(timedelta(hours=1)) >= cfg["max_per_hour"]
                or sends_since(timedelta(days=1)) >= cfg["max_per_day"]):
            hb["deferred"] += 1
            log("relay", f"RATE-CAP deferred {key}")
            continue
        if send_imessage(body, cfg["recipient"]):
            ledger["handled"][key] = {"at": now.isoformat(), "id": alert["id"], "result": "sent"}
            record_send(body, alert["id"])
            recent_hashes.add(text_hash(body))
            log("relay", f"SENT {key} ({alert['priority']}, {len(body)} chars)")
        else:
            hb["deferred"] += 1  # retried next poll; expiry stops endless retries

    hb["pending"] = sum(1 for f in files if f.name not in ledger["handled"])
    hb["sent_today"] = sum(1 for s in ledger["sends"]
                           if datetime.fromisoformat(s["at"]).astimezone(ET).date() == now_et.date())
    hb["pull_failures"] = ledger["pull_failures"]
    prev = read_json(HEARTBEAT, {})
    hb.setdefault("last_pull_ok", prev.get("last_pull_ok"))
    write_json_atomic(LEDGER, ledger)
    write_json_atomic(HEARTBEAT, hb)
    return hb


def main() -> int:
    cfg = load_config()
    if not cfg["recipient"] and not os.environ.get("RELAY_SEND_SINK"):
        log("relay", "ERROR no recipient in config.json — nothing can be delivered")
        return 2
    try:
        with RepoLock():
            hb = process(cfg)
    except TimeoutError as e:
        log("relay", f"skip: {e}")
        return 0
    if hb["sent_this_run"] or hb["rejected_this_run"]:
        log("relay", f"run: sent={hb['sent_this_run']} deferred={hb['deferred']} "
                     f"rejected={hb['rejected_this_run']} pending={hb['pending']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
