# Re-fetch, with maxSupportedTransactionVersion 1, his signatures that the v0 fetch could not read (version-1 txs).
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
lo = int(sys.argv[1]); hi = int(sys.argv[2]); okonly = len(sys.argv) > 3
miss = [x["signature"] for x in S if lo <= (x["blockTime"] or 0) < hi and (not okonly or not x.get("err")) and R.gettx(x["signature"]) is None]
print("missing", len(miss))
for i in range(0, len(miss), 50):
    r = R.txs1(miss[i:i + 50]); print("got", sum(1 for x in r if x), "of", len(r))
print("calls", R.flush_count())
