# The 100 accounts he funded with 0.00105664 SOL on Sep 12 and Sep 15: what are they (getAccountInfo), and are their
# recent transactions his own? Plus the other counterparties active since Oct 17.
import sys, os, json, time, base64, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
F = json.load(open(os.path.join(R.W, "data", "flows.json"))); I = json.load(open(os.path.join(R.W, "data", "cp_now.json")))
small = sorted({f[3] for f in F["flows"] if f[2] == "out" and f[4] == 1056640})
print("accounts funded with exactly 1,056,640 lamports:", len(small), "kinds", collections.Counter(f[7] for f in F["flows"] if f[2] == "out" and f[4] == 1056640))
a = small[0]
ai = R.rpc("getAccountInfo", [a, {"encoding": "base64"}], cache=True)["value"]
d = base64.b64decode(ai["data"][0])
print("example", a, "owner", ai["owner"], "lamports", ai["lamports"], "data len", len(d), "space", ai.get("space"))
if len(d) == 80:
    ver, state = int.from_bytes(d[0:4], "little"), int.from_bytes(d[4:8], "little")
    import parse as P
    print("  nonce version", ver, "state", state, "authority", P.b58e(d[8:40]), "fee lamports/sig", int.from_bytes(d[72:80], "little"))
his = {x["signature"] for x in json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))}
s = R.rpc("getSignaturesForAddress", [a, {"limit": 100}], cache=True)
print("its newest 100 sigs:", len(s), "of them in his signature list:", sum(1 for x in s if x["signature"] in his), "newest", time.strftime("%m-%d %H:%M:%S", time.gmtime(s[0]["blockTime"])), "oldest", time.strftime("%m-%d %H:%M:%S", time.gmtime(s[-1]["blockTime"])))
# how many of his recent txs carry one of these accounts?
rows = [json.loads(l) for l in open(os.path.join(R.W, "data", "rows.jsonl"))]
ks_hit = 0; n = 0
for r in rows:
    if r["bt"] < 1792800000 or r["payer"] != HIM: continue
    n += 1
    t = R.gettx(r["sig"]); m = t["transaction"]["message"]; la = t["meta"].get("loadedAddresses") or {}
    ks = set(m["accountKeys"] + la.get("writable", []) + la.get("readonly", []))
    if ks & set(small): ks_hit += 1
print("his own txs since Oct 24:", n, "that include one of the 100 accounts:", ks_hit)
other = [(k, v) for k, v in I.items() if v["last_bt"] and v["last_bt"] >= 1792195200 and k not in small]
for k, v in other:
    c = F["cp"][k]
    print("other active:", k, time.strftime("%m-%d %H:%M", time.gmtime(v["last_bt"])), "bal", v["lamports"] / 1e9, "owner", v["owner"], "in", c["in_n"], round(c["in_l"] / 1e9, 4), "out", c["out_n"], round(c["out_l"] / 1e9, 4), time.strftime("%Y-%m-%d", time.gmtime(c["first"])))
print("calls", R.flush_count())
