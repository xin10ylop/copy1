import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
miss = [x for x in S if (x["blockTime"] or 0) >= 1792800000 and not os.path.exists(R._path("getTransaction", [x["signature"], R.TXO]))]
print(len(miss), [(x["slot"], time.strftime("%m-%d %H:%M:%S", time.gmtime(x["blockTime"])), x.get("err") is not None) for x in miss[:40]])
if miss:
    j = R._post({"jsonrpc": "2.0", "id": 1, "method": "getTransaction", "params": [miss[0]["signature"], R.TXO]}); R._bump(1)
    print({k: (v if k != "result" else (None if v is None else "tx")) for k, v in j.items()})
print("calls", R.flush_count())
