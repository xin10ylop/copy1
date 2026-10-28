# Month rows (Sep 24 - Oct 24, pumpparse compact): which recurring System-transfer destinations from him in landed buys
# are relay tip accounts? Fee recipients get fee halves, creator vaults get cfee (+ 650,240 top-up), curves get `sol`.
import json, collections, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
TIPS = json.load(open(W + "/ds/rivalpnl/tip_accounts.json"))
rec = [json.loads(l) for l in open(W + "/data/rows.jsonl")]
rec_top = collections.Counter(d for r in rec for d in r["tipto"])
rows = [json.loads(l) for l in open(W + "/ds/month/AHwJSnFN.jsonl")]
dest = collections.defaultdict(collections.Counter); nmint = collections.defaultdict(set)
for r in rows:
    mine = [t for t in r["tr"] if t[1] == HIM and t[2] == 1]
    if r["err"] or not mine: continue
    t = mine[0]; f = t[9] or 0; skip = {t[3], f, f // 2, f - f // 2, t[10] or 0}
    for s, d, l in r["xf"]:
        if s != HIM or d in TIPS or l in skip: continue
        dest[d][l] += 1; nmint[d].add(t[0])
cand = sorted(dest, key=lambda d: -sum(dest[d].values()))
print("destinations (not known tips) receiving non-trade amounts in his landed buys:", len(cand))
for d in cand[:40]:
    print(d, sum(dest[d].values()), "mints", len(nmint[d]), "in recent top-level tips:", rec_top.get(d, 0), dest[d].most_common(4))
