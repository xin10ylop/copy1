# S5. Follow the operators he follows (bundle wallet x fee routing, `entry.follow`)

In short: a launch counts as followed when one of its bundle wallets has a record of him attempting its launches
(2 or more attempts at a rate of 30% or more), kept separately for each fee routing. In mode `on` the rule bot skips
unfollowed rule coins and adds followed coins the rule skips. Found and built on Oct 25 (docs/16).
Out of sample it picks coins he attempts 79-80% of the time, worth +4.74% a trade (docs/16 §8). It ran in the box's rule
config on Oct 25 (docs/17 §8). But at our landing rates the exact replay made only +1.03 SOL in 2.7 days, against his
+33.5 SOL (docs/17 §8). It has been idle since the bot went copy-only (S6, `entry.rule_buys = false`).

| | |
|---|---|
| Status | built; ran live inside the rule bot on Oct 25 (`follow = "on"`, rate 0.3, docs/17 §8); idle since the bot went copy-only (`buys: copies of his buys only (entry.rule_buys = false)`, [check.sh paste](../05-live/check-sh-2026-10-27.txt), Oct 27). Hot-operator sizing built but left at 1.0; coin mode logged only |
| Built from | his selection: he follows operators by their bundle wallets, as two operators per fee routing, and buys a hot operator's coin bigger ([his rules](../02-his-rules/README.md); docs/16 §3, §8, §9, §10) |
| Code | `crates/rugsnipe/src/follow.rs` (`rugsnipe::follow::FollowTracker`, the cold thread); `crates/rugsnipe-feed/src/bundle.rs` (`RunPrice`, the price at create + 10); `crates/pump-codec/src/create_hit.rs` (`CreateHit.creator_fee_bps`); `deploy/bin/rugsnipe-follow-merge`; `deploy/bin/rugsnipe-check` (follow section); `data/follow_seed.json`, `data/follow_seed_today.json` (docs/16 §5, §7, §10, §11) |
| Config keys | `[entry] follow` = off / log / gate / add / on; `follow_wallet` = his wallet; `follow_min_attempts` = 2; `follow_min_rate` = 0.3 (docs/16 §7; the runbook default is 0.5); `follow_min_dev_sol` (default 0.25), `follow_hot_min_value` (0.10), `follow_hot_stake_mult` and `follow_cold_stake_mult` (both 1.0) (docs/08 §9 table, docs/16 §10). Box value on Oct 25: `follow = "on"`, rate 0.3 (docs/17 §8). The check.sh paste does not print these keys |
| Source docs | [docs/16 §1-§11](../docs/16-who-he-follows.md); [docs/17 §1, §8, §9](../docs/17-newest-bot-vs-him-5-days.md) (the replays with the follow on) |
| Research | [analysis/research/2026-10-25/follow/](../analysis/research/2026-10-25/follow/README.md) |

Words used here:
- **create**: the launch transaction of a pump.fun coin. "Create + k" is k slots after it.
- **slot**: one Solana block. The sources disagree on its length. docs/01 C6 (214-221 ms) and docs/16 §8 (about
  0.21 s, Oct 23-25) measured it on chain. The later files say about 0.4 s
  ([copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt) header; docs/19 §13: create + 9 is "about 4 seconds").
  These pages use the later figure, but note that the earlier ones are chain measurements.
- **curve**: the coin's bonding curve. Its SOL and token reserves set the price. "Post-bundle 40 vSOL" (pb 40) means
  40 virtual SOL in the curve after the bundle. The bot's cap is pb <= 40 (`max_post_bundle_sol`, docs/17 §4).
- **operator**: someone who launches many coins, each from a fresh deployer wallet.
- **bundle**: the operator's own buys right behind the create, made with the same few wallets every time.
- **fee routing**: who gets the creator fees. Either the dev keeps them (a plain coin), or a fresh third address gets
  them (the holder-reward mode, docs/16 §11).
- **attempt**: any transaction of his on the mint, landed or failed. His failed buys land too: his own guard rejects
  them (docs/16 intro).
- **landed**: included in a block. **tape**: every trade on a coin over its first slots.
- **out of sample**: scored on data that was not used to pick the setting.
- **tip**: SOL paid to the block leader to order a transaction. 1M lamports = 0.001 SOL.

## The rule

1. **Learn (cold thread).** For each record (bundle wallet, fee routing), count the bundled launches it was in and how
   many of them he attempted. His attempts come from a gRPC filter on `follow_wallet`, failed transactions included.
   An attempt counts when the mint was created in the last 4 slots. The counts are saved every minute to `follow.json`.
   A record unseen for about 3 days is forgotten (docs/16 §5, §8).
2. **Followed.** A record is followed with at least `follow_min_attempts` (2) attempts at a rate of at least
   `follow_min_rate` (0.3). A coin is followed when one of its bundle wallets is, with the coin's own fee routing
   (docs/16 §5, §8).
3. **Act (hot loop, at the fire).**
   - `log`: journal only.
   - `gate`: skip the rule's coins that are not followed (`skip_not_followed`, 0x61).
   - `add`: also buy the followed coins the rule skips, at stake tier 0, through every other check.
   - `on`: both (docs/16 §5). docs/16 §6 recommends `on` with rate 0.3.
4. **Hot operators (sizing, built, off).** A record is hot when its last 3 coins' price at create + 10, over the price
   after the bundle, averages at least `follow_hot_min_value` (0.10). The stake is multiplied by
   `follow_hot_stake_mult` or `follow_cold_stake_mult`. Both stay at 1.0 (docs/16 §10).
5. **Coin mode (logging only).** The verdict line ends `mode plain|holder[+bps<n>]`. Nothing is skipped on it
   (docs/16 §11).
6. **Warm start.** The tracker starts from `data/follow_seed.json`: 9,176 records, 613 of them hot (docs/16 §10).

## How it was found

- **His outside picks.** 713 attempts in 36 h fall outside our rule. They are 34% of his 2,103, but a small part of his
  profit: +3.5 SOL on 201 closed trades, against +23.9 SOL on 366 rule trades (docs/16 §1).
- **No coin feature explains them.** Tested: dev buy and host, tool settings, the creator's history with him, tweets,
  funders. Precision and recall stay low out of sample (docs/16 §2 table). 64% of his outside picks come from creators
  he never traded (docs/16 §2).
- **The bundle wallets do.** An operator rotates deployers but reuses its bundle wallets. Grouped that way, he attempts
  92-100% of some operators' launches. Examples: `5sWHrtKx` 98% of 236 rule coins, `2T3U2FzV` 100% of 14 (docs/16 §3).
- **Fee routing splits an operator in two.** Example: `J4o3bqXK` + 2 wallets got 21 of 36 attempts when the dev kept the
  fees, and 0 of 44 when a third wallet got them (docs/16 §8). The "third wallet" routing is the holder-reward mode:
  601 of 609 holder-reward creates have it (docs/16 §11).
- **Inside an operator, recent value moves him.** After a skip he takes the next coin 9.8% of the time when the
  operator's last coins made -5% or worse, and 39.6% at +10% or better (docs/16 §9). His stake follows the same signal:
  0.909 SOL median on a hot operator, 0.604 on the rest (docs/16 §9, §10).
- **He avoids creator-fee coins.** Holder reward with a `creator_fee_bps`: 2% taken, 1 of 40 inside the cells he
  follows. Plain coins with a fee of 100 bps or more: 0% (docs/16 §11).
- **His exit was not copied.** Selling each followed coin at his learned sell slot per cell was not a proven gain
  (docs/16 §8).

## Backtests

"% a trade" is the value per trade for the first buyer outside the bundle, net of 1.2%. "Sum" adds the per-trade %;
divide by 100 for SOL per 1 SOL staked per trade (docs/16 §4). Fit on Oct 23 00-12 UTC, scored on Oct 23 12-24 and
Oct 24 00-12 UTC unless stated.

| test | period | setting | result | n | source / script |
|---|---|---|---|---|---|
| ex-ante follow, rule coins | out of sample, Oct 23 12-24 / Oct 24 00-12 | wallet key, K 2, R 0.5 | his rate 74% / 74% on followed coins, 11.7% / 8.6% on the rest; 72% / 79% of his picks covered | 613 / 440 coins | docs/16 §3, `ev.py` |
| the four modes | out of sample, same | current rule / gate / add / on (pb <= 40) | +2.45% / +3.63% / +3.17% / +4.53% a trade; sums +3,322 / +2,936 / +4,894 / +4,508 | 1,357 / 808 / 1,545 / 996 | docs/16 §4, `final.py` |
| the coins `add` adds | out of sample, same | followed, rule skips | +8.36% a trade [+6.18, +10.32] | 188 | docs/16 §4 |
| last night replayed | Oct 25 00:00-09:13 | `on`, R 0.3, wallet key / keyed | +0.59 SOL / +1.10 SOL (actual -0.10; his night +0.95) | 72 of our trades | docs/16 §6, §8, `night*.py` |
| the key (wallet, fee routing) | out of sample, same | K 2, R 0.3 | his rate 79% / 80%; +4.74% a trade [+3.82, +5.61]; sum +4,653 | 981 | docs/16 §8, `evkey.py` |
| followed coins he skipped vs took | out of sample, same | K 2, R 0.3 | +2.81% vs +4.62% a trade | 174 / 840 | docs/16 §8, `skipval.py` |
| his exit copied per cell | out of sample, same | median of his last 3 sell slots | +4.04% vs +3.47% (live exit); paired +0.57 pts [-0.39, +1.73] | 895 | docs/16 §8, `exit.py` |
| today, live data | Oct 25 09:13-13:07 | seed, then learn in slot order | he attempted 49 of 67 followed coins (73%), +0.584 SOL for him | 67 | docs/16 §9, `today.py` |
| recent value as well | out of sample, same | attempts + cell's last 3 coins >= +10% | +7.72% a trade [+5.90, +9.69] | 321 | docs/16 §9, `evval.py` |
| hot / cold stakes | out of sample followed coins, 0.55 SOL bankroll | flat 0.5 vs 0.5 hot / 0.33 cold | +23.3 SOL vs +18.8 SOL | 981 | docs/16 §10, `kelly.py` |
| one model of his take | fit Oct 23 00-12, scored later | everything decoded | AUC 0.882 / 0.937 | | docs/16 §10, `model.py` |
| coin mode in the key | out of sample, Oct 23-24 | mode added | adds nothing (79% either way) | | docs/16 §11, `evmode.py` |
| exact replay, box config | Oct 23 00:00 - Oct 25 17:58 | `on`, rate 0.3 / 0.6 / 0.7, bound 0 | projected +1.03 / +1.96 / +2.06 SOL (his +33.5) | 1,816 / 1,153 / 856 fires | docs/17 §8, `five/exact/an2.py`, `replay_days.rs` |
| exact replay, 5% bound | same | rate 0.3 / 0.6 / 0.7, sold at create + 9 | +4.19 / +2.95 / +3.17 SOL | 585 fills at 0.3 | docs/17 §9, `five/copy/bound.py` |
| newest bot vs his buys | Oct 21 00:00 - Oct 25 16:07 | stand-in config, `on`, rate 0.3 | fires on 3,847 coins; he attempted 85% of them, landed 18% | 3,847 | docs/17 §1, `replay_days.rs`, `five/an.py` |

Two notes:
- **Which rate.** With a 0 bound, 0.6 beat 0.3 on every day (docs/17 §8). With the 5% bound, 0.3 stays best
  (docs/17 §9). The later setting is the 5% bound, so 0.3.
- **The exact replay starts empty.** Its follow tracker starts with no records at Oct 23 00:00. The box ran from a seed
  (docs/17 §8).

## Live

The follow ran inside the rule bot. No source splits our live P&L by follow verdict.

- **Live check, Oct 25 14:51-15:36 UTC.** The bot sent on 17 launches. The replay fired on 14, and 12 of them were the
  same. The 5 the replay skipped were follow adds: the box's seeded tracker followed their wallets, the replay's did not
  yet (docs/17 §8).
- **Landing, by what he did** (the exact replay's fires at our live rates, docs/17 §8):

  | he ... | fires | value at +10 | our live landing | our result per fill |
  |---|---|---|---|---|
  | did not try | 611 | +6.0% | 42% (78 of 184) | -0.0145 SOL |
  | tried and failed | 944 | +17.3% | 34% (92 of 267) | +0.0148 SOL |
  | landed | 261 | +7.6% | 0% (0 of 47) | - |

- **Five days live, all configs of the time:** -6.582 SOL on 1,138 coins sent, 517 filled. The fires he tried made
  +1.079 SOL. The fires he did not try made -2.063 SOL (docs/17 §2).
- **Whole bot on Sun Oct 25:** 92 trades, -0.5373 SOL ([copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt),
  by day). The file does not split the day by config or by follow verdict. The copy bot (S6) started at 22:08 UTC
  that day ([fails/README](../analysis/research/2026-10-26/fails/README.md)).
- **Now:** idle. The check.sh paste of Oct 27 11:45 Beirut shows `entry.rule_buys = false`. With the rule off, its
  gates are idle, the follow among them (docs/17 §9, "Copy only").

## Verdict

The follow decodes his selection well: 79-80% of followed coins are his picks, and the model reaches AUC 0.88-0.94
(docs/16 §8, §10). Selection is not our problem, though. On the coins he lands he is first, and our buy fails behind
him. On the coins he skips, ours lose (docs/17 §8). The first spot is an auction, and we win it only when nobody else
wants the coin (docs/17 §3). With the follow on, the rule bot projects +1.03 SOL in 2.7 days, against his +33.5
(docs/17 §8). Copying his landed buy (S6) replaced it. Keep the tracker and the seed as the map of his operators. Do not
expect money from the follow alone at our landing rates.

## Open questions

- **Not built:** the creator and signer as identities (+6-8 points of outside coverage), and coins with no bundle
  through dev-wallet reuse (docs/16 §7, §8).
- **Hot sizing.** `follow_hot_stake_mult = 1.5` waits for a higher stake cap. The cold multiplier waits for our own cold
  trades (docs/16 §10).
- **Creator-fee coins.** A skip waits for our own trades on them (docs/16 §11).
- **Holder-reward skip.** "Skip a holder-reward coin when he did not attempt the signer's previous coin" was listed as
  worth adding (docs/17 §6). The sources do not say whether it was built.
- **Slot length.** 0.21 s (docs/16 §8) against about 0.4 s (later sources). The forget window (1,250,000 slots, "about
  3 days", docs/16 §8) depends on it.

## Sources

- [docs/16-who-he-follows.md](../docs/16-who-he-follows.md) §1-§11
- [docs/17-newest-bot-vs-him-5-days.md](../docs/17-newest-bot-vs-him-5-days.md) §1, §2, §3, §6, §8, §9
- [docs/08-runbook.md](../docs/08-runbook.md) §9 (the `entry.follow` key table and defaults)
- [analysis/research/2026-10-25/follow/README.md](../analysis/research/2026-10-25/follow/README.md) and its scripts
- [analysis/research/2026-10-25/five/exact/README.md](../analysis/research/2026-10-25/five/exact/README.md),
  [five/copy/README.md](../analysis/research/2026-10-25/five/copy/README.md)
- [05-live/check-sh-2026-10-27.txt](../05-live/check-sh-2026-10-27.txt) (status line: `entry.rule_buys = false`)
- [05-live/copy-bot-history-2026-10-28.txt](../05-live/copy-bot-history-2026-10-28.txt) (whole bot by day)
