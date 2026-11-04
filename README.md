# empire-alerts

Replaces Hyperion's Empire Trading layer now that it no longer runs on OpenClaw.
Claude's scheduled tasks (cloud) and the Mac Mini talk through this private repo:

```
Mac Mini ──snapshot/STATUS.json, BRIEFING.md──▶ GitHub ──▶ Claude scheduled tasks
Mac Mini ◀── iMessage ◀── relay ◀── outbox/*.json ◀── GitHub ◀── Claude scheduled tasks
```

| Piece | Where | Schedule |
|---|---|---|
| `relay/publish_snapshot.py` | Mini, launchd `com.empire-alerts.snapshot` | every 15 min (pushes only on change; refresh ≥ every 30 min market hours / 60 min otherwise) |
| `relay/send_outbox.py` | Mini, launchd `com.empire-alerts.relay` | every 2 min |
| Empire pre-market brief | Claude scheduled task | weekdays 8:24 AM ET |
| Empire after-close recap | Claude scheduled task | weekdays 4:47 PM ET |
| Empire watchdog | Claude scheduled task | hourly 8:07 AM–8:07 PM ET, daily |

Empire's own launchd alerts (paper closes, regime monitor, breakers, backup failures, its 8 AM
briefing) are untouched and still text you directly. Texts from this relay start with **"Claude · "**.

## Install on the Mini (once)
```bash
cd ~ && git clone https://github.com/flgatorod/empire-alerts.git && cd empire-alerts
./install.sh          # first run creates config.json and stops
open -e config.json   # set "recipient" to the number/Apple ID that gets Empire's texts
./install.sh          # loads both launchd jobs
./install.sh --test   # sends one real test text
python3 tests/test_relay.py   # 18 safety tests, no sends
```
The Mini needs push access to this repo (same git credentials it uses for empire-trading).
Messages must stay signed in on the Mini with the Apple ID Hyperion used.

## Safety
- One recipient, set only in the Mini's gitignored `config.json`. Alert files can't name one.
- Text only: nothing in `outbox/` is executed, opened or used as a path. Strict schema; anything else is rejected.
- Dedupe by id and by identical text (6 h), caps of 3/run, 6/hour, 25/day, quiet hours 11 PM–8 AM ET (urgent bypasses), 24 h default expiry.
- The snapshot job only reads Empire (localhost API, handoff file, logs, `launchctl list`); it never writes Empire files or touches the kill switch, ARM_LIVE or the order path. 8+ digit numbers and account/recipient keys are stripped before publishing.
- Claude's tasks are read-only to trading and must label figures PAPER/LIVE. See `CLAUDE.md`.

## Troubleshooting
- `tail -f logs/relay.log logs/snapshot.log` · `launchctl list | grep empire-alerts`
- Pause: `./install.sh --uninstall` (keeps config/state). Dry run: `RELAY_SEND_SINK=1 python3 relay/send_outbox.py`.
- If texts fail with an osascript error, open Messages on the Mini once and confirm it's signed in.
