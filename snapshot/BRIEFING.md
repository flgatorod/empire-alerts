# Empire Daily Briefing — 2026-11-13
_Generated 2026-11-13 08:00:05 _

## 1. Market State

- **VIX** 18.32 (-2.03% vs prev close)
- **S&P 500** ~7,590 (SPY $759.02, +0.25%)
- **Oil (USO)** $145.46 (-0.42%)
- **BTC (IBIT)** $39.10 (-3.12%)
- **Regime**: MODERATE
  > MODERATE (owner ruling 2026-11-06, EFFECTIVE 2026-11-05, recorded 2026-11-06): the ruled `to_moderate` trigger breached on the 2026-11-05 close, VIX 28.18 > 27 — the only close above 27 in 65 recorded sessions, reached from a 16.61 close the session before. 5-day avg 21.24, 14-day 19.08, 16 of 65 closes above 17, 3 above 20. Posture knobs UNCHANGED and NO-RETRO: 65/85 edge floors, 7-day earnings blackout, semi block, csp_vix_minimum 14, 50% target / 2.0x stop / 0.70 roll / 1-DTE time stop all hold. The C2 CSP floor is NOT binding in this band (VIX 28.18, 14.18 points clear) — cohort quality, not volatility, is still the constraint. NOTHING HAS OPENED SINCE 2026-10-29: the kill switch has been tripped since 2026-11-03 and the reset is Peter's typed action. READ THE BREACH WITH ITS CAVEATS: it is single-armed, and 'sustained' with no day count is a single-close check — under a 2-day reading it is not breached. SEPARATELY: the six trigger questions are DEFERRED to a trigger-table v2 spec after the deploy reference (owner ruling 2026-11-06 evening, item C). The label is NARRATIVE ONLY — csp_enabled and csp_vix_minimum are the only regime knobs that gate, both unchanged — so an odd direction word is a wrong sentence, not a wrong trade. The watcher's private band table is GONE: its ladder now derives from this file's own regime_change_triggers (#85, closed).
- **Sector leaders**: Energy +0.50%, Financials +0.40%, Materials +0.38%
- **Sector laggards**: Tech -0.18%, Indust +0.00%, Staples +0.00%
- **Triggers**: none armed

## 2. Open Positions

**0 open** — 🔴0 🟠0 🟡0 🟢0

_No open positions._

## 3. Events This Week

- **Fri 11/13** — OPEX: Weekly Options Expiration
- **Fri 11/20** — OPEX: Monthly Options Expiration (Nov 2026)
- **Fri 11/27** — OPEX: Weekly Options Expiration
- Tue 11/17 — HD earnings — HD Earnings Report
- Tue 11/17 — NVDA earnings — NVDA Earnings Report
- Tue 11/17 — DIS earnings — DIS Earnings Report
- Tue 11/17 — JD earnings — JD Earnings Report
- Wed 11/18 — LOW earnings — LOW Earnings Report
- Wed 11/18 — TGT earnings — TGT Earnings Report
- Wed 11/18 — TJX earnings — TJX Earnings Report
- Wed 11/18 — NVDA earnings — NVDA Earnings Report
- Thu 11/19 — WMT earnings — WMT Earnings Report
- Thu 11/19 — INTU earnings — INTU Earnings Report
- Thu 11/19 — BABA earnings — BABA Earnings Report
- ✓ No earnings inside current option windows

## 4. Paper Trading Activity

- **Open**: 15 single-leg + 10 spreads
- **Yesterday**: +4 opens, 4 closes ($42.00 realized)
- **Total closed**: 281 (73% win rate, $3,303.00 total PnL)
- **Real-eligible vs paper-only**: 161 real / 135 paper
  - real_eligible: 161 opened, 147 closed, win_rate=67%, avg=$-13
  - paper_only: 135 opened, 134 closed, win_rate=78%, avg=$38

## 5. Action Items

✓ All positions stable, no action required.

## 6. System Health

- ✓ Token: 3d old, 4d remaining (source: refresh_token_issued) — healthy
- ✓ Dashboard: 238ms
- ✓ Launchd jobs loaded: 29 com.empire.*
- Positions sync: 1-12 16:00:03,695 [empire.positions_sync] INFO: === SYNC COMPLETE: 0 closed, 0 inserted, drift 0 ===
- ✓ No recent errors in *.err logs
