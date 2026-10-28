# C7. The 5-day copy by his tip bucket (2-4M / 4-8M = his 4.8-7.2M steps / 8M+; the size-key copies under 2M apart)
# and by his size bucket (< 0.7 / 0.7-1.1 / 1.1-2 / 2+ SOL): net, P1 / P2, without the best 2, by day (2M copy set,
# 0.5 SOL, live 3M costs). Then: is the live result in each bucket (check.sh him table, filled copies, live_rows.json)
# within the 5-day spread? A bootstrap draws the live number of filled copies from the bucket's 5-day filled landings
# (a random copy, then a random filled landing of it), each at the live mean fixed cost of 0.00705 a fill (0.8817 over
# 125 fills, both bids), 20,000 times: the share of draws at or below the live result.
# python3 -I c7_buckets.py <live_rows.json>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
FIX = fixed_of(3.0); LIVE_FIX = 0.8817 / 125
LR = [x for x in json.load(open(sys.argv[1])) if x["bot"] == "COPIED" and x.get("result") == "filled"]
def tip4(t): return "size key <2M" if t < 2e6 else "2-4M" if t < 4e6 else "4-8M" if t < 8e6 else "8M+"
def size4(s): return "<0.7" if s < 0.7 else "0.7-1.1" if s < 1.1 else "1.1-2" if s < 2.0 else "2+"
rng = random.Random(5)
for name, kf, lk in (("his tip", lambda r: tip4(r["tip"]), lambda x: tip4(x["tip"] * 1e6)),
                     ("his size", lambda r: size4(r["sol"]), lambda x: size4(x["sol"]))):
    print(f"\n== by {name}")
    groups = collections.defaultdict(list)
    for r in LIVE2: groups[kf(r)].append(r)
    for g in sorted(groups):
        sel = groups[g]
        it = [(r, value(r, 0.5, FIX, REF_LIVE)) for r in sel]; it = [(r, v) for r, v in it if v]
        t = line(f"{g} (his net {sum(r['his'] for r in sel):+.2f})", it)
        pool = []
        for r in sel:
            fl = [c for k, c in legs(r, 0.5) if k == "fill"]
            if fl: pool.append(fl)
        lv = [x for x in LR if lk(x) == g]
        if not lv or not pool: continue
        n = len(lv); real = sum(x["ours"] for x in lv)
        sims = sorted(sum(rng.choice(rng.choice(pool)) - LIVE_FIX for _ in range(n)) for _ in range(20000))
        p_le = sum(1 for s in sims if s <= real) / len(sims)
        mean5 = sum(sum(p) / len(p) for p in pool) / len(pool) - LIVE_FIX
        print(f"      live: {n} filled, net {real:+.3f} ({real / n:+.4f} a fill; his {sum(x['its'] for x in lv):+.3f});  5-day filled landings: {mean5:+.4f} a fill at the live cost; "
              f"draws of {n}: median {sims[len(sims) // 2]:+.3f}, 5-95% {sims[len(sims) // 20]:+.3f} .. {sims[19 * len(sims) // 20]:+.3f}; share <= live {p_le:.3f}")
