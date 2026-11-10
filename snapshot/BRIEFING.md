# Empire Daily Briefing — 2026-11-10
_Generated 2026-11-10 08:00:01 _

## 1. Market State

- **VIX** 20.03 (+0.55% vs prev close)
- **S&P 500** ~7,535 (SPY $753.52, +0.11%)
- **Oil (USO)** $139.15 (-2.46%)
- **BTC (IBIT)** $42.03 (-0.69%)
- **Regime**: MODERATE
  > MODERATE (owner ruling 2026-11-06, EFFECTIVE 2026-11-05, recorded 2026-11-06): the ruled `to_moderate` trigger breached on the 2026-11-05 close, VIX 28.18 > 27 — the only close above 27 in 65 recorded sessions, reached from a 16.61 close the session before. 5-day avg 21.24, 14-day 19.08, 16 of 65 closes above 17, 3 above 20. Posture knobs UNCHANGED and NO-RETRO: 65/85 edge floors, 7-day earnings blackout, semi block, csp_vix_minimum 14, 50% target / 2.0x stop / 0.70 roll / 1-DTE time stop all hold. The C2 CSP floor is NOT binding in this band (VIX 28.18, 14.18 points clear) — cohort quality, not volatility, is still the constraint. NOTHING HAS OPENED SINCE 2026-10-29: the kill switch has been tripped since 2026-11-03 and the reset is Peter's typed action. READ THE BREACH WITH ITS CAVEATS: it is single-armed, and 'sustained' with no day count is a single-close check — under a 2-day reading it is not breached. SEPARATELY: the six trigger questions are DEFERRED to a trigger-table v2 spec after the deploy reference (owner ruling 2026-11-06 evening, item C). The label is NARRATIVE ONLY — csp_enabled and csp_vix_minimum are the only regime knobs that gate, both unchanged — so an odd direction word is a wrong sentence, not a wrong trade. The watcher's private band table is GONE: its ladder now derives from this file's own regime_change_triggers (#85, closed).
- **Sector leaders**: Health +0.76%, Financials +0.72%, Staples +0.65%
- **Sector laggards**: Energy -0.77%, Tech -0.51%, Indust -0.47%
- **Triggers armed**:
  - ⚠ VIX 20.0 ≥ 20 (would arm LOW-ELEVATED)

## 2. Open Positions

**0 open** — 🔴0 🟠0 🟡0 🟢0

_No open positions._

## 3. Events This Week

- **Fri 11/13** — OPEX: Weekly Options Expiration
- **Fri 11/20** — OPEX: Monthly Options Expiration (Nov 2026)
- Tue 11/10 — OKLO earnings — OKLO Earnings Report
- Tue 11/10 — RGTI earnings — RGTI Earnings Report
- Tue 11/10 — QBTS earnings — QBTS Earnings Report
- Wed 11/11 — CSCO earnings — CSCO Earnings Report
- Thu 11/12 — DIS earnings — DIS Earnings Report
- Thu 11/12 — CSCO earnings — CSCO Earnings Report
- Thu 11/12 — AMAT earnings — AMAT Earnings Report
- Thu 11/12 — JD earnings — JD Earnings Report
- Tue 11/17 — HD earnings — HD Earnings Report
- Tue 11/17 — NVDA earnings — NVDA Earnings Report
- Tue 11/17 — DIS earnings — DIS Earnings Report
- Tue 11/17 — JD earnings — JD Earnings Report
- ✓ No earnings inside current option windows

## 4. Paper Trading Activity

- **Open**: 13 single-leg + 10 spreads
- **Yesterday**: +13 opens, 0 closes ($0.00 realized)
- **Total closed**: 275 (72% win rate, $3,179.00 total PnL)
- **Real-eligible vs paper-only**: 154 real / 134 paper
  - real_eligible: 154 opened, 142 closed, win_rate=67%, avg=$-14
  - paper_only: 134 opened, 133 closed, win_rate=78%, avg=$38

## 5. Action Items

✓ All positions stable, no action required.

## 6. System Health

- ✓ Token: 0d old, 7d remaining (source: refresh_token_issued) — healthy
- ✓ Dashboard: 491ms
- ✓ Launchd jobs loaded: 29 com.empire.*
- Positions sync: 1-09 16:00:04,856 [empire.positions_sync] INFO: === SYNC COMPLETE: 0 closed, 0 inserted, drift 0 ===
- ⚠ Recent errors in: dashboard.err
