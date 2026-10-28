# The 31 version-1 txs by DeFG8i8z (program BYdq7NJX) that carry his wallet read-only: which coins, and his trades on them.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
rows = [json.loads(l) for l in open(os.path.join(R.W, "data", "rows.jsonl"))]
mytr = collections.defaultdict(list)
for r in rows:
    for e in r["tr"]:
        if e["user"] == HIM: mytr[e["mint"]].append((r["s"], "buy" if e["buy"] else "sell"))
D = [r for r in rows if r["payer"].startswith("DeFG8i8z")]
c = collections.Counter()
for r in D:
    t = R.gettx(r["sig"]); m = t["transaction"]["message"]; meta = t["meta"]; la = meta.get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    mints = sorted({b["mint"] for b in (meta.get("preTokenBalances") or []) + (meta.get("postTokenBalances") or [])})
    owners = sorted({b["owner"] for b in (meta.get("preTokenBalances") or []) + (meta.get("postTokenBalances") or [])})
    hisacc = [b for b in (meta.get("postTokenBalances") or []) if b["owner"] == HIM]
    w = ks.index(HIM); writable = w < m["header"]["numRequiredSignatures"] or (w < len(m["accountKeys"]) and w < len(m["accountKeys"]) - m["header"]["numReadonlyUnsignedAccounts"])
    key = (tuple(mints), tuple(o[:8] for o in owners))
    c[key] += 1
    if c[key] == 1:
        print(time.strftime("%m-%d %H:%M:%S", time.gmtime(r["bt"])), r["s"], "mints", mints, "token owners", [o[:8] for o in owners], "his token accts", len(hisacc), "his writable", writable,
              "his trades on mint:", [(s - r["s"], k) for mi in mints for s, k in mytr.get(mi, [])][:6])
print(c)
s = R.rpc("getSignaturesForAddress", ["DeFG8i8zoJ3hN155nmvLq266ZVxWmNgRaTz5KQVHfe2S", {"limit": 1000}], cache=True)
print("DeFG8i8z newest 1000 sigs: span", time.strftime("%m-%d %H:%M", time.gmtime(s[-1]["blockTime"])), "-", time.strftime("%m-%d %H:%M", time.gmtime(s[0]["blockTime"])), "errs", sum(1 for x in s if x.get("err")))
b = R.rpc("getBalance", ["DeFG8i8zoJ3hN155nmvLq266ZVxWmNgRaTz5KQVHfe2S"], cache=True)
print("DeFG8i8z balance", b["value"] / 1e9)
print("calls", R.flush_count())
