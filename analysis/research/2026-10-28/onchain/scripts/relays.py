# Which relay landed each of his landed buys (the tip account), Oct 17-23 (month rows: known accounts by name, others by
# address prefix) against Oct 24-28; and how he splits his bid (tip vs priority fee) by relay.
import json, os, sys, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
TIPS = N.TIPS
def prov(d):
    if d in TIPS: return TIPS[d]
    for p, n in (("node1", "node1"), ("soyas", "soyas"), ("LandX", "landx"), ("Fa1con", "falcon"), ("noz", "nozomi"), ("astra", "astralane")):
        if d.startswith(p): return n
    if d in {"Eb2KpSC8uMt9GmzyAEm5Eb1AAAgTjRaXWFjKyFXHZxF3", "FCjUJZ1qozm1e8romw216qyfQMaaWKxWsuySnumVCCNe", "ENxTEjSQ1YabmUpXAdCgevnHQ9MHdLv8tzFiuiYJqa13", "6rYLG55Q9RpsPGvqdPNJs4z5WTxJVatMB8zV3WJhs5EK", "Cix2bHfqPcKcM233mzxbLk14kSggUUiz2A87fJtGivXr"}: return "0slot"
    return "other:" + d[:8]
REL = N.relays()
mon = [json.loads(l) for l in open(N.W + "/ds/month/AHwJSnFN.jsonl")]
A = collections.Counter(); AP = collections.defaultdict(list)
for r in mon:
    if r["bt"] < 1792195200 or r["bt"] >= 1792800000 or r["err"]: continue
    mine = [t for t in r["tr"] if t[1] == N.HIM and t[2]]
    if not mine: continue
    ds = [N.TIPS.get(k, k) for k in []]
    names = list(r["tips"].keys()) + [prov(d) for s, d, l in r["xf"] if s == N.HIM and d in REL and d not in TIPS]
    k = names[0] if names else "none"; A[k] += 1; AP[k].append((r["fee"] or 0) - 5000)
B = collections.Counter(); BP = collections.defaultdict(list)
for r in N.ours():
    if r["bt"] < 1792800000 or r["err"] or r["k"] != "buy" or not r["mine"]: continue
    k = prov(r["tipto"][0]) if r["tipto"] else "none"; B[k] += 1; BP[k].append(r["prio"])
na, nb = sum(A.values()), sum(B.values())
print(f"{'relay':18} {'Oct17-23':>9} {'%':>5} {'prio>0':>6} | {'Oct24-28':>9} {'%':>5} {'prio>0':>6}")
for k in sorted(set(A) | set(B), key=lambda k: -(A[k] + B[k])):
    print(f"{k:18} {A[k]:9d} {100*A[k]/na:5.1f} {100*sum(1 for p in AP[k] if p > 50000)/max(len(AP[k]),1):6.0f} | {B[k]:9d} {100*B[k]/nb:5.1f} {100*sum(1 for p in BP[k] if p > 50000)/max(len(BP[k]),1):6.0f}")
