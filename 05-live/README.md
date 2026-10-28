# 05. Live: what the copy bot did with real money, and the raw outputs

In short: the hot copy bot (rugsnipe-hot, on fra1) traded real money with rule strategies from Oct 21 (S0 probe, then
S1/S3), then as a **copy of him** from Oct 25 22:08 UTC (S6), with more wallets from Oct 26 (S7). In check.sh's window
(Oct 26 15:00 → Oct 27 11:45 Beirut) he made **+8.9099 SOL** and our 162 copies of him **−0.0479**. The whole bot was
**−0.7628** on closed trades in that window, and its wallet −1.41. All time (Oct 22-27) it was **−5.1292 SOL**. It
stopped on the daily-loss kill at Oct 27 07:50 UTC. The stuck coin 2RR6sfbi (a wallet 4 copy that couldn't be sold) set
the kill off. The bot is off, fra1 is terminated, and the SOL is back in the owner's Phantom.

## Files here

| File | What it is |
|---|---|
| [`check-sh-2026-10-27.txt`](check-sh-2026-10-27.txt) | `bash ~/check.sh` on fra1, Oct 27 11:45 Beirut, **exactly as pasted** (with the config edits run just before it, which removed wallets 5 and 3). Status, kill, totals, tip test, last 10 trades, by wallet, **every launch buy of him (`== 1 him`)** and of wallets 2, 4, 6, open positions, the daily stop |
| [`copy-bot-history-2026-10-28.txt`](copy-bot-history-2026-10-28.txt) | `history.py --root /root/fra1` on Ohio, Oct 28: the copy bot from fra1's backup, all time and since the start, by day, refused buys, the risk ledger (and the long copy's paper book at shutdown) |
| [`stuck-coin-2RR6sfbi.md`](stuck-coin-2RR6sfbi.md) | **the stuck coin**: graduated at our buy, 405 failed sells, −0.57 SOL, the daily-loss kill, the fix |

## The live phases

| When (UTC) | What traded | Result | Page |
|---|---|---|---|
| Oct 21-23 | S0 LEAD probe (first behind the dev's bundle) | −4.856 SOL on 469 attempts (docs/10 §1) | [S0](../03-strategies/S0-lead-policy-dev-sniping.md) |
| Oct 23 19:18 → about Oct 25-26 | S1 operator wave, with S3's tweet rule (from Oct 24 ~17:29) and S4's rapidlaunch skip; S5 follow on Oct 25 | Oct 24 00:00-12:29: −0.253 on 75 trades, him +1.336 on 126 (docs/11) | [S1](../03-strategies/S1-operator-wave.md), [S3](../03-strategies/S3-tweet-rule.md) |
| Oct 25 22:08 → Oct 27 07:50 | **S6 copy of him**; rule buys switched off (`entry.rule_buys = false`) | check.sh window: him +8.9099, ours −0.0479 on 162 sent | [S6](../03-strategies/S6-copy-him.md) |
| Oct 26 → Oct 27 07:50 | **S7** `copy_more`: 3yrJE1A8 (from ~13:00), JBokzLFR, CxyKYmQo, D5BDDkBt, H9kuqGKN (wallet 4, copy2) | wallet 2 −0.0135, 6 +0.0857, 4 +0.1456; 3 and 5 about −0.39 and −0.54 | [S7](../03-strategies/S7-other-copy-targets.md) |

**By day** (the bot's own database, all trades, after tips and fees, `copy-bot-history-2026-10-28.txt`):

| day | trades | won | net SOL | running |
|---|---|---|---|---|
| Thu Oct 22 | 167 | 29 | −0.4618 | −0.4618 |
| Fri Oct 23 | 156 | 23 | −1.8794 | −2.3413 |
| Sat Oct 24 | 154 | 52 | −1.4777 | −3.8189 |
| Sun Oct 25 | 92 | 26 | −0.5373 | −4.3562 |
| Mon Oct 26 | 234 | 84 | +1.0728 | −3.2835 |
| Tue Oct 27 | 186 | 67 | −1.8458 | −5.1292 |

All time: 989 trades, 988 closed, 281 won; on the curve +2.4081, tips and fees −6.5287, 757 refused buys −1.00866:
**NET −5.1292 SOL**. The race for the first spot cost more in tips and fees than the trades made on the price moves.
(The database starts Oct 22 00:21 UTC. Earlier probe trading is in docs/08 and docs/10.)

## The check.sh window by copied wallet (`BY WALLET`)

| who | its own net | our net | sent | filled | refused | won |
|---|---|---|---|---|---|---|
| **1 him** (AHwJSnFN) | **+8.9099** | **−0.0479** | 162 | 125 | 33 | 44/125 |
| 2 3yrJE1A8 | +2.2099 | −0.0135 | 61 | 51 | 10 | 22/51 |
| 4 H9kuqGKN (copy2) | +36.9199 | +0.1456 | 93 | 77 | 14 | 32/76 |
| 6 D5BDDkBt | +2.0455 | +0.0857 | 8 | 6 | 2 | 4/6 |
| total (shown wallets) | | +0.1699 | 324 | 259 | 59 | 102/258 |

The whole bot since the start was −0.7628, so the removed wallets 3 (JBokzLFR) and 5 (CxyKYmQo) account for about −0.93
(−0.7628 − 0.1699). check.sh hides them, but its totals line still counts their trades. Him, summed row by row (S6
page): +4.63 of his +8.92 was on the 33 copies the 5% bound refused, and we filled his weaker coins (+2.04 for him, −0.05
for us).

## The end (Oct 27, UTC; Beirut = UTC+2)

| When | What |
|---|---|
| 04:55 | 2RR6sfbi (wallet 4 copy, 0.51 SOL) bought; its curve completes; curve sells start failing (405 in all) |
| 07:50:35 | **daily-loss kill**: the day's marked-to-market loss −1.207 SOL ≤ −1 SOL |
| ~09:40 | wallets 5 and 3 removed from `copy_more` and erased from check.sh (`6c7a9a4`) |
| 09:45 | the check.sh paste (11:45 Beirut) |
| ~10:45 | the `[risk]` stop raised to 2 SOL and unkilled (the probe stage's own 1 SOL stop still applied); then `rugsnipe-hot` and `rugsnipe-guard` stopped for good; 2RR6sfbi sold by hand for 0.029 SOL |
| ~12:45 | every rugsnipe unit on fra1 stopped; nonce accounts closed; SOL withdrawn; backup to Ohio |
| Oct 28 | fra1 terminated |

## Money

- The bot wallet `4g49xGbg...` went from 1.7192 to 0.3081 SOL over check.sh's window: −1.4115 = closed trades −0.809,
  2RR6sfbi −0.510, its 405 failed sells −0.092, failed buys −0.001 (every lamport, `stuck-coin-2RR6sfbi.md`).
- Withdrawn Oct 27 to the owner's Phantom `4ZLrCvjc...`: 0.335094 SOL from the bot wallet and 0.0423 from 40 nonce
  accounts. Phantom then held **3.8498 SOL**. The bot wallets are at 0.

## Reading check.sh

- **TRADING:** buying or not, and why (here, the kill and the exact unkill command).
- **results since the start:** closed trades only. Open positions and failed-sell fees are left out (−0.76 here, while
  the wallet lost 1.41).
- **copy on (this process):** his launch buys seen, why some weren't copied (tip under 2M, operator not listed, operator
  bought too few times in 24 h), how many were copied. It prints "operator he bought < 0 times", which suggests the
  operator-count rule was effectively off (S6 open question).
- **TIP TEST:** our 3.0M and 8.0M bids by wallet. **LAST 10 TRADES**, then **BY WALLET**, then one table per wallet.
  *the bot*: COPIED / skip: why / copied, not sent / not seen / not watched yet. *result*: filled / refused (the price
  bound, fee only) / not landed. *landed*: its slot or +N. *behind*: block positions after its buy. *held*: slots.
- check.sh needs fra1's live bot, so it no longer runs anywhere. `history.py` (check mode) rebuilds its totals from the
  backup on Ohio.

## Sources

The three files above; `deploy/bin/rugsnipe-check` and `deploy/bin/rugsnipe-trades` (check.sh's code);
`deploy/bin/rugsnipe-history`; the strategy pages; session records of Oct 27-28.
