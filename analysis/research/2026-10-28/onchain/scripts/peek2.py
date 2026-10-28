import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
for s in sys.argv[1:]:
    S = json.load(open(os.path.join(R.W, "data", "sigs_AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2.json")))
    full = next(x["signature"] for x in S if x["signature"].startswith(s))
    t = R.gettx(full); m = t["transaction"]["message"]; meta = t["meta"]
    la = meta.get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    print("sig", full, "slot", t["slot"], "version", t.get("version"), "header", m["header"], "fee", meta["fee"])
    for i, k in enumerate(ks): print(i, k, meta["preBalances"][i] if i < len(meta["preBalances"]) else "", meta["postBalances"][i] - meta["preBalances"][i] if i < len(meta["postBalances"]) else "")
    print("ixs", [(ks[i["programIdIndex"]][:8], i.get("accounts"), i.get("data")[:60]) for i in m["instructions"]])
    print("inner", [[(ks[i["programIdIndex"]][:8], i.get("accounts"), i.get("data")[:40]) for i in g["instructions"]] for g in meta.get("innerInstructions") or []][:3])
    print("logs", (meta.get("logMessages") or [])[:30])
    print("tok", meta.get("preTokenBalances"), meta.get("postTokenBalances"))
