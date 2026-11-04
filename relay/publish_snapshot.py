#!/usr/bin/env python3
"""empire-alerts snapshot — publish Empire's state for Claude to read.

Runs on the Mac Mini every 15 minutes (launchd com.empire-alerts.snapshot).
Replaces Hyperion's old window into Empire with the same publish-not-share
rule: this job READS Empire (localhost API, handoff file, logs, launchctl) and
WRITES ONLY snapshot/ in this repo. It never touches Empire's files, state,
kill switch, ARM_LIVE or the order path, and never runs an Empire job.

Writes:
  snapshot/STATUS.json   machine-readable (health, gate, ops, KPI, positions, jobs, relay)
  snapshot/BRIEFING.md   copy of Empire's newest daily briefing
Pushes when something changed; during off hours at most hourly.

Privacy: 8+ digit numbers (account numbers) are redacted and keys that look
like account ids / recipients are dropped before anything is written.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ET, REPO, STATE, RepoLock, git, load_config, log,  # noqa: E402
                    now_utc, read_json, write_json_atomic)

SNAP = REPO / "snapshot"
ENDPOINTS = {"health": "/api/health", "gate": "/api/gate",
             "ops": "/api/ops/health", "kpi": "/api/kpi"}
MAX_ENDPOINT_BYTES = 150_000
DROP_KEY_RE = re.compile(r"(account_?(number|num|hash|id)|hash_?value|recipient|phone|token|secret|password)", re.I)
LONG_DIGITS_RE = re.compile(r"(?<![\d.])\d{8,}(?![\d.])")
LOG_FLAG_RE = re.compile(r"ERROR|FAILED|Traceback|CRITICAL", re.I)


def scrub(obj):
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items() if not DROP_KEY_RE.search(str(k))}
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    if isinstance(obj, str):
        return LONG_DIGITS_RE.sub("[redacted]", obj)
    if isinstance(obj, int) and not isinstance(obj, bool) and abs(obj) >= 10**7 and obj == int(obj):
        # bare 8+ digit integers are account numbers far more often than dollars here
        return "[redacted]"
    return obj


def fetch(base: str, path: str) -> dict:
    try:
        with urllib.request.urlopen(base + path, timeout=25) as r:
            raw = r.read(MAX_ENDPOINT_BYTES + 1)
        if len(raw) > MAX_ENDPOINT_BYTES:
            return {"error": f"response larger than {MAX_ENDPOINT_BYTES} bytes — omitted"}
        return json.loads(raw)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"[:300]}


def file_age_min(p: Path):
    try:
        return round((datetime.now().timestamp() - p.stat().st_mtime) / 60, 1)
    except FileNotFoundError:
        return None


def launchd_jobs() -> list:
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=15).stdout
    except Exception as e:
        return [{"error": str(e)}]
    jobs = []
    for line in out.splitlines()[1:]:
        parts = line.split(None, 2)
        if len(parts) == 3 and (parts[2].startswith("com.empire") or parts[2].startswith("com.poolpicks")):
            pid, status, label = parts
            jobs.append({"label": label, "running": pid != "-",
                         "last_exit": int(status) if status.lstrip("-").isdigit() else status})
    return sorted(jobs, key=lambda j: j.get("label", ""))


def log_flags(log_dir: Path, today: str) -> dict:
    """Today's ERROR/FAILED lines per Empire log: a count and the last 3 (trimmed)."""
    flags = {}
    for p in sorted(log_dir.glob("*.log")):
        if file_age_min(p) is not None and file_age_min(p) > 60 * 26:
            continue
        try:
            lines = p.read_text(errors="replace").splitlines()[-400:]
        except Exception:
            continue
        hits = [l for l in lines if today in l and LOG_FLAG_RE.search(l)]
        if hits:
            flags[p.name] = {"count_today": len(hits), "last": [h[:300] for h in hits[-3:]]}
    return flags


def newest_briefing(empire: Path):
    files = sorted((empire / "briefings").glob("*-daily.md"))
    return files[-1] if files else None


def build(cfg: dict) -> tuple[dict, str]:
    now = now_utc()
    empire = Path(cfg["empire_dir"]).expanduser()
    handoff_path = Path(cfg["handoff_path"]).expanduser()
    status = {
        "generated_at": now.isoformat(),
        "generated_at_et": now.astimezone(ET).strftime("%Y-%m-%d %H:%M %Z"),
        "lane_note": "Automation is PAPER. LIVE lane = Stage 2a (CSP-only, typed CONFIRMED). "
                     "Label every figure PAPER or LIVE.",
        "dashboard": {name: fetch(cfg["empire_api"], path) for name, path in ENDPOINTS.items()},
        "positions_handoff": read_json(handoff_path, {"error": f"missing: {handoff_path.name}"}),
        "positions_handoff_age_min": file_age_min(handoff_path),
        "kill_switch_flag_present": (empire / "state" / "HALT.flag").exists(),
        "launchd_jobs": launchd_jobs(),
        "log_flags_today": log_flags(empire / "logs", now.astimezone(ET).strftime("%Y-%m-%d")),
        "relay_heartbeat": read_json(STATE / "relay_heartbeat.json", {}),
    }
    b = newest_briefing(empire)
    status["briefing"] = {"file": b.name if b else None, "age_min": file_age_min(b) if b else None}
    briefing = scrub(b.read_text(errors="replace"))[:60_000] if b else "_No Empire briefing found._\n"
    return scrub(status), briefing


def material(d: dict) -> dict:
    """Status minus fields that change every run, to decide whether to push."""
    d = json.loads(json.dumps(d))
    for k in ("generated_at", "generated_at_et", "relay_heartbeat"):
        d.pop(k, None)
    d.pop("positions_handoff_age_min", None)
    d.get("briefing", {}).pop("age_min", None)
    return d


def market_hours(now_et: datetime) -> bool:
    return now_et.weekday() < 5 and 8 <= now_et.hour < 18


def main() -> int:
    cfg = load_config()
    status, briefing = build(cfg)
    try:
        with RepoLock():
            git("pull", "--rebase", "--quiet", "origin", "main")
            prev = read_json(SNAP / "STATUS.json", {})
            bpath = SNAP / "BRIEFING.md"
            old_briefing = bpath.read_text(errors="replace") if bpath.exists() else None
            changed = material(prev) != material(status) or old_briefing != briefing
            last = prev.get("generated_at")
            age = (now_utc() - datetime.fromisoformat(last)) if last else timedelta(days=1)
            now_et = now_utc().astimezone(ET)
            # Always refresh at least every 30 min in market hours / 60 min otherwise,
            # so a stale snapshot means "the Mini stopped", never "nothing changed".
            max_quiet = timedelta(minutes=30 if market_hours(now_et) else 60)
            if not changed and age < max_quiet - timedelta(minutes=2):
                return 0
            write_json_atomic(SNAP / "STATUS.json", status)
            (SNAP / "BRIEFING.md").write_text(briefing)
            git("add", "snapshot/STATUS.json", "snapshot/BRIEFING.md")
            c = git("-c", "user.name=Empire Mini", "-c", "user.email=empire-mini@localhost",
                    "commit", "-q", "-m", f"snapshot {status['generated_at_et']}")
            if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
                log("snapshot", f"ERROR commit: {(c.stderr or c.stdout)[:300]}")
                return 1
            p = git("push", "-q", "origin", "HEAD:main")
            if p.returncode != 0:
                git("pull", "--rebase", "--quiet", "origin", "main")
                p = git("push", "-q", "origin", "HEAD:main")
            if p.returncode != 0:
                log("snapshot", f"ERROR push: {p.stderr[:300]}")
                return 1
            log("snapshot", "pushed" + (" (changed)" if changed else " (refresh)"))
    except TimeoutError as e:
        log("snapshot", f"skip: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
