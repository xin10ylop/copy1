# Q3a follow-up: every counterparty of his SOL flows (>= 0.0001 SOL): account owner / balance now (getMultipleAccounts),
# and its newest signature (getSignaturesForAddress limit 1): is it still active?   -> data/cp_now.json
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
F = json.load(open(os.path.join(R.W, "data", "flows.json")))
cps = sorted(F["cp"])
print("counterparties", len(cps))
OUT = os.path.join(R.W, "data", "cp_now.json")
info = {}
for i in range(0, len(cps), 100):
    ch = cps[i:i + 100]
    r = R.rpc("getMultipleAccounts", [ch, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}], cache=True)
    for a, v in zip(ch, r["value"]):
        info[a] = dict(lamports=v["lamports"] if v else 0, owner=v["owner"] if v else None, exec=v.get("executable") if v else None)
calls = [("getSignaturesForAddress", [a, {"limit": 1}]) for a in cps]
res = []
for i in range(0, len(calls), 50): res += R.batch(calls[i:i + 50])
for a, r in zip(cps, res):
    x = (r or [None])[0] if r else None
    info[a].update(last_sig=x["signature"] if x else None, last_bt=x["blockTime"] if x else None, last_slot=x["slot"] if x else None)
json.dump(info, open(OUT, "w"))
own = collections.Counter(v["owner"] for v in info.values()); print("owners now:", own.most_common(8))
ts = lambda bt: time.strftime("%Y-%m-%d", time.gmtime(bt)) if bt else None
lm = collections.Counter(ts(v["last_bt"])[:7] if v["last_bt"] else None for v in info.values()); print("last activity month:", sorted(lm.items(), key=lambda kv: str(kv[0])))
act = [(a, v) for a, v in info.items() if v["last_bt"] and v["last_bt"] >= 1792195200]
print("active since Oct 17:", len(act))
for a, v in sorted(act, key=lambda kv: -kv[1]["last_bt"])[:60]:
    c = F["cp"][a]
    print(f"  {a} last {time.strftime('%m-%d %H:%M', time.gmtime(v['last_bt']))} bal {v['lamports']/1e9:9.4f} owner {str(v['owner'])[:8]} | with him: in {c['in_n']} x {c['in_l']/1e9:.3f} out {c['out_n']} x {c['out_l']/1e9:.3f} first {time.strftime('%Y-%m-%d', time.gmtime(c['first']))}")
print("calls", R.flush_count())
