# S6. Copy his landed launch buys (`entry.copy`)

In short: the bot buys right behind his own landed launch buy (create + 0 or + 1) when his tip is at least 2M lamports
or his buy is at least 2 SOL. The price bound is his price + 5%. It sells one slot before his usual sell, and the rule's
own buys are off. Built Oct 25 (docs/17 §9); the 5-day backtest made +8.02 SOL at 0.5 SOL a copy (docs/17 §9). Live on
real money from Oct 25 22:08 UTC. From Oct 26 15:00 to Oct 27 11:45 Beirut time he made +8.9099 SOL, while our 162 copies
made -0.0479 SOL ([check.sh paste](../05-live/check-sh-2026-10-27.txt), BY WALLET). The whole bot hit the 1 SOL
daily-loss kill at Oct 27 09:50 Beirut and is stopped.

| | |
|---|---|
| Status | live on real money from Oct 25 22:08 UTC ([fails/README](../analysis/research/2026-10-26/fails/README.md); docs/19 §6). Measured by check.sh from Oct 26 15:00 Beirut (13:00 UTC). Stopped by the daily-loss kill at Oct 27 09:50:35 Beirut (07:50 UTC); still stopped at 11:45 Beirut ([check.sh paste](../05-live/check-sh-2026-10-27.txt)) |
| Built from | his tip as his conviction; his launch buys at create + 0/1; his create-relative sell slot per operator (the table hold); his current operators ([his rules](../02-his-rules/README.md); docs/17 §5, §9) |
| Code | `crates/rugsnipe/src/copybuys.rs` (his buys per signer, saved to `copy_signers.json`); `crates/rugsnipe/tests/replay_days.rs` (the copy replay); `deploy/bin/rugsnipe-vs-him` (`bash ~/check.sh him`); `deploy/bin/rugsnipe-check` (= `~/check.sh`) and `deploy/bin/rugsnipe-trades` (docs/17 §9, docs/19 §12). The keys are defined in `crates/rugsnipe-core/src/config.rs` (checked in this snapshot) |
| Config keys | `[entry] copy = "on"`, `follow_wallet` = his wallet, `copy_min_sol = 0.0`, `copy_min_tip_lamports = 2_000_000` (live: the status line counts "tip under 2M"), `copy_big_sol = 2.0`, `copy_max_premium = 0.05`, `copy_late_slots = 2`, `copy_listed_only = true`, `copy_signer_min_buys = 2` (the live status line reads as 0: see Open questions), `copy_signer_window_h = 24`, `rule_buys = false` (live: "copies of his buys only (entry.rule_buys = false)") (docs/17 §9; docs/19 §10, §13). Bids 3.0M / 8.0M on an A/B (`bid.ab_by_tier` tier 0, docs/17 §9; TIP TEST). Daily stop 1.0 SOL (live: "daily stop 1.0000 SOL") |
| Source docs | [docs/17 §8-§10](../docs/17-newest-bot-vs-him-5-days.md); [docs/19 §9, §10, §12](../docs/19-copy-targets-and-dip-buys.md) |
| Research | [2026-10-25/five/](../analysis/research/2026-10-25/five/README.md), [five/copy/](../analysis/research/2026-10-25/five/copy/README.md), [five/exact/](../analysis/research/2026-10-25/five/exact/README.md), [2026-10-26/fails/](../analysis/research/2026-10-26/fails/README.md), [oprule/](../analysis/research/2026-10-26/oprule/README.md), [speed/](../analysis/research/2026-10-26/speed/README.md) |

Words used here:
- **create**: a coin's launch transaction. "Create + k" is k slots later.
- **slot**: one Solana block, about 0.4 s by the later sources
  ([copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt) header; docs/19 §13). Earlier chain measurements
  disagree: 214-221 ms (docs/01 C6) and 0.21 s (docs/16 §8).
- **curve**: the coin's bonding curve; its reserves set the price.
- **operator / signer**: a launcher who launches many coins. The signer is the wallet that signs its create.
- **bundle**: the operator's own buys right behind the create.
- **tip**: SOL paid to the block leader to order a transaction (1M lamports = 0.001 SOL). His tip is read from his
  own transaction.
- **price bound / premium**: the highest price over his fill that our buy accepts. Above it the buy fails.
- **landed**: included in a block. **refused**: landed but failed on our bound (pump error 6042); only the fee is lost.
- **tape**: every trade on a coin over its first slots.
- **H**: his usual sell slot after the create for that signer, kept in the operator table.
- **out of sample**: scored on data not used to pick the setting.

Times: the docs use UTC. check.sh prints Beirut time, which was UTC+2 on these dates. The paste says "the UTC day (since
02:00 Beirut)", and docs/19 §12 gives "Oct 26 15:00 Beirut time (13:00 UTC)".

## The rule

1. **Trigger.** His landed buy at create + 0 or + 1, seen as an executed trade on the gRPC stream. The feed reads his
   tip from the System transfers in the same transaction (docs/17 §9, "Built").
2. **Key.** Tip >= `copy_min_tip_lamports` (2M), or size >= `copy_big_sol` (2 SOL) whatever the tip (docs/17 §9). The
   live table agrees. Buys of 2.370 and 3.556 SOL at a 1.0M tip are COPIED, and a 1.778 SOL buy at 1.0M is
   "skip: tip/size low" (him table rows FeDpKGFS, CSMc5K1u, 8qQXjmGz).
3. **Operator.** He bought the signer's launches at least `copy_signer_min_buys` times in the last 24 h. The count is
   kept live and survives restarts. With `copy_listed_only`, the signer must also be in the operator table (docs/17 §9).
4. **Bound and window.** His post-trade price + 5%, sent until create + 2 (docs/17 §9; 5% kept in docs/19 §10, §13).
5. **Exit.** Create + H - 1, one slot before his usual sell. check.sh calls this "sold at his sell - 1" (docs/17 §9;
   check.sh him header). Selling behind his own sell lost 23.4 SOL in the backtest, because his sell is the dump
   (docs/17 §9).
6. **Copy only.** `entry.rule_buys = false`: the rule decides nothing, its gates are idle, and the caps serve the copies
   alone (docs/17 §9).
7. **Caps.** Stage B: 2 open positions, 300 attempts a day, a 1 SOL daily stop. In the backtest they never bound: at most
   2 copies open at once, about 60 a day, and the worst running loss in a day was -0.17 SOL (docs/17 §9, "Every rule
   tested"). Live, the daily stop is one ledger for the whole bot, every copied wallet together (copy-bot-history, daily
   risk ledger; check.sh, last section).

## How it was found

- **The rule bot could not land his coins.** In the exact replay (Oct 23 00:00 - Oct 25 17:58 UTC) the newest bot made
  +1.1 SOL, against his +33.5 SOL. On the coins he landed, our landing rate was 0 of 47 (docs/17 §8).
- **We land, but behind him.** On the coins he landed, 80 of our 83 attempts landed right behind him and failed only on
  our own bound (`max_premium = 0`). 618 of our 1,140 buys over Oct 21-25 failed that way (docs/17 §9).
- **A copy is worth less the farther back it lands.** The value falls with the block positions D between his buy and
  ours (table below). Our copy lands about 90 positions behind him: that is our pipeline, not slowness (docs/17 §9, §10).
- **Key on his tip, not his size.** The tip key holds up on his weak days (docs/17 §9, "His weak days"). The floor was
  lowered from 4M to 2M: his landed tips come in steps (1.0, 1.5, 1.8, 2.4, 3.6, 4.8M), and 1.5-2M is his weak bucket
  (docs/17 §9, "Every rule tested").
- **His current operators.** Copy a signer only after 2 of his buys on it in 24 h. One operator, 8ZN71X, made +5.79 of
  the +8.13 SOL (docs/17 §10).
- **Speed: nothing to build on these boxes.** Firing at every create of his hot operators loses to the copy
  (docs/17 §10).
- **Refused copies.** Since the start, 12 of 35 copies of him and 3yrJE1A8 were refused. Each fix tested over 5 days
  lost money (docs/19 §9, §10).

## Backtests

0.5 SOL a copy, our measured landing distances, sold at H - 1, unless stated. The copy sets differ between scripts
(+8.02 on 298 copies in `ablate.py`, +5.51 on 558 in docs/19 §9), so compare rows inside one source only.

| test | period (UTC) | setting | result (SOL) | n | source / script |
|---|---|---|---|---|---|
| landing D positions after him | Oct 21-25 | his 0.7 SOL+ buys, 10% bound, D = 0 / 10 / 90 / 150 | +10.55 / +5.22 / +0.90 / +0.10 | 651 coins | docs/17 §9, `react_pos.py` |
| copy bot from scratch | Oct 21-25 | his 0.7 SOL+ buys, listed / unlisted signers | +6.55 / -2.25 | 338 / 313 | docs/17 §9, `scratch.py` |
| exit behind his sell | Oct 21-25 | all his buys, sell after seeing his sell | -23.4 | all his buys | docs/17 §9 |
| weak-day key | Oct 21-25 | tip >= 4M, 5% bound | +4.71 (4 of 5 days) | 238 | docs/17 §9, `weakdays.py` |
| operator rule | Oct 21-25 | >= 2 of his buys in 24 h | +4.22 (4 of 5 days) | 226 | docs/17 §9, `recent.py` |
| restarts | Oct 21-25 | count from empty at each restart | +2.41 | 99 | docs/17 §9, `restart.py` |
| big low-tip buys | Oct 21-25 | tip >= 4M or size >= 2 SOL | +5.64 | 232 | docs/17 §9, `tipsize.py` |
| **tip floor 2M** | Oct 21-25 | 2M or size >= 2 SOL | **+8.02** (+1.53 +0.98 +5.24 +0.29 -0.02 by day) | 298 | docs/17 §9, `ablate.py` |
| price bound | Oct 21-25 | 3% / 7.5% / 10% / none (4M key) | +3.36 / +6.18 / +5.77 / +5.86 | | docs/17 §9, `ablate.py` |
| exit | Oct 21-25 | H / H - 2 / flat + 5 / + 9 (4M key) | +2.98 / +3.95 / +4.43 / +3.91 (H - 1: +5.64) | | docs/17 §9, `ablate.py` |
| stake | Oct 21-25 | 0.25 / 0.75 / 1.0 SOL | +2.50 / +8.83 / +12.05 | | docs/17 §9, `ablate.py` |
| landing closer | Oct 21-25 | measured / 45 / 20 / 10 / 0 positions | +5.64 / +5.97 / +6.49 / +7.17 / +10.08 | | docs/17 §9, `tipworth.py` |
| **the +8.02 by period** (Oct 28 re-run) | Oct 21-23 / Oct 24-25 | 2M key, as published | **+7.75 / +0.27** (without each period's best 2: +4.82 / −0.52) | 298 | [copy_relook](../analysis/research/2026-10-28/copy_relook/report.md) §B, `recon.py` |
| live rebuilt step by step (Oct 28) | Oct 24-25 | + live costs, landing, late sells, bid mix | net −0.0004 a fill (live: −0.0004) | | copy_relook §B |
| bid at its own landing (Oct 28) | Oct 21-25 | 3.0M / 8.0M / 1.0M assumed / 1.5M assumed | +7.30 / +6.29 / +7.79 / +7.68 | 298 | copy_relook C8, `c8_bid.py` |
| stake ladders by his tip or size (Oct 28) | picked Oct 21-23, scored Oct 24-25 | best ladder 0.5/1.0/1.5 by tip | +17.28 over 5 days, Oct 24-25 +0.73 (−1.69 without the best 2) | | copy_relook C1 |
| exits by tip bucket, breakers, a second copy after a refusal, the low-tip buys, the operator count (Oct 28) | picked Oct 21-23, scored Oct 24-25 | | none beats H − 1 / none / −0.08 (−0.49) / −2.17 / −0.06 | | copy_relook C2-C6 |
| copy replay (real hot loop) | Oct 23 00:00 - Oct 25 17:58 | `copy = "on"`, H - 1 / H | +4.51 / +2.55 | 122 with a tape | docs/17 §9, `replay_days.rs` |
| fire at the create instead | Oct 23 00:00 - Oct 25 18:00 | copy alone / every hot listed create | +5.50 / +2.69 | 176 copies | docs/17 §10, `speed/prefire.py` |
| copy his failed key attempts | not stated (the 5-day data) | his key coins with no landed buy at create + 0/1 | -0.30 | 19 | docs/17 §10, `speed/failcopy.py` |
| operator rule, timed | Oct 21-25 | live rule / no rule / without 8ZN71X | +8.15 / +6.66 / +2.36 | 299 / 575 | docs/17 §10, `oprule/options.py` |
| wider limit for all | Oct 21-25 | 10% / 15% / none, against 5% | -1.05 / -1.79 / -2.07 added | 558 | docs/19 §9, `fails/prem5.py` |
| second buy after a refusal | Oct 21-25 | 1-3 slots later | -0.50 to -3.57 added | 558 | docs/19 §9, `fails/him_second_try.py` |
| right behind him | Oct 21-25 | D = 0 / D = 10 / real | +11.97 / +8.07 / +5.51 | 558 | docs/19 §9, `fails/prem5b.py` |
| wider limit on a condition | picked Oct 21-23, scored Oct 24-25 | vSOL >= 45 at 7.5% / size >= 1.1 at 10% | -0.009 / -0.027 added | | docs/19 §10, `fails/condlimit.py` |

## Live

**Window.** Oct 26 15:00 Beirut (13:00 UTC) to the paste at Oct 27 11:45:34 Beirut. Trading stopped at 09:50:35
Beirut: "daily_loss: daily P&L marked to market -1207492396 lamports <= -1000000000" (check.sh paste).

**BY WALLET, him** (check.sh paste): ITS NET +8.9099, OUR NET -0.0479 SOL; sent 162, filled 125, refused 33, won
44/125; 377 launch buys of his. Where his net came from: the coins we copied +7.7826 (166), the ones we skipped +1.4461
(206), the ones the bot did not see -0.3071 (5), his failed transactions -0.0116 (1,075).

**The him table, summed by what the bot did** (my sums of the 377 rows; there are no "holding" rows). ITS NET is his
own result on the coin, not what a copy makes (check.sh "how to read").

| the bot | rows | his net (ITS NET) | our net (OUR NET) |
|---|---|---|---|
| skip: tip/size low | 206 | +1.4458 | 0 |
| COPIED, filled | 125 | +2.0354 | -0.0475 |
| COPIED, refused | 33 | +4.6317 | -0.0005 (33 fees of 0.000015) |
| COPIED, not landed | 4 | +0.6494 | 0 |
| copied, not sent | 4 | +0.4664 | 0 |
| not seen | 5 | -0.3072 | 0 |
| all rows | 377 | +8.9215 | -0.0480 |

Checks: +8.9215 plus his failed-transaction fees (-0.0116) is +8.9099, the printed ITS NET. Copied (162 sent, plus 4
not sent) comes to +7.7829, against the printed +7.7826. Our -0.0480 against the printed -0.0479 is rounding. By
Beirut day: Oct 26 (221 rows) his +9.6438, ours +1.0521; Oct 27 (156 rows) his -0.7223, ours -1.1001. Three of the 4
"not sent" came after the kill (10:23-10:41 Beirut). Re-run from the repo root with `python3 -`:

```python
import re, collections
lines = open("05-live/check-sh-2026-10-27.txt").read().splitlines()
a = next(i for i, l in enumerate(lines) if l.startswith("== 1 him"))
b = next(i for i, l in enumerate(lines) if i > a and l.startswith("== 2 "))
row = re.compile(r"^\s+(\d\d):(\d\d):\d\d\s+\S+\s+(holding|[+-]\d+\.\d+)\s+(?:([+-]\d+\.\d+)\s+)?"
                 r"(?:[+-]\d+\.\d+%\s+)?(skip: tip/size low|COPIED|copied, not sent|not seen)\s+(.*)$")
by, day, prev = collections.defaultdict(lambda: [0, 0.0, 0.0]), "Oct 27", None
for l in lines[a:b]:
    m = row.match(l)
    if not m:
        continue
    hh, mm, its, ours, bot, rest = m.groups()
    t = int(hh) * 60 + int(mm)
    if prev is not None and t > prev:
        day = "Oct 26"                 # newest first: the clock jumps up at midnight
    prev = t
    if its == "holding":
        continue                       # no net yet (none in this table)
    if bot == "COPIED":
        bot += ", " + next(r for r in ("filled", "refused", "not landed") if r in rest)
    for k in (bot, "day " + day, "all rows"):
        by[k][0] += 1; by[k][1] += float(its); by[k][2] += float(ours or 0)
for k, (n, s_its, s_ours) in sorted(by.items()):
    print(f"{k:22s} {n:4d}  ITS NET {s_its:+.4f}  OUR NET {s_ours:+.4f}")
```

**What the table shows.** We filled his weaker coins and were refused on his better ones. On the 33 refused coins he made
+4.6317; 24 of them were positive for him, the biggest FeDpKGFS at +1.5656. On the 125 we filled he made +2.0354 and we
made -0.0475. The largest losses were Oct 27 fills between 01:24 and 03:53 Beirut: CSMc5K1u -0.3047, HvjYQ3VW -0.2978,
DR8or4ud -0.2835, 3Ye1Wgff -0.2780, 7QsUeqFq -0.2698. The best fill was HQT8xbhA at +0.7061 (him table).

**The bigger-tip test** (TIP TEST since Oct 26 18:20 Beirut; its rule: "keep the higher bid only if it lands closer
(d_avg) AND nets more per copy"):

| our bid | copies | filled | failed | not landed | in his slot | d_avg | net | per copy |
|---|---|---|---|---|---|---|---|---|
| 3.0M | 56 | 41 | 14 | 1 | 36 | 156 | -0.0169 | -0.0003 |
| 8.0M | 79 | 59 | 20 | 0 | 52 | 149 | -0.4863 | -0.0062 |

8M landed 7 positions closer on average and netted less per copy, so it fails the test's own rule. Before 18:20 every
copy of him used 3.0M: 27 copies, +0.4558 (my sum of the him table rows before 18:20). The TIP TEST's filled / failed
split differs a little from the table rows. For 8M from 18:20 the rows give 61 filled, 16 refused and 2 not landed.

**The first live day** (Oct 25 22:08 - Oct 26 16:00 UTC; it overlaps the check.sh window from 13:00 UTC): 12 of 35
copies of him and 3yrJE1A8 were refused. Filled, they would have made +1.15 SOL, +0.65 of it on him, and two coins
carry most of it (docs/19 §9).

**The whole bot** (all copied wallets; [copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt)): since the
start (Oct 26 15:00), 417 trades, 150 won, NET -0.7628 SOL. By day: Mon Oct 26 +1.0728, Tue Oct 27 -1.8458. The risk
ledger for 2026-10-27 (UTC) shows realized -0.7085, 140 buys, killed: DailyLoss. The wallet went from 1.7192 to 0.3081
SOL (check.sh paste). The four copies of him among the last 10 trades staked 0.225-0.443 SOL (28kvwz6r, 3ndMDGDD,
F4sw1HnJ, FMo3m6Ce; history file), not the backtests' 0.5.

**What stopped it: the stuck coin 2RR6sfbi.** The copy of him was stopped by a coin that wasn't his. 2RR6sfbi was a
wallet 4 copy (0.51 SOL, Oct 27 06:55 Beirut). It graduated to its PumpSwap pool as we bought, and the bot only knew how
to sell on the curve. 405 sells failed over about five hours while the coin fell about 95%. Counted at its falling price
in the shared wallet, it pushed the day past the 1 SOL daily stop at 09:50:35 Beirut, and every copy stopped, his
included. It cost about 0.57 SOL (0.48 of the stake plus 0.09 of failed-sell fees). check.sh's "since the start" line
(−0.76) leaves it out because the position never closed. The fix (`af681ad`: sell a graduated coin on its pool) is in
this repo's code but was never deployed. Any coin he buys can graduate in the seconds we hold it, so the same thing
could have happened on his copies. Full account: [`../05-live/stuck-coin-2RR6sfbi.md`](../05-live/stuck-coin-2RR6sfbi.md).

## Verdict

The mechanism works: we land behind him, mostly in his slot (TIP TEST "in its slot": 36 of 56 at 3M, 52 of 79 at
8M). The money does not follow. In this window the copy broke even (-0.0479 SOL on 162 sent), while he made +8.91
SOL. The copies we filled were his weaker coins, and the refused copies held over half of what he made (+4.63 of
+8.92 in the table rows). That is the auction effect of docs/17 §3, now at a 5% bound: a coin that moves more than 5%
before we land is refused. Over 5 days every fix for refusals lost (docs/19 §9, §10). Landing right behind him would
roughly double the backtest (+11.97 against +5.51, docs/19 §9). But those positions belong to transactions already
in flight, so a tip does not buy them (docs/17 §9, docs/19 §9). The live 8M tip did not land meaningfully closer
either. The daily stop, which never bound in the backtest, bound live. It counts
every copied wallet: S6 itself lost only -0.0479. The copy of him is not a loss maker on this sample. It is also far
from the backtest's +8.02 SOL over 5 days, most of which came on one day (Oct 23: +5.24, docs/17 §9).

## Open questions (as of Oct 28; the review is [07-restart](../07-restart/README.md))

- **Operator rule live?** Settled by the code review: the box ran `copy_signer_min_buys = 0` (check.sh reads the config
  file the service loads, and a missing key would print 2). With `copy_listed_only` on, the count is worth −0.06 over
  the 5 days (copy_relook C6). The owner's paste of the backup's config confirms it (07-restart §6.0). The window was
  also about 13 h, not 24 (a 400 ms slot constant; fixed).
- **Unkill or not.** The review's answer: a restart as a measured small test, him alone in his own wallet, 0.5 SOL,
  bid 3.0M with a 1.5M A/B (07-restart §6). Expected at the backtest's last two days: about zero.
- **Data mismatch.** docs/19 §9 lists 9387oQyF as landed at create + 3 and refused. check.sh lists it as "not landed".
  Still open.
- **Landing closer.** Nothing on these boxes; Cherry FRA is 1-2 positions behind the old building (box study). The one
  untested feed is Triton Preconfs (box study §5).
- **Bid.** 8.0M fails its own rule: +6.29 over 5 days at its landing against +7.30 for 3.0M, about 0.1 of curve for
  1.16 of cost (copy_relook C8). The restart runs 3.0M against 1.5M.
- **The bucket that lost live.** His 4.8-7.2M tips: −1.44 on 41 fills (5 won) in two bursts, where the 5 days give about
  zero (copy_relook C7). The next window's split answers whether it was noise.

## Sources

- [docs/17-newest-bot-vs-him-5-days.md](../docs/17-newest-bot-vs-him-5-days.md) §3, §5, §8, §9 (all subsections), §10
- [docs/19-copy-targets-and-dip-buys.md](../docs/19-copy-targets-and-dip-buys.md) §6, §9, §10, §12, §13
- [05-live/check-sh-2026-10-27.txt](../05-live/check-sh-2026-10-27.txt): status lines, TIP TEST, LAST 10 TRADES, BY
  WALLET, "== 1 him" table, daily stop
- [05-live/copy-bot-history-2026-10-28.txt](../05-live/copy-bot-history-2026-10-28.txt): the whole bot by day, risk
  ledger, last 10 trades
- Research: [five/README.md](../analysis/research/2026-10-25/five/README.md),
  [five/copy/README.md](../analysis/research/2026-10-25/five/copy/README.md),
  [five/exact/README.md](../analysis/research/2026-10-25/five/exact/README.md),
  [2026-10-26/fails/README.md](../analysis/research/2026-10-26/fails/README.md),
  [oprule/README.md](../analysis/research/2026-10-26/oprule/README.md),
  [speed/README.md](../analysis/research/2026-10-26/speed/README.md)
