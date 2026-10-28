# live_decomp: the live copies of him, decomposed (Oct 28)

One script, no data fetch: it reads the check.sh paste of Oct 27 (`05-live/check-sh-2026-10-27.txt`, the `== 1 him`
table) and splits the 162 copies by bid, day, his tip, his size, landing slot and slots held, separating the curve
P&L from the tips and fees. Results in `07-restart/README.md` §2.

```
python3 -I analysis/research/2026-10-28/live_decomp/live_decomp.py
```

Headline: the 125 filled copies made +0.834 SOL on the curve and paid 0.882 in tips and fees (net -0.048). The 8.0M
arm paid 0.584 in fees on 61 fills for +0.098 on the curve; the 3.0M arm paid 0.298 on 64 fills for +0.736. The
stake was 0.5 SOL on 122 of 125 fills (median 0.499).
