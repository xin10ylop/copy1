# C2. The exit by his conviction bucket: his tip >= 8M (his hot coins) against 2-8M (and the size-key copies under 2M),
# on the 2M copy set, 0.5 SOL, live 3M costs. Exits: H - k (listed signers; unlisted: his modal first sell - k, as
# ablate.py), flat create + 5 / 7 / 9. Picked per bucket on P1 (Oct 21-23), scored on P2 (Oct 24-25), each without its
# best 2 copies too. A hold at or past his first sell sells right after it (exit_at, as every copy script).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
FIX = fixed_of(3.0)
def hk(k): return lambda r: (r["H"] - k) if r["listed"] else (hold(r) + 1 - k)
EXITS = [("H", hk(0)), ("H-1 (live)", hk(1)), ("H-2", hk(2)), ("H-3", hk(3)), ("+5", lambda r: 5), ("+7", lambda r: 7), ("+9", lambda r: 9)]
BK = [("tip >= 8M", lambda r: r["tip"] >= 8e6), ("tip 2-8M", lambda r: 2e6 <= r["tip"] < 8e6), ("size key, tip < 2M", lambda r: r["tip"] < 2e6)]
for lab, f in BK:
    sel = [r for r in LIVE2 if f(r)]
    so = [r["soff"] for r in sel if r["soff"] is not None]; Hs = [r["H"] for r in sel if r["listed"]]
    print(f"\n== {lab}: {len(sel)} copies; his first sell after the create: median {st.median(so) if so else None}, "
          f"{dict(sorted(collections.Counter(min(x, 15) for x in so).items()))}; table H (listed): {dict(sorted(collections.Counter(Hs).items()))}")
    res = []
    for el, hf in EXITS:
        t = line(f"exit {el}", [(r, value(r, 0.5, FIX, REF_LIVE, hold_fn=hf)) for r in sel]); t["lab"] = el; res.append(t)
    b = max(res, key=lambda t: t["p1x"]); live = next(t for t in res if t["lab"] == "H-1 (live)")
    print(f"   picked on P1 w/o best 2: {b['lab']} (P1 {b['p1']:+.2f} [{b['p1x']:+.2f}]) -> P2 {b['p2']:+.2f} [{b['p2x']:+.2f}];  H-1 on P2: {live['p2']:+.2f} [{live['p2x']:+.2f}]")
print("\n== combined: each bucket's P1 pick against H-1 everywhere")
picks = {}
for lab, f in BK:
    sel = [r for r in LIVE2 if f(r)]
    best = max(EXITS, key=lambda e: (lambda it: sum(v["net"] for r, v in it if r["day"] in P1) - sum(sorted([v["net"] for r, v in it if r["day"] in P1], reverse=True)[:2]))(
        [(r, value(r, 0.5, FIX, REF_LIVE, hold_fn=e[1])) for r in sel if value(r, 0.5, FIX, REF_LIVE, hold_fn=e[1])]))
    picks[lab] = best
print("   picks: " + ", ".join(f"{k}: {v[0]}" for k, v in picks.items()))
def comb(r):
    for lab, f in BK:
        if f(r): return picks[lab][1](r)
line("per-bucket P1 picks", [(r, value(r, 0.5, FIX, REF_LIVE, hold_fn=comb)) for r in LIVE2])
line("H-1 everywhere (live)", [(r, value(r, 0.5, FIX, REF_LIVE)) for r in LIVE2])
for a, b in (("+5", "H-1 (live)"), ("H-2", "H-1 (live)"), ("H-1 (live)", "+7"), ("H-1 (live)", "+9")):
    fa = dict(EXITS)[a]; fb = dict(EXITS)[b]
    line(f"hot (>= 8M) {a}, others {b}", [(r, value(r, 0.5, FIX, REF_LIVE, hold_fn=(fa if r["tip"] >= 8e6 else fb))) for r in LIVE2])
