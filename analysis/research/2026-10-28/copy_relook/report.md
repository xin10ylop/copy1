# The copy of him (S6), re-run and extended: report (Oct 28)

Scripts: `copy_relook/` (run order in its README). Logs: `out/logs/`. Every number comes from one of those logs. The log
is named in each section. UTC unless stated; the live table is in Beirut time (UTC+2).
P1 = Oct 21-23, P2 = Oct 24-25 (to 16:07). [x] = without that period's best 2 copies. 0.5 SOL a copy unless stated.

## A. Reproduction: all match

| doc number | script (log) | reproduced |
|---|---|---|
| 2M key or size >= 2 SOL: +8.02 on 298; by day +1.53 +0.98 +5.24 +0.29 -0.02 | ablate.py (A_ablate) | +8.02, 298, +1.53 +0.98 +5.24 +0.29 -0.02 |
| stake 0.25 / 0.75 / 1.0: +2.50 / +8.83 / +12.05 | ablate.py | +2.50 / +8.83 / +12.05 (4M key, 232 copies, not the 2M set) |
| price limit 3% / 7.5% / 10% / none (4M key): +3.36 / +6.18 / +5.77 / +5.86 | ablate.py | same; 2M key at 7.5%: +8.37 (ablate2.py) |
| exit H / H-2 / +5 / +9 (4M key): +2.98 / +3.95 / +4.43 / +3.91; H-1 +5.64 | ablate.py | same |
| D = 0 / 10 / 90 / 150: +10.55 / +5.22 / +0.90 / +0.10 | S6 cites react_pos.py | printed by **scratch.py** (A_scratch). react_pos.py prints D = 1/5/20/50/...; its D=1 +10.276 and D=20 +4.160 agree |
| 558 copies +5.51; wider 10/15/none -1.05 / -1.79 / -2.07 | fails/prem5.py | +5.51; +4.46 / +3.72 / +3.44, so -1.05 / -1.79 / -2.07 |
| D=0 +11.97, D=10 +8.07, real +5.51 | fails/prem5b.py | +11.97, +8.07 |
| live rule +8.15 (299), without 8ZN71X +2.36; no rule +6.66 (575) | oprule/options.py | same (needed SP/oprule/arrival.py and op8zn.txt, which no archive holds; recreated) |
| landing closer: measured / 45 / 20 / 10 / 0 = +5.64 / +5.97 / +6.49 / +7.17 / +10.08 | tipworth.py | same |

The `ext` archive was needed: copyval.py, under every five/copy script, reads `SP/ext/replay/tables` and `out.jsonl`.

## B. Live against the backtest

**Live facts** (live_parse.py, B_live_parse):
- 125 fills. Stake median 0.499, mean 0.492 SOL; 7 under 0.45.
- Curve +0.8342, fees 0.8817, net -0.0475.

| bid | fills | fees a fill | fees - bid | curve | net | net a fill | his net on those coins |
|---|---|---|---|---|---|---|---|
| 3.0M | 64 | 0.00465 | 0.00165 | +0.7362 | +0.4387 | +0.0069 | +2.22 |
| 8.0M | 61 | 0.00958 | 0.00158 | +0.0980 | -0.4862 | -0.0080 | -0.19 |

**The stake x bid table** (recon.py §1, B_recon). These are the 2M set's 298 copies at our 5-day landing distances,
all in his slot. Fixed cost = bid + 0.0016 per fill (3M 0.0046, 8M 0.0096). Fills per copy 0.78.

| stake | curve | fixed 3M / 8M | net 3M | worst day | /copy | P2 [w/o best 2] | net 8M | worst day | /copy | P2 [w/o best 2] |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.25 | +4.39 | 1.07 / 2.23 | +3.32 | -0.06 | +0.0111 | -0.04 [-0.42] | +2.16 | -0.18 | +0.0073 | -0.33 [-0.71] |
| 0.30 | +5.28 | 1.07 / 2.23 | +4.21 | -0.06 | +0.0141 | +0.01 [-0.46] | +3.05 | -0.15 | +0.0102 | -0.28 [-0.74] |
| 0.50 | +8.84 | 1.07 / 2.23 | +7.77 | -0.04 | +0.0261 | +0.21 [-0.58] | +6.61 | -0.13 | +0.0222 | -0.09 [-0.87] |
| 0.75 | +13.35 | 1.07 / 2.23 | +12.28 | -0.02 | +0.0412 | +0.46 [-0.73] | +11.12 | -0.11 | +0.0373 | +0.16 [-1.02] |
| 1.00 | +17.92 | 1.07 / 2.23 | +16.85 | +0.00 | +0.0565 | +0.71 [-0.88] | +15.69 | -0.09 | +0.0526 | +0.42 [-1.17] |
| 1.50 | +27.24 | 1.07 / 2.23 | +26.17 | +0.05 | +0.0878 | +1.25 [-1.17] | +25.01 | -0.04 | +0.0839 | +0.95 [-1.46] |

- The fixed cost is the same at every stake, so the curve is the lever.
- The brief's 0.0045 / 0.0095 gives +4.23 / +3.07 at 0.3 SOL and +7.79 / +6.63 at 0.5.
- **Price impact, as the scripts model it.**
  - The curve is constant product. Our buy's tokens are q = t0 - k / (v0 + s_in).
  - Our tokens stay in the curve until the exit. The exit is the tape's state shifted by q: out = vr q / (tr - q), less 1.25% pump fee each way.
  - Others' token amounts are kept fixed, so traders behind us pay more SOL because of our buy, and our exit gets that back. This flatters bigger stakes.
  - With others' SOL fixed instead (`curve_solfixed`), 3M gives +3.23 / +7.39 / +15.33 / +22.79 at 0.25 / 0.5 / 1.0 / 1.5. The token-fixed model gives +3.32 / +7.77 / +16.85 / +26.17.
- **Without each period's best 2, P2 loses at every stake, and more at bigger stakes.**

**Where the copy lands** (recon.py; the live landings from refused/live.json + refused/tape, Oct 26 04:34 - Oct 27
00:22 UTC):
- 112 copies of him with a tape. 77 (69%) landed in his slot, a median 126 positions behind him (the backtest's D: median ~92). 33 landed in the next slot (median index 49), and 2 later.

| 5-day model, 3M costs | all 298 | his create + 0 (189) | his create + 1 (109) |
|---|---|---|---|
| his slot, backtest D | +7.77 [+4.84], P2 +0.21 | +4.48, P2 +0.43 | +3.29, P2 -0.22 |
| his slot, live positions | +7.66, P2 +0.20 | +4.41, P2 +0.44 | +3.26, P2 -0.24 |
| next slot, live positions (pessimistic for c+1) | +6.66, P2 +0.22 | +3.60, P2 +0.55 | +3.06, P2 -0.33 |

| live (filled) | n | our net | his net |
|---|---|---|---|
| landed in his slot | 86 | -0.4557 | +0.0056 |
| landed + 1 slot | 38 | +0.4101 | +1.9703 |
| his buy create + 0 | 76 | +0.3023 | +0.4821 |
| his buy create + 1 | 49 | -0.3498 | +1.5533 |
| his c+1, we landed in his slot | 33 | -0.5768 | +0.3560 |

The live losses were not on "+1 slot" fills. They were on his create + 1 buys copied in his own slot. The 5-day model
agrees on direction: his create + 1 copies lose on P2 (-0.22) and the create + 0 copies don't (+0.43).

**Step by step to the live setup** (recon.py §4):

| step | 5 days | P1 [w/o best 2] | P2 [w/o best 2] | curve / fill | net / fill | P2 curve / fill | P2 net / fill |
|---|---|---|---|---|---|---|---|
| ablate.py as published | +8.02 | +7.75 [+4.82] | +0.27 [-0.52] | +0.0381 | +0.0346 | +0.0081 | +0.0045 |
| + live fixed cost at 3M | +7.77 | +7.56 | +0.21 [-0.58] | +0.0381 | +0.0335 | +0.0081 | +0.0035 |
| + live landing (31% next slot) | +7.35 | +7.14 | +0.20 [-0.58] | +0.0377 | +0.0331 | +0.0083 | +0.0037 |
| + 16% of sells one slot late | +6.92 | +6.81 | +0.12 [-0.64] | +0.0357 | +0.0311 | +0.0067 | +0.0021 |
| + the live bid mix (0.00705 a fill) | +6.38 | +6.40 [+3.46] | -0.02 [-0.77] | +0.0357 | +0.0287 | **+0.0067** | **-0.0004** |
| **live, 125 fills** | -0.0475 | | | **+0.0067** | **-0.0004** | | |

**Calibration on real fills** (calib_live.py, B_calib_live):
- 50 fills of him (Oct 26 15:36 to Oct 27 01:32 Beirut) have our buy and sell on a live tape.
- Real curve +0.7663. The tape's own amounts give +0.7674.
- The model at our real entry and real sell slot reads +0.4751; at the backtest's landing, +0.4890.
- So the model is 0.0058 a fill **below** reality (0.0055 at the backtest's landing). By where we landed, the backtest-landing model is 0.0069 low on the 40 his-slot fills and +0.0001 on the 10 next-slot fills. It is not optimistic for him (unlike the 0.0155 a fill measured on wallet 4, docs/19 §13).

## C. New angles

**C1. Stake by his conviction** (c1_stake_ladder.py, 3M costs). Capital is the most SOL in copies open at once.

| ladder | 5 days [w/o best 2] | P1 [x] | P2 [x] | capital | worst intraday drawdown | lowest running day | net / SOL of capital |
|---|---|---|---|---|---|---|---|
| flat 0.5 | +7.77 [+4.84] | +7.56 [+4.64] | +0.21 [-0.58] | 1.00 | -0.86 | -0.20 | +7.77 |
| flat 1.0 | +16.85 [+10.90] | +16.14 [+10.19] | +0.71 [-0.88] | 2.00 | -1.65 | -0.23 | +8.42 |
| tip 0.5/0.75/1.0 | +12.47 [+9.43] | +12.01 [+8.97] | +0.46 [-1.14] | 1.75 | -1.76 | -0.36 | +7.13 |
| **tip 0.5/1.0/1.5 (P1 pick)** | +17.28 [+13.54] | +16.55 [+12.81] | **+0.73 [-1.69]** | 2.50 | -2.66 | -0.50 | +6.91 |
| tip 1.0/0.75/0.5 (reverse) | +12.14 [+6.20] | +11.68 [+5.74] | +0.46 [-0.46] | 2.00 | -0.78 | -0.17 | +6.07 |
| size 0.5/0.75/1.0 | +11.16 [+6.94] | +10.45 [+6.23] | +0.71 [-0.74] | 2.00 | -1.17 | -0.12 | +5.58 |
| size 0.5/1.0/1.5 | +14.61 [+9.07] | +13.39 [+7.85] | +1.22 [-0.89] | 3.00 | -1.48 | -0.13 | +4.87 |

- Tip buckets are 2-4M, 4-8M (his 4.8-7.2M steps) and 8M+. Size buckets are < 1, 1-2 and >= 2 SOL.
- At 0.5 SOL: tip 2-4M +3.73 [+0.80]; **4-8M +0.16 [-0.75]**; 8M+ +3.88 [+2.71]. Size < 1: +3.51; 1-2: +2.16; >= 2: +2.10 [+0.35].
- One landing per copy (300 draws) barely changes the risk, because the coin decides it: flat 0.5 has a worst intraday drawdown of -0.94.
- **Verdict:** no ladder beats flat out of sample without the best 2. A stake ladder only rescales P1's winners.

**C2. Exit by bucket** (c2_exit_bucket.py). His first sell comes a median 7 slots after the create in both buckets
(table H mostly 6 or 10).

| bucket | H | H-1 | H-2 | +5 | +7 | +9 | P1 pick -> P2 [x] | H-1 on P2 [x] |
|---|---|---|---|---|---|---|---|---|
| tip >= 8M (149) | +1.82 | **+3.88** | +2.76 | +3.63 | +2.98 | +2.43 | H-1 -> -0.07 [-0.85] | -0.07 [-0.85] |
| tip 2-8M (143) | +2.33 | **+2.47** | +2.16 | +1.14 | +1.38 | +2.07 | H-2 -> -0.08 [-0.17] | +0.29 [-0.10] |

- The per-bucket P1 picks together make +6.32 (P2 -0.17). H-1 everywhere makes +7.77 (P2 +0.21).
- Hot coins at +5 with the rest at H-1: +7.52. Hot coins at H-2: +6.65.
- **Verdict:** keep H-1 everywhere.

**C3. Sell timing** (c3_sell_late.py, calib_live.py):
- **Live sells with a fixed target** (JBokzLFR +5, CxyKYmQo +12, 3yrJE1A8 +29): of 100, 83 landed on target, 1 early, 14 one slot late and 2 two or more late. So **16% land late**.
- **His coins** (72 fills with a tape): 35 sold before his first sell's slot (+0.297), 14 a slot or more after it (-0.166), 1 in his slot before him, and 22 have no sell of his on the tape.
- **In the backtest, the H-1 sell is at or after his first sell on 20% of copies.**
- Every sell one slot late: +5.07 instead of +7.77 (-2.70, -0.0091 a copy; P2 -0.40). Two slots late: +3.60.
- At the measured 16%: +7.34 (-0.43).

**C4. Circuit breakers** (c4_breakers.py; 0.5 SOL, 3M costs; live = the real him table, 158 copies, -0.048):

| breaker | 5 days: skips, net change | live: skips, net change |
|---|---|---|
| (a) 3 losses >= 15% in a row, 60 min pause | 0, 0 | 11, **-0.350** |
| (b) 2 dumps >= 30% within 30 min, 60 min pause | 3, **+0.397** (all Oct 24) | 18, **-0.130** |
| (c) copies' day stop -0.5 | 0, 0 | 35, -0.130 |
| (c) copies' day stop -1.0 | 0, 0 | 32, **-0.648** |
| (d) operator out 3 h after a dump | 8, +0.027 | no operator in the table |

- Live, each pause forgoes the big winner that came right after the dumps: HQT8xbhA +0.706 at 03:59 Beirut.
- Clustering in the 5 days: 8 dumps in 233 fills. 3 had another dump within 30 min (shuffles: median 0, p 0.07). 5 fell on an operator with 2+ dumps (median 2, p 0.09).
- Clustering live: 8 dumps in 125 fills. 7 had another within 30 min (median 3, **p 0.015**): Oct 27 01:24-01:25 and 03:49-03:57 Beirut.
- **Verdict:** dumps cluster in time live. No breaker pays on both samples.

**C5. Refused and low-tip** (c5_refused_lowtip.py):
- **The second copy as specified** (tip >= 8M, refusal price <= his + 10%, lands at create + 1, bound + 10%, sold at + 5): 28 copies, 21.6 landings re-bought, **-0.08 [-0.49]**; P1 -0.19, P2 +0.11 [-0.20]. Sold at H-1 instead: -0.21.
- **The low-tip key as specified** (size >= 1.0 and tip >= 1.5M): **0 buys in the 5 days** with the operator rule. Without the rule there are 3 (-0.05 at 0.5, -0.08 at 1.0). Live there were 2 rows (his -0.018). His 1.5-1.8M-tip buys are 0.4-0.89 SOL in all but 3 cases.
- Wider: size >= 1.0 at any low tip (65 buys, his +2.54) makes -1.21 at 0.5 and -2.15 at 1.0. All 531 low-tip buys make -2.17 and -2.00.
- **Both lose. Stop.**

**C6. Operator rule** (c6_oprule.py; options.py's set at 3M costs):

| rule | n | 5 days [x] | by day | P2 [x] | without 8ZN71X |
|---|---|---|---|---|---|
| live: >= 2 in 24 h and in the table | 299 | +7.90 [+4.98] | +1.58 +0.92 +5.07 +0.36 -0.02 | +0.34 [-0.45] | +2.15 |
| count off (`copy_signer_min_buys = 0`), table kept | 399 | +7.96 [+5.03] | +2.05 +0.48 +5.18 +0.31 -0.07 | +0.24 [-0.55] | +2.20 |
| no count, no table | 575 | +6.19 [+3.27] | +1.00 -0.60 +4.99 +0.30 +0.50 | +0.80 [+0.02] | +0.44 |

- Rule on minus count off, by day: -0.48 +0.44 -0.11 +0.05 +0.05, total **-0.06**.
- Rule on minus no rule at all: +0.58 +1.52 +0.07 +0.06 -0.52, total +1.71.
- `copy_listed_only = true` live, so if the count was 0 (status line, line 46: "operator he bought < 0 times"), it cost about nothing.

**C7. By bucket, and is live noise?** (c7_buckets.py):
- The bootstrap draws the live number of fills from the bucket's 5-day filled landings, at the live 0.00705 a fill, independently.
- Live dumps clustered (C4), so this understates the tails.

| bucket | 5 days [x] | P2 | live fills, net | 5-day draws: median (5-95%) | share <= live |
|---|---|---|---|---|---|
| tip 2-4M | +2.31 [+0.41] | +0.08 | 32, +0.458 | +0.561 (-0.304 .. +3.571) | 0.457 |
| tip 4-8M | +0.16 [-0.75] | +0.21 | 41, **-1.437** | -0.033 (-0.822 .. +1.155) | **0.000** |
| tip 8M+ | +3.88 [+2.71] | -0.07 | 46, +1.402 | +1.439 (-0.045 .. +3.135) | 0.484 |
| size key, tip < 2M | +1.42 [-0.05] | -0.01 | 6, -0.470 | (pool of 6 coins) | 0.000 |
| size < 0.7 | -0.18 [-0.62] | -0.18 | 49, +0.910 | -0.221 | 0.994 |
| size 0.7-1.1 | +3.69 [+1.39] | -0.03 | 41, -0.079 | +1.275 | 0.065 |
| size 1.1-2 | +2.16 [+1.11] | -0.06 | 26, -0.369 | +1.077 | 0.031 |
| size 2+ | +2.10 [+0.35] | +0.48 | 9, -0.509 | +2.271 (pool of 11) | 0.000 |

- The brief's live "2-4M n38 -0.01" includes the 6 size-key copies under 2M. Split out: 2-4M is n 32 at +0.458, and the size key is n 6 at -0.470.
- The 4-8M bucket is about zero over the 5 days as well (+0.0010 a fill). Live it lost far beyond that, in two clustered bursts. Live small buys did better than the 5 days. The live misses go both ways.

**C8. The bid** (c8_bid.py):
- **Fixed cost per fill = bid + 0.0016:** 1.0M 0.0026, 1.5M 0.0031, 3.0M 0.0046, 8.0M 0.0096. Over the 5-day set's 232 fills: 0.60 / 0.72 / 1.07 / 2.23.
- **What the bid bought live** (his copies on the tapes):
  - 3.0M: 53 copies, 64% in his slot, a median 150.5 positions behind him.
  - 8.0M: 48 copies, 75% in his slot, a median 124 behind.
  - check.sh's TIP TEST says 156 against 149 d_avg.
- **The 5-day at-create fires by our tip** (positions after the create, share in the create slot): 1.0M 91.5 (61%), 1.5M 98 (70%), 3.0M 80 (63%), 6.0M 83 (64%). No clear effect.
- **Value of landing closer** (2M set, 3M costs): measured +7.77. Break-even extra tip a fill: D=45 +1.5M, D=20 +3.1M, D=10 +5.5M, D=0 +15.0M. Every decile 7 positions closer adds +0.08 (+0.35M a fill); 20 closer adds +0.15 (+0.62M a fill).

| bid, at its landing | 5 days [x] | P2 [x] |
|---|---|---|
| 3.0M at its live landing (36% next slot) | +7.30 [+4.37] | +0.22 [-0.56] |
| 8.0M at its live landing (25% next slot, ~26 closer) | **+6.29** [+3.38] | -0.08 [-0.85] |
| 1.0M at the 3M landing (assumed; not measured for copies) | +7.79 [+4.86] | +0.32 [-0.47] |
| 1.5M at the 3M landing (assumed) | +7.68 [+4.75] | +0.29 [-0.50] |

- **Verdict:** 8M doesn't earn back its extra 0.005 a fill: -1.01 over the 5 days (+6.29 against +7.30). That is 1.16 more in fixed cost against about 0.1 more curve. A lower bid is worth +0.3 to +0.4 over the 5 days if it lands the same; that has to be measured live (an A/B of 1.5M against 3.0M).

**C9. A key on his whole bid, tip + priority** (c9_bidkey.py, C9_bidkey log; 0.5 SOL, 3M costs, measured D, H-1, >= 2 in 24 h):
- His priority fee is the walk's transaction fee minus 5,000. It equals cu_price x cu_limit in bids.json on all 1,684 buys, and the on-chain agent's rows.jsonl on all 454 buys in both. No RPC call was needed.
- His buys that fail the tip key (tip < 2M, size < 2) number 531. 130 of them have tip + priority >= 2M; every one of those has a 1.0M tip and 1.4-29M priority.

| key | copies | 5 days [w/o best 2] | P1 [x] | P2 [x] | per copy | by day |
|---|---|---|---|---|---|---|
| tip >= 2M or size >= 2 (live) | 298 | **+7.77** [+4.84] | +7.56 [+4.64] | **+0.21** [-0.58] | +0.0261 | +1.50 +0.91 +5.16 +0.25 -0.04 |
| tip + priority >= 2M or size >= 2 | 428 | +6.94 [+4.01] | +7.38 [+4.45] | -0.44 [-1.23] | +0.0162 | +1.41 +1.15 +4.83 -0.24 -0.20 |
| tip + priority >= 3M | 372 | +6.50 [+3.58] | +6.98 [+4.05] | -0.48 [-1.26] | +0.0175 | +1.69 +0.91 +4.38 -0.28 -0.19 |
| tip + priority >= 4M | 331 | +4.57 [+2.64] | +5.07 [+3.14] | -0.50 [-1.29] | +0.0138 | +0.13 +0.38 +4.55 -0.27 -0.23 |
| tip + priority >= 6M | 276 | +4.89 [+2.96] | +5.57 [+3.63] | -0.68 [-1.46] | +0.0177 | +0.23 +0.68 +4.66 -0.43 -0.24 |
| **added alone at 2M** (bid key, not tip key) | 130 | **-0.83** [-1.41] | -0.18 [-0.74] | -0.65 [-1.01] | -0.0064 | -0.10 +0.24 -0.33 -0.49 -0.15 |
| added alone at 3M / 4M / 6M | 110 / 99 / 82 | -1.14 / -0.89 / -0.79 | | -0.62 / -0.62 / -0.57 | | |

- He made +3.73 on the 130 added buys (+0.029 a buy). The copy loses there on 4 of 5 days.
- A higher threshold also drops tip-key coins with low priority. At 4M it drops all 66 copies with 2-4M tips (+2.31).
- **Are the added copies the refused ones? No, they are a different set.** A coin is in one key or the other, so the added bucket shares no coin with the tip key's 76 copies that had a refused landing. Its refusal rate is about the same: 19% of landings, against 22%.
- **Verdict:** keep the tip key. The priority-paid bids are profitable for him (he lands them first) but not for a copy 90+ positions behind.

### C10. Day rules: a profit target, a trailing stop, hours of the day (asked Oct 28 evening)

`c10_day_rules.py`, `logs/C10_day_rules.txt`. The copies walked in buy order; a rule knows only the copies whose exit
came before the next buy (as C4). The 5-day 2M set at the restart's settings (1.0 SOL, the 1.5M bid) makes +17.20
(+3.23, +2.28, +10.88, +0.77, +0.03 by day); at the live settings (0.5, 3M) +7.77.

**(a) Stop the day at a profit target.** Every target loses, because the edge is in the tail of the good days.

| target (1.0 SOL) | copies skipped | forgone | 5 days become | one landing per copy, median [5-95%] |
|---|---|---|---|---|
| +0.5 | 203 | +11.34 | +5.86 | -11.42 [-14.58 .. -10.72] |
| +1.0 | 161 | +9.71 | +7.49 | -9.72 [-10.38 .. -9.04] |
| +1.5 | 122 | +9.24 | +7.95 | -9.43 |
| +2.0 | 118 | +8.42 | +8.78 | -8.38 |
| +3.0 | 52 | +7.36 | +9.84 | -7.34 |

At 0.5 SOL / 3M the +0.5 target forgoes +4.19 of +7.77. Oct 23 alone made +10.88 at 1.0 SOL, +4.16 of it in the 23
UTC hour; a +1 target keeps +1.01 of it. **Live** (check.sh's him table, 158 copies, -0.05: Oct 26 +0.37, Oct 27
-0.42) a +0.5 or +1.0 target would have added +0.43 / +0.70, because Oct 26 peaked at +1.07 and gave it back. That is
one day with no good tail; the 5 days say the tail is the whole result.

**(b) A trailing day stop** (stop the day once its realized P&L falls X below its peak): -0.19 at X = 1.0 (9 skips)
and -0.47 at X = 0.5 (57 skips) over 5 days; live +0.35 at 0.25 and +0.16 at 0.5. Within noise either way; not built
(the bot has the loss stop from zero, `max_daily_loss_lamports`, which C4 (c) already scored).

**(c) Hours.** By 4-hour UTC block (Beirut = +2), P1 / P2, without the best 2 in brackets:

| UTC block (Beirut) | n | P1 Oct 21-23 | P2 Oct 24-25 |
|---|---|---|---|
| 00-03 (02-05) | 55 | +1.31 [+0.47] | +0.51 [-0.17] |
| 04-07 (06-09) | 34 | +0.91 [+0.19] | -0.04 [-0.18] |
| 08-11 (10-13) | 24 | +1.09 [+0.18] | -0.30 [-0.52] |
| 12-15 (14-17) | 45 | +1.70 [+0.80] | +0.42 [-0.06] |
| 16-19 (18-21) | 58 | +1.64 [-0.23] | +0.22 [-0.80] |
| 20-23 (22-01) | 82 | +9.74 [+3.80] | +0.00 [-1.16] |

No block loses on P1, so there is no hour rule to pick; the block that made P1 (20-23 UTC, +9.74) made +0.00 on P2.
Skipping the 2 weakest P1 blocks (04-11 UTC) changes P2 by +0.34 on 21 copies: noise. His own buys run all day:
25-46 an hour at 07-11 UTC (09-13 Beirut), 70-152 an hour at 12-23 UTC. Live by Beirut hour, our net and his on the
same coins move together (01 and 03 Beirut: ours -0.67 / -0.62, his -1.77 / -2.23): the bad hours were his bad hours,
not a time of day.

**Verdict:** no profit target, no trailing stop, no trading hours. The one day rule stays the loss stop.

## What the owner should take from this

1. **The live result was not a broken backtest.** Rebuilt with the live costs, landing, sell latency and bids, the model's Oct 24-25 gives the same per-fill result as live (curve +0.0067, net -0.0004). The model is, if anything, low per fill on him (-0.0058). The +8.02 came from Oct 21-23 and a few coins (8ZN71X; without the best 2, P2 is -0.52).
2. **The stake multiplies the curve. It does not fix it.** Costs are fixed per fill, so a bigger stake helps when the curve is positive. Without the best 2, Oct 24-25 is negative at every stake, from -0.42 at 0.25 to -1.17 at 1.5. No conviction ladder holds out of sample.
3. **Drop the 8M bid.** It cost +1.16 over 5 days for about +0.1 of curve. Keep 3.0M, or A/B 1.5M.
4. **Nothing else passes:** exits by bucket, breakers, refused retries, low-tip copies, the operator count, a key on tip + priority (C9: the 130 coins it adds lose -0.83), and the day rules (C10: a +1 SOL day target forgoes +9.7 of +17.2 over 5 days at 1.0 SOL; no hour of the day holds out of sample). The live losses clustered in two bursts and in the 4-8M tips, where the 5-day copy was already about zero.
