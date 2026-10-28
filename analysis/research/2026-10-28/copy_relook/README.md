# The copy of him, re-run and extended before a restart (Oct 28)

The 5-day copy backtest (`2026-10-25/five/copy/`, `2026-10-26/fails/`, `2026-10-26/oprule/`) reproduced, set against
the live copies of Oct 26-27 (`05-live/check-sh-2026-10-27.txt`, "== 1 him"), and eight new questions for a
him-only restart. Every number below is printed by a script here; the logs are in the run's `OUT/logs/`.

Rules as in the repo: picked on P1 (Oct 21-23 UTC), scored on P2 (Oct 24-25 to 16:07); each also without its best 2
copies [in brackets]; every cost counted. The copy set is ablate.py's +8.02 one (his tip >= 2M or size >= 2 SOL,
>= 2 of his buys on the signer in 24 h, 5% bound, sold at H - 1), 298 copies, unless stated.

In the repo: `report.md` (every table) and `logs/` (the run of Oct 28 these numbers come from; `run_all.sh` writes a
fresh `OUT/logs/`). The curated reading is `07-restart/README.md` §2-§3.

## Run order

```
bash setup.sh /home/user/copy1            # unpack dec ext month fp full univ rivalpnl helpers oos refused fails hold; SP/oprule
bash run_all.sh /home/user/copy1 OUT      # about 30 s; every script below, logs in OUT/logs
```
- `ext` is needed after all: `copyval.py` (under every five/copy script) reads `SP/ext/replay/tables/` and `out.jsonl`.
- `oprule/options.py` reads `SP/oprule/arrival.py` and `SP/oprule/op8zn.txt`, which no archive holds. `setup.sh`
  copies `arrival.py` from the repo and writes 8ZN71X's address (the one `8ZN71X...` address in `data/operators/*.json`).
- `fails/prem5.py` opens `scratch.py` beside itself, `prem5b.py` opens `./scratch.py`: both run from `SP/dec/copy`
  (fails/README). The SP copies of the five/copy and fails scripts are byte-identical to the repo's.

| script | what it does |
|---|---|
| `base.py` | ablate.py's loaders (exec'd from SP/dec/copy), the P&L split into curve and fixed cost, live costs, P1/P2 lines, drawdowns, a second price-impact model, one-landing draws |
| `check_base.py` | base.py must give ablate.py's +8.02 on 298 copies with the model's costs (it does: +8.0161) |
| `live_parse.py` | the 377 rows of the live him table -> `live_rows.json`; stake, fees by bid, results by tip, size, slot, day |
| `recon.py` | Part B: stake x bid; landing slot by his buy slot; the live landings from the tapes (-> `live_landing.json`); the step-by-step reconciliation |
| `calib_live.py` | the model against 50 real fills on the live tapes (refused/tape); our sells against his first sell (-> `calib_live.json`) |
| `c1_stake_ladder.py` | C1 stake by his tip or size; capital, drawdowns |
| `c2_exit_bucket.py` | C2 exits by tip bucket |
| `c3_sell_late.py` | C3 how often our live sells land late; the backtest with late sells |
| `c4_breakers.py` | C4 four circuit breakers, 5-day and live; do dumps cluster |
| `c5_refused_lowtip.py` | C5 the second copy after a refusal (tip >= 8M, <= 10%, create + 1, + 5); the low-tip skips |
| `c6_oprule.py` | C6 the operator rule on and off at live costs, by day |
| `c7_buckets.py` | C7 the copy by his tip and size bucket; the live buckets against a bootstrap of the 5-day ones |
| `c8_bid.py` | C8 fixed cost by bid; what 3M and 8M bought live; the value of a landing distance |
| `c9_bidkey.py` | C9 the key on tip + priority (his priority = the walk's fee - 5,000) at 2/3/4/6M against the tip key; the added bucket by day; overlap with the refused coins |

## Costs and the model

- **Curve** = what the round trip returns minus the stake: the constant-product curve, our buy's own price impact, our
  tokens left in the curve until the exit (`out = vr q / (tr - q)`), pump's 1.25% each way. **Fixed** = buy tip +
  sell tip + priority + base fees, per filled copy. The scripts' model uses 0.00352. Live it was the bid + 0.0016
  (fees column: 3.0M 0.00465 on 64 fills, 8.0M 0.00958 on 61). A refused copy costs 0.000015 (live) instead of 0.0001.
- The model keeps the other traders' token amounts fixed, so the traders behind us pay more SOL because of our buy and
  our exit gets that back. That flatters a bigger stake. `curve_solfixed` keeps their SOL fixed instead (sensitivity).
- The backtest puts every copy in his slot, D positions behind him (D = our 5-day at-create landings, median ~92). Live,
  31% of our copies landed a slot or more later and the rest a median 126 behind him (`recon.py`).

## Results

**Part A: reproduced, every number** (`OUT/logs/A_*.txt`). Two notes. The D = 0/10/90/150 row (+10.55/+5.22/+0.90/+0.10)
is printed by `scratch.py` ("value by a FIXED landing distance D"), not by `react_pos.py`, which prints D = 1/5/20/...
with matching values at D = 1 and 20. The stake (+2.50/+8.83/+12.05), price-limit and exit rows of ablate.py are on the
4M key (232 copies), not the 2M one.

**Part B: the live break-even is what the backtest says for its own last two days.** Step by step to the live setup
(0.5 SOL): +8.02 -> live fixed costs +7.77 -> live landing +7.35 -> 16% of sells a slot late +6.92 -> the live bid mix
+6.38. That last setting on P2 alone: curve +0.0067 and net -0.0004 a fill. Live: curve +0.0067 and net -0.0004 a fill
(125 fills). The +8.02 is P1 (+7.75) and its best copies: P2 +0.27, -0.52 without its best 2. On 50 real fills the
model reads 0.0058 a fill *below* reality (`calib_live.py`), so the model is not optimistic per fill. The difference
is the period.

**C1-C8: nothing new passes out of sample.** Details and tables in report.md.
- Conviction ladders: best on P1 (tip 0.5/1.0/1.5) gives P2 +0.73 [-1.69], against flat 0.5's +0.21 [-0.58].
- Exits by bucket: the per-bucket P1 picks give P2 -0.17; H - 1 everywhere gives +0.21.
- Breakers: 0 to +0.40 over the 5 days, -0.13 to -0.65 live.
- The second copy after a refusal: -0.08 [-0.49].
- Low-tip copies lose, and the specified key (size >= 1.0 and tip >= 1.5M) has 0 buys in the 5 days.
- The operator count rule is worth -0.06 with the table kept.
- The mid-tip bucket (4-8M) is about zero over the 5 days: +0.16 [-0.75].
- 8M costs 1.16 SOL more than 3M over the 5 days and buys about +0.1 of curve.
- A key on tip + priority >= 2M adds 130 copies. They lose -0.83 [-1.41], P2 -0.65, and they are not the refused coins.
