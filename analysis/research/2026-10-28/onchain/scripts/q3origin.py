# Origins: the 2025 funding hop (49Fr9YPN <- 2vQv4MSo), the 2025 exit hop (Hr9ejPfd -> ?), where Gj9srqLh's SOL for him
# came from (the transaction before each of its transfers to him), and 4yN2vFSi's October activity.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
HIM = P.HIM
F = json.load(open(os.path.join(R.W, "data", "flows.json"))); mine = set(F["cp"])
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
def sigs(a, n=1000, **kw):
    o = {"limit": n}; o.update(kw); return R.rpc("getSignaturesForAddress", [a, o], cache=True) or []
def show(sig, who):
    t = R.rpc("getTransaction", [sig, R.TXO1], cache=True); c = P.compact_any(t, who)
    return c, [(s[:8], d[:8], round(l / 1e9, 4)) for s, d, l, inner, k in c["xf"] if not inner and l and l >= 1e6]
# 1. 2vQv4MSo
s = sigs("2vQv4MSouYFdzBhPwGZJ3LhS5amLX9Rk3ucqvxNY5d4b")
print("2vQv4MSo: newest-1000 span", ts(s[-1]["blockTime"]), "..", ts(s[0]["blockTime"]), "count", len(s), "balance", R.rpc("getBalance", ["2vQv4MSouYFdzBhPwGZJ3LhS5amLX9Rk3ucqvxNY5d4b"], cache=True)["value"] / 1e9)
for x in s[:3]: print("   ", ts(x["blockTime"]), show(x["signature"], "2vQv4MSouYFdzBhPwGZJ3LhS5amLX9Rk3ucqvxNY5d4b")[1][:4])
# 2. Hr9ejPfd forward
s = sigs("Hr9ejPfdkTWP2Qp6B9EkhTr694BTgz62rafsCvdQpcH1")
for x in s: print("Hr9ejPfd", ts(x["blockTime"]), show(x["signature"], "Hr9ejPfdkTWP2Qp6B9EkhTr694BTgz62rafsCvdQpcH1")[1][:4])
# 3. Gj9srqLh: before each transfer to him
G = "Gj9srqLhRMtmasG1zxbHdw86ymDHdmVEvCV3Cs9SYBWy"
for f in [f for f in F["flows"] if f[3] == G]:
    print("Gj9srqLh", f[2], ts(f[0]), f[4] / 1e9, "SOL")
    pv = sigs(G, 4, before=f[1])
    for x in pv:
        c, xs = show(x["signature"], G)
        if xs: print("     before:", ts(x["blockTime"]), "payer", c["payer"][:8], xs[:4])
# 4. 4yN2vFSi in October
Y = "4yN2vFSi9kFW2wwz5konV83QAao2rEJcpyTijgkh1Aea"
s = [x for x in sigs(Y) if x["blockTime"] >= 1790812800]   # since Oct 1
print("4yN2vFSi txs since Oct 1:", len(s))
cnt = collections.Counter()
for x in s[:40]:
    c, xs = show(x["signature"], Y)
    cnt[(c["payer"] == Y, tuple(sorted(p[:8] for p in c["progs"])))] += 1
    if len(xs): print("   ", ts(x["blockTime"]), "payer", c["payer"][:8], xs[:4])
print("  kinds:", cnt.most_common(6))
print("calls", R.flush_count())
