"""Relay safety tests. Run: python3 tests/test_relay.py  (no network, no sends)."""

import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

TMP = Path(tempfile.mkdtemp())
os.environ.update(RELAY_REPO=str(TMP), RELAY_STATE_DIR=str(TMP / "state"),
                  RELAY_CONFIG=str(TMP / "config.json"), RELAY_SEND_SINK="1")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "relay"))
import send_outbox as s  # noqa: E402
import publish_snapshot as p  # noqa: E402

SENT = []
s.send_imessage = lambda text, rcpt: SENT.append(text) or True
CFG = {**s.load_config(), "recipient": "+15555550100"}
OUT = TMP / "outbox"
RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)


def reset():
    shutil.rmtree(TMP / "state", ignore_errors=True)
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    SENT.clear()


def put(name, **kw):
    now = kw.pop("_now", datetime(2026, 11, 5, 15, 0, tzinfo=timezone.utc))
    d = {"id": name, "created_at": now.isoformat(), "priority": "normal", "text": f"hello {name}"}
    d.update(kw)
    (OUT / f"{name}.json").write_text(json.dumps(d))


NOON = datetime(2026, 11, 5, 17, 0, tzinfo=timezone.utc)      # 12:00 ET
NIGHT = datetime(2026, 11, 6, 4, 0, tzinfo=timezone.utc)      # 23:00 ET
run = lambda now=NOON, cfg=CFG: s.process(cfg, now=now, do_pull=False)

reset(); put("a1"); run()
check("sends a valid alert with the prefix", SENT == ["Claude · hello a1"])
run()
check("never sends the same file twice", len(SENT) == 1)

reset(); put("b1", recipient="+19999999999"); put("b2", command="rm -rf ~"); run()
check("rejects files naming a recipient or carrying extra keys", SENT == [])
led = json.loads((TMP / "state/sent.json").read_text())["handled"]
check("rejections are recorded, not retried", all("rejected" in v["result"] for v in led.values()))

reset(); (OUT / "c1.json").write_text("not json {"); put("c2", priority="high"); put("c3", text="x" * 1600)
put("c4", id="../../etc/passwd"); put("c5", created_at="2026-11-05 10:00"); run()
check("rejects malformed json, bad priority, oversize text, bad id, naive timestamp", SENT == [])

reset(); put("d1", text="same"); put("d2", text="same"); run()
check("dedupes identical text within 6h", len(SENT) == 1)

reset(); put("e1", text="first", id="dup"); (OUT / "e2.json").write_text(json.dumps(
    {"id": "dup", "created_at": NOON.isoformat(), "priority": "normal", "text": "second"})); run()
check("dedupes a reused id", SENT == ["Claude · first"])

reset(); put("f1", _now=NOON - timedelta(hours=30)); run()
check("drops alerts past the default 24h expiry", SENT == [])
reset(); put("f2", expires_at=(NOON - timedelta(minutes=1)).isoformat()); run()
check("honors an explicit expires_at", SENT == [])

reset(); put("g1", _now=NIGHT); put("g2", _now=NIGHT, priority="urgent"); run(NIGHT)
check("quiet hours hold normal, pass urgent", SENT == ["Claude · hello g2"])
run(NIGHT + timedelta(hours=9, minutes=5))  # 8:05 AM ET next morning
check("held alert goes out after quiet hours", SENT == ["Claude · hello g2", "Claude · hello g1"])

reset()
for i in range(10):
    put(f"h{i}", text=f"msg {i}")
run()
check("per-run cap (3)", len(SENT) == 3)
run(NOON + timedelta(minutes=2)); run(NOON + timedelta(minutes=4))
check("per-hour cap (6)", len(SENT) == 6)
run(NOON + timedelta(minutes=70))
check("resumes after the hour window", len(SENT) == 9)

reset(); (OUT / "i1.json").write_text(json.dumps(
    {"id": "i1", "created_at": NOON.isoformat(), "priority": "normal", "text": "a\x07b\x1b[31m"})); run()
check("strips control characters", SENT == ["Claude · ab[31m"])

hb = json.loads((TMP / "state/relay_heartbeat.json").read_text())
check("writes a heartbeat", hb["last_poll"].startswith("2026-11-05"))

# scrub
scrubbed = p.scrub({"account_number": "12345678", "acct": "Schwab 87654321 cash", "value": 25000.5,
                    "nested": [{"hashValue": "ABC", "ticker": "DELL"}], "recipient": "+1555"})
check("scrub drops account/recipient keys and redacts 8+ digit runs",
      scrubbed == {"acct": "Schwab [redacted] cash", "value": 25000.5, "nested": [{"ticker": "DELL"}]})
check("in_quiet_hours wraps midnight", s.in_quiet_hours(NIGHT.astimezone(s.ET), CFG)
      and not s.in_quiet_hours(NOON.astimezone(s.ET), CFG))

shutil.rmtree(TMP, ignore_errors=True)
bad = [n for n, ok in RESULTS if not ok]
print(f"\nRELAY TESTS: {len(RESULTS) - len(bad)}/{len(RESULTS)} green")
sys.exit(1 if bad else 0)
