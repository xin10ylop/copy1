import json, collections, struct, os, time
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
rows = [json.loads(l) for l in open(W + "/data/rows.jsonl")]
rec = [r for r in rows if r["bt"] >= 1792800000]
TIPS = json.load(open(W + "/ds/rivalpnl/tip_accounts.json"))
c = collections.Counter(); gl = collections.Counter(); gs = collections.Counter(); tipdest = collections.Counter(); errs = collections.Counter()
for r in rec:
    k = ("buy" if any(p.startswith("buy") for p in r["pix"]) else "sell" if any(p.startswith("sell") for p in r["pix"]) else "other", bool(r["err"]))
    c[k] += 1
    if r["g_slot"]: gl[(k, len(r["g_slot"]) // 2)] += 1
    if r["g_state"]: gs[(k, len(r["g_state"]) // 2)] += 1
    for d, l in r["tipto"].items(): tipdest[(TIPS.get(d, "UNKNOWN:" + d[:8]))] += 1
    if r["err"]: errs[(k[0], r["err"][:60])] += 1
print(c); print("slot guard sizes", gl); print("state guard sizes", gs); print("tip dest", tipdest.most_common(30)); print(errs.most_common(12))
# guard semantics on landed buys
ex = 0
for r in rec:
    if r["err"] or not any(p.startswith("buy") for p in r["pix"]) or not r["g_slot"]: continue
    b = bytes.fromhex(r["g_slot"]); a = [struct.unpack_from("<Q", b, o)[0] for o in range(0, len(b) - 7, 8)]
    s = bytes.fromhex(r["g_state"]) if r["g_state"] else b""; sa = [struct.unpack_from("<Q", s, o)[0] for o in range(0, len(s) - 7, 8)]
    mine = [e for e in r["tr"] if e["user"] == HIM]
    if ex < 4: print("buy slot", r["s"], "slot guard", a, "state guard", sa, "trade", {k: mine[0][k] for k in ("sol", "tok", "vsol", "vtok", "rtok")} if mine else None, "tip", r["tip"], "cup", r["cup"], "cul", r["cul"], "fee", r["fee"], "d", r["d"], r["pix"], r.get("buyargs")); ex += 1
