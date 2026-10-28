# Where did the SOL he sent out (Aug 23 - Sep 3) go next, and where did the SOL he received come from just before?
#   out-recipients: the transaction right after his deposit (their forward), its System-transfer destinations.
#   in-senders: the transaction right before their sweep to him, its System-transfer sources into them.
import sys, os, json, time, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
HIM = P.HIM
F = json.load(open(os.path.join(R.W, "data", "flows.json")))
big = [f for f in F["flows"] if f[4] >= 1e9 and 1787443200 <= f[0] < 1788480000]   # >= 1 SOL, 2026-08-23 .. 2026-09-04
outs = [f for f in big if f[2] == "out"]; ins = [f for f in big if f[2] == "in"]
random.seed(7); so = random.sample(outs, min(60, len(outs))); si = random.sample(ins, min(60, len(ins)))
def around(addr, sig, after=True):
    # signatures of addr just newer (after=True) or just older than sig
    if after:
        page = R.rpc("getSignaturesForAddress", [addr, {"limit": 5, "until": sig}], cache=True) or []
        return page[-1]["signature"] if page else None
    page = R.rpc("getSignaturesForAddress", [addr, {"limit": 2, "before": sig}], cache=True) or []
    return page[0]["signature"] if page else None
fwd = collections.Counter(); fwd_amt = collections.defaultdict(int); fwd_ex = {}; delay = []
for f in so:
    nx = around(f[3], f[1], True)
    if not nx: fwd["(no later tx)"] += 1; continue
    t = R.rpc("getTransaction", [nx, R.TXO1], cache=True); c = P.compact_any(t, f[3])
    for s, d, l, inner, k in c["xf"]:
        if s == f[3] and l > 1e8: fwd[d] += 1; fwd_amt[d] += l; fwd_ex[d] = (f[4], l, c["bt"] - f[0])
    delay.append(c["bt"] - f[0])
print("out-recipients sampled", len(so), "| forward destinations:", len(fwd))
for d, n in fwd.most_common(12): print("   ", d, n, "x", round(fwd_amt[d] / 1e9, 3), "SOL; example (his deposit, forwarded, seconds later)", fwd_ex.get(d))
print("   delay deposit -> forward (s): median", sorted(delay)[len(delay) // 2] if delay else None, "min", min(delay) if delay else None, "max", max(delay) if delay else None)
src = collections.Counter(); src_ex = {}
for f in si:
    pv = around(f[3], f[1], False)
    if not pv: src["(no earlier tx)"] += 1; continue
    t = R.rpc("getTransaction", [pv, R.TXO1], cache=True); c = P.compact_any(t, f[3])
    got = [(s, l) for s, d, l, inner, k in c["xf"] if d == f[3] and s != f[3] and l > 1e7]
    kind = "pump trade" if c["my_trades"] else ("transfer in" if got else "other: " + ",".join(sorted(p[:8] for p in c["progs"])))
    src[kind if not got else "from " + got[0][0]] += 1; src_ex[kind] = pv
print("in-senders sampled", len(si), "| their tx just before the sweep to him:")
for k, n in src.most_common(15): print("   ", k, n)
print("calls", R.flush_count())
json.dump(dict(fwd=fwd.most_common(), src=src.most_common()), open(os.path.join(R.W, "data", "q3hops.json"), "w"))
