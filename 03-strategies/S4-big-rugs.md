# S4. Big rugs: what predicts them and what reduces them

In short: research on the night of 2026-10-24 into the coins that lose 30% or more on S3's tweet rule (docs/15). On
1,881 rule coins, 42 big losses (2.2%) make 27% of all the money lost, and they come from the same insider-heavy
launches as the big winners, so almost every skip rule costs more than it saves (docs/15 §1-2). One rule held in all
three 12-hour periods: skip coins from `m.rapidlaunch.io` whose insiders are on the dumper list (+0.40 SOL over 36 h)
(docs/15 §3). It shipped as `entry.dumper_skip_hosts`, with the rapidlaunch fix `entry.hidden_dev_buy = "grpc"`
(docs/15 §6), and both were on the box by Oct 25 (docs/17 §8). Idle since the rule buys were switched off (docs/17 §9).
The pre-buy cap `max_post_bundle_sol = 40` (docs/11 Q2) stays.

| | |
|---|---|
| Status | research; two gates built; rapidlaunch dumper skip and hidden dev buy on the box by Oct 25 (docs/17 §8); no live result of the skip reported; idle since rule buys are off (`entry.rule_buys = false`, docs/17 §9) |
| Built from | not one of his rules. The 40 cap (listed under rule 2, picks, in [his rules](../02-his-rules/README.md)) comes from his and our losses above 40 (docs/11 Q2); the copy problem comes from his tweet coins (rule 3, S3) |
| Code | `crates/rugsnipe/src/dumpers.rs` (the dumper list: cold thread marks, hot loop checks at the create), `crates/rugsnipe/tests/hidden_dev.rs`, `crates/pump-codec/tests/create_hit_fixtures.rs`, fixture `crates/pump-codec/fixtures/tx/rapidlaunch_create_v2_cpi_dev_buy.json`, [`deploy/bin/rugsnipe-check`](../deploy/bin/rugsnipe-check) (hits by host); `analysis/scripts/strategy/operators_refresh.py --drop-dumpers` (table side, docs/09) |
| Config keys | `entry.dumper_skip` (`"log"` / `"skip"`), `entry.dumper_skip_hosts`, `entry.hidden_dev_buy`, `entry.max_post_bundle_sol`, `entry.tweet_feed`, `entry.tweet_feed_keys` (docs/15 §3, §4, §6; docs/08 §9) |
| Source docs | [docs/15](../docs/15-big-rugs.md) §1-6; [docs/11](../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md) Q2; [docs/08](../docs/08-runbook.md) §9 (`dumper_skip`); [docs/17](../docs/17-newest-bot-vs-him-5-days.md) §4 |
| Research | [`analysis/research/2026-10-24/rugs/`](../analysis/research/2026-10-24/rugs/) (docs/15 names only the folder; the per-row scripts below are matched by their header comments); the coin set comes from `corrected/bt.py` (docs/14); docs/11's `rugs.py` and `q2.py` are in `analysis/research/2026-10-24/` |

Words: a **create** launches a coin; a **slot** is one Solana block (about 200 ms, docs/01 C6); the **curve** is the
pump.fun price formula, and its virtual SOL reserve starts at 30 (docs/11 Q2); the **bundle** is the dev's own buys right
behind the create; **insiders** are the creator, the signer and the bundle wallets; a **big loss** is -30% or worse for
the first outside buyer (docs/15); a **copy** is a later coin on a tweet an earlier coin used; the **dumper list** marks
insider wallets whose launch was dumped; **out of sample** means scored on data the rule was not chosen on.

## The rule (what is in the bot)

1. **Cap the entry:** skip a post-bundle virtual SOL reserve above 40 (`entry.max_post_bundle_sol = 40`, docs/11 Q2).
2. **Exit mode:** S3's live `"exit"` sells a coin that is not first on its tweet at create + 3. That already removes a
   third of the big losses: 65 at hold 10, 42 under `"exit"` (docs/15 §1).
3. **Dumper skip on rapidlaunch only** (docs/15 §3, §6), switched on together with the hidden dev buy:

```toml
[entry]
hidden_dev_buy = "grpc"
dumper_skip = "skip"
dumper_skip_hosts = ["m.rapidlaunch.io"]   # j7 and uxento hits stay journaled and fired
```

4. **TweetStream copy skip** (`entry.tweet_feed = "on"`, S3) would catch about one copy in five (docs/15 §4).

**The dumper list** (docs/08 §9, 2026-10-23): the cold thread tracks every bundled launch and marks the create's signer
and the bundle wallets when they sold at least half of their tokens by create + 3; the set persists in `state.db`
(`dumpers`). `"log"` journals `dumper <mint> logged (would skip)`, `"skip"` drops the create as `skip_dumper`.

**The rapidlaunch blind spot** (docs/15 §6, 2026-10-25): the tool buys for the dev by CPI inside the create. The shreds
copy of the create arrives about 6 ms before gRPC, carries no inner instructions, reads a 0 SOL dev buy, fails the
dev-buy template and is dropped. `hidden_dev_buy = "grpc"` parks such a create and checks the template on the executed
buy at the fire.

## How it was found

- **Rugs are atomic** (docs/11 Q2): the 6 trades below -20% on Oct 24 (2 ours, 4 his) are the same event every time.
  All insider wallets sell their whole bundle in one slot, usually 4 transactions back to back, 0 to 9 slots after the
  entry. No exit rule can sell first. docs/15 §1: insiders had sold half their tokens by slot +2 in 30 of the 62 big
  losses at hold 10. (docs/15 counts 65 big losses at hold 10 in the same section; the source gives both numbers.)
- **Rugs and big winners are the same coins** (docs/15 §1): every big loss had insiders holding 18-27% of the supply
  after the bundle. Coins under 15% never lost 30% but are worth only +1.5%; at 25% or more they are worth +6.9% and lose
  30% 7% of the time (hold 10).
- **Exits that react fail** (docs/09 "Exit clocks"): a sell on the creator set's first sell, on a big outside buy,
  take-profits and stops all lost: "a rug is one block".
- **The first dumper skip** (docs/08 §9, `dumper_skip`): dry run +0.6 points per fill out of sample for skipping such
  operators (post-hoc, 52 launches); left in `"log"`.

## Backtests

Data for docs/15 rows: the 1,881 rule coins of docs/14 (Oct 23 all day, Oct 24 00-12 UTC), live `"exit"` policy, net
of 1.2%, 0.5 SOL stakes; "P&L, 36 h" is the change against no skip, summed over the three 12-hour periods (docs/15).

| Test (skip, unless stated) | Period | Coins hit | Their value | Big losses removed (of 42) | Result | Source |
|---|---|---|---|---|---|---|
| The bot's dumper list | 36 h | 482 | +2.27% | 30 | -5.46 SOL | docs/15 §2; `rug_rules.py` |
| An insider dumped 4+ launches | 36 h | 285 | +3.32% | 16 | -4.73 SOL | docs/15 §2; `rug_rate.py` |
| An insider's dump rate 50%+ (2+ known launches) | 36 h | 40 | +0.12% | 7 | -0.02 SOL | same |
| Deployer's last coin was a big loss | 36 h | 56 | +4.83% | 4 | -1.35 SOL | docs/15 §2; `rug_track.py` |
| Deployer's last 10 coins average below 0 | 36 h | 412 | +0.50% | 12 | -1.04 SOL | same |
| Template's last coin was a big loss | 36 h | 57 | +3.51% | 4 | -1.00 SOL | same |
| Deployer launches mostly copies (60%+ of last 20) | 36 h | 220 | +5.14% | 5 | -5.66 SOL | docs/15 §2; `rug_copyrate.py` |
| Ticker or name of a tool coin of the last 60-300 s | 36 h | 529-824 | +1.8 to +2.2% | 8-17 | -5.3 to -8.7 SOL | docs/15 §2; `rug_recent.py` |
| Ticker or name in a tweet an earlier coin used (tweet book) | 36 h | 762 | +2.73% | 14 | -10.39 SOL | docs/15 §2; `rug_book.py` |
| Tweet feed's copy call, every author followed | 36 h | 530 | +2.61% | 13 | -6.91 SOL | docs/15 §2; `rug_feed.py` |
| Sell the dumper-list coins at create + 3 | 36 h | 482 | | 39 -> 40 | -5.82 SOL | docs/15 §2 |
| Sell on the insiders' first sell, or at 10 / 25 / 50% sold | 36 h | all | +3.67 to +3.73% (+3.68% now) | 64-65 (65 now) | 0 | docs/15 §2; `rug_exit.py` |
| Wait for slot +1, buy only if insiders have not sold | 36 h | all | +0.26% (+2.97% now) | 52 (42 now) | -25.5 SOL | docs/15 §2; `rug_wait.py` |
| **Dumper list and `m.rapidlaunch.io`** | Oct 23 00-12 UTC | 35 | -1.47% | 3 of 13 | +0.26 SOL | docs/15 §3; `rug_combo.py` |
| same | Oct 23 12-24 UTC | 12 | -0.21% | 2 of 12 | +0.01 SOL | same |
| same | Oct 24 00-12 UTC | 25 | -1.01% | 3 of 17 | +0.13 SOL | same |
| same, all | 36 h | 72 | -1.10% | 8 of 42 | +0.40 SOL | same |
| Same rule, list counting insider sells within 5 slots | 36 h | 119 | +0.56% | | -0.33 SOL | docs/15 §3 |
| Copies sold at create + 1 instead of + 3 | 36 h | copies | -0.1% against -0.2% | big losses 12 against 24 | | docs/15 §2 |
| Second TweetStream key (5 more handles) | 36 h | copy calls 104 -> 147 | | big losses among them 2 -> 6 | | docs/15 §4; `next5.py` |
| Rapidlaunch coins, with or without a dumper-list insider | 36 h | 72 of 190 | -1.1% / +5.2% | 8 | | docs/15 §6 |
| Post-bundle cap at 40 (chain truth, post hoc) | Oct 24 00:00-12:29 | above 40: us 4, him 29 | | us 1 rug, him 2 | us -0.364 SOL, him -0.839 SOL above 40 | docs/11 Q2 |
| Skip a creator 3 h after one of its launches dumps | Oct 24 00:00-12:29 | | | | saves him 1.54 SOL, costs us 0.26 SOL (not adopted) | docs/11 Q2 |
| Higher flat bid above 40 (curve model) | Oct 21-25 | 4M / 16M / 24M | | | +2.8 / +5.3 / +6.0 SOL; without the top 10 coins -1.0 / -0.4 / -0.8 SOL | docs/17 §4 |

## Live

- **Oct 24 00:00-12:29 UTC** (docs/11 Q2): 6 trades below -20% (2 ours, 4 his). Above 40: our 4 trades -0.364 SOL with
  1 rug, his 29 trades -0.839 SOL with 2 rugs.
- **Oct 24 17:29-18:39 UTC** (docs/15 §1): 2 of our 33 live trades lost 40%. Both were copies (j7, dev 5, post-bundle
  39.3 and 39.9, on tweets by @thegoat195923 and @toly). Our copies made -7.75%, our first coins +4.38%. The backtest
  rate is 2.2 big losses in 100; "the live 2 in 33 is above that rate, on a small sample" (docs/15 §5).
- **Copy verdict latency** (docs/15 §2): the metadata fetch is p50 0.6-0.9 s live; 3 verdicts in 4 land at slot +2 or
  later, so the create + 1 cut is out of reach. "That latency is on the tool's server."
- **Rapidlaunch** (docs/15 §6, 2026-10-25): the live bot had traded no `m.rapidlaunch.io` coin (0 of 107 attempts),
  against 10% of the backtest's rule coins; the copied wallet landed 9 overnight.
- **On the box by Oct 25** (docs/17 §8): `dumper_skip = "skip"` on `m.rapidlaunch.io`, `hidden_dev_buy = "grpc"`,
  `max_post_bundle_sol = 40`. No live result of the skip is reported.
- **Above 40, five days Oct 21-25** (docs/17 §4): our 25 wins there lost -1.149 SOL (-9.4% a trade), against his 153 at
  +21.3%.

## Verdict

- **Rugs cannot be removed without the gains** (docs/15 §5): they come out of the same insider-heavy launches. A
  dumper's next launch, a deployer whose last coin rugged, a template that rugged: each of those coins is worth more
  than the average one (docs/15 §2). Those skips were dropped.
- **What reduces them** (docs/15 §5): the exit mode (65 -> 42, live), the feed's copy skip once `"on"` (about a fifth
  of the copies) and the rapidlaunch dumper skip if the live day confirms it (about 8 of 42). Together "at most a third
  of the remaining big losses". The 40 cap (docs/11 Q2) sits in front of all of them.
- **The cap stays** after a five-day re-test: no flat bid fixes the coins above 40, and nothing we see before the fire
  reproduces his bid (docs/17 §4, §6).
- **Since docs/17 §9** the box buys copies only, with `dumper_skip` off, so the S4 gates no longer act.

## Open questions

- Does the rapidlaunch dumper skip hold live? docs/15 §3 asked for a live day in `"log"` first; no result is reported.
- The bot's dumper list flags more wallets than the research list, which makes the rule fragile (docs/15 §3).
- The copy verdict needs the tool's metadata server; only a launch tool's own feed would make it faster (docs/15 §2,
  docs/13 §4).
- 65 against 62 big losses at hold 10: docs/15 §1 gives both.

## Sources

- [docs/15-big-rugs.md](../docs/15-big-rugs.md)
- [docs/11-operator-bot-vs-copied-wallet-2026-10-24.md](../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md) Q2
- [docs/08-runbook.md](../docs/08-runbook.md) §9 config table (`dumper_skip`, `dumper_skip_hosts`)
- [docs/09-operator-wave.md](../docs/09-operator-wave.md) "Exit clocks", [docs/14-corrected-backtest.md](../docs/14-corrected-backtest.md) §1-2
- [docs/17-newest-bot-vs-him-5-days.md](../docs/17-newest-bot-vs-him-5-days.md) §4, §6, §8, §9
- [analysis/research/2026-10-24/rugs/](../analysis/research/2026-10-24/rugs/), [analysis/research/2026-10-24/README.md](../analysis/research/2026-10-24/README.md)
