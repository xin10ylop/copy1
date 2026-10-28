# Verify that his buy's slot-guard lower bound is the coin's create slot: for a sample of his coins, read the mint's
# oldest signature (getSignaturesForAddress paged to the end) and that transaction (is it the pump create?).
#   run.sh createslot.py N  -> data/createslot.json
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
from sigs import all_sigs
N = int(sys.argv[1]) if len(sys.argv) > 1 else 80
T = json.load(open(os.path.join(R.W, "data", "trips.json")))["trips"]
T.sort(key=lambda t: t["bt"]); step = max(1, len(T) // N); samp = T[::step][:N]
out = []
for t in samp:
    s = all_sigs(t["mint"], max_pages=10, head_cache=False, before=t["sell_sigs"][-1] if t.get("sell_sigs") else t["buy_sig"])
    if not s: continue
    old = s[-1]
    tx = R.rpc("getTransaction", [old["signature"], R.TXO1])
    c = P.compact(tx) if tx else {}
    out.append(dict(mint=t["mint"], g_lo=t["g_lo"], buy_slot=t["buy_slot"], first_sig_slot=old["slot"], n_sigs_before_buy=len(s),
                    is_create=any(p.startswith("create") for p in c.get("pix", [])), create_payer=c.get("payer"), sell1=t["sell_slots"][0]))
json.dump(out, open(os.path.join(R.W, "data", "createslot.json"), "w"))
cmp = collections.Counter((o["is_create"], o["first_sig_slot"] - o["g_lo"]) for o in out)
print("sampled", len(out), "(is_create, create slot - guard lo):", cmp.most_common())
print("H = first sell - create:", sorted(collections.Counter(o["sell1"] - o["first_sig_slot"] for o in out if o["is_create"]).items()))
print("calls", R.flush_count())
