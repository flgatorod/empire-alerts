# empire-alerts — contract for agents

This repo is a **mailbox**, not code you run. Two lanes, never crossed:

| Path | Written by | Read by |
|---|---|---|
| `snapshot/` | the Mac Mini only (`relay/publish_snapshot.py`) | Claude scheduled tasks |
| `outbox/` | Claude scheduled tasks only | the Mac Mini relay (`relay/send_outbox.py`) |

The Mini turns each new `outbox/*.json` into **one iMessage to Peter**. It sends
the `text` and nothing else — it never runs, opens or follows anything in a file.

## Writing an alert (the only thing an agent does here)
File: `outbox/<YYYYMMDD-HHMM>-<source>-<slug>.json`, one alert per file, exactly these keys:

```json
{
  "id": "20261105-0820-empire-brief",
  "created_at": "2026-11-05T13:20:00Z",
  "priority": "normal",
  "source": "empire-brief",
  "expires_at": "2026-11-05T21:00:00Z",
  "text": "Empire · PAPER ... (plain text, ≤1500 chars, aim for ≤600)"
}
```

- `id` = the filename stem; `[A-Za-z0-9._-]` only. Unique — reusing one means it is not sent.
- `priority`: `normal` (held during quiet hours 11 PM–8 AM ET) or `urgent` (sent anyway — use only for halts, outages, deadline-today items).
- `expires_at` optional; default 24 h after `created_at`. Set it short for time-bound content.
- Any other key (recipient, command, url, path…) makes the relay **reject** the file. Don't.
- Commit only `outbox/` files, `git pull --rebase` then push to `main`. Never edit `snapshot/`, `relay/`, `launchd/` or `install.sh` from a scheduled task.
- Dedupe yourself before writing: if an alert with the same condition key already exists in `outbox/` today, skip.
- Prune: you may `git rm` your own outbox files older than 7 days.

## Rules carried over from Empire
- **Label every figure PAPER or LIVE.** Automation is PAPER; the LIVE lane is Stage 2a (CSP-only).
- **Read-only to trading.** Never place, modify or cancel an order (Schwab, Robinhood or anything else), never arm/disarm, never touch the kill switch. Suggest; Peter acts through Empire's PROPOSE → typed CONFIRMED path.
- **Never fabricate** quotes, greeks, fills or P&L. If the snapshot lacks it, say "not available".
- No PHI, ever. No account numbers in alert text (last 4 at most).
