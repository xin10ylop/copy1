# 04. Backtests: an index of every test in this repo

Every backtest behind strategies S0-S7, with its period, result and source. The strategy pages
(`../03-strategies/`) explain each one. Research scripts are under `analysis/research/<date>/<topic>/`. Each folder's
README gives the run order, and the data is in `data/datasets/` (CLAUDE.md "Datasets"). "% a trade" is the mean
return per trade after costs unless stated. [a, b] is a 95% interval.

## S0: LEAD policy (dev sniping)

| Test | Period | Result | Source |
|---|---|---|---|
| naive: buy at the end of slot 0, TP 2x | random arm, Oct 12-14 | −18.6% [−23, −14], n = 396 | docs/05 §2 |
| his arming rule, walk-forward (3+ of the last 10 hit +100%) | 16-day sample | out-of-sample hit rate 18.6-21.8% against 43-48% needed | docs/05 §5.3; `analysis/scripts/gap1` |
| his rule, TP +100%, no stop | last 40% of 675 bundled launches; deep = 133 random | −10.5% [−13.9, −6.9]; deep −21.1% | docs/04 §1 |
| his bot's exits on his rule | same | −0.8%; deep −4.6% | docs/04 §1 |
| buy on dev sell / snipe delay | same | −13.1% / −16.9%; deep −22.0% / −28.5% | docs/04 §1 |
| **LEAD**, test split | last 40% by time | +3.5% [+1.4, +5.8], n = 200 | docs/04 §3 |
| **LEAD**, fresh holdout | pulled Oct 14 after the freeze | **+3.7% [+0.7, +6.6], n = 150** | docs/04 §3; `orchestrator_checks.py` |
| LEAD, pooled out of sample | Oct 12-14 | +3.5% [+1.9, +5.2], n = 427 | docs/04 §3 |
| LEAD, dense window | Oct 14 02:05-08:05 UTC | +2.5% [+1.6, +3.4], n = 915 (quiet −0.9%, busy +9.4%) | docs/04 §3 |
| LEAD, critic's holdout | Oct 14 08:43-13:43 UTC | +3.2% [+1.5, +4.9], n = 222 | docs/04 §3 |
| LEAD at rank 2 | same | +0.8% | docs/04 §3 |
| LEAD, combined realistic fills | same | −0.4% [−2.0, +1.3] | docs/04 §3; `critic_realistic.py` |
| LEAD + entry filter (skip the bottom tertile) | 480 pre-registered launches, Oct 14 | +4.6% against +3.2% plain | docs/04 §3a; `data/reports/strategy/entry_filter_v1.json` |
| per-operator arming | fresh holdout | +2.9% armed against +3.2% unarmed | docs/04 §5 |
| copy-trading pump wallets | 905 fresh launches | −7.0% [−9.5, −4.5] | docs/04 §5 |
| SOL a day (model) | | +9.0 SOL/day [−5.0, +20.3] at 0.5 SOL, 20% landing | docs/04 §4; `pnl_model.py` |
| **live probe** | Oct 21-23 | **−4.856 SOL on 469 attempts** | docs/10 §1 |

## S1: operator wave

| Test | Period | Result | Source |
|---|---|---|---|
| exit holds, three rotations, his holds | 48 h to Oct 24 | +13.78 / +9.07 / +18.18 SOL | docs/09; `operator_clock.py` |
| operator clock with the both-halves check | same | +16.99 / +13.50 / +19.47 SOL | docs/09 |
| F5XvCe42: hold 1 against hold 7 | two days to Oct 24 | +0.33 / +0.43 against +4.62 / +3.79 SOL (59 launches) | docs/09 |
| each operator's best hold fitted on one day | 48 h | loses both ways: +6.71 against +9.00, +4.51 against +6.14 | docs/09 |
| drop losers | 48 h, 78 operators, 3,177 launches | flagged operators' later launches −1.12 and −1.38 SOL | docs/09 |
| looser drop | same | −0.56 SOL on later launches, but drops 79 winners worth +6.9 | docs/09 |
| stake-tier floor at 1, out of sample | Oct 24 | +0.2% a trade (9) against +16.8% (30) for the skipped | docs/08 §9 |
| flat 0.6 SOL stake on his day | Oct 23 | +9.8 of his +17.8 SOL | docs/08 §9 |
| post-bundle cap at 40 (post hoc) | Oct 24 00:00-12:29 | us +0.265 at ≤ 40 (71), −0.364 above (4); him +2.180 (97), −0.839 (29) | docs/11 Q2; `rugs.py`, `q2.py` |
| our day rebuilt one change at a time | same | −0.253 → about +0.42 SOL | docs/11; `final.py` |
| skip a creator 3 h after a dump | same | saves him 1.54 SOL, costs us 0.26 | docs/11 Q2 |
| paper wide (projected) | | follower-rich share 36-41% against about 52% to break even | docs/09 |
| **live** | Oct 24 00:00-12:29 UTC | **−0.253 SOL on 75 trades; him +1.336 on 126** | docs/11 |

## S2: micro-scalp v2

| Test | Period | Result | Source |
|---|---|---|---|
| dry run, per attempt | 22 h and 5.5 h runs | +1.14% / +1.56% | docs/10 §2 |
| replay of in-class attempts at rank 1 | Oct 21-23 | +1.17% [−0.36, +2.69], n = 401 | docs/10 §2 |
| **races we won** | Oct 21-23 | **−1.73% before costs, −2.63% [−4.21, −1.05] after**, n = 188 | docs/10 §2 |
| races we lost | Oct 21-23 | +3.56% before costs, +2.66% after, n = 213 | docs/10 §2 |
| won races by stake 0.02 / 0.25 / 0.5 | Oct 21-23 | −1.61% / −1.67% / −1.73% | docs/10 §2 |
| won races by landing slot | Oct 21-23 | creation slot −3.03% (111), next slot +0.32% (76) | docs/10 §2 |
| won vs lost, by bundle size | Oct 21-23 | small −1.86 vs +2.55%; mid −4.96 vs +7.70%; big −1.02 vs +0.68% | docs/10 §2 |
| races where we beat him / he didn't fire | Oct 21-23 | +9.1% (n = 6) / −3.1% (n = 156) | docs/10 §2 |
| flat bid curve, 2M row | 2,885 launches | positive at 2M by class; every class loses from 18M up | docs/10 §4 |
| expected v2 | Oct 21-23 mix | about −2.6% a landed trade, about −15 SOL a day | docs/10 §2 |

## S3: tweet rule

| Test | Period | Result | Source |
|---|---|---|---|
| docs/13's rule "on" (superseded) | Oct 23 and Oct 24 00-12 UTC | +5.0% [+3.2, +7.0], n = 342 | docs/13 §1 |
| docs/13 "exit" (superseded) | same | +3.15%, n = 547 | docs/13 §4 |
| docs/13 deployer key | same | signer +3.6% (345); signer or creator +4.6% (447) | docs/13 §2 |
| **corrected, buy all, hold 10** | Oct 23 00-12 / 12-24 / Oct 24 00-12 | +4.07% / +3.88% / +3.10% | docs/14 §2; `corrected/bt_all.py` |
| **corrected, all coins** | the three | **+3.68% [+2.71, +4.69], n = 1,881** | docs/14 §2 |
| corrected "exit" / "on" | same | +2.97% [+2.25, +3.65] / +5.12% | docs/14 §2 |
| hold at create + 2/4/6/8/9/10/12 | same | +0.2 / +1.7 / +2.5 / +3.4 / +3.7 / +3.7 / +3.6% | docs/14 §3 |
| first coins against the rest, hold 10 | same | +5.1% against +1.5% | docs/14 §3 |
| long holds (every 6th coin) | same | +4.9% at 10-12, +4.2% at 16, +3.6% at 30 (n = 300) | docs/14 §3; `hold30.py` |
| his per-deployer hold against flat 10 | same | +3.53% against +3.68% | docs/14 §3 |
| value by his stake tier, before costs | same | +4.44% / +5.91% / +10.87% (1,620 / 170 / 91) | docs/14 §4; `stakes.py` |
| tweet feed, 2 s lag | same | 7 coins/h, 95% truly first; +4.27% against +3.59% | docs/14 §6; `tweetfeed.py` |
| TweetStream "first" / "copy" call | same | +1.7% vs +2.1% on coins we won; copy −2.49% (21) vs +3.20% (76) | docs/14 §7 |
| authors he favours | ranked Oct 23 00-12, scored later | +6.44% (335) against +1.85% (84) | docs/14 §6; `authors.py` |
| exit for rule fires at 5% premium | Oct 23 00:00 → Oct 24 12:00 | table hold +4.39, flat +9 +5.41, flat +10 +4.81 SOL (1,066 fires) | docs/17 §9 |
| exact replay of the box's rule bot | Oct 23 00:00 → Oct 25 17:58 | +1.1 SOL over 2.7 days against his +33.5 (1,816 fires) | docs/17 §8; `crates/rugsnipe/tests/replay_days.rs` |

## S4: big rugs (on the 1,881 rule coins, "exit" mode, 0.5 SOL, over 36 h unless stated)

| Test | Result | Source |
|---|---|---|
| skip the bot's dumper list (all hosts) | 482 coins, +2.27%, 30 of 42 big losses removed, −5.46 SOL | docs/15 §2; `rug_rules.py` |
| skip if an insider dumped 4+ launches / dump rate ≥ 50% | −4.73 / −0.02 SOL | docs/15 §2; `rug_rate.py` |
| skip on the deployer's or template's last coins | −1.35 / −1.04 / −1.00 SOL | docs/15 §2; `rug_track.py` |
| skip deployers that mostly launch copies | −5.66 SOL | docs/15 §2; `rug_copyrate.py` |
| skip a reused ticker/name (60-300 s) | −5.3 to −8.7 SOL | docs/15 §2; `rug_recent.py` |
| skip tweet-book matches / the feed's copy call | −10.39 / −6.91 SOL | docs/15 §2; `rug_book.py`, `rug_feed.py` |
| sell dumper-list coins at create + 3 | −5.82 SOL | docs/15 §2 |
| sell on the insiders' first sell (10/25/50% sold) | 0 SOL | docs/15 §2; `rug_exit.py` |
| wait for slot +1, buy only if insiders haven't sold | −25.5 SOL | docs/15 §2; `rug_wait.py` |
| **skip dumper list on rapidlaunch only** | Oct 23 00-12 +0.26, 12-24 +0.01, Oct 24 00-12 +0.13; **all +0.40 SOL** (72 skipped, −1.10%) | docs/15 §3; `rug_combo.py` |
| the same with a 5-slot insider-sell list | −0.33 SOL | docs/15 §3 |
| rapidlaunch coins with / without a dumper-list insider | −1.1% against +5.2% | docs/15 §6 |
| higher flat bid above 40 vSOL (curve model, Oct 21-25) | 4M / 16M / 24M: +2.8 / +5.3 / +6.0; without the top 10 coins −1.0 / −0.4 / −0.8 | docs/17 §4 |

## S5: follow (bundle wallet × fee routing)

| Test | Period | Result | Source |
|---|---|---|---|
| ex-ante follow, rule coins | Oct 23 12-24 / Oct 24 00-12 | his rate 74% / 74%; 72% / 79% of his picks covered | docs/16 §3; `ev.py` |
| four modes: rule / gate / add / on | same | +2.45% / +3.63% / +3.17% / +4.53% a trade | docs/16 §4; `final.py` |
| coins that `add` adds | same | +8.36% (188) | docs/16 §4 |
| night replay | Oct 25 00:00-09:13 | +0.59 / +1.10 SOL keyed (actual −0.10) | docs/16 §6, §8 |
| **(wallet, fee routing) key** | out of sample | **79% / 80% of his attempts, +4.74% (981)** | docs/16 §8; `evkey.py` |
| skipped vs taken followed coins | out of sample | +2.81% vs +4.62% | docs/16 §8; `skipval.py` |
| his exit per cell | out of sample | +4.04% vs +3.47% | docs/16 §8; `exit.py` |
| today | Oct 25 09:13-13:07 | 49 of 67 (73%), his +0.584 | docs/16 §9; `today.py` |
| recent value | out of sample | +7.72% (321) | docs/16 §9; `evval.py` |
| hot/cold stakes | out of sample | +23.3 vs +18.8 SOL | docs/16 §10; `kelly.py` |
| a model of his take | out of sample | AUC 0.882 / 0.937 | docs/16 §10; `model.py` |
| coin mode in the key | Oct 23-24 | adds nothing | docs/16 §11; `evmode.py` |
| **exact replay**, rate 0.3 / 0.6 / 0.7 | Oct 23 00:00 → Oct 25 17:58 | **+1.03 / +1.96 / +2.06 SOL** (his +33.5) | docs/17 §8 |
| the same at a 5% bound | same | +4.19 / +2.95 / +3.17 | docs/17 §9; `bound.py` |
| newest bot against his buys | Oct 21 → Oct 25 16:07 | 3,847 fires, 85% attempted by him | docs/17 §1 |

## S6: copy him (Oct 21-25 tapes unless stated; 0.5 SOL a copy)

| Test | Result (SOL) | Source |
|---|---|---|
| landing D positions behind him | D = 0 +10.55 … D = 150 +0.10 | docs/17 §9; `react_pos.py` |
| copy from scratch, listed / unlisted operators | +6.55 / −2.25 | docs/17 §9; `scratch.py` |
| exit behind his sell | −23.4 | docs/17 §9 |
| tip ≥ 4M at 5% | +4.71 | `weakdays.py` |
| ≥ 2 buys in 24 h | +4.22 | `recent.py` |
| restarts | +2.41 | `restart.py` |
| 4M or ≥ 2 SOL | +5.64 | `tipsize.py` |
| **2M floor (the built rule)** | **+8.02 on 298 copies** | docs/17 §9; `ablate.py` |
| price bound 3% / 7.5% / 10% / none | +3.36 / +6.18 / +5.77 / +5.86 | `ablate.py` |
| exit H / H−2 / +5 / +9 | +2.98 / +3.95 / +4.43 / +3.91 | `ablate.py` |
| stake 0.25 / 0.75 / 1.0 | +2.50 / +8.83 / +12.05 | `ablate.py` |
| landing closer | +5.64 to +10.08 | `tipworth.py` |
| copy replay H−1 / H (Oct 23 → Oct 25 17:58) | +4.51 / +2.55 | `replay_days.rs` |
| pre-fire vs copy (Oct 23 → Oct 25 18:00) | +2.69 vs +5.50 | `prefire.py` |
| copy his failed attempts | −0.30 | `failcopy.py` |
| operator rule, timed | +8.15 / +6.66 / +2.36 | `oprule/options.py` |
| wider limit | −1.05 / −1.79 / −2.07 | `fails/prem5.py` |
| second buy after a refusal | −0.50 to −3.57 | `fails/him_second_try.py` |
| right behind him: D = 0 / 10 / real | +11.97 / +8.07 / +5.51 | `fails/prem5b.py` |
| conditional wider limit (picked Oct 21-23, scored Oct 24-25) | −0.009 / −0.027 added | `fails/condlimit.py` |
| **live** (Oct 26 15:00 → Oct 27 11:45 Beirut) | **he +8.9099, our 162 copies −0.0479** | `05-live/check-sh-2026-10-27.txt` |

**Oct 28 re-run and extension** ([`analysis/research/2026-10-28/copy_relook/`](../analysis/research/2026-10-28/copy_relook/README.md), picked on Oct 21-23, scored on Oct 24-25, [without the best 2 copies]):

| Test | Result | Source |
|---|---|---|
| every published number above (ablate, scratch D table, prem5/prem5b, options, tipworth) | reproduced | `report.md` §A |
| the +8.02 by period | Oct 21-23 +7.75 [+4.82]; Oct 24-25 +0.27 [−0.52] | §B, `recon.py` |
| live rebuilt step by step (3M cost, 31% next-slot landing, 16% late sells, the bid mix) on Oct 24-25 | net −0.0004 a fill, as live | §B |
| stake × bid, 5 days | 3M: +3.32 / +7.77 / +16.85 / +26.17 at 0.25 / 0.5 / 1.0 / 1.5; Oct 24-25 [x] negative at every stake | §B |
| stake ladder by his tip 0.5/1.0/1.5 | +17.28 [+13.54]; Oct 24-25 +0.73 [−1.69]; capital 2.5 SOL | C1 |
| exits by tip bucket | the per-bucket picks −0.17 on Oct 24-25 against +0.21 for H − 1 everywhere | C2 |
| sells one slot late (16% measured live) | −0.43 over 5 days (−2.70 if every sell) | C3 |
| circuit breakers (4 kinds) | 0 to +0.40 over 5 days, −0.13 to −0.65 live | C4 |
| a second copy after a refusal; the low-tip buys | −0.08 [−0.49]; all 531 low-tip buys −2.17 | C5 |
| the operator count with the table kept | −0.06 over 5 days; the table alone +1.71 | C6 |
| the bid at its own landing | 3.0M +7.30, 8.0M +6.29; 1.5M +7.68 if it lands as 3M (untested) | C8 |
| a key on his tip + priority fee (from the on-chain re-check) | the 130 added copies −0.83 [−1.41], 4 of 5 days negative; the whole key +6.94 against +7.77 | C9, `c9_bidkey.py` |

## S7: other copy targets

| Test | Period | Result (SOL) | Source |
|---|---|---|---|
| selection split | Oct 23-25 | +1.57 / +0.26 / −0.68; backwards −0.59 / −0.03 / −2.70 | `wallets/split.py` |
| 13 finalists out of sample | Oct 25 18:00 → Oct 26 11:00 / 14:50 | −4.86 (1,052) / −4.84 (1,608) | `oos_screen.py` |
| JBokzLFR fixed exit +5 / +9 | in / out of sample | +1.10 / +1.93; +0.97 / +1.40 | `oos_screen_nosell.py` |
| dump-and-bounce, early / later | | −26 to −66 (1,305); 0 of 144 positive | `flush/bounce.py`, `flush/later.py` |
| 3yrJE1A8 exit grid | Oct 24 → Oct 26 12:00 | +5: +3.42 … **+29: +8.28** | `w3/grid.py`, `eval.py` |
| 3yrJE1A8 after its first sell / early sells / take profit | same | +3.35 / +7.07 / +8.91 vs +8.25 | `eval.py`, `early.py`, `tp.py` |
| 3yrJE1A8 no limit / second try / 2 SOL at 7.5-10% | same | +8.01 / −0.13 to +0.29 / +0.28, −0.17 | `w3/prem.py`, `second_try.py`, `condlimit.py` |
| 3yrJE1A8 on SOL coins only | Oct 24-26 | +6.32 (166) | `w3/solonly.py` |
| second search, 7 wallets | Oct 25 18:00 → Oct 26 17:15 | +0.30 … −1.66 | `wallets2/process2.py` |
| CxyKYmQo / D5BDDkBt halves | same | +1.44 / +0.71; +0.72 / +0.72 | `wallets2/process3.py` |
| AMDEmVoc / JBbbosQC / M8CcrseQ | same | −1.27 / −1.31 / −0.64 | `process3.py` |
| own result vs a copy (top 30 earners) | Oct 25 18:00 → Oct 26 17:40 | +320.7 vs +7.2 | `ownvscopy.py` |
| 6anjqMe, all / size 1-2 SOL | Oct 21-25 (Oct 1-20) | +0.25, −4.49 / +2.26 (−0.48) | `six/copy.py`, `copy2.py` |
| **live** (check.sh window) | Oct 26 15:00 → Oct 27 11:45 Beirut | wallet 2 −0.0135 (61 sent), wallet 6 +0.0857 (8); wallets 3, 5 about −0.39, −0.54 | `05-live/check-sh-2026-10-27.txt`; session notes |

Wallet 4 (H9kuqGKN) tests are in the copy2 repo (`04-backtests/`).
