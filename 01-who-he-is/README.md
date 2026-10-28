# Who he is: the copied wallet AHwJSnFN (operator 1, "him")

> **In short:**
> - He is `AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2`. The docs first meet him as the best wallet of 2026-10-23: 430 landed round trips, +17.8 SOL ([docs/09][d09]).
> - Sep 24 - Oct 24 he made +151.6 SOL on 19 active days. He lands 400-600 trades a day at 0.6-0.8 SOL, wins 47-51% and holds 1-2 s. He trades from one wallet, with no linked wallets ([docs/12][d12] §1).
> - He buys first behind a launch's own bundle, with an on-chain guard, and sells at a fixed slot after the create. He follows operators by their bundle wallets and sizes his tip to his conviction ([docs/16][d16], [docs/17][d17] §5).
> - Live as our copy target (Oct 26 15:00 to Oct 27 11:45, Beirut time) he made +8.9099 SOL. Our 125 filled copies made -0.0479 SOL ([live check][live]).
> - His rules, with what our bot does about each one, are on the next page: [02-his-rules][rules].

## Words used here

- **create**: the transaction that launches a pump.fun coin. "create + 10" means 10 slots after the create's slot.
- **slot**: one Solana block, about 0.21 s ([docs/16][d16] §8). **Block position**: a transaction's index inside the block.
- **curve** (bonding curve): pump.fun's price formula for a new coin. The price rises as SOL goes in. It starts at 30
  virtual SOL (**vSOL**) ([docs/11][d11] Q2). **Post-bundle**: the curve right after the bundle.
- **bundle**: the buys that the launch's own wallets (the **creator set**) place right behind the create.
- **operator**: the person or bot behind a series of launches. The **create signer** is the create's fee payer, and
  our operator table keys on it ([docs/09][d09]; [docs/13][d13] §2). A **listed** signer is one in that table.
- **tip**: an extra payment that makes a transaction land early. It is paid only if the transaction lands. Amounts are
  in lamports: 1M = 1,000,000 lamports = 0.001 SOL. **mSOL** here means 0.001 SOL.
- **premium**: how far above the post-bundle price a buy may fill. **Tape**: every transaction on a coin in its first
  slots. **v10**: the price at create + 10 over the post-bundle price, minus 1 ([docs/17][d17]).
- **Out of sample**: measured on data that was not used to choose the rule.

## 1. How he was found

[docs/09][d09] calls him "the best wallet of 2026-10-23" and decodes a rule set from that day: 430 landed round trips,
+17.8 SOL. All 430 buys were the first trade after the launch's bundle: 278 landed in the create slot and 152 in the
next. The 33 create signers he traded 3+ times carried 289 of the 430 trades and 13.6 of the 17.8 SOL ([docs/09][d09],
"The rule set"). docs/09 does not state the window of that decode. For the whole of Oct 23, docs/12 §1 and docs/17 §9
give +26.1 and +26.14 SOL.

## 2. Results

**The month.** Sep 24 to Oct 24 (30,499 transactions) he made **+151.6 SOL on 19 active days**, with no trading on Oct
3-14. The wallet's balance rose by +153.8 SOL. The profit stays in the wallet: there are no withdrawals and no funding
wallet ([docs/12][d12] §1). His wallet started sniping in Aug 2026: 12,554 signatures and 6,442 buy attempts before Sep
24, and before that "36 in Jan 2025, then nothing" ([docs/16][d16] §9).

| day (UTC) | his result, SOL | source |
|---|---|---|
| Sep 26 | +21.7 | docs/12 §1 |
| Oct 1-2, Oct 15-16 | 0.01 SOL stakes, which look like test runs | docs/12 §1 |
| Oct 17 / 18 / 19 / 20 | +4.7 / +26.5 / +20.1 / +10.0 | docs/12 §1 |
| Oct 21 / 22 / 23 | +11.4 / +8.2 / +26.1 (docs/12); +11.38 / +8.24 / +26.14 (docs/17, whole wallet) | docs/12 §1, docs/17 §9 |
| Oct 24 | +5.23 (00:00-12:29 alone: +1.336 net on 126 trades, docs/11) | docs/17 §9 |
| Oct 25 (to about 18:00) | +2.82 | docs/17 §9 |
| Oct 26 15:00 to Oct 27 11:45 Beirut | +8.9099 on 377 launch buys | [live check][live] |

## 3. Profile at a glance

| measure | value | source |
|---|---|---|
| landed trades a day | 400-600 | docs/12 §1 |
| attempts | one transaction per launch. Oct 24 00-12 UTC: 570 attempted, 126 landed | docs/12 §2 |
| attempts a day (the replay's candidate launches: dev buy >= 0.25 SOL) | Oct 23: 1,590 tried, 418 landed. Oct 24: 1,209 / 293 | docs/17 §8 |
| failed buys | 74% of his buy transactions this month, each about 11,000 lamports | docs/16 intro, docs/12 §2 |
| stake | 0.6-0.8 SOL typical. 0.6 SOL base, up to 3.6 SOL | docs/12 §1, §2 |
| win rate | 47-51% | docs/12 §1 |
| hold | 1-2 s. Counted from the create: slot +6 or +10 (146 of 154 full-tape trades; 2,930 of 3,407 since Oct 16) | docs/12 §1, docs/14 §3 |
| positions | not limited by them: he held an open position at only 7 of 741 launches | docs/16 §10 |
| programs | all 23,929 buy transactions of the month are top-level pump buys | docs/16 §10 |

## 4. One wallet, nobody linked (since Sep 4, 2026)

His two guard programs are the slot window `A5c1eN7M...` and the curve state `8jzqTjED...`. Nobody else uses them,
and every sampled signer over 39-47 h is him. Nobody co-signs. His only transfers are 0.25-0.5 SOL test sends
([docs/12][d12] §1). No wallet on the tapes copies him and lands close behind him ([docs/17][d17] §9, "A bigger tip").

**Corrected on Oct 28** by the on-chain re-check of his whole history
([`analysis/research/2026-10-28/onchain/report.md`](../analysis/research/2026-10-28/onchain/report.md) §3): the
statement holds **since Sep 4, 2026**, not before. The wallet was funded in Jan 2025 (22.97 SOL through fresh
pass-through wallets, withdrawn two days later), restarted on Aug 17, 2026 with 199 SOL from `Gj9srqLh`, launched 37
pump coins itself (−2.93 SOL), and from Aug 25 to Sep 3 was the hub of a fleet: 232 wallets swept 3,246 SOL into it and
3,212 SOL went out through 220 three-hop chains to wallets that pump-traded and swept back (229 of the 232 are closed
now). He deployed both guard programs himself on Sep 6 (he is the upgrade authority; of their 80,951 signatures, 0 are
by anyone else). The Oct 1 test sends went to 55 fresh wallets that only paid relay tip accounts and swept back. One
linked wallet is still active, `4yN2vFSi` (his dev wallet, 2.97 SOL), which deployed an unused program on Oct 22. No
SOL has entered or left the wallet since Oct 3. Oct 24-28 he made +31.32 SOL on 1,401 landed buys, about 30% fewer a
day than on Oct 17-23 and half the daily profit ([07-restart](../07-restart/README.md) §1).

## 5. How he executes

| step | what he does | source |
|---|---|---|
| buy window | the `A5c1eN` guard allows the buy only in the create slot or the next. Window width 1 on all 6,304 landed buys; 66% land in the create slot, 34% in the next | docs/12 §2 |
| first behind the bundle | the `8jzqTj` guard checks the curve's real token reserve against the exact post-bundle value. If anyone trades first, the buy fails with custom error 100 for about 11,000 lamports (11,001 in docs/17 §5) | docs/12 §2 |
| position in the block | his landed buys sit a median 91 block positions after the create (p10 38): 1,060 in the create slot, 624 in the next (Oct 21-25) | docs/17 §9 |
| speed against us | under European slot leaders (the validator that builds the block) his median is 103 positions and 63% land in the create slot. Ours: 90 and 66% | docs/17 §10 |
| buy tip | see below: 0-1M on coins he rates low, up to 48M on coins he rates high | docs/17 §3, §5 |
| sell | a slot guard that starts at the planned slot, with no end. 0.5M priority fee plus a 1M tip. Later measured at about 1.3M a sell; 22% land a slot after his usual one | docs/12 §2, docs/14 §5 |
| sending | base fee plus a tip that is paid only on landing. Fan-out to many relays behind one durable nonce (one signed transaction, sent many ways, that lands once) | docs/09 rule 4 |
| cost | median round trip 3.3 mSOL, 0.75% of stake. Ours on Oct 24 was 9.0 mSOL, 1.77% | docs/11 |

**His tip, as the docs learned it.** [docs/09][d09] first saw a flat ~1.5M tip paid only on landing (rule 4). Its
2026-10-24 stake-tier row adds bids of about 1.5M at tier 0 and 6-24M (about 1% of the stake) above, and says he "took
14 of 16 head-to-head races on bid, 15 in the same slot". [docs/12][d12] §2 puts it as a 1.5M routine tip with no
priority fee, and about 12M (an 8M tip) when he wants a launch badly; it says he "won all 16 such races against us on
Oct 23". [docs/16][d16] §10 measures his median tip at 1.0M, hot or cold. [docs/17][d17] §3 and §5 give the fullest
picture. He bids 0-1M on coins he rates low and 8-48M on coins he rates high (§5 gives that range as 1.5-48M). His
landed tips come in steps: 1.0, 1.5, 1.8, 2.4, 3.6, 4.8, 7.2, 12, 18, 24M and up. On high-conviction coins the tip is
1-2% of the stake, and the stake rises too (0.6-1.8 SOL).

## 6. How he selects

**Layer 1: tweet coins.** In the sampled hour, 31 of 31 launches he attempted link in their metadata to a specific
tweet. Over 12 hours, 444 of his 469 attempts with readable metadata do. Three launch tools deploy these coins within
seconds of the tweet: j7tracker, uxento and rapidlaunch ([docs/12][d12] §3).

| feature (Oct 24 00-12, qualifying tweet coins: he took 424 of 2,055, 20.6%) | his attempt rate |
|---|---|
| launch tool | uxento 38.8%, j7tracker 22.4%, rapidlaunch 23.0%; other hosts 0-5% |
| dev buy | exactly 3.0 SOL 32%, 1.0 SOL 21%; **1.05-2.95 SOL only 3-5%** |
| image server | Axiom's old CDN 81%, its current CDN 19% |

On tweet age, the docs measure two different sets. On that qualifying set, he attempts 53% of coins made 2-5 s after
the tweet, 22% under 2 s, 29% at 5-10 s, and none on tweets over 1 h old ([docs/12][d12] §3). On the first coins of
his deployer list he attempts 82% at 2-5 s, 67% at 5-10 s and 51% under 2 s ([docs/14][d14] §6). He does not use a
coin's first-or-copy status: he attempts 55-56% of first coins and 40-43% of copies, with the same hold. Docs/14 reads
this as a tweet feed with a lag of about 2 s: rebuilt that way, it calls 7 coins an hour, 95% of them truly first, and
he attempted 75% of them ([docs/14][d14] §6).

**Layer 2: deployers he already trades.** He attempts 9% / 49% / 61% / **91%** of a creator's launches when he
attempted 0 / 1 / 2-4 / 5+ of its earlier launches that day. Once a deployer is on his list he takes almost every
launch, and new ones get in at about 9% ([docs/12][d12] §4). About a third of his trades are on signers he has never
traded ([docs/09][d09], "Paper wide").

**Layer 3: operators, by bundle wallet and fee routing.** An operator launches from a fresh deployer each time but
buys its bundle with the same few wallets. He follows those wallets. Example: `5sWHrtKx` (+2 others) was in 236 rule
coins and he attempted 98% ([docs/16][d16] §3). He also splits each operator by fee routing, meaning who gets the
creator fees: the dev itself, or a fresh third wallet. The third-wallet case is the coin's holder-reward mode, and he
treats the two as separate operators ([docs/16][d16] §8, §11). Keyed this way, he attempts 82-83% of followed coins out
of sample at a 0.5 rate threshold. Followed coins carried +16.19 of his +20.97 SOL (77%) over Oct 23 12-24 and Oct 24
00-12 ([docs/16][d16] §8). He takes 2% of holder-reward coins that carry a `creator_fee_bps`, and 0% of plain coins
with one of 100 or more ([docs/16][d16] §11).

**Layer 4: hot operators, and his size.** Inside an operator, what moves him is its recent coins' price at create +
10. After a skip he takes the next coin 41% of the time when its last 5 coins are in the top third by that measure,
and 16% when they are in the bottom third ([docs/16][d16] §10). He sizes the same way: a median of 0.909 SOL on a hot
operator's coin against 0.604 otherwise. "He buys a hot operator's coin at 1.5x, and those coins are worth twice the
rest" ([docs/16][d16] §9). On hot coins he lands at create + 1 more often (51% against 36%) and sells sooner (median 6
slots against 9) ([docs/16][d16] §10). His on/off is sticky: after he skips an operator's coin, he skips its next one
48% of the time (11-15% otherwise), and 78% of the time on holder-reward coins ([docs/17][d17] §5).

**What does not explain him.** Public coin features don't, and 64% of his outside picks come from creators he never
traded ([docs/16][d16] §2). Inside an operator, apart from the recent value above, the pre-buy state does not separate
his takes: not compute price, tip, uri host, name, dev wallet age, funding, the slot leader, nor his own recent P&L
(41% taken after losses, 50% after gains). The clear skip is a bundle inside the create transaction: he took 3 of 409
([docs/16][d16] §9). Nothing seen
before the buy reproduces his high bids ([docs/17][d17] §4).

**How much is explained.** One model fit on Oct 23 00-12 and scored later reaches an AUC of 0.882 and 0.937. He takes
93-96% of the top tenth of coins it ranks and 1-10% of the bottom half ([docs/16][d16] §10). His choice carries value.
The first outside buyer at create + 10, before costs, makes +6.3% mean (+3.3% median) on the 555 launches he
attempted, against +2.8% (-1.1%) on 204 qualifying launches he skipped ([docs/12][d12] §5).

## 7. His operators

| operator (key) | what the docs record | source |
|---|---|---|
| 8ZN71X... (signer) | he has traded it since Sep 26. Its 38 copies made +5.79 of the copy backtest's +8.13 SOL. Its creates fell from 123 (Oct 23) to 76 (Oct 24) and 37 (Oct 25, to 18:00) | docs/17 §10 |
| 8ZN71XTd (creator) | its 03:18 pair dumped on Oct 24. Skipping a creator for 3 h after a dump would have saved him 1.54 SOL (not adopted) | docs/11 Q2 |
| `5sWHrtKx` / `C57Ax2Bc` (bundle) | 236 rule coins, 98% attempted. Oct 24 12:00 - Oct 25 09:13: 50 of 64 when the dev keeps the fees, 41 of 69 with a third wallet | docs/16 §3, §8 |
| `5Eb5rURZ` / `J5dUdMdH` (bundle) | 87 rule coins, 92%. Same night: 25 of 26 against 12 of 27 | docs/16 §3, §8 |
| `DnkLKQtY`, `HeYpA9MA`, `89jFbt1W`, `2T3U2FzV` | 58 rule coins at 93%; 28, 27 and 14 outside coins at 93%, 93% and 100% | docs/16 §3 |
| `J4o3bqXK`, `Gg3ska7S` (bundle) | dev keeps the fees: 21 of 36, 14 of 24. Third wallet: 0 of 44, 0 of 39 | docs/16 §8 |
| CVmkctkS (creator) | he fired on 37 of the 39 of its launches we took on Oct 24 | docs/11 Q1 |
| 6sEEeA... (signer) | brand new, hot within the night of Oct 25-26 | docs/17 §10 |
| X personas | @devvvooooor (241 coins on Oct 23-24, 92% attempted by him), @igetsjiggy6767, @thedev1738, @ddddddd8a, @lilbruhfish; terrythedevv | docs/14 §7, docs/16 §8 |

**Turnover.** 60-70% of his trades each day come from operators absent from the previous day's table ([docs/09][d09],
"Keeping the table fresh"). The box's table keeps three days of his signers: 1,034 on Oct 25. The backtest's 4-hourly
tables held 40 to 64 signers, his current operators ([docs/17][d17] §9). On his big day, Oct 23, his key buys (tip >= 2M
or size >= 2 SOL) made +17.72 SOL on operators he had bought 2+ times in the past 24 h, and +1.80 on operators brand
new that month ([docs/17][d17] §10).

## 8. His weak days

- He made money every day of Oct 21-25. The two weakest were Oct 24 (+5.23 SOL) and Oct 25 (+2.82 SOL, to about 18:00)
  ([docs/17][d17] §9).
- A copy of his 0.7 SOL+ buys on listed signers kept 20-28% of his result on strong days and lost on his weak ones:
  +1.62, +0.49, +5.28, -0.38, -0.47 SOL. Each copy starts about 8 points behind him: about 3 points of price plus our
  round trip. Keyed on his tip (>= 4M) instead, the copy was positive on 4 of 5 days ([docs/17][d17] §9).
- Over his month, on signers he bought 2+ times in 24 h, his tip >= 4M buys were positive on 11 of 16 days. His big
  low-tip bets (tip < 4M, >= 2 SOL) were positive on 7 of 12 days, with losing days of -0.10 to -0.40 SOL
  ([docs/17][d17] §9, "His big low-tip buys").
- His losers are mostly rugs: the insiders sell their whole bundle in one slot, and he eats the dumps that come inside
  his hold ([docs/11][d11] Q2; [docs/17][d17] §5). On Oct 24 00:00-12:29 his 29 trades above 40 vSOL lost -0.839 SOL,
  including 2 rugs ([docs/11][d11] Q2). His low bids lose for him too: above 40, on coins where both of us bid about 1M,
  his 8 wins had a v10 of -11% ([docs/17][d17] §3).

## 9. Him as a copy target

- **The first spot is an auction.** He wins it on the coins he bids high for. Above 40 vSOL he took 153 first spots at a
  median bid of 8.0M (v10 +21.3%). We took 25 at 4.0M (v10 -4.2%): "Our wins are the coins nobody else would pay for"
  ([docs/17][d17] §3).
- **We cannot land his coins at the create.** When he lands first, our exact-state bound fails right behind him: 80 of
  our 83 attempts on those coins ([docs/17][d17] §9). The live copy therefore reacts to his landed buy. It lands about
  90 block positions behind him, which is the pipeline itself ([docs/17][d17] §9-10).
- **Copying behind his sell loses.** Copies that sell after seeing his sell lost 23.4 SOL: "his sell is the dump". The
  copy sells one slot before his known hold ([docs/17][d17] §9).
- **Listed signers only.** 904 of his 1,684 coins were on unlisted signers. They made him +13.2 SOL, against +39.7 on
  the 780 listed coins, and every exit we tried on the unlisted ones lost ([docs/17][d17] §9).

**Live, Oct 26 15:00 to Oct 27 11:45 Beirut time** ([live check][live], "1 him"):

| his launch buys | his net | our copies sent / filled / refused | our wins | our net | his net on coins we copied / skipped | his failed txs |
|---|---|---|---|---|---|---|
| 377 | +8.9099 SOL | 162 / 125 / 33 | 44 of 125 | -0.0479 SOL | +7.7826 (166) / +1.4461 (206) | 1,075, -0.0116 SOL |

The bot's daily-loss kill stopped all trading at 09:50:35 Beirut on Oct 27. The daily P&L behind it is the whole
bot's, across every copied wallet, not only him ([live check][live]).

## 10. The comparison wallet: 6anjqMe

`6anjqMeWigQFo5wpciARAunVQUXTqoat8w8fFWarCkpc` made +92.8 SOL over 23.5 days from Oct 1 (+3.9 a day), with its own
private program `satasbJp...` ([docs/12][d12] §8). On SOL-priced coins in Oct 21-25 it made +8.01 SOL on 1,660 coins
(+0.005 a buy, 39% wins). It buys into a curve already at a median 40 SOL and sells on the price within a few slots:
its trades held 0-5 slots made +16.89 SOL, and those held 10+ lost -23.12 SOL ([docs/18][d18]). The slices that looked
good on Oct 21-25 failed on Oct 1-20, so the verdict is "no slice of his trades is worth copying at our speed". The
bot keeps copying AHwJSnFN, whose create-relative exit a copy can know in advance ([docs/18][d18], "Why it fails where
AHwJSnFN works").

## 11. Discovery timeline

| date | what we learned about him | doc § |
|---|---|---|
| 2026-10-23 | best wallet of the day: 430 round trips, +17.8 SOL. First behind the bundle 430/430. Sells at create + H. Repeat operators carry the profit. Flat ~1.5M tip | docs/09, "The rule set" |
| 2026-10-23 | H in {1, 3, 6, 10} on 132/132 (6 h) and 444/444 (24 h). 60-70% of each day's trades come from new operators | docs/09, "Keeping the table fresh" |
| 2026-10-24 | stake 0.4 SOL x 1.5^a x 2^tier. Tier returns +2.3% / +7.3% / +21.3%. High bids win contested launches | docs/09, table row "stake tier" |
| 2026-10-24 | head to head, 00:00-12:29: him +1.336 SOL, us -0.253. His failed buy shows in our block (51 of 57). His costs are 0.75% against our 1.77% | docs/11 |
| 2026-10-24 | full month: +151.6 SOL, no linked wallets, two guard programs. He picks tweet coins and deployers he already trades, and stakes by his record | docs/12 §1-5 |
| 2026-10-24 | a tweet-coin rule built on his deployers: +5.0% a trade (overstated: see the next row) | docs/13 §1 |
| 2026-10-24 evening | the corrected value is +3.68%. He sells at +6 or +10 per deployer (86% repeat). Stake 0.4 x 2^tier. He favours first coins 2-10 s after the tweet, which a ~2 s tweet feed explains | docs/14 §1-6 |
| 2026-10-25 | he follows operators by bundle wallet and fee routing (79-83% out of sample, 77% of his profit). Hot operators get 1.5x his size. Model AUC 0.882 / 0.937. He has sniped since Aug 2026 | docs/16 §3-11 |
| 2026-10-25 | the first spot is an auction. He bids 0-1M low and 8-48M high, so we land his rejects. His tip is his conviction. The copy sells at H - 1, on operators he bought 2+ times in 24 h | docs/17 §1-9 |
| 2026-10-26 | he is no faster than us (103 against 90 positions). One operator (8ZN71X) carries the copy backtest. New operators lose for the copy | docs/17 §10 |
| 2026-10-26 | 6anjqMe tested as a second target: rejected | docs/18 |
| 2026-10-27 | live copy window: he +8.9099 SOL, our copies -0.0479 SOL | 05-live/check-sh-2026-10-27.txt |

## Sources

- [docs/09-operator-wave.md][d09]
- [docs/11-operator-bot-vs-copied-wallet-2026-10-24.md][d11]
- [docs/12-how-the-copied-wallet-trades.md][d12]
- [docs/13-tweet-coins.md][d13] (its numbers are corrected by docs/14)
- [docs/14-corrected-backtest.md][d14]
- [docs/16-who-he-follows.md][d16]
- [docs/17-newest-bot-vs-him-5-days.md][d17]
- [docs/18-copy-6anjqMe.md][d18]
- [analysis/research/2026-10-24/README.md][r24] (the scripts behind docs/11 and docs/12: `pull_month.py`, `profile.py`,
  `guards.py`, `guard_users.py`, `funders.py`)
- [analysis/research/2026-10-25/follow/README.md][r25f] and [analysis/research/2026-10-25/five/README.md][r25v] (the
  scripts behind docs/16 and docs/17)
- [05-live/check-sh-2026-10-27.txt][live] (row "1 him" and its section)

[d09]: ../docs/09-operator-wave.md
[d11]: ../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md
[d12]: ../docs/12-how-the-copied-wallet-trades.md
[d13]: ../docs/13-tweet-coins.md
[d14]: ../docs/14-corrected-backtest.md
[d16]: ../docs/16-who-he-follows.md
[d17]: ../docs/17-newest-bot-vs-him-5-days.md
[d18]: ../docs/18-copy-6anjqMe.md
[r24]: ../analysis/research/2026-10-24/README.md
[r25f]: ../analysis/research/2026-10-25/follow/README.md
[r25v]: ../analysis/research/2026-10-25/five/README.md
[live]: ../05-live/check-sh-2026-10-27.txt
[rules]: ../02-his-rules/README.md
