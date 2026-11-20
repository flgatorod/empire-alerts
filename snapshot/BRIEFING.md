# Empire Daily Briefing — 2026-11-20
_Generated 2026-11-20 08:00:02 _

## 1. Market State

- **VIX** 30.83 (+8.40% vs prev close)
- **S&P 500** ~7,096 (SPY $709.65, -0.87%)
- **Oil (USO)** $136.96 (-0.82%)
- **BTC (IBIT)** $34.78 (-0.85%)
- **Regime**: MODERATE
  > MODERATE (owner ruling 2026-11-06, EFFECTIVE 2026-11-05, recorded 2026-11-06): the ruled `to_moderate` trigger breached on the 2026-11-05 close, VIX 28.18 > 27 — the only close above 27 in 65 recorded sessions, reached from a 16.61 close the session before. 5-day avg 21.24, 14-day 19.08, 16 of 65 closes above 17, 3 above 20. Posture knobs UNCHANGED and NO-RETRO: 65/85 edge floors, 7-day earnings blackout, semi block, csp_vix_minimum 14, 50% target / 2.0x stop / 0.70 roll / 1-DTE time stop all hold. The C2 CSP floor is NOT binding in this band (VIX 28.18, 14.18 points clear) — cohort quality, not volatility, is still the constraint. NOTHING HAS OPENED SINCE 2026-10-29: the kill switch has been tripped since 2026-11-03 and the reset is Peter's typed action. READ THE BREACH WITH ITS CAVEATS: it is single-armed, and 'sustained' with no day count is a single-close check — under a 2-day reading it is not breached. SEPARATELY: the six trigger questions are DEFERRED to a trigger-table v2 spec after the deploy reference (owner ruling 2026-11-06 evening, item C). The label is NARRATIVE ONLY — csp_enabled and csp_vix_minimum are the only regime knobs that gate, both unchanged — so an odd direction word is a wrong sentence, not a wrong trade. The watcher's private band table is GONE: its ladder now derives from this file's own regime_change_triggers (#85, closed).
- **Sector leaders**: Staples +1.26%, Utilities +0.62%, Health +0.57%
- **Sector laggards**: Tech -2.39%, Comms -0.69%, Discr -0.64%
- **Triggers armed**:
  - ⚠ VIX 30.8 ≥ 20 (would arm LOW-ELEVATED)

## 2. Open Positions

**0 open** — 🔴0 🟠0 🟡0 🟢0

_No open positions._

## 3. Events This Week

- **Fri 11/20** — Monthly opex Friday
- **Fri 11/20** — OPEX: Monthly Options Expiration (Nov 2026)
- **Fri 11/27** — OPEX: Weekly Options Expiration
- **Fri 12/04** — OPEX: Weekly Options Expiration
- Tue 11/24 — BABA earnings — BABA Earnings Report
- Tue 11/24 — DELL earnings — DELL Earnings Report
- Wed 11/25 — DE earnings — DE Earnings Report
- Fri 11/27 — DELL earnings — DELL Earnings Report
- ✓ No earnings inside current option windows

## 4. Paper Trading Activity

- **Open**: 14 single-leg + 10 spreads
- **Yesterday**: +8 opens, 8 closes ($-648.00 realized)
- **Total closed**: 300 (72% win rate, $2,598.00 total PnL)
- **Real-eligible vs paper-only**: 179 real / 135 paper
  - real_eligible: 179 opened, 165 closed, win_rate=67%, avg=$-14
  - paper_only: 135 opened, 135 closed, win_rate=78%, avg=$37

## 5. Action Items

✓ All positions stable, no action required.

## 6. System Health

- ✓ Token: 3d old, 4d remaining (source: refresh_token_issued) — healthy
- ✓ Dashboard: 278ms
- ✓ Launchd jobs loaded: 29 com.empire.*
- Positions sync: 1-19 16:00:08,780 [empire.positions_sync] INFO: === SYNC COMPLETE: 0 closed, 0 inserted, drift 0 ===
- ✓ No recent errors in *.err logs
