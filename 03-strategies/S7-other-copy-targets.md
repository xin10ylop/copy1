# S7. Copy other wallets beside him (`entry.copy_more`)

In short: this is the S6 copy pointed at other wallets. Each listed wallet's launch buys (create + 0/1) of at least
`min_sol` are bought behind it, with the same bound and window but none of his filters. Each copy is sold at a fixed
create + hold. Two wallet searches on Oct 26 found that most profitable wallets cannot be copied (docs/19 §1, §2, §11).
6anjqMe was rejected (docs/18). Live from Oct 26 (docs/19 §6). By Oct 27 11:45 Beirut, wallet 2 (3yrJE1A8) stood at
-0.0135 SOL on 61 copies sent and wallet 6 (D5BDDkBt) at +0.0857 on 8
([check.sh paste](../05-live/check-sh-2026-10-27.txt)). Wallets 3 (JBokzLFR) and 5 (CxyKYmQo) lost about -0.39 and
-0.54 SOL and were removed on Oct 27 (session notes, Oct 27). The bot is stopped by the daily-loss kill.

| | |
|---|---|
| Status | built; live on real money from Oct 26: 3yrJE1A8 from about 13:00 UTC, with `min_sol = 1.5` from 13:26 UTC (docs/19 §6). Stopped with the whole bot by the daily-loss kill at Oct 27 09:50:35 Beirut (07:50 UTC). Wallets 3 and 5 were taken out of the config on Oct 27 (the sed commands at the top of the check.sh paste). Wallets 2 and 6 stay in the config. Wallet 4 (H9kuqGKN) and its copies belong to a different repo (copy2), and its pages live in the copy2 repo |
| Built from | not his rules: the S6 copy machinery ([his rules](../02-his-rules/README.md) for what S6 copies) with each wallet's own exit, e.g. 3yrJE1A8's 20- or 30-slot sell timer (docs/19 §5, §8) |
| Code | `deploy/bin/rugsnipe-check` (= `~/check.sh`) and `deploy/bin/rugsnipe-trades` (the per-wallet tables, cache in `/var/cache/rugsnipe-trades/<wallet>.json`) (docs/19 §12). `CopyMore` and its checks (at most 8 wallets, hold 1-300, `max_premium` in [0, 0.5)) are in `crates/rugsnipe-core/src/config.rs`, and the hot loop in `crates/rugsnipe/src/hot.rs` (checked in this snapshot; the docs do not name them) |
| Config keys | `[entry] copy_more = [{ wallet, mode = off/log/on, min_sol, hold_to_create_slots, max_premium }]`, up to 8 wallets; a buy also needs `entry.copy` on (docs/19 §5, §13). Live line in the paste after wallet 5's removal and before wallet 3's: `{ wallet = "3yrJE1A8...", min_sol = 1.5, hold_to_create_slots = 29 }`, `{ wallet = "JBokzLFR...", mode = "log", hold_to_create_slots = 5 }`, `{ wallet = "D5BDDkBt...", hold_to_create_slots = 9 }`, plus wallet 4's entry. The paste does not show the global `copy_max_premium`; docs/19 §13 says 3yrJE1A8 keeps 5% |
| Source docs | [docs/18](../docs/18-copy-6anjqMe.md) (all); [docs/19 §1-§13](../docs/19-copy-targets-and-dip-buys.md) |
| Research | [2026-10-26/wallets/](../analysis/research/2026-10-26/wallets/README.md) (with `specs.txt`), [wallets2/](../analysis/research/2026-10-26/wallets2/README.md), [holders/](../analysis/research/2026-10-26/holders/README.md), [flush/](../analysis/research/2026-10-26/flush/README.md), [w3/](../analysis/research/2026-10-26/w3/README.md), [six/](../analysis/research/2026-10-26/six/README.md) |

Words used here:
- **create**: a coin's launch transaction. "Create + k" is k slots later.
- **slot**: one Solana block, about 0.4 s by the later sources
  ([copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt) header). Earlier chain measurements say 214-221 ms
  (docs/01 C6).
- **curve**: the coin's bonding curve; its reserves set the price. **operator**: a launcher of many coins.
- **bundle**: the operator's own buys right behind the create. **launch buy**: a wallet's buy at create + 0 or + 1,
  outside the dev's bundle (docs/19 §1).
- **tip**: SOL paid to the block leader to order a transaction (1M lamports = 0.001 SOL).
- **price bound / premium**: the highest price over the copied wallet's fill that our buy accepts.
- **landed**: included in a block. **refused**: landed but failed on our bound (pump error 6042), fee only.
- **tape**: every landed trade on a coin over its first slots (13 here).
- **out of sample**: scored on data not used to pick the wallet or the exit.
- **chain-true**: the wallet's SOL balance change on its own transactions, fees and tips included (docs/19 intro).

Times: the docs use UTC. check.sh prints Beirut time, UTC+2 on these dates ("the UTC day (since 02:00 Beirut)" in the
paste; docs/19 §12).

## The rule

1. For each wallet in `copy_more`: its launch buy of at least `min_sol` is bought behind it, as his are in S6. Same
   +5% bound (or the wallet's own `max_premium`), same window and risk caps, none of his filters (docs/19 §5, §13).
2. Sold at create + `hold_to_create_slots`, whatever the wallet does. Its own sell does not trigger ours (docs/19 §5).
3. `mode` off / log / on per wallet. Journal line `copyw <mint> by <wallet> ... -> buy|log|skip_small` (docs/19 §5).
4. Bids and the daily stop are shared with S6. The TIP TEST A/B ran 3.0M and 8.0M bids on every wallet (check.sh).

## How it was found

- **First search** (Oct 23 00:00 - Oct 25 18:00 UTC). 251 wallets made 30+ launch buys. The selection decays: pick on
  two days, score the third, and the top 5 make +1.57 SOL but the top 20 make -0.68 (docs/19 §1). Out of sample (Oct 25
  18:00 - Oct 26 11:00) the 13 finalists, one copy per coin, made -4.86 SOL on 1,052 copies. JBokzLFR (+1.52 on 90) and
  3yrJE1A8 (+0.53) held up (docs/19 §1).
- **Why the profitable ones cannot be copied** (docs/19 §2). A copy keeps only the market's move between their buy and
  their first sell, less about 5% in costs:

  | wallet | the move between its buy and its first sell |
  |---|---|
  | him, key buys on hot operators | mean +13.0%, median +5.4% |
  | him, other launch buys | mean +5.0% |
  | 3yrJE1A8 | mean +11.0%, median +7.0% |
  | 9apNtyQc (+41.8 SOL itself) | mean +5.8%; a copy loses (-6.12 following its sells) |

  The 88 launch holders with 15+ closed coins lost -757 SOL together (Oct 24-26). The rival CWiNFA broke even at
  -0.47 SOL on 979 launch buys. The biggest winners are insider clusters inside the dev's bundle, and a copy lands 11-28%
  above their price (docs/19 §2).
- **Dump-and-bounce** (buy after a big sell, sell the bounce). Buying right after the early dumps lost -26 to -66 SOL on
  1,305 trades. 1 of 912 variants was positive in total, and 0 of 144 on later dumps. Not built (docs/19 §3).
- **6anjqMe rejected** (docs/18). He buys into a curve that is already moving and leaves within a few slots. His best
  slice on Oct 21-25 (size 1-2 SOL, +2.26) lost at every exit on Oct 1-20. The tip slice did not hold on Oct 1-20
  either.
- **3yrJE1A8.** A copy lands at its price (median +0.2%), and it sells 4-6 s after buying (docs/19 §2). It sells on two
  timers, 20 or 30 slots after its buy, chosen at random as far as the chain shows. So the copy holds to create + 29
  (docs/19 §5, §8). Its own trades from Oct 25 22:08 to Oct 26 13:22 UTC split by size. Its 2 SOL buys: 43 coins, 25
  wins, its mean +7.5%, a 0.5 SOL copy at its prices +1.60 SOL. Its 0.5 SOL buys: 22 coins, -1.4%, copy -0.15. So from
  13:26 UTC only the 2 SOL buys are copied (`min_sol = 1.5`, docs/19 §6).
- **JBokzLFR** went in at create + 5, every size (docs/19 §7). Later it was set to `mode = "log"` (the copy_more line in
  the paste) and then removed (Oct 27).
- **A data fix.** 1,101 of 4,808 tapes were coins priced in another token. Without them 3yrJE1A8's copy is +6.32 SOL,
  not +8.25 (docs/19 §11).
- **Second search** (Oct 26 evening). Exits were picked on Oct 25 18:00 - Oct 26 06:00 and scored on 06:00 - 17:15.
  Of 8 candidates one passed (wallet 4). Of the next five, CxyKYmQo and D5BDDkBt passed (docs/19 §11).
- **What wallets make against what a copy makes.** The 30 wallets that made the most made +320.7 SOL themselves.
  Copying them makes +7.2, and 13 of the 30 lose as a copy (docs/19 §11, `ownvscopy.py`).
- **One view** (docs/19 §12). `bash ~/check.sh` numbers the wallets: 1 him, 2 3yrJE1A8, 3 JBokzLFR, then the other
  copy_more wallets in config order (4 H9kuqGKN, 5 CxyKYmQo, 6 D5BDDkBt). It shows the last 10 trades, BY WALLET, and
  one table per wallet. Wallets 3 and 5 were erased from it on Oct 27.

## Backtests

0.5 SOL copies, our measured landing distances, +5% bound, unless stated.

| test | period (UTC) | setting | result (SOL) | n | source / script |
|---|---|---|---|---|---|
| selection on an unseen day | Oct 23-25 | top 5 / 10 / 20; backwards | +1.57 / +0.26 / -0.68; -0.59 / -0.03 / -2.70 | | docs/19 §1, `wallets/split.py` |
| 13 finalists out of sample | Oct 25 18:00 - Oct 26 11:00 | one copy per coin | -4.86 (JBokzLFR +1.52 on 90, 3yrJE1A8 +0.53) | 1,052 | docs/19 §1, `wallets/oos_screen.py` |
| finalists out of sample, longer | Oct 25 18:00 - Oct 26 14:50 | one copy per coin | -4.84 (JBokzLFR +1.84 on 116, 3yrJE1A8 +1.70 on 130) | 1,608 | docs/19 §7, `oos_screen.py` |
| JBokzLFR, sold at a fixed slot | in sample Oct 23-25 / out of sample 4 blocks | create + 5 / + 9 | +1.10 / +0.97; out of sample +1.93 / +1.40 | | docs/19 §7, `oos_screen_nosell.py` |
| dump-and-bounce, early dumps | not stated (the complete 13-slot tapes, by day) | buy right after, any exit | -26 to -66; 1 of 912 variants positive | 1,305 | docs/19 §3, `flush/bounce.py` |
| dump-and-bounce, later dumps | same | +50% / +100% run then a 30-40% flush | 0 of 144 variants positive | 271 / 59 events | docs/19 §3, `flush/later.py` |
| 3yrJE1A8 exit grid | Oct 24 - Oct 26 12:00 | sold at its buy + 5 / 14 / 24 / **29** | +3.42 / +5.22 / +7.39 / **+8.28** | 256 / 247 / 249 / 252 | docs/19 §5, `w3/grid.py`, `w3/eval.py` |
| 3yrJE1A8 after its first sell | same | its first sell, else + 29 | +3.35 | 280 | docs/19 §5, `w3/eval.py` |
| 3yrJE1A8 early sells / own take-profit | same | follow early sells / +30% TP | +7.07 / +8.91 (against +8.25) | | docs/19 §8, `w3/early.py`, `w3/tp.py` |
| 3yrJE1A8 limit / second try | same | no limit / a second buy at +1..+3 | +8.01 (against +8.25) / -0.13 to +0.29 added | 252 | docs/19 §9, `w3/prem.py`, `w3/second_try.py` |
| 3yrJE1A8 2 SOL buys, wider limit | same | 7.5% / 10% | +0.28 / -0.17 added | | docs/19 §10, `w3/condlimit.py` |
| 3yrJE1A8, SOL coins only | Oct 24-26 | create + 29; 0.5 SOL buys / 2 SOL buys | +6.32 total; +3.33 / +2.99 | 166 | docs/19 §11, `w3/solonly.py` |
| second search (7 shown) | exit picked Oct 25 18:00 - Oct 26 06:00, scored 06:00 - 17:15 | 6anjqMeW / dKMjeGJ4 / 8ksFdx6i / CWUqhP2g / 9qz7cWBq / 9pdYXJGy / AEgTuy8L, 2nd half | +0.30 / +0.14 / -0.27 / -0.62 / -1.66 / -0.71 / +0.26 (thin or fails) | 152-410 buys each | docs/19 §11, `wallets2/process2.py` |
| next five | first half / second half | CxyKYmQo at + 12 / D5BDDkBt at + 9, 1st / 2nd half | +1.44 / +0.71; +0.72 / +0.72 (both pass) | 131 / 40 | docs/19 §11, `wallets2/process3.py` |
| next five, failures | first half / second half | AMDEmVoc / JBbbosQC / M8CcrseQ, 2nd half | -1.27 / -1.31 / -0.64 | 392 / 132 / 79 | docs/19 §11, `process3.py` |
| own result vs a copy | Oct 25 18:00 - Oct 26 17:40 | top 30 earners | +320.7 themselves, +7.2 as copies | 30 wallets | docs/19 §11, `wallets2/ownvscopy.py` |
| D5BDDkBt before it was watched | its 44 coins before the bot watched it (dates not stated) | create + 9 at 5% / 15% | +2.15 (before the 0.0155 a fill correction); 15% about +0.24 better after it | 44 | docs/19 §13 |
| 6anjqMe, all | Oct 21-25 | best exit (12 slots after his buy) / one slot before his sell | +0.25 / -4.49 | 546 | docs/18, `six/copy.py` |
| 6anjqMe, size 1-2 SOL | Oct 21-25 / Oct 1-20 | 12 slots / best exit | +2.26 / -0.48 (every exit loses) | 143 / 254 | docs/18, `six/copy2.py` |

Two notes. docs/19 §5 gives +8.28 SOL for 3yrJE1A8 at create + 29, while §8-§9 compare against +8.25. After the
other-quote coins are removed it is +6.32 (docs/19 §11, the later figure). The D5BDDkBt row is before the per-fill
correction of docs/19 §13 except where stated.

## Live

Window: Oct 26 15:00 Beirut (13:00 UTC) to the paste at Oct 27 11:45:34 Beirut. Trading stopped at 09:50:35 Beirut
(daily-loss kill, check.sh paste).

**BY WALLET** (check.sh paste; ITS NET is the wallet's own result, OUR NET our copies):

| who | ITS NET | OUR NET | sent | filled | refused | won | its coins | its net: copied / skipped / not seen / before watched | its failed tx |
|---|---|---|---|---|---|---|---|---|---|
| 2 3yrJE1A8 | +2.2099 | -0.0135 | 61 | 51 | 10 | 22/51 | 113 | +5.5703 (68) / -2.5037 (42) / -0.3904 (3) / - | -0.4662 (1,665) |
| 6 D5BDDkBt | +2.0455 | +0.0857 | 8 | 6 | 2 | 4/6 | 31 | +0.6788 (8) / +0.2176 (1) / -0.0524 (1) / +1.2518 (21) | -0.0502 (4) |

**The two tables, summed by what the bot did** (my sums of the rows; no "holding" rows in either). Wallet 2: filled
51, its net +4.6367, ours -0.0133; refused 9, its +0.4493; failed (instruction_error) 1, its -0.0190; copied but not
sent 7, its +0.5032; skipped under `min_sol` 40, its -0.8651; skipped because the coin was already ours 2, its
-1.6385; not seen 3, its -0.3903. Wallet 6: filled 6, its +0.6085, ours +0.0858; refused 2, its +0.0701; before it was
watched 21, its +1.2515; coin ours 1, its +0.2176; not seen 1, its -0.0524. The totals plus the failed-transaction
fees match ITS NET (wallet 2: +2.6763 - 0.4662; wallet 6: +2.0953 - 0.0502). Re-run from the repo root with
`python3 -`:

```python
import re, collections
lines = open("05-live/check-sh-2026-10-27.txt").read().splitlines()
status = r"(skip: < min_sol|skip: coin ours|COPIED|copied, not sent|not seen|not watched yet)"
row = re.compile(r"^\s+\d\d:\d\d:\d\d\s+\S+\s+(holding|[+-]\d+\.\d+)\s+(?:([+-]\d+\.\d+)\s+)?"
                 r"(?:[+-]\d+\.\d+%\s+)?" + status + r"\s+(.*)$")
for head in ("== 2 3yrJE1A8", "== 6 D5BDDkBt"):
    a = next(i for i, l in enumerate(lines) if l.startswith(head))
    b = next(i for i, l in enumerate(lines) if i > a and (l.startswith("== ") or "how to read" in l))
    by = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for l in lines[a:b]:
        m = row.match(l)
        if not m or m.group(1) == "holding":
            continue
        its, ours, bot, rest = m.groups()
        if bot == "COPIED":
            bot += ", " + next(r for r in ("filled", "refused", "not landed", "failed") if r in rest)
        for k in (bot, "all rows"):
            by[k][0] += 1; by[k][1] += float(its); by[k][2] += float(ours or 0)
    print(head)
    for k, (n, s_its, s_ours) in sorted(by.items()):
        print(f"  {k:20s} {n:4d}  ITS NET {s_its:+.4f}  OUR NET {s_ours:+.4f}")
```

**TIP TEST** (since Oct 26 18:20 Beirut; keep the higher bid only if it lands closer and nets more per copy):

| wallet | bid | copies | filled | failed | in its slot | d_avg | net | per copy |
|---|---|---|---|---|---|---|---|---|
| 3yrJE1A8 | 3.0M | 30 | 25 | 5 | 19 | 125 | -0.4964 | -0.0165 |
| 3yrJE1A8 | 8.0M | 15 | 14 | 1 | 12 | 142 | +0.4021 | +0.0268 |
| D5BDDkBt | 3.0M | 3 | 2 | 1 | 1 | 35 | +0.1465 | +0.0488 |
| D5BDDkBt | 8.0M | 5 | 3 | 2 | 4 | 339 | -0.0607 | -0.0121 |

For 3yrJE1A8 the 8M copies netted more but landed farther back, so the test's rule does not pass. The samples are
small.

- **3yrJE1A8's first live copy** (3c3WaGz7, a 0.5 SOL buy, before `min_sol = 1.5`) lost -44.5% (docs/19 §6; the
  paste shows it at 15:22 Beirut, -0.2224 SOL).
- **3yrJE1A8's copies** held 27-31 slots, consistent with the create + 29 exit (wallet 2 table, "held").
- **D5BDDkBt** was at +2.03 itself and -0.04 for us at 00:45 Beirut on Oct 27, "too few to judge" (docs/19 §13). Its
  table marks buys up to 19:36 Beirut on Oct 26 as "not watched yet". The first copy is at 19:47.
- **Wallets 3 and 5.** JBokzLFR lost about -0.39 SOL and CxyKYmQo about -0.54 SOL live. Both were removed from the
  config and erased from check.sh on Oct 27 (session notes, Oct 27). The paste begins with the `sed` commands that
  removed them, then `grep -cE 'CxyKYmQo|JBokzLFR'` prints 0 and "config ok". The running process still counted "5 other
  wallet(s)" at 11:45 Beirut; the paste shows no restart after the edit.
- **Whole bot.** -0.7628 SOL since the start (Oct 26 15:00) on 417 trades
  ([copy-bot-history](../05-live/copy-bot-history-2026-10-28.txt)). The wallets still listed in BY WALLET total
  +0.1699. The difference, -0.7628 - 0.1699 = -0.9327 SOL, is consistent with the session's -0.39 and -0.54 for
  wallets 3 and 5.

## Verdict

Copying other wallets has not paid. The searches show why: a copy keeps only the move after the copied buy, and the
biggest earners make theirs by being first or inside the bundle (docs/19 §2, §11). Of the wallets that went live,
3yrJE1A8 is flat (-0.0135 on 61 sent) while it made +2.21 itself. On the 51 coins we filled it made +4.64, and our
copies made -0.013. D5BDDkBt is slightly positive on 6 fills, too few to judge. JBokzLFR and CxyKYmQo lost about
-0.93 SOL together, more than the whole bot's net since the start (-0.7628). The config still holds 3yrJE1A8 and
D5BDDkBt, but neither has shown a copy profit beyond noise. Do not add wallets on a 1-2 day screen: the selection
decays out of sample (docs/19 §1).

## Open questions

- **3yrJE1A8's gap.** It made +4.6367 on the 51 coins we filled, while our copies made -0.0133. Is it the timer we
  cannot see (docs/19 §8) or our landing?
- **Bid for 3yrJE1A8.** 8M netted +0.0268 a copy against -0.0165 at 3M, on 15 and 30 copies, but landed farther back.
  The test's rule rejects it; a longer sample would settle it.
- **Restart config.** After the Oct 27 edit the config holds 3yrJE1A8, D5BDDkBt and wallet 4. Whether to unkill with
  them, or with him only (S6), is not decided in the sources.
- **The live losses of wallets 3 and 5** are known only from session notes. Their tables were erased from check.sh, so
  this repo cannot re-check them.

## Sources

- [docs/18-copy-6anjqMe.md](../docs/18-copy-6anjqMe.md)
- [docs/19-copy-targets-and-dip-buys.md](../docs/19-copy-targets-and-dip-buys.md) §1-§13
- [05-live/check-sh-2026-10-27.txt](../05-live/check-sh-2026-10-27.txt): the `sed` / `grep` commands and the copy_more
  line (top), TIP TEST, BY WALLET, the "== 2 3yrJE1A8" and "== 6 D5BDDkBt" tables
- [05-live/copy-bot-history-2026-10-28.txt](../05-live/copy-bot-history-2026-10-28.txt): the whole bot since the start
- Session notes, Oct 27: the live losses of wallets 3 and 5
- Research: [wallets/](../analysis/research/2026-10-26/wallets/README.md),
  [wallets2/](../analysis/research/2026-10-26/wallets2/README.md),
  [holders/](../analysis/research/2026-10-26/holders/README.md),
  [flush/](../analysis/research/2026-10-26/flush/README.md), [w3/](../analysis/research/2026-10-26/w3/README.md),
  [six/](../analysis/research/2026-10-26/six/README.md)
