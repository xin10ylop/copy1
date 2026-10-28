# The Oct 1 test wallets: read every transaction of the ones with <= 40 txs and 40 spread txs of the busier ones;
# count pump / token-program use and where their SOL went (top-level transfer destinations).
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P, norm as N
REL = N.relays()
Pf = json.load(open(os.path.join(R.W, "data", "prof_oct1.json")))
tot = collections.Counter(); dest = collections.Counter(); destl = collections.Counter(); n_tx = 0; memo = 0
for a, p in Pf.items():
    s = R.rpc("getSignaturesForAddress", [a, {"limit": 1000}], cache=True) or []
    if p.get("n", 0) > 1000:
        o = {"limit": 1000, "before": s[-1]["signature"]}; s += R.rpc("getSignaturesForAddress", [a, o], cache=True) or []
    sel = [x["signature"] for x in (s if len(s) <= 40 else s[:: max(1, len(s) // 40)])]
    for i in range(0, len(sel), 50):
        for t in R.txs1(sel[i:i + 50]):
            if not t: continue
            c = P.compact_any(t, a); n_tx += 1
            for pr in c["progs"]: tot[pr[:8]] += 1
            for s_, d, l, inner, k in c["xf"]:
                if s_ == a and not inner and d != a:
                    g = "relay tip account" if d in REL else ("him" if d == P.HIM else "other")
                    dest[g] += 1; destl[g] += l
print("Oct 1 wallets:", len(Pf), "txs read:", n_tx, "programs:", tot.most_common(10))
print("their outgoing top-level transfers:", {k: (dest[k], round(destl[k] / 1e9, 4)) for k in dest})
print("calls", R.flush_count())
