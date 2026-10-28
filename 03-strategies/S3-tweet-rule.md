# S3. Tweet rule: his deployers' coins, first coin on a fresh tweet

In short: built on 2026-10-24 on top of the operator bot (S1). Buy launch-tool coins (j7tracker, uxento, rapidlaunch)
with a template dev buy and a post-bundle curve of at most 40 virtual SOL, from a deployer he traded in the last 7 days,
and sell at create + 10 (docs/13 §1, §6). The "tweet check" (is this the first coin on a fresh tweet?) needs the coin's
metadata file, which arrives too late for the buy (docs/13 §4). docs/13 reported +5.0% a trade; docs/14 re-measured on
complete tapes: +3.68% buying all and holding 10, +2.97% in the live "exit" mode, and advised `tweet_gate = "log"`
(docs/14 §2). Live in "exit" mode by Oct 24 17:29 UTC (docs/14 §5, docs/15 §1). Rule buys were off by Oct 26-27,
when the box bought copies only (docs/17 §9). The TweetStream copy skip (`entry.tweet_feed`) was built and ran in "log"
only.

| | |
|---|---|
| Status | live from Oct 24 evening to Oct 25-26 in "exit" mode (docs/17 §8 lists `tweet_gate = "exit"` in the box's config); then rule buys off (`entry.rule_buys = false`, docs/17 §9, [check output](../05-live/check-sh-2026-10-27.txt)); `tweet_feed` built, "log" only |
| Built from | [his rules](../02-his-rules/README.md) 2 (picks: his 7-day deployer list, launch tools, dev-buy templates), 3 (the tweet layer), 5 (hold: create + 10 here) |
| Code | `crates/rugsnipe/src/tweet.rs` (tweet check, `TweetBook`), `crates/rugsnipe/src/tweetfeed.rs` and `crates/rugsnipe-feed/src/ws/tweetstream.rs` (feed lane), `crates/rugsnipe/tests/tweet_gate.rs`, [`deploy/bin/rugsnipe-check`](../deploy/bin/rugsnipe-check) (check.sh views), `analysis/scripts/strategy/operators_refresh.py --source rpc` (the 7-day deployer table) |
| Config keys | `[entry]` `require_bundle`, `operators_only`, `operator_holds = false`, `uri_hosts`, `dev_buy_sol = []`, `dev_buy_round = false`, `dev_buy_ranges_sol`, `max_post_bundle_sol = 40.0`, `min_stake_tier = 0`, `presend_mode = "log"`, `tweet_gate`, `tweet_max_age_s = 3600`, `tweet_late_slots = 1`, `tweet_min_dev_sol`; `tweet_feed`, `tweet_feed_url`, `tweet_feed_keys`, `tweet_feed_window_s`; `[exit.default] hold_to_create_slots = 10` (docs/13 §6, docs/14 §8); `entry.tweet_cut_tip_lamports` (docs/08 §9); `bid.ab_by_tier`, `sell_tip_lamports`, `dump_tip_lamports` (docs/14 §5) |
| Source docs | [docs/13](../docs/13-tweet-coins.md) §1-6 (superseded numbers), [docs/14](../docs/14-corrected-backtest.md) §1-8 (the correction), [docs/12](../docs/12-how-the-copied-wallet-trades.md) §3-4 |
| Research | docs/13: [`analysis/research/2026-10-24/tweets/`](../analysis/research/2026-10-24/README.md) (`pipeline_day.py`, `dataset_day.py`, `early_fast.py`, `rows.py`, `policy*.py`, `createonly.py`, `symnew.py`, `lateness.py`, `late2.py`, `rivals_sel.py`, `final.py`, `halves.py`, `whofirst.py`, `signer_key.py`, `speed.py`, `namematch.py`); docs/14: `analysis/research/2026-10-24/corrected/` (`fulltape.py`, `fee_bias.py`, `bt.py` engine, `bt_all.py` tables, `hold30.py`, `stakes.py`, `race_bids.py`, `his_first.py`, `tweetfeed.py`, `authors.py`); feed trial: [`analysis/scripts/tweetstream/`](../analysis/scripts/tweetstream/) (`ts_logger.py`, `ts_lead.py`, `feed_linked.py`) |

Words: a **create** launches a coin; a **slot** is one Solana block (about 200 ms, docs/01 C6); the **curve** is the
pump.fun price formula, and its "virtual SOL" reserve starts at 30 (docs/11 Q2); the **bundle** is the dev's own buys
right behind the create; the **deployer** or operator is the create's signer (fee payer); a **copy** is a later coin on
a tweet an earlier coin already used; a **tip** pays the block producer on landing; a **tape** is a coin's full trade
list; **out of sample** means scored on data the rule was not chosen on. 1M lamports = 0.001 SOL; mSOL = 0.001 SOL.

## The rule

Buy a launch only when all of these hold (docs/13 §1):
1. its metadata is on `metadata.j7tracker.io`, `meta.uxento.io` or `m.rapidlaunch.io`;
2. the dev buy is a template amount: 0.95-1.05, 2.95-4.05, 4.95-5.05, or 7 SOL and up;
3. the post-bundle curve is at most 40 virtual SOL (docs/11's rug cap);
4. it is the first coin on its tweet, and the tweet is under an hour old (the tweet check);
5. the deployer is one he traded in the last 7 days.

Sell at create + 10. (docs/13 §1 says "hold 10 slots after entry"; its config and docs/14 §2 count from the create.)

**Modes of `tweet_gate`** (docs/13 §6, docs/14 §2):
- `"on"`: park the create until the verdict and fire only on `first`. From Frankfurt it gives up most first spots.
- `"exit"`: buy conditions 1-3 and 5 at full speed; a copy, stale or no-tweet verdict that arrives after the buy cuts
  the hold (docs/14: the non-first coin is sold at create + 3).
- `"log"`: journal the verdicts, leave the trades alone. docs/14 §2's recommendation.

**Deployer key** (docs/13 §2): the table keys on the create's signer. On tool coins the signer differs from the `creator`
field 31% of the time, and then the creator is a fresh address. The table must remember 7 days and refresh every 4 h;
`operators_refresh.py --source rpc` runs on Triton when the Helius key is at its limit (docs/13 §6).

## How it was found

- **His coins are tweet coins** (docs/12 §3): 31 of 31 launches he attempted in a sampled hour link to a tweet, and
  444 of 469 with readable metadata in 12 h. His attempt rate is 38.8% on uxento, 22.4% on j7tracker, 23.0% on
  rapidlaunch, 0-5% elsewhere; dev buys of 1.05-2.95 SOL get only 3-5%.
- **Each condition's value** (docs/13 §2, before the correction, net 1.77%): tool + template +0.2% (99 coins/h); + cap
  +0.2%; + first coin on a fresh tweet +2.5% (52/h); + his deployer +5.0% (20/h). His list without the tweet check +2.8%;
  his list on non-first coins -0.9%. Neither the tweet check alone nor his list alone held in every half-day.
- **Why the bot cannot wait** (docs/13 §4): on tweet-first coins the first outside buy lands in the create slot on 55%
  of launches. A metadata fetch from Frankfurt takes 222-388 ms (uxento), 256-411 ms (j7tracker), 105-112 ms
  (rapidlaunch). The bot was first on 40 of the 125 deployer-list launches it raced on Oct 24.
- **What did not hold** (docs/13 §3): name or ticker "not seen in 2 minutes" in place of the tweet check (-3.0% on Oct 24
  08-12); buying all and selling early when the check fails (-1.5% against +1.0%); his live attempts in place of the
  7-day list (no better).

## What docs/14 corrected

Two faults in docs/13's trade files (docs/14 §1):
- **No pump fee** on most coins: a buy cost `sol` instead of `sol + 1.25%`. On 427 coins with both formats the value was
  overstated by +1.6 points at hold 1 and +2.3 at hold 10.
- **Cut and missing tapes:** at most 150 transactions per coin; 1,113 of 2,440 coins hit the cap (620 before slot +10).
  111 coins with more than 40,000 transactions were dropped entirely: the biggest winners.

`fulltape.py` re-pulled 2,260 coins (Oct 23 all day, Oct 24 00-12 UTC) with no cap; 1,884 have a first outside buy
behind the bundle at 40 SOL or less (docs/14 §1; its table says 1,881). Costs are now our measured round trip of 1.2%
(6.2 mSOL on 0.5 SOL), not docs/13's 1.77%.

| | docs/13 (superseded) | docs/14 (corrected) |
|---|---|---|
| data | Oct 23 and Oct 24, 00-12 UTC, weighted samples | Oct 23 all day + Oct 24 00-12 UTC, complete tapes |
| cost per trade | 1.77% | 1.2% |
| `"on"` (tweet decides) | +5.0% [+3.2, +7.0], 342 trades | +5.12%, "out of reach" |
| `"exit"` | +3.15%, 547 trades | +2.97% [+2.25, +3.65] |
| buy all, hold 10 | +2.75%, 545 trades | **+3.68% [+2.71, +4.69]**, 1,881 coins |
| exit cut | one slot after entry | create + 3 |
| setting to run | `"exit"` | `"log"`: the copy cut loses in every period |

## Backtests

| Test | Period | Setting | Result | n | Source |
|---|---|---|---|---|---|
| docs/13 rule, `"on"` (superseded) | Oct 23 + Oct 24, 00-12 UTC | net 1.77% | +5.0% [+3.2, +7.0]; half-days +4.0 / +5.1 / +5.7 / +4.8% | 342 | docs/13 §1; `tweets/final.py`, `halves.py` |
| docs/13 `"exit"` (superseded) | same | full speed, copy sold a slot after entry | +3.15% | 547 | docs/13 §4 |
| docs/13 deployer key by signer / signer or creator | same | | +3.6% [+2.1, +5.3] / +4.6% [+2.9, +6.3] | 345 / 447 | docs/13 §2; `signer_key.py` |
| docs/13 expected day (superseded) | 00-12 UTC only | `"exit"`, 32% first-spot rate, 0.5 SOL | about +3.8 SOL/day at our costs | about 10 trades/h | docs/13 §5 |
| Corrected, buy all, hold 10 | Oct 23 00-12 UTC | net 1.2% | +4.07% [+2.39, +5.89] | 41 coins/h | docs/14 §2; `corrected/bt_all.py` |
| same | Oct 23 12-24 UTC (new) | net 1.2% | +3.88% [+2.70, +5.25] | 66 coins/h | same |
| same | Oct 24 00-12 UTC | net 1.2% | +3.10% [+1.03, +5.73] | 50 coins/h | same |
| same, all | Oct 23 + Oct 24 00-12 | net 1.2% | +3.68% [+2.71, +4.69] | 1,881 | same |
| Corrected `"exit"` / `"on"` | same | | +2.97% [+2.25, +3.65] / +5.12% | 1,881 | same |
| Hold at create + H | same | H = 2 / 4 / 6 / 8 / 9 / 10 / 12 | +0.2 / +1.7 / +2.5 / +3.4 / +3.7 / +3.7 / +3.6% | 1,881 | docs/14 §3; `bt_all.py` |
| Hold, first coins against the rest | same | H = 10 | +5.1% against +1.5% | 1,881 | docs/14 §3 |
| Long holds, every 6th coin | same | H = 10-12 / 16 / 30 | +4.9% / +4.2% / +3.6% | 300 | docs/14 §3; `hold30.py` |
| His per-deployer hold against flat 10 | same | | +3.53% against +3.68% | 1,881 | docs/14 §3 |
| Value by his stake tier (before costs) | same | tier 0 / 1 / 2 | +4.44% / +5.91% / +10.87% | 1,620 / 170 / 91 | docs/14 §4; `stakes.py` |
| Stake schemes (ranking only) | same | flat 0.5 SOL, 50% land rate | +18.2 mSOL a trade, +11.4 SOL/day (his ladder scaled: +1.6 SOL/day) | about 627 trades/day | docs/14 §4 |
| Tweet feed, 2 s lag, 10 s window | same | "first" call | 7 coins/h, 95% truly first; +4.27% against +3.59% | not given | docs/14 §6; `tweetfeed.py` |
| TweetStream lag 0.2 s, "first" call | same | coins we won | +1.7% against +2.1% (adds nothing) | 8.5 coins/h | docs/14 §7; `tweetfeed.py` re-run |
| TweetStream lag 0.2 s, "copy" call | same | coins we won | -2.49% against +3.20%; right 60% of the time | 21 / 76 | docs/14 §7; `tweetfeed.py` re-run |
| Tweet authors he favours (ranked Oct 23 00-12) | later coins | took 70%+ / 30% or less | +6.44% / +1.85% | 335 / 84 | docs/14 §6; `authors.py` |
| Exit for the rule's fires | Oct 23 00:00 to Oct 24 12:00 | table H / flat +9 / flat +10, at max_premium 5% | +4.39 / +5.41 / +4.81 SOL | 1,066 fires | docs/17 §9 "The exit" |
| Exact replay of the box's rule bot (follow included) | Oct 23 00:00 to Oct 25 17:58 | box config, live landing rates | +1.1 SOL over 2.7 days, against his +33.5 SOL | 1,816 fires | docs/17 §8; `crates/rugsnipe/tests/replay_days.rs` |

## The tweet feed (TweetStream) and `entry.tweet_feed`

- **How he picks** (docs/14 §6): he attempts 82% of first coins created 2-5 s after their tweet, 51% under 2 s. A tweet
  feed with a lag of about 2 s explains it. But that call finds only 21% of first coins: "+0.7 points on 7 coins an
  hour, not worth a paid feed and a build yet".
- **A fast feed** (docs/14 §7): TweetStream, 165 ms median from the post's own timestamp. Its "copy" call (a ticker or
  name matching a tweet an earlier coin took, within 30 min) fires 15 times an hour. Skipping those would lift our
  trades from about +2.0% to +3.2% on four fifths of the volume. "Small sample; to be measured before it is built."
- **Coverage** (docs/14 §7): the top 5 authors wrote 26% of the later coins' tweets, the top 50 41%. @devvvooooor alone
  had 241 coins on Oct 23-24, 92% of them attempted by him. docs/15 §4: expect the feed to catch about one copy in five.
- **Built** (docs/14 §8): one websocket per key in `entry.tweet_feed_keys`, posts kept for `tweet_feed_window_s` (1,800
  s). At every tweet-host create the coin's ticker (3+ characters) or name (4+) is matched against posts received before
  it: `first`, `copy` or `none`. `"log"` journals; `"on"` also skips a copy before the park (`skip_tweetfeed_copy`, 0x60).
- **Plan** (docs/14 §7): a 3-day, 5-account trial with a logger on the box (`ts_logger.py`); a post must arrive before
  its coins' creates for the copy call to work.

## Live

- **Oct 24 17:29-18:04 UTC** (docs/14 §5): in the 22 races we won, 95 buys failed right behind ours: 6 bid over 3M, 34
  bid 1.5-3M, 55 bid 1.5M or less. The copied wallet was behind us on 10.
- **Oct 24 17:29-18:39 UTC** (docs/15 §1): 33 live trades; 2 lost 40%, both copies. Our copies made -7.75%, our first
  coins +4.38%.
- **Verdict delay live** (docs/15 §2): the metadata fetch takes p50 0.6-0.9 s; 3 verdicts in 4 land at slot +2 or later.
- **Night of Oct 25** (docs/08 §9, `tweet_cut_tip_lamports`): two of the three big copy losses dumped in the slot before
  the cut sell landed; cut a slot earlier, the 29 copies would have made +2.0 points each.
- **Feed in log mode, Oct 25** (`analysis/scripts/tweetstream/feed_linked.py`, header): only 44 of 116 copy calls were
  copies by the tweet check.
- **Mode on the box:** docs/14 §2 advised `"log"`, but docs/17 §8 lists `tweet_gate = "exit"` in the box's config on
  Oct 25. Then docs/17 §9 turned the rule off (`rule_buys = false`, with `tweet_gate`, `tweet_feed`, `follow` and
  `dumper_skip` off); by Oct 26-27 the box printed "copies of his buys only" ([check output](../05-live/check-sh-2026-10-27.txt)).

## Verdict

- **Kept, then retired.** The deployer list, the template, the 40 cap and a flat hold held on complete data: +3.68% a
  trade, positive in all three 12-hour periods (docs/14 §2).
- **Changed by docs/14:** run the tweet check in `"log"` (the copy cut loses in every period); keep `operator_holds =
  false` and hold 10; flat 0.5 SOL stakes; sells 2M -> 0.5M; an A/B bid ladder (`bid.ab_by_tier`, commit c03c4cc; until
  2026-10-25 it read the mint's last byte, odd on every pump.fun mint, so every race bid the second ladder) (docs/14 §3-5).
- **Changed by docs/17 §9:** flat create + 9 and `max_premium = 0.05` for rule fires; then rule buys off for the copy.
- **Why live fell short:** at our live landing rates the whole rule bot projects +1.1 SOL over 2.7 days against his
  +33.5 SOL; its money comes only from coins he tries and loses (docs/17 §8).

## Open questions

- A launch tool's own live feed (mint plus tweet) is "the one paid item that could make `"on"` work"; no public API was
  found (docs/13 §4, docs/14 §6).
- The copy skip rests on 21 against 76 trades (docs/14 §7), and the live log was 44 of 116 calls right (`feed_linked.py`).
- The bid A/B ladder's result is not reported.

## Sources

- [docs/13-tweet-coins.md](../docs/13-tweet-coins.md), [docs/14-corrected-backtest.md](../docs/14-corrected-backtest.md)
- [docs/12-how-the-copied-wallet-trades.md](../docs/12-how-the-copied-wallet-trades.md) §3-4, [docs/15-big-rugs.md](../docs/15-big-rugs.md) §1-2, §4
- [docs/08-runbook.md](../docs/08-runbook.md) §9 config table, [docs/17-newest-bot-vs-him-5-days.md](../docs/17-newest-bot-vs-him-5-days.md) §8-9
- [analysis/research/2026-10-24/README.md](../analysis/research/2026-10-24/README.md), [analysis/scripts/tweetstream/](../analysis/scripts/tweetstream/)
- [05-live/check-sh-2026-10-27.txt](../05-live/check-sh-2026-10-27.txt)
