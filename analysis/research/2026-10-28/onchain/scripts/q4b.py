# Is the priority-fee part of his bid informative on other days? Per UTC day Oct 16 - Oct 28: his net on
# key buys (tip >= 2M or size >= 2 SOL), on non-key buys whose tip + priority >= 2M, and on the rest.
import json, os, sys, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
T24 = 1792800000; T16 = 1792108800
rows = [r for r in N.month() if T16 <= r["bt"] < T24] + [r for r in N.ours() if r["bt"] >= T24]
T = N.trips(rows); D = collections.defaultdict(list)
for t in T: D[time.strftime("%m-%d", time.gmtime(t["bt"]))].append(t)
key = lambda t: t["tip"] >= 2e6 or t["sol"] >= 2e9
prio_only = lambda t: not key(t) and t["tip"] + t["prio"] >= 2e6
print(f"{'day':5} {'key n':>5} {'key net':>8} | {'prio-only n':>11} {'net':>8} {'per buy':>8} | {'rest n':>6} {'net':>8} {'per buy':>8}")
tot = collections.defaultdict(float); cnt = collections.Counter(); pos = collections.Counter()
for d in sorted(D):
    G = D[d]; a = [t for t in G if key(t)]; b = [t for t in G if prio_only(t)]; c = [t for t in G if not key(t) and not prio_only(t)]
    for nm, s in (("key", a), ("prio", b), ("rest", c)):
        v = sum(t["pnl"] for t in s); tot[nm] += v; cnt[nm] += len(s); pos[nm] += v > 0
    print(f"{d:5} {len(a):5d} {sum(t['pnl'] for t in a):+8.3f} | {len(b):11d} {sum(t['pnl'] for t in b):+8.3f} {sum(t['pnl'] for t in b)/max(len(b),1):+8.4f} | {len(c):6d} {sum(t['pnl'] for t in c):+8.3f} {sum(t['pnl'] for t in c)/max(len(c),1):+8.4f}")
for nm in ("key", "prio", "rest"): print(f"total {nm}: {cnt[nm]} buys, {tot[nm]:+.3f} SOL, {tot[nm]/max(cnt[nm],1):+.4f} a buy, positive days {pos[nm]}/{len(D)}")
pr = collections.Counter(round(t["prio"] / 1e6, 1) for t in T if prio_only(t)); print("prio-only buys: priority fee (M) top", pr.most_common(8))
