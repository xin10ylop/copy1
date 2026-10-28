# Markdown tables for the report (all from cached data; no RPC).
import json, os, sys, collections, time, statistics as St
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
T24 = 1792800000; T17 = 1792195200
ours = [r for r in N.ours() if r["bt"] >= T24]; mon = [r for r in N.month() if r["bt"] < T24]
day = lambda bt: time.strftime("%m-%d", time.gmtime(bt))
STEPS = [1.0, 1.5, 1.8, 2.4, 3.6, 4.8, 7.2, 12, 18, 24]
def stats(rows, T):
    lb = sum(1 for r in rows if r["k"] == "buy" and not r["err"] and r["mine"]); fb = sum(1 for r in rows if r["k"] == "buy" and r["err"])
    cl = [t for t in T if t["closed"]]; tips = [t["tip"] for t in T]
    H = [t["sells"][0] - t["g"][0] for t in T if t["sells"] and t["g"]]
    hs = [t["sells"][0] - t["s"] for t in T if t["sells"]]
    return dict(lb=lb, fb=fb, net=sum(r["d"] for r in rows) / 1e9, trade=sum(t["pnl"] for t in T), fails=-sum(r["d"] for r in rows if r["err"]) / 1e9,
                win=100 * sum(1 for t in cl if t["pnl"] > 0) / max(len(cl), 1), stake=St.median([t["sol"] for t in T]) / 1e9 if T else 0,
                stake_mean=St.mean([t["sol"] for t in T]) / 1e9 if T else 0, ge2=100 * sum(1 for x in tips if x >= 2e6) / max(len(tips), 1),
                key=100 * sum(1 for t in T if t["tip"] >= 2e6 or t["sol"] >= 2e9) / max(len(T), 1),
                bid2=100 * sum(1 for t in T if t["tip"] + t["prio"] >= 2e6) / max(len(T), 1),
                prio=100 * sum(1 for t in T if t["prio"] >= 1e5) / max(len(T), 1), c0=100 * sum(1 for t in T if t["g"] and t["s"] == t["g"][0]) / max(len(T), 1),
                hold=St.median(hs) if hs else 0, H610=100 * sum(1 for h in H if h in (6, 10)) / max(len(H), 1), per=sum(t["pnl"] for t in T) / max(len(T), 1))
def row(lab, s, days=1):
    return (f"| {lab} | {s['lb']/days:.0f} | {s['fb']/days:.0f} | {100*s['fb']/max(s['lb']+s['fb'],1):.0f}% | {s['net']/days:+.2f} | {s['trade']/days:+.2f} | {s['fails']/days:.4f} | {s['per']:+.4f} | {s['win']:.1f}% | "
            f"{s['stake']:.3f} / {s['stake_mean']:.3f} | {s['ge2']:.1f}% | {s['key']:.1f}% | {s['bid2']:.1f}% | {s['prio']:.1f}% | {s['c0']:.1f}% | {s['hold']:.0f} | {s['H610']:.1f}% |")
hdr = ("| UTC day | landed buys | failed buys | fail % | net SOL (all his txs) | trade P&L | failed-tx cost | per buy | win % | stake median / mean | tip >= 2M | copy key (tip >= 2M or >= 2 SOL) | tip + priority >= 2M | priority >= 0.1M | at create+0 | median hold (slots from buy) | sold at create+6/+10 |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
print(hdr)
R = collections.defaultdict(list)
for r in ours: R[day(r["bt"])].append(r)
TT = collections.defaultdict(list)
for t in N.trips(ours): TT[day(t["bt"])].append(t)
for d in sorted(R): print(row(d + (" (to 14:56)" if d == "10-28" else ""), stats(R[d], TT[d])))
print(row("**Oct 24-28, all**", stats(ours, N.trips(ours))))
m17 = [r for r in mon if r["bt"] >= T17]; print(row("Oct 17-23 (7 days), a day", stats(m17, N.trips(m17)), 7))
md = sorted({day(r["bt"]) for r in mon if r["k"] == "buy"}); act = [d for d in md]
print(row(f"Sep 24 13:11 - Oct 23 ({len(act)} days with trades), a day", stats(mon, N.trips(mon)), len(act)))
# tip steps
def steps(T):
    c = collections.Counter()
    for t in T:
        m = t["tip"] / 1e6; k = next((f"{s:g}" for s in STEPS if abs(m - s) < 0.05), None)
        c[k or ("< 1.0" if m < 0.95 else "other")] += 1
    n = sum(c.values()); return {k: (v, 100 * v / n) for k, v in c.items()}, n
print()
a, na = steps(N.trips(m17)); b, nb = steps(N.trips(ours))
print("| landed tip (M lamports) | Oct 17-23 | Oct 24-28 |\n|---|---|---|")
for k in ["< 1.0"] + [f"{s:g}" for s in STEPS] + ["other"]:
    print(f"| {k} | {a.get(k, (0, 0))[0]} ({a.get(k, (0, 0))[1]:.1f}%) | {b.get(k, (0, 0))[0]} ({b.get(k, (0, 0))[1]:.1f}%) |")
print(f"| all | {na} | {nb} |")
# hold table
print()
tr = json.load(open(N.W + "/data/trips.json"))["trips"]
P = collections.Counter(t["sell_g"][0][0] - t["g_lo"] for t in tr if t["sell_g"] and t["sell_g"][0])
L = collections.Counter(t["sell_slots"][0] - t["g_lo"] for t in tr if t["sell_slots"])
n = len(tr)
print("| H (slots after the create) | planned (his sell guard's start slot) | landed (his first sell) |\n|---|---|---|")
for h in sorted(set(P) | set(L)):
    if P[h] + L[h] >= 5: print(f"| {h} | {P[h]} ({100*P[h]/n:.1f}%) | {L[h]} ({100*L[h]/n:.1f}%) |")
print(f"| all | {sum(P.values())} | {sum(L.values())} |")
secs = [t["sell_bts"][0] - t["bt"] for t in tr if t["sell_bts"]]
print("median hold seconds (blockTime sell - buy):", St.median(secs), "p10/p90", sorted(secs)[len(secs) // 10], sorted(secs)[9 * len(secs) // 10])
print("sell lands at its guard start + k:", sorted(collections.Counter(t["sell_slots"][0] - t["sell_g"][0][0] for t in tr if t["sell_g"] and t["sell_g"][0]).items()))
print("sells per coin:", collections.Counter(t["n_sells"] for t in tr).most_common(4), "buys per coin:", collections.Counter(t["n_buys"] for t in tr).most_common(3))
st = collections.Counter(t["sell_tip"][0] for t in tr if t["sell_tip"]); sf = collections.Counter(t["sell_fee"][0] for t in tr if t["sell_fee"])
print("sell tip top:", st.most_common(4), "sell fee top:", sf.most_common(4))
