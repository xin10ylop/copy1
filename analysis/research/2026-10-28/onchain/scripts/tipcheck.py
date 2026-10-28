# Can a month row (pumpparse compact: tip = known tip accounts, xf = other System transfers incl. inner) give the full tip?
# Test the reconstruction on the recent rows where the exact top-level tip is known.
import json, collections, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
TIPS = json.load(open(W + "/ds/rivalpnl/tip_accounts.json"))
rows = [json.loads(l) for l in open(W + "/data/rows.jsonl")]
ok = bad = 0; ex = []
for r in rows:
    if r["bt"] < 1792800000 or r["err"] or not any(p.startswith("buy") for p in r["pix"]): continue
    mine = [e for e in r["tr"] if e["user"] == HIM and e["buy"]]
    if not mine: continue
    e = mine[0]; f = e.get("fee") or 0; amts = {e["sol"], f, e.get("cfee"), f // 2, f - f // 2}
    known = sum(l for s, d, l, inner, k in r["xf"] if s == HIM and k == 2 and d in TIPS)
    unk = sum(l for s, d, l, inner, k in r["xf"] if s == HIM and k == 2 and d not in TIPS and l not in amts)
    if known + unk == r["tip"]: ok += 1
    else:
        bad += 1
        if len(ex) < 5: ex.append((r["tip"], known, unk, [(d[:8], l, inner, k) for s, d, l, inner, k in r["xf"]], e["sol"], e.get("fee"), e.get("cfee")))
print("match", ok, "mismatch", bad); [print(x) for x in ex]
