# 07. Restart the copy of him: the review of Oct 28 2026

> **In short**
> - **The live copy did not fail; it ran out of edge.** The 125 filled copies made +0.834 SOL on the curve and paid
>   0.882 in tips and fees (net -0.048). Rebuilt with the live costs, landing and bids, the 5-day backtest's own last two
>   days (Oct 24-25) give the same per-fill result: curve +0.0067, net -0.0004 a fill. **The +8.02 SOL backtest was Oct
>   21-23 and a few coins**: Oct 24-25 alone made +0.27, and -0.52 without their best 2 copies
>   ([copy_relook](../analysis/research/2026-10-28/copy_relook/report.md) §B).
> - **He is the same machine at lower volume**: Oct 24-28 +31.32 SOL on 1,401 landed buys, about 307 a day against
>   437 on Oct 17-23 and half the daily profit (+7.0 against +15.3); the same stakes, tip steps, guards, relays, holds
>   (6 or 10 planned on 91%). 249 SOL in the wallet, nothing in or out since Oct 3. **The wallet has a history the docs
>   missed**: a 232-wallet sniper fleet swept 3,246 SOL through it in Aug-Sep 2026 and is closed now; he deployed both
>   guard programs himself (nobody else has ever called them); one dev wallet (4yN2vFSi) is still active and deployed
>   an unused program on Oct 22 ([onchain](../analysis/research/2026-10-28/onchain/report.md)).
> - **What costs money and is now fixed in the code:** the 8M bid arm (−0.30 SOL over the window for 7 positions
>   closer), a graduated coin whose sell had given up stayed unsold for ever, a sell that gives up was a dead end, a
>   lease-loss edge case, the signer window was 13 h not 24 h, and signers with a hold under 4 could not be sold before
>   him. Every fix has a test; 317 tests pass.
> - **Nothing new passes out of sample**: stake ladders by his tip, exits by bucket, circuit breakers, a second copy
>   after a refusal, the low-tip buys, the operator count, and the one angle the chain offered (a fifth of his bids
>   sit in the priority fee, which the tip key does not see: the 130 coins a tip + priority key adds lose −0.83 SOL
>   over 5 days). The refused copies and the skipped buys stay refused and skipped: every way to take them tested
>   negative, again.
> - **If the copy restarts**, it restarts as a measured small test, him alone, 0.5 SOL, bid 3.0M with a 1.5M A/B,
>   in Frankfurt (TeraSwitch FRA2 first, Cherry FRA EPYC 9355 at €599/mo if not in stock), on the Triton feed with
>   Riptide raced against the standard endpoint. Expected result at the backtest's last two days: about zero. The
>   restart buys information, not income, unless his good days come back (his Oct 21-23 made the copy +7.75).

Everything below is dated Oct 28 2026. Times are UTC unless marked Beirut (UTC+2). Every figure has a source: a page of
this repo, a script, or a paste of the owner's. Nothing is running: fra1 was terminated on Oct 28.

The four reviews of this session, in full:
[`code-review-2026-10-28.md`](code-review-2026-10-28.md) (the copy path's code),
[`../analysis/research/2026-10-28/copy_relook/`](../analysis/research/2026-10-28/copy_relook/README.md) (the backtests
re-run and extended, with `report.md`), [`../06-infrastructure/box-and-feed-2026-10-28.md`](../06-infrastructure/box-and-feed-2026-10-28.md)
(the box and the feed), [`../analysis/research/2026-10-28/live_decomp/`](../analysis/research/2026-10-28/live_decomp/README.md)
(the live copies decomposed), [`../analysis/research/2026-10-28/onchain/`](../analysis/research/2026-10-28/onchain/report.md)
(him re-checked on chain: Oct 24-28, his whole history, the wallet's links).

## 1. Where he stands today (Oct 28)

From the on-chain re-check (every transaction of his since Oct 24, failed ones included; his full signature list back
to Jan 2025; 19,656 RPC calls, about $0.20; `analysis/research/2026-10-28/onchain/report.md`):

| UTC day | landed buys | failed | net SOL | per buy | win | tip >= 2M | tip + priority >= 2M | planned H = 6 or 10 |
|---|---|---|---|---|---|---|---|---|
| Oct 24 | 315 | 954 | +5.23 | +0.017 | 48% | 33% | 47% | 68% |
| Oct 25 | 235 | 797 | +6.98 | +0.030 | 43% | 40% | 57% | 60% |
| Oct 26 | 372 | 1,088 | +10.20 | +0.028 | 50% | 40% | 57% | 63% |
| Oct 27 | 305 | 1,005 | +5.76 | +0.019 | 46% | 39% | 58% | 66% |
| Oct 28 (to 14:56) | 174 | 473 | +3.15 | +0.018 | 49% | 43% | 54% | 59% |
| **Oct 24-28** | **1,401** | 4,317 | **+31.32** | +0.022 | 47.5% | 38% | 55% | 64% |
| Oct 17-23, a day | 437 | 1,263 | +15.30 | +0.035 | 47% | 42% | 56% | 68% |

- **The same trader.** The stake ladder (0.395 x 1.5^a, doubling), the tip steps, 64% in the create slot, a 2 s hold,
  the two guard programs, the same relays (helius 35%, nozomi 35%), the same 100 nonce accounts. Every coin has one buy
  and one sell. His sell lands on the planned slot 68.5% of the time and one slot later 27.1%.
- **Lower volume, half the profit a day** since Oct 24: about 307 landed buys a day against 437, +7.0 SOL a day against
  +15.3, +0.022 a buy against +0.035. His profit per buy is what the copy lives on.
- **The docs' profile is Oct 17-23's.** In September he sold at create + 2 to + 5 and won 35%; the + 6 / + 10 holds
  started on Oct 16.
- **Part of his bid is the priority fee.** 21.5% of his landed buys carry a priority fee of 0.1M or more (56% of the
  nozomi-landed ones), on the same ladder as the tip (a 1.0M tip with 3.8M priority is a 4.8M bid). The copy keys on
  the tip alone: in the live window it took 167 of 377 coins (+7.52 for him); 78 more had tip + priority >= 2M and made
  him +4.86 (+0.062 a buy); over Oct 16-28 that bucket made him +23.5 SOL on 637 buys, positive 12 of 13 days. **As a
  copy it loses** (copy_relook C9, `c9_bidkey.py`): the 130 coins a tip + priority >= 2M key adds over the 5 days make
  −0.83 SOL [−1.41], negative on 4 of 5 days; all 130 carry a 1.0M tip with 1.4-29M of priority, 69 are his create + 1
  buys, and he made +3.73 on them by being first. The whole key: +6.94 against +7.77 over 5 days, Oct 24-25 −0.44
  against +0.21. The tip key stays.

**The wallet's links** (the owner's ask; `report.md` §3):
- **Funded Jan 16 2025** with 22.97 SOL through three fresh pass-through wallets, one coin launched, 24.09 SOL withdrawn
  two days later the same way. **Restarted Aug 17 2026** with 199 SOL in five transfers from `Gj9srqLh` (which also took
  83.7 SOL from the fleet's biggest sweeper and paid 46.3 SOL to a Raydium trading wallet; 1.0 SOL left, idle).
- **He launched 37 pump coins himself** (36 on Aug 17-18), net −2.93 SOL.
- **Aug 25 - Sep 3 he was the hub of a fleet**: 232 wallets swept 3,246 SOL into him (59 of 60 sampled sweeps came
  right after the sender's own pump trade), and 3,212 SOL went out through 220 three-hop chains of fresh wallets, each
  chain in one second, to wallets that pump-traded and swept back. 229 of the 232 are closed; the fleet is dormant.
- **Sep 6 he deployed both guard programs** (`A5c1eN7M`, `8jzqTjED`): he is the upgrade authority, neither was ever
  upgraded, and of their 80,951 signatures **0 are by anyone else**. Sep 12-15: 100 durable nonce accounts, his.
- **Oct 1: 55 fresh wallets** got 0.25-0.5 SOL and swept back the same day. They never traded: 1,046 of their
  transactions are System/Memo sends to relay tip accounts. Relay-landing tests.
- **Since Oct 3: no SOL in or out.** No withdrawals; 249.05 SOL at the end of Oct 28 (217.72 on Oct 23).
- **One linked wallet is still active: `4yN2vFSi`** (2.97 SOL): he funded it in August, it moved SOL with him and the
  fleet, and on **Oct 22** it deployed a new 2,189-byte program (`7SVCZWEj`, 4 transactions ever, unused) and sent
  0.001 SOL test tips with a memo to every one of his relays. His dev wallet.
- **Nobody co-signs** except his own new keys (mints, programs, nonces). He holds one pump token. A third-party bot
  (`DeFG8i8z`) referenced his wallet read-only in 31 transactions on two of his coins around his sell: it watches him,
  it is not him.
- So "one wallet, no linked wallets" (docs/12 §1) is true **since Sep 4**. Before that he ran the fleet. Nothing in
  this changes the copy, but it says who he is: an operator with a few hundred wallets' worth of infrastructure, not
  a lone trader.

Checked from this session directly (Triton JSON-RPC, 15:00 UTC):
- He is trading now: his newest transaction at 15:01:18 UTC (`operators_refresh.py --source rpc --hours 2`).
- His balance: 249.068 SOL (`getBalance`).
- His last two hours (13:03-15:01 UTC): 66 landed trades on 33 coins, 33 round trips, +1.018 SOL, 106 failed
  transactions. Sell slot minus create slot: 10 on 18 coins, 6 on 14, 3 on 1 (33 of 33 in his usual set). His buy
  landed at create + 0 on 22 and + 1 on 11. His stakes 0.403-2.426 SOL (0.403 the most common). Only 4 of the 26
  signers in the window had two of his buys. Source: the refresh script's own log, run from this container.
- The slot: 3,037 slots in 679 s on Oct 28 (14:49:59 to 15:01:18 UTC), about 225 ms. docs/16 §8 measured 212 ms. The
  code assumed 400 ms in one place (§4).

## 2. What the live copy really did (Oct 26 15:00 - Oct 27 11:45 Beirut), decomposed

The `== 1 him` table of [`05-live/check-sh-2026-10-27.txt`](../05-live/check-sh-2026-10-27.txt), 377 rows, parsed row
by row (`analysis/research/2026-10-28/live_decomp/live_decomp.py`). The stake of a filled copy is OUR NET / our %.

| the 125 filled copies | SOL |
|---|---|
| curve P&L (sold minus paid, before costs) | **+0.834** |
| tips and fees on those 125 fills | **-0.882** |
| net | -0.048 |

**The copies made money on the curve and the fixed costs ate all of it.** The stake was 0.5 SOL on 122 of 125
(median 0.499); only the last three, on Oct 27 morning, were smaller as the shared wallet emptied (`stake_fits_balance`).

| cut | n | won | our net | fees | curve | his net on the same coins | per copy |
|---|---|---|---|---|---|---|---|
| bid 3.0M | 64 | 25 | +0.439 | 0.298 | +0.736 | +2.22 | +0.0069 |
| bid 8.0M | 61 | 19 | -0.486 | 0.584 | +0.098 | -0.19 | -0.0080 |
| Oct 26 (Beirut day) | 69 | 25 | +1.052 | 0.457 | +1.510 | +5.52 | +0.0153 |
| Oct 27 | 56 | 19 | -1.100 | 0.425 | -0.675 | -3.48 | -0.0196 |
| his tip 2-4M (tip key alone) | 32 | | +0.458 | | | | +0.0143 |
| size key only (his 2 SOL+, tip under 2M) | 6 | | -0.470 | | | | -0.0783 |
| his tip 4.8-7.2M | 41 | 5 | -1.437 | 0.298 | -1.139 | -1.70 | -0.0351 |
| his tip 8M+ | 46 | 21 | +1.402 | 0.312 | +1.714 | +3.37 | +0.0305 |
| landed in his slot | 86 | 29 | -0.456 | 0.609 | +0.153 | +0.01 | -0.0053 |
| landed one slot later | 38 | 15 | +0.410 | 0.263 | +0.673 | +1.97 | +0.0108 |
| his buy at create + 1, copied in his own slot | 33 | | -0.577 | | | +0.36 | -0.0175 |

(The tip-bucket rows: live_decomp; the 2-4M / size-key split and the last row: copy_relook §B and §C7.)

- **The 8M bid cost 0.005 SOL more per fill and landed 7 positions closer** (TIP TEST d_avg 149 against 156; on the
  tapes about 26 closer, 75% in his slot against 64%). Over 61 fills that is -0.30 SOL of tips for about +0.1 of curve.
  The 3M arm alone was +0.44 on 64 copies.
- **Oct 26 was in line with the backtest** (+0.015 a copy; the 5-day backtest is +0.027 a copy at 0.5 SOL). **Oct 27
  was his weak day** (he lost -3.48 on the coins we copied, -0.72 on the day's 156 rows), and the copy lost more than
  him, as docs/17 §9 warned it does on his weak days.
- **Seven dumps did it**: CSMc5K1u -0.305, HvjYQ3VW -0.298, DR8or4ud -0.284, 3Ye1Wgff -0.278, 7QsUeqFq -0.270,
  4s85HKoM -0.235, 4q3ser1u -0.167: -1.84 SOL, five of them between 03:49 and 03:57 Beirut on Oct 27. He lost on six of
  the seven himself. Without the two worst the fills were +0.56; without the two best, -1.09. Live, 7 of 8 dumps came
  within 30 minutes of another (p 0.015, copy_relook C4); in the 5-day data they did not cluster (p 0.07).
- **The 33 refused copies**: his net +4.63 on them, 18 at tips of 8M or more. 15 of the 33 landed a slot after him (the
  reactors with 18-50M tips went first, docs/19 §9). Every fix for refusals tested negative over 5 days (docs/19
  §9-§10) and again here (§3).
- **His 4.8-7.2M tips lost 5 of 41 live**, far outside what the 5 days give for that bucket (none of 20,000 resamples
  reached -1.44; the bucket itself is about zero over the 5 days, +0.16, -0.75 without its best 2). Two clustered
  bursts, not a bucket to key on.

**The reconciliation** (copy_relook §B, `recon.py`): from `ablate.py`'s +8.02 to the live setup, step by step, on
the backtest's own Oct 24-25:

| step | 5 days | Oct 24-25 | Oct 24-25, curve a fill | net a fill |
|---|---|---|---|---|
| ablate.py as published | +8.02 | +0.27 (-0.52 without the best 2) | +0.0081 | +0.0045 |
| + the live fixed cost at 3M (bid + 0.0016) | +7.77 | +0.21 | +0.0081 | +0.0035 |
| + the live landing (31% a slot later, median 126 positions behind him) | +7.35 | +0.20 | +0.0083 | +0.0037 |
| + 16% of sells one slot late (measured live) | +6.92 | +0.12 | +0.0067 | +0.0021 |
| + the live bid mix (0.00705 a fill) | +6.38 | -0.02 | **+0.0067** | **-0.0004** |
| **live, 125 fills** | | | **+0.0067** | **-0.0004** |

On 50 real fills with our buy and sell on a tape, the model reads 0.0058 SOL a fill *below* reality: it is not
optimistic for him. The gap between +8.02 and break-even is the period, not the model.

## 3. Every decision, re-explored

Picked on Oct 21-23, scored on Oct 24-25, and without the best 2 copies [in brackets], as the repo's convention asks.
3M costs, 0.5 SOL, the 298-copy set unless stated. Sources: copy_relook `report.md` §C (scripts `c1`-`c8`), the code
review, the live decomposition.

| decision | as it ran live | re-explored | verdict for the restart |
|---|---|---|---|
| **the bid** | 3.0M / 8.0M A/B, tip-only on every leader class | 8M at its own landing: +6.29 over 5 days against +7.30 for 3M (1.16 more cost, ~0.1 more curve). 1.0-1.5M would add +0.3 to +0.4 if it lands as 3M does; untested for copies (c8) | **3.0M, A/B 1.5M**; keep the lower bid only if d_avg is no worse and net per copy is higher. Tip-only split stays (a refused copy costs 15k lamports, not the bid) |
| **the stake** | 0.5 SOL (122 of 125) | costs are fixed a fill, so the stake multiplies the curve: 3M net +3.32 / +7.77 / +16.85 / +26.17 at 0.25 / 0.5 / 1.0 / 1.5 over 5 days. But Oct 24-25 without the best 2: -0.42 / -0.58 / -0.88 / -1.17. The curve model flatters big stakes (others' tokens held fixed; SOL fixed gives +15.33 at 1.0) | **0.5 SOL.** Raise it only after a week whose curve is positive without its best 2 |
| **stake by his conviction** | flat | tip ladder 0.5/1.0/1.5: +17.28 over 5 days [+13.54], Oct 24-25 +0.73 [**-1.69**], capital 2.5 SOL, worst drawdown -2.66; every ladder rescales Oct 21-23's winners (c1) | **no ladder** |
| **his tip floor 2M** | 2M | by bucket over 5 days: 2-4M +2.31 [+0.41], 4-8M +0.16 [-0.75], 8M+ +3.88 [+2.71] (c7) | **2M stays** (4-8M is about zero both ways; nothing to key on) |
| **his 2 SOL+ buys at any tip** (`copy_big_sol`) | on | +1.42 on 6 over 5 days, all Oct 23 [-0.05], Oct 24-25 -0.01; live -0.47 on 6 | **off** until a week of journaled data says otherwise |
| **the 5% bound** | 5% | 10% / 15% / none: -1.05 / -1.79 / -2.07 (reproduced); a second copy after a refusal (tip >= 8M, within 10%, still create + 1, sold at +5): -0.08 [-0.49] (c5) | **5%; no second copy** |
| **the skipped low-tip buys** | skipped (206 live, his +1.45) | size >= 1.0 and tip >= 1.5M: 0 buys in 5 days. All 531 low-tip buys: -2.17 at 0.5, -2.00 at 1.0 (c5) | **skipped** |
| **his priority-fee bids** (new, from the chain) | not seen by the tip key | a key on tip + priority >= 2M adds 130 copies over 5 days: −0.83 [−1.41], 4 of 5 days negative; the whole key +6.94 against +7.77, Oct 24-25 −0.44 against +0.21; 3M / 4M / 6M thresholds worse (c9) | **tip key stays** |
| **the exit H - 1** | H - 1 | by bucket (tip >= 8M: H-1 +3.88 best; 2-8M: H-1 +2.47 best); the per-bucket picks make -0.17 on Oct 24-25 against +0.21 for H-1 everywhere (c2). Live: copies sold at create + 9 (H = 10 signers) -1.67 on 60, at + 5 (H = 6) +0.70 on 52, one window | **H - 1 everywhere**; watch the H = 10 group in the next window |
| **sell timing** | 0.5M sell tips | 16 of 100 live sells with a fixed target landed a slot or more late; every sell one slot late costs -2.70 over 5 days, so the measured 16% costs -0.43 (c3) | keep 0.5M; count late sells in the next window before paying more |
| **the operator rule** | the box ran `copy_signer_min_buys = 0` (the config, read correctly by check.sh), with `copy_listed_only` on | with the table kept, the count is worth -0.06 over 5 days (by day -0.48 +0.44 -0.11 +0.05 +0.05); against no rule and no table, +1.71 (c6). The window was 13 h in wall time, not 24 (code review Q1.3) | **2 in 24 h, as documented**, with the window fixed: it is the table that matters |
| **circuit breakers** | none | pause after 3 losses / 2 dumps in 30 min / a copies-only day stop / an operator out 3 h after a dump: 0 to +0.40 over 5 days, -0.13 to -0.65 live (each pause forgoes HQT8xbhA +0.71 right after the dumps) (c4) | **none** |
| **H under 4 signers** | copied, sold at +2 or at his own slot | H = 3 sells at +2, at or before our fill; H = 1 at his dump (code review Q4.3); none in this window | **skipped** (`skip_short_hold`, built) |
| **the daily stop** | 1 SOL, every copied wallet together | marked to market every second; one unsellable position carries into the next UTC day (Q6.1) | 1 SOL, **him alone in his own wallet** |
| **where the copy lands** | 69% in his slot, 31% a slot later, median 126 positions behind (tapes) | the losses were not on the late fills (+0.41 on 38); they were on his create + 1 buys copied in his own slot (-0.58 on 33), and the 5-day model agrees in direction (-0.22 on Oct 24-25) | nothing to build: a copy cannot know his slot before it sends |
| **the feed** | Triton gRPC post-execution; the shreds copy of his buy 6 ms earlier was not used for copies | copying the pre-execution copy would copy his failed guards (-0.30 over 5 days); Riptide is the same gRPC with a faster path (box study §5) | **race Riptide against the standard endpoint for 2 h, keep the winner; keep Deshred on for the measurement** |
| **the box** | fra1, "Frankfurt bare metal" (provider not recorded) | TeraSwitch FRA2 0 ms extra; Cherry FRA +0.25-0.33 ms (1-2 positions); Latitude +0.6; AWS eu-central-1 +0.6-0.8; Ohio never (0% of leaders, +104 ms) (box study §3) | **TeraSwitch FRA2, else Cherry FRA EPYC 9355 by the hour**; §5 |

## 4. What changed in this commit (code and config)

| change | file | why |
|---|---|---|
| **him-only config template** | `config/copy-him.example.toml` | the live file was probe-a plus edits nobody has. This one carries every key of the copy with its reason, validated with `rugsnipe-ctl config validate` against a signed stage-b ArmSet (only the two credential refusals remain, as for probe-a). Bid 3.0M with a 1.5M A/B, tip-only split, `copy_big_sol` off, 0.5 SOL, `stake_min_sol` 0.35, the re-arm below |
| **a graduated coin whose sell had given up is sold on the pool** | `crates/rugsnipe-exit/src/decide.rs` (`on_complete`, `rearm`), test `completion_behind_a_given_up_order_sells_on_the_pool` | the Oct 27 fix (`af681ad`) re-sent only orders still alive; the lane's report of the completed curve can come after the 4 tries of a 2M dump tip (about 8 slots), and then nothing was ever sold (code review Q5.1, reproduced). Now the order is placed again from scratch on the pool, with a fresh budget |
| **a sell that gives up is no longer a dead end** | `decide.rs`, `policy.rs` (`sell_retry.rearm_after_slots`, default 2,700 slots, about 10 min), `types.rs` (`Alert::SellRearmed`), test `a_given_up_order_is_placed_again_after_the_interval` | after `max_tries` or the spend cap the position sat unsold until a restart (Q4.4). Now it is placed again every `rearm_after_slots` while open, at the base dump tip, and the hot loop journals `CRITICAL sell ... gave up` and `... placed again` (before, the alert was an rslog record only) |
| **a sell sent without the exits lease is taken back** | `crates/rugsnipe/src/hot.rs` (`sell`, `!owned`) | it counted as sent, burned its tries, and the hot loop never sold once the lease came back (Q8.1); now it is `unsent`: due again next slot, no try, no tip |
| **the signer window is 24 h** | `hot.rs` `SLOTS_PER_HOUR` 9,000 -> 16,000 | the constant assumed 400 ms slots; the chain runs about 212-225 ms (§1), so `copy_signer_window_h = 24` acted as about 13 h, and the saved counts were pruned at 13 h (Q1.3) |
| **signers with a hold under 4 are not copied** | `hot.rs` `copy_trade` (`skip_short_hold`, `COPY_MIN_HOLD = 4`), test `a_signer_with_a_hold_under_4_is_not_copied`; labels in `deploy/bin/rugsnipe-trades` and `rugsnipe-vs-him` | H = 3 sells at +2, H = 1 at his own dump (Q4.3). Counted with the unlisted ones in the status line, its own reason in the journal |
| **why a copy was not sent is journaled** | `hot.rs` (`last_decision`, `copy <mint> not sent: <reason>`) | the copy line said `-> buy` before 14 later gates could drop it; check.sh showed "copied, not sent" with no cause (Q7.2) |
| **the copy counter is seeded from chain** | `analysis/scripts/strategy/operators_refresh.py --copy-signers-seed`, `deploy/systemd/rugsnipe-operators.service` | `copy_signer_min_buys` counts his buys per signer live and starts empty on a fresh box (99 of 226 copies kept, docs/17 §9). The refresh writes his last 24 h of launch buys per signer as `copy_signers.json` whenever the hot unit is not running. Tested against today's chain: 26 signers, 33 buys in 2 h, 135 calls, 18 s |
| **the ArmSet's size is a flag** | `analysis/scripts/make_paper_armset.py --size-sol` | the copy's stake is min(ArmSet size, `[probe] b.max_probe_lamports`, `entry.stake_by_tier[0]`); stage b's default size is 0.25, the live copies staked 0.5 |
| **check.sh reconciles the wallet** | `deploy/bin/rugsnipe-check` | "results since the start" counted closed trades only (-0.76 while the wallet lost 1.41). It now prints the open positions at cost and the rest (failed sells' fees, nonce rent), and warns when more than 0.02 SOL left the wallet outside trades |

Tests: `cargo test -p rugsnipe -p rugsnipe-core -p rugsnipe-exit`: 317 passed, 0 failed (47 binaries), on the pinned
1.97.1 toolchain. Not changed, and worth knowing (code review): graduation is detected only from a failed sell (one
failed sell per graduation; Q5.2); his tip is read from his top-level System transfers and reads 0 when the logs are
truncated (Q8.2); one nonce per mint by hash with no fallback (Q8.4); the 4-hourly restarts miss his buys for 5-20 s
each (Q8.8).

## 5. The box and the feed

From [`06-infrastructure/box-and-feed-2026-10-28.md`](../06-infrastructure/box-and-feed-2026-10-28.md) (measured Oct
28 from TeraSwitch's looking glass and Cherry's plan API; VERIFIED / SOURCED / UNVERIFIED marked there).

- **fra1's provider was never recorded** in the repo (only "Frankfurt bare metal, user `ops`"); most likely TeraSwitch
  FRA2. The owner's invoice settles it.
- **Nothing beats Frankfurt** for a bot that reacts to his landed buy: 35% of leader slots are in Frankfurt, 21% in
  Amsterdam; every sender and Triton sit in TeraSwitch FRA. **Ohio: never** (0% of leaders in its metro, +104-108 ms to
  Frankfurt; the copy would land about 500 positions behind on EU leaders).
- **Cherry Servers FRA is close, not the same**: Equinix FR13, 360 m from TeraSwitch FRA2, 0.32-0.42 ms round trip
  today against 0.07-0.12 ms inside the building (Oct 14 it measured 0.089 ms). That is 1-2 of the ~126 positions we
  land behind him. In stock: EPYC 9355 32-core at €599/mo or €1.026/h. The repo's €989 EPYC 9375F and every 10 Gbps
  plan show no stock in Frankfurt. Accept a Cherry box below 0.5 ms average on the day-one pings, not the checklist's
  0.2 (the owner's call).
- **Order**: TeraSwitch FRA2 bare metal (~$425/mo, stock unknown, their site blocks automated reads), else Cherry FRA
  by the hour, with the day-one test before committing. No second site: Amsterdam would add 0.3-1.8 SOL a month at
  most, and the routing between two boxes is not built.
- **The feed under the Triton plan**: Dragon's Mouth gRPC at $0.08/GB is included; **Riptide** (the lower-latency path
  to the same stream, same token, "first 81.8% of the time") is included; **Deshred** (pre-execution, the 6 ms lead
  fra1 measured) is a paid beta on all plans and fra1 ran it. The three anycast endpoints answer in under 0.1 ms from
  the Frankfurt router. The $75 of credit lasts roughly 10-30 days at the repo's volume estimates: watch the portal.
  Do not buy raw shreds, DZ Edge or LaserStream for this bot. **Triton Preconfs** (Harmonic ~15 ms, BAM ~8 ms ahead,
  with the result) are the one feed that could move the copy closer to him; about $95 a day for the two Frankfurt
  regions, no adapter in the code yet, on request only. A one-day log of his transactions' lead is the test.
- **Shred prices moved**: Triton FRA/AMS raw shreds are $1,500/mo or $0.59 per 15 min today (the repo had $0.18 / from
  $900).

## 6. Runbook: from the Ohio backup to the first copy

Everything the owner runs, one block each, with what it should print. `~/rugsnipe` is a clone of **this repo
(copy1)** on each box: the code is the Oct 28 snapshot plus this commit. (The upstream `xin10ylop/rugsnipe` does not
carry this commit; point the boxes here.)

### 6.0 On Ohio now: what the backup holds (prints names and config lines, never key contents)

```bash
sudo ls -la /root/fra1/etc/rugsnipe/ /root/fra1/etc/rugsnipe/keys/ /root/fra1/var/lib/rugsnipe/
sudo grep -nE '^(mode|stage|rule_buys|copy|follow|max_buys_per_hour|spread|max_probe|max_snipe|max_daily|stake|lamports|split|ab_by_tier|by_tier|sell_tip|dump_tip|hold_to|max_premium|operators_file|tweet|dumper|leader_regions|min_hot|cu_limit)' /root/fra1/etc/rugsnipe/rugsnipe.toml
sudo python3 -I -c 'import json;d=json.load(open("/root/fra1/var/lib/rugsnipe/copy_signers.json"));print(len(d),"signers",sum(len(v) for v in d.values()),"of his buys kept")' 2>&1 | tail -1
```
What it should print: the key files `probe-keypair.json` and `api-keys.toml` listed (0400); the config lines, among
them `copy_signer_min_buys = 0` (the code review expects 0: it settles the S6 page's open question) and the `split`
line (expected tip-only); the copy counter's signer count, or "No such file". **Paste the output back.** It holds no
secret: the config names credentials, it never holds them. Also: which provider's invoice fra1 was on (§5).

### 6.1 Rent the box and accept it

TeraSwitch FRA2 if they have stock (`deploy/frankfurt-checklist.md` §1 has the spec: 9950X or similar, 64-128 GB,
NVMe, a 10 GbE NIC, a public IPv4 without NAT, Ubuntu 24.04); else Cherry Servers Frankfurt, EPYC 9355, hourly. Then
the **day-one checklist** of the box study, §6 step A (one copy-paste block: CPU, NAT check, `deploy/latency_probe.sh
30`, 100-ping runs to the five in-building targets, Nozomi, BlockRazor, the three Triton addresses, Astralane and
Amsterdam, the Triton DNS and connect times, `mtr` to Jito), with the expected values and fail thresholds in its table.
Keep `~/latency-day1.txt`; fra1's was never saved. Cancel the box if it fails.

### 6.2 Install (on the box, as the ops user)

```bash
cd ~ && git clone https://github.com/xin10ylop/copy1 rugsnipe && cd rugsnipe && git checkout claude/affectionate-allen-nrv6o7
git config core.hooksPath .githooks
bash deploy/install.sh --role hot --dry-run | tail -20
sudo bash deploy/install.sh --role hot
sudo /opt/rugsnipe/bin/tune-hot.sh --apply && sudo systemctl enable rugsnipe-tune.service
cat /opt/rugsnipe/REVISION; chronyc tracking | grep -E 'System time|Reference'
```
What it should print: the dry run's planned actions, then the real install ending in the REVISION line with this
commit's hash and `role=hot`; `System time` under 1 ms against `ntp.frankfurt.jito.wtf`. The build takes 10-20 minutes
the first time (`cargo build --release --locked`).

### 6.3 Keys: copy the two files from the backup, never their contents

On your laptop (two hops through it; `OHIO` and `BOX` are the hosts):
```bash
scp -3 ubuntu@OHIO:/tmp/k/probe-keypair.json ubuntu@OHIO:/tmp/k/api-keys.toml ops@BOX:/tmp/
```
Before that, on Ohio, root copies them to a place `ubuntu` can read, and removes that copy right after:
```bash
sudo mkdir -p /tmp/k && sudo cp /root/fra1/etc/rugsnipe/keys/probe-keypair.json /root/fra1/etc/rugsnipe/keys/api-keys.toml /tmp/k/ && sudo chown ubuntu /tmp/k/* && sudo chmod 600 /tmp/k/*
# ... scp ...
sudo rm -rf /tmp/k
```
On the box:
```bash
sudo install -d -m 0700 /etc/rugsnipe/keys && sudo install -m 0400 -o root -g root /tmp/probe-keypair.json /tmp/api-keys.toml /etc/rugsnipe/keys/ && rm -f /tmp/probe-keypair.json /tmp/api-keys.toml
sudo nano /etc/rugsnipe/keys/api-keys.toml
```
In the editor, set these lines (values from the Triton portal's **backend** endpoint; every value in double quotes):
```toml
GRPC_TOKEN = "<the token part of the backend URL, after the last />"
GRPC_B_TOKEN = "<the same token>"
DESHRED_TOKEN = "<the same token>"
TRITON_URL = "https://<endpoint>.mainnet.rpcpool.com/<token>"
RPC_URL = "https://<endpoint>.mainnet.rpcpool.com/<token>"
```
Keep `HELIUS_KEY`, `NOZOMI_KEY`, `ASTRALANE_KEY`, `BLOCKRAZOR_KEY`, `TG_TOKEN`, `TG_CHAT` as they were. Then
`sudo chmod 0400 /etc/rugsnipe/keys/*`. The probe wallet is the old one, `4g49xGbgHZk3QYR1o6QSfDUbHmJZFwN6iDp6Vco1skff`
(emptied Oct 27, its token accounts closed). **The Triton token was pasted in a chat on Oct 28: rotate it in the
portal once the box is stable, then update these lines.**

### 6.4 The ArmSet (on Ohio, where the signing key is), stage b at 0.5 SOL

```bash
cd ~/rugsnipe && git fetch -q origin claude/affectionate-allen-nrv6o7 && git checkout -q claude/affectionate-allen-nrv6o7 && git pull -q
sudo rm -rf /tmp/armset-copy-b
python3 -I analysis/scripts/make_paper_armset.py --kind class --ver 201 --probe-allowed --probe-stage b --size-sol 0.5 --valid-hours 360 --out /tmp/copy-b.json
sudo /opt/rugsnipe/bin/rugsnipe-ctl armset sign --key /etc/rugsnipe/keys/armset-signing.key --in /tmp/copy-b.json --out-dir /tmp/armset-copy-b
ls /tmp/armset-copy-b/
```
What it should print: `valid 360 h (until <15 days ahead>)`, then `ver 201 sha256 <64 hex> signer <pubkey> ...
probe_allowed=true`, and two files `armset-201-SHA.json` and `.json.sig`. Write the SHA down. Copy the two files to
the box (`scp -3` through the laptop as above) into `/var/lib/rugsnipe/armsets/` with
`sudo install -m 0640 -o rugsnipe -g rugsnipe`. The signer pubkey printed here is `[secrets] armset_pubkey` below.
(If Ohio's `rugsnipe-ctl` is older than this commit, `sudo bash deploy/install.sh --role analytics` first.)

### 6.5 The config

```bash
sudo install -m 0640 -o root -g rugsnipe /opt/rugsnipe/src/config/copy-him.example.toml /etc/rugsnipe/rugsnipe.toml
sudo nano /etc/rugsnipe/rugsnipe.toml      # armset_pubkey, cold_wallet (your Phantom 4ZLrCvjc...), grpc.url (https://<endpoint>.mainnet.rpcpool.com)
sudo /opt/rugsnipe/bin/rugsnipe-ctl config validate /etc/rugsnipe/rugsnipe.toml --armset /var/lib/rugsnipe/armsets/armset-201-SHA.json --clock-offset-ms 0.05 --post-exec-healthy
```
What it should print: `armset: ArmSet ver 201 ... probe_allowed=true probe_stage=b`, then exactly two REFUSED lines,
`credential "probe-keypair" missing` and `credential "api-keys" missing` (the known false alarm of this check; the dry
run of 6.8 is the real one). Any other REFUSED line: stop and paste it.

### 6.6 Nonces (0.042 SOL of rent for 32 buy and 8 sell accounts) and funding

Send **2.5 SOL** from Phantom to `4g49xGbgHZk3QYR1o6QSfDUbHmJZFwN6iDp6Vco1skff` first (0.5 x 2 open copies, the
0.1 floor, the nonce rent, tips, and room for the 1 SOL daily stop). Then:
```bash
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 32 --dry-run | tail -3
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 32 | tail -2
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 8 --pool sell | tail -2
```
What it should print: the dry run's `would create` rows and `DRY RUN: nothing was signed or sent`; then
`done: created 32, existed 0, failed 0` and `done: created 8, existed 0, failed 0`. **Never start the hot unit before
both say done** (docs/08 §9 step 3c: a missing pool account is quarantined for good).

### 6.7 The operator table and the copy counter's seed (hot unit NOT running)

```bash
sudo systemctl start rugsnipe-operators.service; sudo journalctl -u rugsnipe-operators -n 12 --no-pager
sudo python3 -I -c 'import json;d=json.load(open("/etc/rugsnipe/operators.json"));print(len(d),"signers in the table")'
sudo python3 -I -c 'import json;d=json.load(open("/var/lib/rugsnipe/copy_signers.json"));print(len(d),"signers,",sum(len(v) for v in d.values()),"of his launch buys,",sum(1 for v in d.values() if len(v)>=2),"signers with 2+")'
```
What it should print: the refresh's lines `(a) ... landed trades`, `(b) ... round trips`, `wrote N signers`, and
`copy seed: N signers, M of its launch buys ... -> /var/lib/rugsnipe/copy_signers.json`; then the two counts. The
table needs 20 round trips in his last 24 h (he does 400-600 a day). If the service fails, paste its journal.

### 6.8 The feed race, the Jito relay, the dry run, the start

- **The feed race** (box study §6 step B): with `[feeds]` carrying `grpc` = your endpoint, `grpc_b` = Riptide
  (`https://riptide.rpcpool.com`, `x_token = "GRPC_B_TOKEN"`) and `deshred` = Riptide (`DESHRED_TOKEN`), run the
  paper dry run for 2 hours, then
  `sudo journalctl -u rugsnipe-hot --since -2h --no-pager | grep -A 12 '"first_seen"' | tail -14`. Expect `first_by`
  to name the feed that wins most creates and `grpc_behind_shreds` p50 near 6 ms. Keep the winner as `grpc`, turn
  `grpc_b` off for the real run, keep `deshred` on. If `shreds` is not ahead, Deshred is not enabled on the account
  (a Triton ticket).
- **Jito relay**: the four install lines at the top of `deploy/nginx/jito-relay.conf`, then its curl check.
- Then docs/08 §9 steps 5 (dry run), 6a (no stray tokens in the wallet), 6b (the hot unit's drop-in with `--armset
  /var/lib/rugsnipe/armsets/armset-201-SHA.json --rpc-url cred:RPC_URL`), 6c (`install.sh --role hot --probe-armset
  ...`, enable guard, hot and the target), 6d (`sudo systemctl start rugsnipe.target`). Then:
```bash
cp ~/rugsnipe/deploy/bin/rugsnipe-check ~/check.sh && bash ~/check.sh start && bash ~/check.sh
```
What it should print: `TRADING: yes`, the wallet line, `buys: copies of his buys only (entry.rule_buys = false)`,
and the copy line `copy on (this process): his launch buys N  not copied: tip under 2M ..., operator not listed ...,
operator he bought < 2 times in 24 h ...` (the `< 2` must read 2). Paste the first `bash ~/check.sh` back.

### 6.9 The first week's rules

- `bash ~/check.sh` every few hours and `bash ~/check.sh him` once a day; paste them. The new line under "results
  since the start" explains the wallet change; its WARNING means SOL left the wallet outside trades: stop and paste.
- **The bid**: the TIP TEST decides. Keep 1.5M only if it lands no farther behind him (d_avg) and nets more per copy
  than 3.0M; else set `ab_by_tier = []` and run 3.0M alone.
- **The stake stays 0.5** until a week's copies are positive on the curve without their best 2 (the §3 rule). Then
  1.0 SOL needs a new ArmSet (`--size-sol 1.0`), `max_probe_lamports = 1_000_000_000` in `[risk]` and `[probe] b`,
  `stake_by_tier = [1_000_000_000, ...]`, and about 4 SOL in the wallet.
- **The daily stop** (1 SOL) now stops his copies alone. If it latches on a day he loses, that is the stop doing its
  job: unkill the next day (06-infrastructure §4), do not raise it.
- Any `CRITICAL` in the journal (`sudo journalctl -u rugsnipe-hot | grep CRITICAL`): a sell that gave up; it is
  placed again every ~10 minutes, and the coin's token account still holds the tokens. Paste the lines.
- **Stop the test** after 7 days or 500 copies, whichever first, and read it the way §2 reads the last one: curve
  against fixed cost, by bid, by day, without the best 2.

## 7. Open questions

- **The box's live config** (§6.0 settles `copy_signer_min_buys`, the split and the sell tips): until it is pasted,
  the code review's readings of them are inferences from the paste.
- **His 4-8M tips**: about zero over 5 days, -1.44 live in two bursts. Noise or a change in who bids 4-8M? The next
  window's bucket split answers it.
- **His create + 1 buys copied in his own slot** lost live and in the model's Oct 24-25. A copy cannot see his slot
  before it sends; whether the create + 0 / + 1 split holds over more days is for the next window.
- **Triton Preconfs**: the only untested way to land closer. A one-day log (~$95) before any code.
- **Landing**: 31% of copies land a slot after him; a bigger tip did not change that. Deshred-triggered copies would
  copy his failed guards unless the bot predicts his guard from the pre-execution curve (box study §5, item 2).
- **The bid key** (tip + priority >= 2M) is closed: his result on those coins is strong (§1), the copy's is not (C9).
- **His dev wallet 4yN2vFSi** deployed something on Oct 22. If his pattern changes (a new program in his transactions,
  a third guard, a new relay), `bash ~/check.sh him` shows his failed-transaction count and tips first.

## 8. Sources

- [`05-live/check-sh-2026-10-27.txt`](../05-live/check-sh-2026-10-27.txt), parsed by
  `analysis/research/2026-10-28/live_decomp/live_decomp.py` (§2).
- [`code-review-2026-10-28.md`](code-review-2026-10-28.md) (§3, §4: Q1-Q8).
- [`../analysis/research/2026-10-28/copy_relook/report.md`](../analysis/research/2026-10-28/copy_relook/report.md)
  and its scripts and logs (§2 reconciliation, §3: A, B, C1-C8).
- [`../06-infrastructure/box-and-feed-2026-10-28.md`](../06-infrastructure/box-and-feed-2026-10-28.md) (§5, §6.1,
  §6.8).
- [`../03-strategies/S6-copy-him.md`](../03-strategies/S6-copy-him.md), [`../02-his-rules/README.md`](../02-his-rules/README.md),
  docs/17 §9-§10, docs/19 §9-§10 (the rules as they ran).
- [`../analysis/research/2026-10-28/onchain/report.md`](../analysis/research/2026-10-28/onchain/report.md) and its
  scripts (§1, §7).
- `docs/08-runbook.md` §9 (the probe steps this runbook follows), `docs/07-deploy.md` §5-§6.
- The refresh script's log of Oct 28 15:03 UTC (§1), run from this session's container against the owner's Triton
  endpoint.
