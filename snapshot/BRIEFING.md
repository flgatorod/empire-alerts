# Empire Daily Briefing — 2026-11-23
_Generated 2026-11-23 08:00:04 _

## 1. Market State

- **VIX** 31.39 (-12.54% vs prev close)
- **S&P 500** ~7,070 (SPY $707.03, +2.50%)
- **Oil (USO)** $136.89 (-1.96%)
- **BTC (IBIT)** $34.68 (+5.03%)
- **Regime**: MODERATE
  > MODERATE (owner ruling 2026-11-06, EFFECTIVE 2026-11-05, recorded 2026-11-06): the ruled `to_moderate` trigger breached on the 2026-11-05 close, VIX 28.18 > 27 — the only close above 27 in 65 recorded sessions, reached from a 16.61 close the session before. 5-day avg 21.24, 14-day 19.08, 16 of 65 closes above 17, 3 above 20. Posture knobs UNCHANGED and NO-RETRO: 65/85 edge floors, 7-day earnings blackout, semi block, csp_vix_minimum 14, 50% target / 2.0x stop / 0.70 roll / 1-DTE time stop all hold. The C2 CSP floor is NOT binding in this band (VIX 28.18, 14.18 points clear) — cohort quality, not volatility, is still the constraint. NOTHING HAS OPENED SINCE 2026-10-29: the kill switch has been tripped since 2026-11-03 and the reset is Peter's typed action. READ THE BREACH WITH ITS CAVEATS: it is single-armed, and 'sustained' with no day count is a single-close check — under a 2-day reading it is not breached. SEPARATELY: the six trigger questions are DEFERRED to a trigger-table v2 spec after the deploy reference (owner ruling 2026-11-06 evening, item C). The label is NARRATIVE ONLY — csp_enabled and csp_vix_minimum are the only regime knobs that gate, both unchanged — so an odd direction word is a wrong sentence, not a wrong trade. The watcher's private band table is GONE: its ladder now derives from this file's own regime_change_triggers (#85, closed).
- **Sector leaders**: Tech +3.73%, Comms +2.69%, Indust +2.24%
- **Sector laggards**: Discr +0.00%, Health +0.47%, Staples +0.49%
- **Triggers armed**:
  - ⚠ VIX 31.4 ≥ 20 (would arm LOW-ELEVATED)

## 2. Open Positions

**0 open** — 🔴0 🟠0 🟡0 🟢0

_No open positions._

## 3. Events This Week

- **Fri 11/27** — OPEX: Weekly Options Expiration
- **Fri 12/04** — OPEX: Weekly Options Expiration
- Tue 11/24 — BABA earnings — BABA Earnings Report
- Tue 11/24 — DELL earnings — DELL Earnings Report
- Wed 11/25 — DE earnings — DE Earnings Report
- Fri 11/27 — DELL earnings — DELL Earnings Report
- ✓ No earnings inside current option windows

## 4. Paper Trading Activity

- **Open**: 15 single-leg + 10 spreads
- **Yesterday**: +0 opens, 0 closes ($0.00 realized)
- **Total closed**: 305 (71% win rate, $2,094.00 total PnL)
- **Real-eligible vs paper-only**: 185 real / 135 paper
  - real_eligible: 185 opened, 170 closed, win_rate=65%, avg=$-17
  - paper_only: 135 opened, 135 closed, win_rate=78%, avg=$37

## 5. Action Items

✓ All positions stable, no action required.

## 6. System Health

- ⚠ Token: 6d old, 1d remaining (source: refresh_token_issued) — warn
- ✓ Dashboard: 277ms
- ✓ Launchd jobs loaded: 29 com.empire.*
- Positions sync: 1-20 16:00:06,594 [empire.positions_sync] INFO: === SYNC COMPLETE: 0 closed, 0 inserted, drift 0 ===
- ✓ No recent errors in *.err logs
