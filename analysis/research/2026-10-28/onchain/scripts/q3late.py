# Flows after the Aug 25 - Sep 3 burst: list every one (Sep 4 onward), and the 2025 / Aug 17-23 ones.
import json, os, time, collections
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = json.load(open(W + "/data/flows.json"))["flows"]
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
big = [f for f in F if f[4] >= 100000]
for f in big:
    if f[0] < 1787616000 or f[0] >= 1788393600 + 86400: print(ts(f[0]), f[2], f[3], f[4] / 1e9, "payer", f[5][:8], f[6], f[1][:16])
