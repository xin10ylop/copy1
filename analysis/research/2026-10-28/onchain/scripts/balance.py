# His balance over his life (UTC days): Triton rows carry pre/post balances; month rows carry deltas, chained from the
# last Triton balance before them and checked against the first Triton balance after them. Also his own coin launches.
import json, os, time, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
HIM = N.HIM
rows = [json.loads(l) for l in open(N.W + "/data/rows.jsonl")]
mrows = [json.loads(l) for l in open(N.W + "/ds/month/AHwJSnFN.jsonl")]
MLO, MHI = 1790255495, 1792847349
tri = sorted([r for r in rows if r["post_bal"] is not None], key=lambda r: (r["s"], r["sig"]))
pre = [r for r in tri if r["bt"] < MLO]; post = [r for r in tri if r["bt"] > MHI]
bal = pre[-1]["post_bal"]; start_m = bal
for r in sorted(mrows, key=lambda r: (r["s"], r["sig"])): bal += r["d"]
first_after = min((r for r in tri if r["bt"] > MHI), key=lambda r: (r["s"], r["sig"]))
print(f"balance before month rows {start_m/1e9:.4f}; + month deltas = {bal/1e9:.4f}; first Triton tx after: pre {first_after['pre_bal']/1e9:.4f} (gap = txs between Oct 24 13:09 and our first row are in both sources)")
day = lambda bt: time.strftime("%Y-%m-%d", time.gmtime(bt))
last = {}
for r in pre: last[day(r["bt"])] = r["post_bal"]
b = start_m
for r in sorted(mrows, key=lambda r: (r["s"], r["sig"])): b += r["d"]; last[day(r["bt"])] = b
for r in post: last[day(r["bt"])] = r["post_bal"]
keep = ["2025-01-16", "2025-01-19", "2026-08-17", "2026-08-18", "2026-08-25", "2026-08-29", "2026-09-01", "2026-09-03", "2026-09-06", "2026-09-07", "2026-09-19", "2026-09-23", "2026-09-30", "2026-10-02", "2026-10-16", "2026-10-23", "2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28"]
print("end-of-day balance (SOL):", ", ".join(f"{k} {last[k]/1e9:.2f}" for k in keep if k in last))
# his own launches
cr = [r for r in rows if any(p.startswith("create") for p in r["pix"]) and r["payer"] == HIM]
mints = {}
for r in cr:
    e = [x for x in r["tr"] if x["user"] == HIM]
    if e: mints[e[0]["mint"]] = r["bt"]
pnl = collections.defaultdict(float)
for r in rows:
    for e in r["tr"]:
        if e["user"] == HIM and e["mint"] in mints: pnl[e["mint"]] += r["d"] / 1e9; break
print("coins he launched himself:", len(mints), "on", sorted(collections.Counter(day(b) for b in mints.values()).items()), "his net on them", round(sum(pnl.values()), 3), "SOL (sum of his deltas on their txs)")
