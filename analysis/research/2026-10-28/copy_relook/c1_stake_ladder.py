# C1. Stake by his conviction. The 2M copy set (ablate.py's +8.02 rule), his slot at our measured D, 5% bound, H - 1,
# live costs at the 3.0M bid (0.0046 a filled copy, 0.000015 a refusal). Ladders keyed on his tip (2-4M / 4-8M / 8M+;
# his landed tips in 4-8M are 4.8-7.2M; the size-key copies under 2M take the first rung) or his size (< 1 / 1-2 / >= 2
# SOL). Picked on P1 (Oct 21-23), scored on P2 (Oct 24-25), each also without its best 2 copies. Capital = the most
# SOL in copies open at once (each copy holds its stake from his buy to our exit, refused or not: conservative).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
FIX = fixed_of(3.0)
def tip3(r): return 0 if r["tip"] < 4e6 else 1 if r["tip"] < 8e6 else 2
def size3(r): return 0 if r["sol"] < 1.0 else 1 if r["sol"] < 2.0 else 2
LADDERS = [("flat 0.5", lambda r: 0.5), ("flat 0.75", lambda r: 0.75), ("flat 1.0", lambda r: 1.0)]
for lad in ((0.5, 0.75, 1.0), (0.5, 1.0, 1.5), (0.25, 0.5, 1.0), (0.5, 0.5, 1.0), (1.0, 0.75, 0.5)):
    LADDERS.append((f"tip {lad[0]}/{lad[1]}/{lad[2]}", lambda r, lad=lad: lad[tip3(r)]))
for lad in ((0.5, 0.75, 1.0), (0.5, 1.0, 1.5), (0.5, 0.5, 1.0)):
    LADDERS.append((f"size {lad[0]}/{lad[1]}/{lad[2]}", lambda r, lad=lad: lad[size3(r)]))
cache = {}
def v_at(r, s):
    k = (r["m"], s)
    if k not in cache: cache[k] = value(r, s, FIX, REF_LIVE)
    return cache[k]
def capital(sel, f):
    ev = []
    for r in sel:
        ev.append((t_buy(r), f(r))); ev.append((t_exit(r), -f(r)))
    run = peak = 0.0
    for t, x in sorted(ev, key=lambda e: (e[0], e[1])):
        run += x; peak = max(peak, run)
    return peak
print("his tip buckets in the set:", dict(collections.Counter(tip3(r) for r in LIVE2)), " size buckets:", dict(collections.Counter(size3(r) for r in LIVE2)))
res = []
print(f"{'ladder':22} {'staked':>7} {'capital':>7}  results (SOL)")
for lab, f in LADDERS:
    it = [(r, v_at(r, f(r))) for r in LIVE2]; it = [(r, v) for r, v in it if v]
    staked = sum(f(r) for r, _ in it); cap = capital([r for r, _ in it], f); dd, _, low = intraday_dd(it)
    print(f"{lab:22} {staked:7.1f} {cap:7.2f}", end="")
    t = line("", it, extra=f"  intraday: worst drawdown {dd:+.2f}, lowest running day P&L {low:+.2f}  net per SOL of capital {sum(v['net'] for _, v in it) / cap:+.2f}")
    t.update(lab=lab, cap=cap, dd=dd, staked=staked); res.append(t)
best = max(res, key=lambda t: t["p1x"])
print(f"\npicked on P1 without its best 2: {best['lab']} (P1 {best['p1']:+.2f} [{best['p1x']:+.2f}]); scored on P2: {best['p2']:+.2f} [{best['p2x']:+.2f}]")
flat = next(t for t in res if t["lab"] == "flat 0.5")
print(f"against flat 0.5 on P2: {flat['p2']:+.2f} [{flat['p2x']:+.2f}]")
print("\nper SOL staked, by bucket (curve and net per copy at 0.5 SOL; P1 / P2):")
for name, key, labs in (("tip", tip3, ("2-4M (+ size-key < 2M)", "4-8M", "8M+")), ("size", size3, ("< 1", "1-2", ">= 2"))):
    for b in range(3):
        sel = [r for r in LIVE2 if key(r) == b]
        it = [(r, v_at(r, 0.5)) for r in sel]; it = [(r, v) for r, v in it if v]
        line(f"{name} {labs[b]}", it)
print("\nrisk with one landing per copy (the per-copy mean over 10 landings smooths it):")
for lab in ("flat 0.5", "flat 1.0", best["lab"], "tip 1.0/0.75/0.5", "size 0.5/1.0/1.5"):
    f = dict(LADDERS)[lab]
    print(f"   {lab:20} " + fmt_risk(sim_risk(LIVE2, f, FIX)))
