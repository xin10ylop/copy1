# Q3b: every signature that ever touched his two guard programs (full getSignaturesForAddress history), minus his own
# signature list (complete to 2026-10-28 14:56:35 UTC). Anything left is someone else's -> fetch it, tally fee payers.
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
from sigs import all_sigs
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json"))); his = {x["signature"] for x in S}; his_new = max(x["slot"] for x in S)
PROGS = {"slot guard": "A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp", "state guard": "8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez"}
res = {}
for name, p in PROGS.items():
    s = all_sigs(p, max_pages=200)
    json.dump(s, open(os.path.join(R.W, "data", f"sigs_{p}.json"), "w"))
    old = [x for x in s if x["slot"] <= his_new]
    other = [x for x in old if x["signature"] not in his]
    payers = collections.Counter()
    for i in range(0, len(other), 50):
        for x, t in zip(other[i:i + 50], R.txs1([y["signature"] for y in other[i:i + 50]])):
            payers[t["transaction"]["message"]["accountKeys"][0] if t else "unread"] += 1
    res[name] = dict(program=p, sigs=len(s), up_to_his_newest=len(old), his=sum(1 for x in old if x["signature"] in his), others=len(other), payers=payers.most_common(),
                     first=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(s[-1]["blockTime"])), newest=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(s[0]["blockTime"])),
                     newer_than_his_list=len(s) - len(old))
    print(name, p, "| all sigs", len(s), "| first", res[name]["first"], "| up to his newest slot", len(old), "of which his", res[name]["his"], "| others", len(other), payers.most_common(10),
          "| newer than his list", res[name]["newer_than_his_list"])
# his txs that do NOT appear in the programs' lists (sanity: buys use both, sells use the slot guard)
rows = [json.loads(l) for l in open(os.path.join(R.W, "data", "rows.jsonl"))]
json.dump(res, open(os.path.join(R.W, "data", "q3b.json"), "w"), indent=1)
print("calls", R.flush_count())
