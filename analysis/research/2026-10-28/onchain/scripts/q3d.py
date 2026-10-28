# Q3d: co-signers on his transactions (whole history we hold), and the token accounts he holds now.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
rows = [json.loads(l) for l in open(os.path.join(R.W, "data", "rows.jsonl"))]
mrows = [json.loads(l) for l in open(os.path.join(R.W, "ds", "month", "AHwJSnFN.jsonl"))]
c = collections.Counter(); co = collections.Counter(); n = 0
for r in rows + mrows:
    sg = r["signers"]
    if HIM not in sg: continue
    n += 1; c[len(sg)] += 1
    for k in sg:
        if k != HIM: co[k] += 1
print("txs he signed (Triton + month rows):", n, "by number of signers:", dict(c), "co-signers:", co.most_common(10))
ext = collections.Counter(r["payer"] for r in rows if HIM not in r["signers"]); print("txs others signed that include him (Triton rows):", sum(ext.values()), "distinct payers", len(ext))
toks = {}
for prog in ("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"):
    r = R.rpc("getTokenAccountsByOwner", [HIM, {"programId": prog}, {"encoding": "jsonParsed"}], cache=False)
    for v in r["value"]:
        i = v["account"]["data"]["parsed"]["info"]
        toks[v["pubkey"]] = (prog[:8], i["mint"], i["tokenAmount"]["uiAmountString"], v["account"]["lamports"], i.get("state"))
print("token accounts he holds now:", len(toks))
nonpump = {k: v for k, v in toks.items() if not v[1].endswith("pump")}
print("  ending in 'pump':", len(toks) - len(nonpump), "| others:", len(nonpump))
for k, v in list(toks.items())[:40]: print("   ", k, v)
json.dump(toks, open(os.path.join(R.W, "data", "tokens_now.json"), "w"))
print("calls", R.flush_count())
