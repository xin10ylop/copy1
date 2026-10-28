# Fetch (and cache) full transactions for a set of his signatures.
#   run.sh fetch.py recent      -> every signature since 2026-10-24 00:00 UTC (failed included)
#   run.sh fetch.py early       -> every successful signature before the month data (2026-09-24 13:11 UTC)
import sys, os, json, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
T24 = 1792800000  # 2026-10-24 00:00 UTC
assert time.strftime("%Y-%m-%d %H:%M", time.gmtime(T24)) == "2026-10-24 00:00"
MLO = 1790255460  # ~ month data start (09-24 13:11 UTC); exact boundary below
mode = sys.argv[1]
if mode == "recent": todo = [x["signature"] for x in S if (x["blockTime"] or 0) >= T24]
elif mode == "early":
    rows_lo = int(sys.argv[2]) if len(sys.argv) > 2 else MLO
    todo = [x["signature"] for x in S if (x["blockTime"] or 0) < rows_lo and not x.get("err")]
elif mode == "list": todo = json.load(open(sys.argv[2]))
print(mode, "todo", len(todo), flush=True)
B = 50
chunks = [todo[i:i + B] for i in range(0, len(todo), B)]
miss = 0; t0 = time.time()
def one(c):
    r = R.txs(c); return sum(1 for x in r if x is None)
with ThreadPoolExecutor(max_workers=4) as ex:
    for k, m in enumerate(ex.map(one, chunks)):
        miss += m
        if k % 20 == 0: print(time.strftime("%H:%M:%S"), k * B, "missing", miss, "calls", R.flush_count(), flush=True)
print("done", len(todo), "missing", miss, "calls", R.flush_count(), "secs", int(time.time() - t0))
