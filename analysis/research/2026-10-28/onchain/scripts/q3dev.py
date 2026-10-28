# 4yN2vFSi (funded by him on Aug 23, two-way transfers with him): its program deploys and the programs it calls;
# who else invokes those programs. Also 973AR4f9 (Gj9srqLh's outflow).
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
HIM = P.HIM; Y = "4yN2vFSi9kFW2wwz5konV83QAao2rEJcpyTijgkh1Aea"
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
s = R.rpc("getSignaturesForAddress", [Y, {"limit": 1000}], cache=True)
progs = collections.Counter(); deploy = []; other = collections.Counter(); allx = []
for i in range(0, len(s), 50):
    for x, t in zip(s[i:i + 50], R.txs1([y["signature"] for y in s[i:i + 50]])):
        if not t: continue
        m = t["transaction"]["message"]; la = t["meta"].get("loadedAddresses") or {}
        ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
        tops = {ks[ix["programIdIndex"]] for ix in m["instructions"]}
        for p in tops: progs[(p, ks[0] == Y)] += 1
        if "BPFLoaderUpgradeab1e11111111111111111111111" in tops: deploy.append((ts(t["blockTime"]), ks[0][:8], [k for k in ks[:8]]))
        c = P.compact_any(t, Y)
        allx.append((t["blockTime"], c["payer"], c["xf"], tops))
print("4yN2vFSi: all", len(s), "sigs read; top-level programs (program, signed by it):")
for (p, own), n in progs.most_common(25): print("   ", p, own, n)
print("deploy-related txs:", len(deploy))
for d in deploy[:12]: print("   ", d)
# SOL counterparties over all its txs (top-level transfers)
cin = collections.Counter(); cout = collections.Counter(); lin = collections.Counter(); lout = collections.Counter()
for bt, payer, xf, tops in allx:
    for a, b, l, inner, k in xf:
        if inner or not l: continue
        if b == Y and a != Y: cin[a] += 1; lin[a] += l
        if a == Y and b != Y: cout[b] += 1; lout[b] += l
print("in  (top 15 by SOL):", [(k[:8], cin[k], round(lin[k] / 1e9, 3)) for k, _ in lin.most_common(15)], "distinct", len(cin), "total", round(sum(lin.values()) / 1e9, 3))
print("out (top 15 by SOL):", [(k[:8], cout[k], round(lout[k] / 1e9, 3)) for k, _ in lout.most_common(15)], "distinct", len(cout), "total", round(sum(lout.values()) / 1e9, 3))
by_month = collections.Counter(ts(bt)[:7] for bt, *_ in allx); print("its txs by month:", sorted(by_month.items()))
json.dump(dict(progs=[[p, o, n] for (p, o), n in progs.items()], deploy=deploy), open(os.path.join(R.W, "data", "q3dev.json"), "w"))
print("calls", R.flush_count())
