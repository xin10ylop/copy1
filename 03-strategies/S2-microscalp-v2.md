# S2. Micro-scalp v2: the LEAD rebuilt on the live plumbing

In short: built on 2026-10-24 to replace the operator wave (S1) on the live box. It is S0's LEAD again: the dry run's
code (0aae91c) plus every live fix that does not change the strategy, with the LEAD's exits and a 2M bid (docs/10 §3-5).
A chain-truth replay of Oct 21-23 showed why live missed the dry run: the races we win lose -2.63% after costs at 0.5
SOL, against the dry run's +1.1-1.6% per attempt (docs/10 §2). Shelved at 13:00 UTC the same day, before any deploy;
never ran live. The code is in commit 0f0d78a and is not on this branch (docs/10 banner).

| | |
|---|---|
| Status | built, shelved 2026-10-24 13:00 UTC, never deployed; the live box stayed on S1 |
| Built from | none of his rules: it is S0's LEAD. He appears only as a marker: a race we win against his guarded buy pays (docs/10 §2). His guard is rule 1 in [his rules](../02-his-rules/README.md) |
| Code | commit 0f0d78a (v2); base 0aae91c (the dry run); the live operator bot is 3a79c22 (docs/10 banner). `deploy/bin/rugsnipe-microscalp-config` and `deploy/test_microscalp_config.py` are in 0f0d78a, not on this branch. `deploy/bin/rugsnipe-check` judges a live day (a later version is on this branch). The exit spec is `config/paper-lead.example.toml` at 0aae91c |
| Config keys | `[entry]` `require_bundle = true`, `filter = "multi_bundle"`, `max_premium = 0.02`, `filter_mode = "log"`; `[exit.default]` `tp = [[1.15, 1.0]]`, `insider_sell = "bundle"`, `no_activity_ms = 1_000`, `phantom_sl = { after_ms = 1_000, drop = 0.15 }`, `max_hold_slots = 5`, `tp_slip_bps = 2500`, `sell_retry = { every_slots = 2, max_tries = 15, tip_mult = 2.0 }`, `sell_tip_lamports`, `dump_tip_lamports` (2M); `bid.lamports = 2_000_000`; `max_buys_per_hour = 600`, `spread_buys_per_hour = false`, `max_probes_per_day = 6_000`, `max_buys_per_op_per_day = 6_000`; `senders.nozomi_bundle`, `risk.max_bid_lamports` (docs/10 §3, §5) |
| Source docs | [docs/10](../docs/10-microscalp-v2.md) §1-8; background [docs/04](../docs/04-strategy.md) §2 |
| Research | scratchpad scripts, not in the repo: `mslive/recon.py`, `mslive/stakes.py`, `mslive/followers.py` (docs/10 §2), `ms/bidcurve.py` (docs/10 §4). Note: `analysis/research/2026-10-24/corrected/recon.py` and `stakes.py` are different scripts (docs/14's tweet-rule coins) |

Words: a **create** launches a coin; a **slot** is one Solana block (about 200 ms, docs/01 C6); the **curve** is the
pump.fun price formula; the **bundle** is the dev's own buys right behind the create; a **race** is the contest for the
first spot behind the bundle; a **tip** pays the block producer only on landing, while a priority fee is paid even by
a transaction that lands and fails; the **premium** is what we pay over the post-bundle price; a **tape** is a coin's
full trade list; the **dry run** is the paper lane (simulated fills, no money) on the live feed; the **probe** is the
small real-money run of Oct 21-23. 1M lamports = 0.001 SOL; mSOL here means 0.001 SOL.

## The rule

The LEAD of docs/04 §2, with the dry run's exact exit spec (docs/10 §5):
- **Universe (class gate):** a real buy fires only when a bundle wallet is outside the creator set (the user, the
  creator argument, the fee payer, the create's signers and its in-transaction buyers) (docs/10 §3).
- **Run derivation:** the creator set's trades plus buys chained at most 2 apart; an outside buy marks the launch
  NOT_FIRST and never moves the anchor (docs/10 §3).
- **Entry:** first behind the bundle, at most +2% over the post-bundle price.
- **Exit** at the first of: +15% on value; a bundle-wallet sell; 1 s with no trade; -15% after 1 s; slot + 5.
- **Bid:** 2M on the buy, the sell and the dump (a 4M round trip, the dry run's own); the Harmonic copy sent as a
  Nozomi bundle, paid only when it lands; tip-only plain copies (docs/10 §1, §4).
- **Not ported:** every operator-wave rule (operator table, hold-to-create, stake tiers, dev-buy template, dumper skip,
  leader regions, pre-send gate, paper wide). The binary refuses their config keys (docs/10 §3).

## How it was found

**Why live missed the dry run** (docs/10 §1). Every transaction of the probe wallet (850) and the full tape of every
attempted mint (474), replayed with the dry run's exits; the replay matches the dry run's paper rows (median gap 0.00
points). Columns r1 to real are the mean per landed trade, % of stake:

| period (Oct 21-23) | attempts | landed | r1 | @fill | curve | real | SOL real | failed copies SOL |
|---|---|---|---|---|---|---|---|---|
| A: probe-A 0.02 SOL, any create | 108 | 75% | -0.5 | -1.6 | -1.9 | -16.7 | -0.426 | 0.041 |
| B: 0.25 SOL, require_bundle, 4 SOL bound | 44 | 45% | -1.1 | -2.1 | -2.9 | -4.9 | -0.298 | 0.054 |
| C: bound fixed, sell bid 50k | 94 | 45% | -0.9 | -1.0 | -2.3 | -4.3 | -0.568 | 0.117 |
| D: sell bid 3.4M, old exit clock | 29 | 34% | +5.7 | +5.7 | +7.3 | +4.0 | +0.051 | 0.049 |
| E: new exit clock, 0.5 SOL | 125 | 46% | -3.1 | -3.6 | -5.2 | -7.9 | -2.363 | 0.310 |
| F: pre-execution fix, max_hold 50 | 69 | 64% | -3.3 | -3.4 | -4.2 | -9.6 | -1.252 | 0.167 |
| total | 469 | | | | | | -4.856 | 0.738 |

r1 = the dry run's exits at the dry run's fill (rank 1 at the post-bundle price); @fill = the same exits at our real
fill; curve = our real exits, net of pump fees; real = the chain's SOL deltas.

Each gap is a layer, and v2 closes each one (docs/10 §1):

| layer | live cost | cause | v2 fix |
|---|---|---|---|
| entry price (r1 to @fill) | 0.1-1.5 points | class gate wider than the dry run's; anchor moved by an outside buy | class gate and run derivation as in the dry run |
| exits (@fill to curve) | 0.3-1.6 points | exits drifted; sells landed 3-8 slots late on 50k bids | the dry-run exit spec verbatim; sells at 2M, fanned out, nonce first |
| costs (curve to real) | 1.4-5.4 points at 0.25-0.5 SOL | 3.4-3.5M priority fees on every copy, including those that land and fail | a 2M bid, the Nozomi bundle route, tip-only plain copies |

With every layer closed, a landed trade scores **r1 minus about 0.9 points** (a 4.5 mSOL round trip at 0.5 SOL). So
v2's result is set by r1: the value of the races we win (docs/10 §1).

**The gap code cannot close** (docs/10 §2). Before the first outside buy, the launches where we were the first outside
buyer (162) and those where a rival was (238) look the same (median bundle 7.20 against 8.02 SOL, 3 wallets, dev buy
2.96). After it they differ: a rival's first buy draws 3.12 other buyers and 1.43 SOL in the next 2 slots, ours 1.62
buyers and 0.34 SOL. Two explanations: the followers follow the
rival, or the rival knows which launches will be pushed. Under either, the dry run's count (rival removed, its
followers kept) is out of reach.

## Backtests

| Test | Period | Setting | Result | n | Source |
|---|---|---|---|---|---|
| Dry run (paper lane, per attempt) | 22 h and 5.5 h runs, dates not given | LEAD exits | +1.14% (22 h), +1.56% (5.5 h) | not given | docs/10 §2 |
| Replay of in-class attempts at rank 1 | Oct 21-23 | dry-run exits | +1.17% [-0.36, +2.69] | 401 | docs/10 §2; `mslive/recon.py` |
| Races we won, re-scored | Oct 21-23 | 0.5 SOL | -1.73% before costs; -2.63% [-4.21, -1.05] after a 4.5 mSOL round trip; -13.2 mSOL a trade | 188 | docs/10 §2; `mslive/stakes.py` |
| Races we lost, re-scored | Oct 21-23 | 0.5 SOL | +3.56% before costs; +2.66% after; +13.3 mSOL a trade | 213 | same |
| Won races by stake | Oct 21-23 | 0.02 / 0.25 / 0.5 SOL | -1.61% / -1.67% / -1.73% before costs (impact does not explain the gap) | 188 | same |
| Won races by landing slot | Oct 21-23 | creation slot / one slot later | -3.03% [-4.73, -1.34] / +0.32% | 111 / 76 | docs/10 §2 |
| Won against lost, by bundle size | Oct 21-23 | small / mid / big | -1.86 vs +2.55%; -4.96 vs +7.70%; -1.02 vs +0.68% | 401, in size terciles | docs/10 §2; `mslive/followers.py` |
| Micro-scalp races where we beat him | Oct 21-23 | dry-run exits | +9.1% [+2.8, +15.5] | 6 | docs/10 §2 |
| Micro-scalp races where he did not fire | Oct 21-23 | dry-run exits | -3.1% [-4.7, -1.6] | 156 | docs/10 §2 |
| Flat bid curve, 2M row (mSOL per launch, two halves) | not dated | 0.5 SOL | Harmonic +4.6/+1.0, BAM +4.1/+1.5, Jito +4.6/+2.3, Firedancer +10.8/+3.7; from 18M up every class loses on both halves | 2,885 launches | docs/10 §4; `ms/bidcurve.py` |
| Expected v2 result | Oct 21-23 mix | 0.5 SOL | about -2.6% per landed trade; about -15 SOL a day at docs/04's 1,150 landed trades | | docs/10 §2 |

The bid curve uses the same optimistic counterfactual as the dry run: it ranks bids, it does not promise their sign
(docs/10 §4).

## Live

Never live. docs/10 §6 planned a **measurement run** on fra1 with the daily loss stop as its budget: at -13 mSOL per
landed trade a verdict needs about 150 trades, about 2 SOL of expected loss at 0.5 SOL or 1.3 SOL at 0.25 SOL.

How the run would have been read (docs/10 §7):
- `per_attempt_pct` is the number to watch; break-even is 0.
- One trade varies by about 15.6%, so a mean is good to about ±3.0 points at 100 trades, ±2.2 at 200, ±1.5 at 400.
- After 150 landed trades: stop below 0; continue only above +1%; in between, run to 400 and decide.
- `tp` exits should be a real share (7 of 188 won races Oct 21-23, against 40 of 213 lost ones); `nozomi_bundle`
  should show lost = 0.

Deploy order (docs/10 §6): stop `rugsnipe-operators.timer` and `rugsnipe-paper-wide.service` first, keep the old
binaries and config, convert with `rugsnipe-microscalp-config`, validate, then switch. Rollback (docs/10 §8): the state
database is compatible both ways (schema 5).

## Verdict

- **Shelved** at 2026-10-24 13:00 UTC; "the live box stays on the operator bot" (docs/10 banner).
- **Why:** v2 fixes every execution gap but not the one that decides the P&L. The races we win are not the races the
  dry run counted; on the Oct 21-23 mix v2 should make about -2.6% per landed trade, and the daily stop would trip
  first (docs/10 §2).
- **What carried forward:** "beating an informed rival pays" (docs/10 §2). A race against his guarded buy marks a
  launch an informed buyer wants. That points to S1 and S3, which trade his launches. The same cost layers (failed
  copies, sell bids) were later worked on in the operator bot (docs/11 "Costs", docs/14 §5).

## Open questions

- Which explanation holds: followers who follow known rivals, or rivals who know which launches will be pushed (docs/10
  §2)?
- The Harmonic bundle route "can change the mix, which is the one thing a run can measure that the tapes cannot"
  (docs/10 §2). It was never run.
- The dry run's dates and sample sizes are not given in docs/10.

## Sources

- [docs/10-microscalp-v2.md](../docs/10-microscalp-v2.md) (all sections)
- [docs/04-strategy.md](../docs/04-strategy.md) §2 (the LEAD), [S0](S0-lead-policy-dev-sniping.md)
- [docs/11-operator-bot-vs-copied-wallet-2026-10-24.md](../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md) (the bot that stayed live)
- [deploy/bin/rugsnipe-check](../deploy/bin/rugsnipe-check)
