# Q3a table: his SOL flows with other accounts, by period (>= 0.0001 SOL; dust separately).
import json, os, time, collections, calendar
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = json.load(open(W + "/data/flows.json"))["flows"]
u = lambda s: calendar.timegm(time.strptime(s, "%Y-%m-%d"))
P = [("2025-01-16 .. 01-19", u("2025-01-16"), u("2025-01-20")), ("2026-08-17 .. 08-23", u("2026-08-17"), u("2026-08-24")),
     ("2026-08-25 .. 09-03", u("2026-08-25"), u("2026-09-04")), ("2026-09-04 .. 09-30", u("2026-09-04"), u("2026-10-01")),
     ("2026-10-01 .. 10-02", u("2026-10-01"), u("2026-10-03")), ("2026-10-03 .. 10-28 14:56", u("2026-10-03"), u("2026-10-29"))]
print("| period (UTC) | in: transfers | in: SOL | in: wallets | out: transfers | out: SOL | out: accounts | dust in (< 0.0001 SOL) |\n|---|---|---|---|---|---|---|---|")
for lab, a, b in P:
    f = [x for x in F if a <= x[0] < b]; big = [x for x in f if x[4] >= 100000]
    i = [x for x in big if x[2] == "in"]; o = [x for x in big if x[2] == "out"]; d = [x for x in f if x[4] < 100000]
    print(f"| {lab} | {len(i)} | {sum(x[4] for x in i)/1e9:.3f} | {len({x[3] for x in i})} | {len(o)} | {sum(x[4] for x in o)/1e9:.3f} | {len({x[3] for x in o})} | {len(d)} ({sum(x[4] for x in d)} lamports) |")
big = [x for x in F if x[4] >= 100000]
print(f"| all | {sum(1 for x in big if x[2]=='in')} | {sum(x[4] for x in big if x[2]=='in')/1e9:.3f} | | {sum(1 for x in big if x[2]=='out')} | {sum(x[4] for x in big if x[2]=='out')/1e9:.3f} | | {sum(1 for x in F if x[4] < 100000)} |")
# the Sep 4-30 outflows by kind
f = [x for x in F if u("2026-09-04") <= x[0] < u("2026-10-01") and x[4] >= 100000]
print("Sep 4-30 out by amount:", collections.Counter((x[4], x[7]) for x in f).most_common(6))
# dust payers since Oct 1
d = [x for x in F if x[4] < 100000 and x[0] >= u("2026-10-01")]
print("dust since Oct 1:", len(d), "from", len({x[5] for x in d}), "payers")
