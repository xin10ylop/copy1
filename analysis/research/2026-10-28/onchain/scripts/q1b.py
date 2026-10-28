# Q1 detail: tip values outside the step list, priority-fee values, planned hold (sell guard start - create), programs.
import json, os, collections, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
T24 = 1792800000; T17 = 1792195200  # Oct 17 00:00 UTC
ours = [r for r in N.ours() if r["bt"] >= T24]; mon = [r for r in N.month() if r["bt"] < T24]
STEPS = [0, 0.5, 1.0, 1.5, 1.8, 2.4, 3.2, 3.6, 4.8, 6.4, 7.2, 8.0, 12, 15, 18, 24, 30, 36, 48]
for lab, rows in (("month Oct17-23", [r for r in mon if r["bt"] >= T17]), ("Oct24-28", ours)):
    T = N.trips(rows)
    oth = collections.Counter(round(t["tip"] / 1e6, 2) for t in T if not any(abs(t["tip"] / 1e6 - s) < 0.05 for s in STEPS))
    pr = collections.Counter(round(t["prio"] / 1e6, 2) for t in T)
    print(lab, "coins", len(T), "| tips off-step top:", oth.most_common(12))
    print("   prio (M) top:", pr.most_common(10))
    bid = collections.Counter(round((t["tip"] + t["prio"]) / 1e6, 1) for t in T); print("   tip+prio (M) top:", bid.most_common(12))
    st = collections.Counter(round(t["sol"] / 1e9, 3) for t in T); n = len(T)
    print("   stake:", [(k, v, round(100 * v / n, 1)) for k, v in st.most_common(9)])
    # stake x tip
    g2 = [t for t in T if t["tip"] >= 2e6]; l2 = [t for t in T if t["tip"] < 2e6]
    import statistics as St
    print(f"   tip>=2M: {len(g2)} coins, median stake {St.median([t['sol'] for t in g2])/1e9:.3f}, net {sum(t['pnl'] for t in g2):+.3f}, per buy {sum(t['pnl'] for t in g2)/len(g2):+.4f}; "
          f"tip<2M: {len(l2)}, median stake {St.median([t['sol'] for t in l2])/1e9:.3f}, net {sum(t['pnl'] for t in l2):+.3f}, per buy {sum(t['pnl'] for t in l2)/len(l2):+.4f}")
    # landing position: buy slot - create slot
    pos = collections.Counter(t["s"] - t["g"][0] for t in T if t["g"]); print("   buy at create +k:", sorted(pos.items()))
# planned hold from the sell's slot guard (ours: full rows)
rows = [json.loads(l) for l in open(N.W + "/data/rows.jsonl")]
tr = json.load(open(N.W + "/data/trips.json"))["trips"]
P = collections.Counter(t["sell_g"][0][0] - t["g_lo"] for t in tr if t["sell_g"] and t["sell_g"][0]); n = sum(P.values())
print("Oct24-28 planned H (sell guard start - create):", sorted((k, v, round(100 * v / n, 1)) for k, v in P.items()), "n", n)
# month planned H: sell rows' calls carry the guard (first 48 bytes hex)
mrows = [json.loads(l) for l in open(N.W + "/ds/month/AHwJSnFN.jsonl")]
lo = {}; ph = collections.defaultdict(collections.Counter)
import time
for r in sorted(mrows, key=lambda r: r["s"]):
    mine = [t for t in r["tr"] if t[1] == N.HIM]
    if r["err"] or not mine: continue
    gs = next((h for p, h, na in r["calls"] if p == N.SLOTG), None)
    if not gs: continue
    a = struct.unpack_from("<Q", bytes.fromhex(gs), 0)[0]
    if mine[0][2] and mine[0][0] not in lo: lo[mine[0][0]] = a
    elif not mine[0][2] and mine[0][0] in lo and lo[mine[0][0]] is not None:
        ph[time.strftime("%m-%d", time.gmtime(r["bt"]))][a - lo[mine[0][0]]] += 1; lo[mine[0][0]] = None
for d in sorted(ph):
    n = sum(ph[d].values()); print("month", d, "planned H:", sorted((k, round(100 * v / n)) for k, v in ph[d].items() if v >= 3), "n", n, "H in {6,10}:", round(100 * (ph[d][6] + ph[d][10]) / n, 1))
# programs
mp = collections.Counter(p for r in mrows for p in {c[0] for c in r["calls"]})
rp = collections.Counter(p for r in rows if r["bt"] >= T24 and r["payer"] == N.HIM for p in set(r["tops"]))
print("month non-standard programs:", mp.most_common(10)); print("Oct24-28 programs in his own txs:", rp.most_common(12))
