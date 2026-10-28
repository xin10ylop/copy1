# The Aug 25 - Sep 3 fleet now: the wallets that swept SOL to him (in >= 0.1 SOL) and the first hops he funded (out >= 0.1 SOL):
# account still open? balance? last activity? And what the last transaction of the few active after Oct 1 was.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
F = json.load(open(os.path.join(R.W, "data", "flows.json"))); I = json.load(open(os.path.join(R.W, "data", "cp_now.json")))
A, B = 1787616000, 1788480000   # 2026-08-25 .. 2026-09-04 UTC
sw = {f[3] for f in F["flows"] if f[2] == "in" and f[4] >= 1e8 and A <= f[0] < B}
hop = {f[3] for f in F["flows"] if f[2] == "out" and f[4] >= 1e8 and A <= f[0] < B}
ts = lambda bt: time.strftime("%Y-%m-%d", time.gmtime(bt)) if bt else "-"
for nm, S in (("sweepers (sent him SOL)", sw), ("first hops (he funded)", hop)):
    v = [I[a] for a in S]
    print(f"{nm}: {len(S)} wallets; open now {sum(1 for x in v if x['owner'])}; SOL held now {sum(x['lamports'] for x in v)/1e9:.4f}; last activity by month {sorted(collections.Counter(ts(x['last_bt'])[:7] for x in v).items())}")
    for a in S:
        x = I[a]
        if x["last_bt"] and x["last_bt"] >= 1790812800:
            t = R.rpc("getTransaction", [x["last_sig"], R.TXO1], cache=True); c = P.compact_any(t, a)
            print("   active after Oct 1:", a, ts(x["last_bt"]), "bal", x["lamports"] / 1e9, "last tx payer", c["payer"][:8], "programs", sorted(p[:8] for p in c["progs"]), "own pump trade", bool(c["my_trades"]),
                  "transfers", [(s[:8], d[:8], l) for s, d, l, i, k in c["xf"]][:3])
print("calls", R.flush_count())
