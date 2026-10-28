# One more hop at both ends of his 2025 episode: B8djRJNX (paid 2vQv4MSo -> 49Fr9YPN -> him) and AJsaFJJg (got his
# 24.08 SOL via Hr9ejPfd); also 973AR4f9 (Gj9srqLh's big outflow). Activity size, balance, sample of counterparties.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M", time.gmtime(bt))
full = {}
for f in ("B8djRJNX", "AJsaFJJg", "973AR4f9"):
    pass
# resolve full addresses from cached txs
need = {"B8djRJNX": ("2vQv4MSouYFdzBhPwGZJ3LhS5amLX9Rk3ucqvxNY5d4b", True), "AJsaFJJg": ("Hr9ejPfdkTWP2Qp6B9EkhTr694BTgz62rafsCvdQpcH1", False), "973AR4f9": ("Gj9srqLhRMtmasG1zxbHdw86ymDHdmVEvCV3Cs9SYBWy", False)}
for pre, (via, inbound) in need.items():
    s = R.rpc("getSignaturesForAddress", [via, {"limit": 1000}], cache=True)
    for x in s:
        t = R.rpc("getTransaction", [x["signature"], R.TXO1], cache=True)
        ks = t["transaction"]["message"]["accountKeys"]
        hit = [k for k in ks if k.startswith(pre)]
        if hit: full[pre] = hit[0]; break
for pre, a in full.items():
    s = R.rpc("getSignaturesForAddress", [a, {"limit": 1000}], cache=True)
    bal = R.rpc("getBalance", [a], cache=True)["value"]
    sel = [x["signature"] for x in s[:: max(1, len(s) // 12)]][:12]
    cps = collections.Counter(); progs = collections.Counter(); own = 0
    for t in R.txs1(sel):
        if not t: continue
        c = P.compact_any(t, a); own += c["payer"] == a; progs.update(p[:8] for p in c["progs"])
        for s_, d, l, inner, k in c["xf"]:
            if not inner and l: cps[(s_ if d == a else d)[:8]] += 1
    print(f"{pre}: {a} sigs(newest page) {len(s)}{'+' if len(s) == 1000 else ''} span {ts(s[-1]['blockTime'])} .. {ts(s[0]['blockTime'])} bal {bal/1e9:.3f} | sample {len(sel)} own-signed {own} programs {progs.most_common(5)} counterparties {len(cps)}")
print("calls", R.flush_count())
