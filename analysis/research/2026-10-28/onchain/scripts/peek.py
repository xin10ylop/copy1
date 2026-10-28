import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
rec = [x for x in S if (x["blockTime"] or 0) >= 1792800000]
progs = collections.Counter(); progs_ok = collections.Counter(); ver = collections.Counter(); nsig = collections.Counter(); fp = collections.Counter()
for x in rec:
    t = R.gettx(x["signature"])
    if not t: continue
    m = t["transaction"]["message"]; la = t["meta"].get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    tops = tuple(sorted({ks[i["programIdIndex"]] for i in m["instructions"]}))
    progs[tops] += 1
    ver[str(t.get("version"))] += 1; nsig[m["header"]["numRequiredSignatures"]] += 1; fp[ks[0]] += 1
for k, v in progs.most_common(20): print(v, [p[:8] for p in k])
print(ver, nsig, fp)
x = next(x for x in rec if not x.get("err"))
t = R.gettx(x["signature"]); print(json.dumps(t)[:3000])
