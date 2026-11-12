# Empire Daily Briefing — 2026-11-12
_Generated 2026-11-12 08:00:04 _

## 1. Market State

- **VIX** 18.36 (+4.97% vs prev close)
- **S&P 500** ~7,562 (SPY $756.15, -0.48%)
- **Oil (USO)** $140.80 (-0.47%)
- **BTC (IBIT)** $41.19 (-2.49%)
- **Regime**: MODERATE
  > MODERATE (owner ruling 2026-11-06, EFFECTIVE 2026-11-05, recorded 2026-11-06): the ruled `to_moderate` trigger breached on the 2026-11-05 close, VIX 28.18 > 27 — the only close above 27 in 65 recorded sessions, reached from a 16.61 close the session before. 5-day avg 21.24, 14-day 19.08, 16 of 65 closes above 17, 3 above 20. Posture knobs UNCHANGED and NO-RETRO: 65/85 edge floors, 7-day earnings blackout, semi block, csp_vix_minimum 14, 50% target / 2.0x stop / 0.70 roll / 1-DTE time stop all hold. The C2 CSP floor is NOT binding in this band (VIX 28.18, 14.18 points clear) — cohort quality, not volatility, is still the constraint. NOTHING HAS OPENED SINCE 2026-10-29: the kill switch has been tripped since 2026-11-03 and the reset is Peter's typed action. READ THE BREACH WITH ITS CAVEATS: it is single-armed, and 'sustained' with no day count is a single-close check — under a 2-day reading it is not breached. SEPARATELY: the six trigger questions are DEFERRED to a trigger-table v2 spec after the deploy reference (owner ruling 2026-11-06 evening, item C). The label is NARRATIVE ONLY — csp_enabled and csp_vix_minimum are the only regime knobs that gate, both unchanged — so an odd direction word is a wrong sentence, not a wrong trade. The watcher's private band table is GONE: its ladder now derives from this file's own regime_change_triggers (#85, closed).
- **Sector leaders**: Health +1.11%, Staples +0.67%, Financials +0.46%
- **Sector laggards**: Tech -1.74%, Comms -0.16%, Discr -0.08%
- **Triggers**: none armed

## 2. Open Positions

**0 open** — 🔴0 🟠0 🟡0 🟢0

_No open positions._

## 3. Events This Week

- **Fri 11/13** — OPEX: Weekly Options Expiration
- **Fri 11/20** — OPEX: Monthly Options Expiration (Nov 2026)
- Thu 11/12 — DIS earnings — DIS Earnings Report
- Thu 11/12 — CSCO earnings — CSCO Earnings Report
- Thu 11/12 — AMAT earnings — AMAT Earnings Report
- Thu 11/12 — JD earnings — JD Earnings Report
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
- **Yesterday**: +4 opens, 2 closes ($82.00 realized)
- **Total closed**: 277 (73% win rate, $3,261.00 total PnL)
- **Real-eligible vs paper-only**: 158 real / 134 paper
  - real_eligible: 158 opened, 143 closed, win_rate=67%, avg=$-13
  - paper_only: 134 opened, 134 closed, win_rate=78%, avg=$38

## 5. Action Items

✓ All positions stable, no action required.

## 6. System Health

- ✓ Token: 2d old, 5d remaining (source: refresh_token_issued) — healthy
- ✓ Dashboard: 241ms
- ✓ Launchd jobs loaded: 29 com.empire.*
- Positions sync: 1-11 16:00:04,404 [empire.positions_sync] INFO: === SYNC COMPLETE: 0 closed, 0 inserted, drift 0 ===
- ⚠ Recent errors in: dashboard.err
