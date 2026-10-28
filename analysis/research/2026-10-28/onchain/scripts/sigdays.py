import json, time, collections, sys, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = json.load(open(W + "/data/sigs_AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2.json"))
rows = [json.loads(l) for l in open(W + "/ds/month/AHwJSnFN.jsonl")]
md = collections.Counter(time.strftime("%Y-%m-%d", time.gmtime(r["bt"])) for r in rows)
mde = collections.Counter(time.strftime("%Y-%m-%d", time.gmtime(r["bt"])) for r in rows if r["err"])
d = collections.Counter(); e = collections.Counter()
for x in s:
    k = time.strftime("%Y-%m-%d", time.gmtime(x["blockTime"] or 0)); d[k] += 1; e[k] += bool(x.get("err"))
mon = collections.Counter(k[:7] for k in d.elements())
print("by month:", sorted(mon.items()))
for k in sorted(d):
    if k >= "2026-09-20": print(k, d[k], e[k], "| month-data", md.get(k, 0), mde.get(k, 0))
lo = min(r["bt"] for r in rows); hi = max(r["bt"] for r in rows)
print("month data rows", len(rows), "range", time.strftime("%m-%d %H:%M", time.gmtime(lo)), time.strftime("%m-%d %H:%M", time.gmtime(hi)))
ss = {x["signature"] for x in s}; ms = {r["sig"] for r in rows}
print("month sigs not in triton list", len(ms - ss), "triton sigs in month range not in month", sum(1 for x in s if lo <= (x["blockTime"] or 0) <= hi and x["signature"] not in ms))
