# S1. Operator wave: his entry, his operator list, his exit clock

In short: decoded on 2026-10-23 from that day's best wallet, him (430 landed round trips, +17.8 SOL) (docs/09). Buy first
behind the dev's own bundle at zero premium, only on create signers in an operator table built from his trades, and
sell 100% at create + H, where H is his own hold for that signer (docs/09 rules 1-3). It ran live from Oct 23 19:18 UTC
(docs/10 §2). On Oct 24 00:00-12:29 UTC it netted -0.253 SOL on 75 trades while he made +1.336 SOL on 126 (docs/11).
It stayed the live bot when S2 was shelved (docs/10 banner); S3's tweet rule and S4's rug cap were added on top. By
Oct 26-27 the box bought copies of his buys only (`entry.rule_buys = false`), which still use this page's operator table
and holds (docs/17 §9; [check output](../05-live/check-sh-2026-10-27.txt)).

| | |
|---|---|
| Status | live from Oct 23 19:18 UTC; base of the live bot through S3/S4; rule buys off by Oct 26-27 (copies only); the operator table and its refresh still feed the copy |
| Built from | [his rules](../02-his-rules/README.md) 1 (entry: first behind the bundle), 2 (picks: template and operator table), 5 (hold: create + H per operator), 6 (stake tiers), 7 (tips) |
| Code | `crates/rugsnipe/src/operators.rs` (`operators::create_signer`), `crates/rugsnipe/src/setup.rs` (`setup::min_tokens_out_at`), `crates/rugsnipe/src/hot.rs` (park, `skip_not_first`), `crates/rugsnipe-exit/src/decide.rs` (`ExitReason::HoldTo`), `crates/rugsnipe/tests/operator_wave.rs`; units `deploy/systemd/rugsnipe-operators.{service,timer}`, `deploy/systemd/rugsnipe-paper-wide.service`, overlay [`deploy/paper-wide.toml`](../deploy/paper-wide.toml); tables [`data/operators/`](../data/operators/) (`ahw-2026-10-23*.json`, `ahw-2026-10-24-tier.json`) |
| Config keys | `entry.max_premium = 0.0`, `entry.require_bundle`, `entry.operators_file`, `entry.operators_only`, `entry.operators_exclude`, `entry.bundle_wallets = [3]`, `entry.bundle_wait_us`, `entry.dev_buy_round` (+ `_min`, `_max`), `entry.dev_buy_sol`, `entry.dev_buy_tol_sol`, `entry.max_post_bundle_sol`, `entry.max_bundle_sol`, `entry.uri_hosts`, `entry.uri_hosts_deny`, `entry.stake_by_tier`, `entry.min_stake_tier`, `bid.by_tier`, `exit.default.hold_to_create_slots`, and the other exits off (`tp = []`, `insider_sell = "off"`, `no_activity_ms = 0`, `phantom_sl` zero, `max_hold_slots = 0`) (docs/09 table) |
| Source docs | [docs/09](../docs/09-operator-wave.md) (all), [docs/11](../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md) (all), [docs/10](../docs/10-microscalp-v2.md) §2 (the race table), [docs/12](../docs/12-how-the-copied-wallet-trades.md) §2, §6, [docs/08](../docs/08-runbook.md) §9 config table |
| Research | [`analysis/scripts/strategy/`](../analysis/scripts/strategy/): `operators_from_rt.py`, `operators_refresh.py`, `operator_clock.py`, `paper_wide_report.py` and their `test_*.py`; docs/11's "Today's trades" stage in [`analysis/research/2026-10-24/`](../analysis/research/2026-10-24/README.md): `pull_wallets.py`, `pull_tapes.py`, `pull_his.py`, `trades.py`, `q1.py`, `him.py`, `rugs.py`, `q2.py`, `final.py`, `csv.py`. The per-trade CSVs of docs/11 are not in the repo |

Words: a **create** launches a coin; a **slot** is one Solana block (about 200 ms, docs/01 C6); the **curve** is the
pump.fun price formula; the **bundle** is the dev's own buys right behind the create; an **operator** here is a create
signer (the create's fee payer); a **tip** pays the block producer only when the transaction lands; the **premium** is
what we pay over the post-bundle price; a **tape** is a coin's full trade list; **out of sample** means scored on data
the rule was not fitted on; **paper** means simulated fills, no money. 1M lamports = 0.001 SOL; mSOL here means 0.001 SOL.

## The rule

From docs/09 "The rule set":
1. **Entry: first behind the dev's own bundle, at zero premium.** The buy asserts the exact post-bundle curve state and
   fails cheaply if anyone traded first. Slot window: the create slot or the next.
2. **Picks.** Only signers in the operator table (`operators_only`). His picks favour a round dev buy, a bundle of
   exactly 3 outside wallets and above all repeat operators.
3. **Exit: 100% at create + H**, H constant per signer (1, 3, 6 or 10); unknown signers get 6 or 10. No take-profit,
   stop, insider or idle trigger.
4. **Fees.** Base fee plus a flat tip of about 1.5M paid only on landing.

**Pick template** (docs/09 "Picks"): round dev buy of 1-6 SOL, 3 bundle wallets, dev + bundle about 7 SOL (p90 17),
post-bundle market cap 36-65 SOL (post-bundle virtual SOL about 37-47), hosts `uxento.io`, `j7tracker.io`, `gg.sc`
favoured, `ipfs.io` disfavoured. Suggested caps: `max_post_bundle_sol = 47.0`, `max_bundle_sol = 17.0`. docs/11 Q2 later
set the cap at 40 (S4).

**Stake tiers** (2026-10-24): his stake is `0.4 SOL x 1.5^a x 2^b`, `b` his confidence tier; `entry.stake_by_tier`
copies it (docs/09 table).

**Keeping the table fresh** (docs/09): `operators_refresh.py` rebuilds it from the chain every 4 hours at :50 UTC
(`rugsnipe-operators.timer`), merges with decay, drops signers below `--min-n` and, with `--drop-dumpers`, signers whose
creator set sold within 3 slots. `operator_clock.py` then replaces his hold with the operator's own sell clock when the
clock made more in each half of the last 48 h; it also drops measured signers that lose at every hold 1..15.

**What is not copied** (docs/09): his exact-state guard (ours lets a buy through behind a sell), his relay set, and his
detection latency: he landed first 430 of 430 times; we land in the create slot about 62% of the time with a European
leader.

**Paper wide** (docs/09): a paper instance (`rugsnipe-paper-wide.service`, `entry.operators_exclude = true`) trades the
signers the live bot skips. Rule: after 150+ closed paper trades, open the table only if the paper mean is +3% or more
and both halves are positive.

## How it was found

- **His day** (docs/09): 430 landed round trips, +17.8 SOL. 430 of 430 landed with no outside buyer ahead; 278 in the
  create slot, 152 in the next. The 33 signers with 3+ trades carry 289 trades and 13.6 SOL. A bundle of exactly 3
  wallets on 69% of trades.
- **The exit clock** (docs/09): his sell's slot guard starts at L, and L - create is 10 (207 trades), 6 (186), 3 (27)
  or 1 (10), never anything else. The per-signer hold explains 93% of sells in sample, 74% out of sample. The checks
  repeat it: 132/132 offsets in a 6 h window and 444/444 in a 24 h run; 11/11 and 47/47 signers keep the same H.
- **Counting origin.** docs/12 §2 counts his hold from his buy (k = 2 to 10, mostly 5, 6 or 10); docs/09 and docs/14 §3
  count from the create (docs/14: +6 or +10 on 146 of 154 trades). Same clock, different origin.
- **His guards** (docs/12 §2): slot window program `A5c1eN7M...` and curve-state program `8jzqTjED...`; a failed buy
  costs him about 11,000 lamports. Routine buy: 1.5M tip; when he wants a launch badly, about 12M.
- **Operator clocks** (docs/09 "Exit clocks"): DRXPafDu sells at slot 12 / 11.5 on 95% / 91% of launches on two days,
  ENskGQev at 12 / 12, F5XvCe42 at 8 / 7.
- **Table decay** (docs/09): "60-70% of the best wallet's trades each day come from operators absent from the previous
  day's table" in one paragraph; in another, 60% of his 2026-10-23 trades were on the previous day's signers and 15% the
  next evening. The two statements measure different things; both say the table goes stale within a day.

## Backtests

| Test | Period | Setting | Result | n | Source |
|---|---|---|---|---|---|
| Exit holds, three rotations (fit on 2 of 3 16 h periods, score the third) | 48 h to 2026-10-24 | his holds | +13.78 / +9.07 / +18.18 SOL | not given | docs/09 Exit clocks; `operator_clock.py` |
| same | same | operator clock with the both-halves check | +16.99 / +13.50 / +19.47 SOL | not given | same |
| F5XvCe42 hold 1 against hold 7 | two days to 2026-10-24 | first spot, our costs | +0.33 / +0.43 against +4.62 / +3.79 SOL | 59 launches | docs/09 Exit clocks |
| Each operator's best hold fitted on one day | 48 h | scored on the other day | lost both ways: +6.71 against +9.00, +4.51 against +6.14 SOL | not given | docs/09 Exit clocks |
| Drop losers (lose at every hold, both halves) | 48 h, 2026-10-24 | 78 operators, 3,177 bundled launches | flagged operators' later launches -1.12 and -1.38 SOL | 3,177 launches | docs/09 "Losers leave" |
| Looser drop (his hold loses both halves) | same | flags 17 operators | later launches -0.56 SOL, but drops 79 winners worth +6.9 SOL | 17 operators | same |
| Stake-tier floor at 1, out of sample | his first 12 h to his last 12 h, 2026-10-24 | tier 1+ operators only | +0.2% a trade (9) against +16.8% (30) for the tier-0 ones it skips | 39 | docs/08 §9 (`min_stake_tier`) |
| Flat 0.6 SOL stake on his day | 2026-10-23 | no tiers | +9.8 of his +17.8 SOL | 430 | docs/08 §9 (`stake_by_tier`) |
| Post-bundle cap at 40 vSOL (chain truth, post hoc) | Oct 24 00:00-12:29 | split at 40 | us: 71 trades +0.265 / 4 trades -0.364 SOL; him: 97 +2.180 / 29 -0.839 SOL | 75 / 126 | docs/11 Q2; `rugs.py`, `q2.py` |
| Our day rebuilt one change at a time | Oct 24 00:00-12:29 | cap 40, sell when he is not in our slot, post-04:00 failure cost, 1.5M sells | -0.253 -> +0.110 -> +0.160 -> +0.312 -> about +0.42 SOL | 75 | docs/11 "Our day, rebuilt"; `final.py` |
| Skip a creator 3 h after a dump | same | | saves him 1.54 SOL, costs us 0.26 SOL (not adopted) | not given | docs/11 Q2; `q2.py` |
| Paper wide, projected | not dated | picks-model precision 0.30 / 0.44 | follower-rich share 36-41% against a break-even of about 52% | not given | docs/09 Paper wide |

## Live

**Oct 23 19:18 to Oct 24 03:27 UTC** (docs/10 §2, chain results after fees and tips):

| | trades | won | median | mean |
|---|---|---|---|---|
| we beat him (his buy failed behind ours) | 40 | 21 | +2.0% | -0.3% [-6.4, +5.8] |
| the same without the 2 rugs | 38 | | | +2.8% [-1.8, +7.4], +0.54 SOL |
| he did not fire | 35 | 8 | -3.9% | -1.6% |

**Oct 24 00:00 to 12:29 UTC** (docs/11 "The day"):

| | trades | mean | median | trades SOL | failed copies | net SOL |
|---|---|---|---|---|---|---|
| us, all day | 75 | -0.35% | -2.64% | -0.099 | 140, 0.154 SOL | -0.253 |
| him, all day | 126 | +1.59% | +0.95% | +1.341 | 466, 0.005 SOL | +1.336 |
| us, since 04:00 | 42 | -0.05% | -3.46% | -0.013 | 0.001 SOL | -0.014 |
| him, since 04:00 | 64 | +2.89% | +1.77% | +1.358 | 0.003 SOL | +1.355 |

- **Costs** (docs/11, `him.py`): before 04:00 our failed copies carried a 3M priority fee (0.153 SOL); after, 15,000 lamports
  against his 11,000. Median round trip: ours 9.0 mSOL (1.77% of stake), his 3.3 mSOL (0.75%).
- **Where his money is** (docs/11): 104 trades on launches our bot never fired on, +2.36 SOL (59 from creators we never
  fired on); 22 trades where we also fired and lost the race, -1.02 SOL.
- **Can we see him fire?** (docs/11 Q1, `q1.py`): his failed buy is in our block on 51 of 57 trades. Our trades split: he fired
  behind us 51 trades +1.60% (+0.418 SOL); later 6 trades -3.5% (-0.118 SOL); never 18 trades -4.82% (-0.398 SOL).
- **Stake tiers** went live on 2026-10-24 at 0.25 / 0.5 / 1.0 SOL on a 2.2 SOL bank; with the floor at 1 (01:05-01:30)
  the bot raced 4 times and landed 0 (docs/08 §9).
- **CmwFWFQs**: our 10 trades on it lost -0.17 SOL; `operator_clock.py` flags it (docs/09).
- **Speed**: on Oct 24 the bot was first on 40 of the 125 deployer-list launches it raced (docs/13 §4).
- **Five days, Oct 21-25** (docs/17 §2): -6.582 SOL on 1,138 coins sent, under "the configs of the time" (S0, S1, S3 and
  later rules mixed). The box's per-day ledger, also mixed, is in [copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt).

## Verdict

- **Kept** as the live base: v2 (S2) was shelved and "the live box stays on the operator bot" (docs/10 banner).
- **Changed:** the cap moved to 40 vSOL (docs/11 Q2, S4); S3 replaced the per-signer hold with a flat create + 10,
  because his per-deployer setting does not help us (+3.53% against +3.68%, docs/14 §3); `min_stake_tier` stays 0
  (docs/08 §9).
- **What it could not close** (docs/11, docs/12 §6): the 104 launches we never fire on, about 1 point of cost per trade,
  and his per-launch conviction, which is not visible before the buy (docs/08 §9, `min_stake_tier`).
- **Followed by** S3 (tweet rule), then the follow and copy rules of docs/16 and docs/17 §9; by Oct 26-27 the box ran
  copies only (`entry.rule_buys = false`, [check output](../05-live/check-sh-2026-10-27.txt)).

## Open questions

- The paper-wide instance's result is not reported in any doc read here.
- `operator_clock.py`'s clocks have backtest evidence (above) but no reported live result.
- What sets his 6 or 10 per deployer is not reported. It repeats his previous setting 86% of the time whether that trade
  won or lost, and it is not the insiders' dump clock (docs/14 §3).
- Whether a live feed of his attempts (failed buys included) would close the gap of the 104 launches we never fired on
  (docs/11 closing paragraph, docs/12 §7).

## Sources

- [docs/09-operator-wave.md](../docs/09-operator-wave.md), [docs/11-operator-bot-vs-copied-wallet-2026-10-24.md](../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md)
- [docs/10-microscalp-v2.md](../docs/10-microscalp-v2.md) banner and §2; [docs/12-how-the-copied-wallet-trades.md](../docs/12-how-the-copied-wallet-trades.md) §2, §6
- [docs/08-runbook.md](../docs/08-runbook.md) §9 config table (`operators_file`, `stake_by_tier`, `min_stake_tier`, `hold_to_create_slots`)
- [docs/13-tweet-coins.md](../docs/13-tweet-coins.md) §4, [docs/14-corrected-backtest.md](../docs/14-corrected-backtest.md) §3, [docs/17-newest-bot-vs-him-5-days.md](../docs/17-newest-bot-vs-him-5-days.md) §2, §9
- [analysis/research/2026-10-24/README.md](../analysis/research/2026-10-24/README.md), [analysis/scripts/strategy/](../analysis/scripts/strategy/)
- [05-live/check-sh-2026-10-27.txt](../05-live/check-sh-2026-10-27.txt), [05-live/copy-bot-history-2026-10-28.txt](../05-live/copy-bot-history-2026-10-28.txt)
