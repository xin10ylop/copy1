# The wallets that funded him or traded SOL both ways with him: sample 60 of their transactions (spread over their
# newest 3,000 signatures) and tally their SOL counterparties and programs.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
HIM = P.HIM
F = json.load(open(os.path.join(R.W, "data", "flows.json"))); mine = set(F["cp"])
for a in sys.argv[1:]:
    s = []; before = None
    for _ in range(3):
        o = {"limit": 1000}
        if before: o["before"] = before
        page = R.rpc("getSignaturesForAddress", [a, o], cache=True) or []
        s += page
        if len(page) < 1000: break
        before = page[-1]["signature"]
    step = max(1, len(s) // 60); sel = [x["signature"] for x in s[::step]][:60]
    txs = []
    for i in range(0, len(sel), 50): txs += R.txs1(sel[i:i + 50])
    cin = collections.Counter(); cout = collections.Counter(); lin = collections.Counter(); lout = collections.Counter(); progs = collections.Counter(); payers = collections.Counter(); pump = 0
    for t in txs:
        if not t: continue
        c = P.compact_any(t, a); payers[c["payer"] == a] += 1
        progs.update(p[:8] for p in c["progs"]); pump += bool(c["my_trades"])
        for src, d, l, inner, k in c["xf"]:
            if inner: continue
            if d == a and src != a: cin[src] += 1; lin[src] += l
            if src == a and d != a: cout[d] += 1; lout[d] += l
    ts = lambda bt: time.strftime("%Y-%m-%d", time.gmtime(bt))
    print(f"== {a}: sigs {len(s)}{'+' if len(s) >= 3000 else ''} {ts(s[-1]['blockTime'])} .. {ts(s[0]['blockTime'])}; sampled {len(txs)}; signed by it {payers[True]}; own pump trades {pump}; programs {progs.most_common(6)}")
    print("   in from :", [(k[:8] + ("*" if k in mine else ""), v, round(lin[k] / 1e9, 3)) for k, v in cin.most_common(8)], "distinct", len(cin))
    print("   out to  :", [(k[:8] + ("*" if k in mine else ""), v, round(lout[k] / 1e9, 3)) for k, v in cout.most_common(8)], "distinct", len(cout))
print("(* = also a counterparty of his)  calls", R.flush_count())
