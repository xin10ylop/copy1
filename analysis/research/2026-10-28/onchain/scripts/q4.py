# Q4: his launch buys since Oct 26 13:00 UTC (= 15:00 Beirut, UTC+2), split by the copy key (tip >= 2M, tip = his
# top-level System transfers, as the bot reads it), and the live window of the check.sh paste (to Oct 27 09:45:34 UTC).
import json, os, sys, collections, time, statistics as St
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
A = 1793019600; assert time.strftime("%Y-%m-%d %H:%M", time.gmtime(A)) == "2026-10-26 13:00"
B = A + 20 * 3600 + 45 * 60 + 34   # 2026-10-27 09:45:34 UTC = 11:45:34 Beirut, when check.sh ran
rows = [r for r in N.ours() if r["bt"] >= A]
def report(lo, hi, label):
    rs = [r for r in rows if lo <= r["bt"] < hi]
    T = [t for t in N.trips(rs)]
    launch = [t for t in T if t["g"] and t["s"] - t["g"][0] in (0, 1)]
    fails = [r for r in rs if r["err"]]
    print(f"== {label}: {time.strftime('%m-%d %H:%M:%S', time.gmtime(lo))} - {time.strftime('%m-%d %H:%M:%S', time.gmtime(min(hi, max(r['bt'] for r in rs))))} UTC")
    print(f"   coins he bought (landed) {len(T)}, at create+0/1 {len(launch)}, all closed {all(t['closed'] for t in T)}; his net on them {sum(t['pnl'] for t in T):+.4f} SOL; "
          f"failed txs {len(fails)} costing {-sum(r['d'] for r in fails)/1e9:.4f} SOL; balance change, all his txs {sum(r['d'] for r in rs)/1e9:+.4f}")
    for name, f in (("KEY: tip >= 2M or size >= 2 SOL", lambda t: t["tip"] >= 2e6 or t["sol"] >= 2e9), ("not key", lambda t: not (t["tip"] >= 2e6 or t["sol"] >= 2e9)),
                    ("tip >= 2M", lambda t: t["tip"] >= 2e6), ("tip < 2M", lambda t: t["tip"] < 2e6), ("size >= 2 SOL and tip < 2M", lambda t: t["sol"] >= 2e9 and t["tip"] < 2e6),
                    ("BID KEY: tip + priority >= 2M or size >= 2 SOL", lambda t: t["tip"] + t["prio"] >= 2e6 or t["sol"] >= 2e9),
                    ("tip + priority >= 2M", lambda t: t["tip"] + t["prio"] >= 2e6), ("tip < 2M but tip + priority >= 2M", lambda t: t["tip"] < 2e6 <= t["tip"] + t["prio"]),
                    ("tip + priority < 2M", lambda t: t["tip"] + t["prio"] < 2e6)):
        s = [t for t in T if f(t)]
        if not s: continue
        print(f"   {name:36s} {len(s):4d} coins  net {sum(t['pnl'] for t in s):+8.4f}  per buy {sum(t['pnl'] for t in s)/len(s):+.4f}  wins {sum(1 for t in s if t['pnl']>0)}/{len(s)}"
              f"  median stake {St.median([t['sol'] for t in s])/1e9:.3f}  without best 2: {sum(sorted(t['pnl'] for t in s)[:-2]):+.4f}")
    return T
T1 = report(A, B, "LIVE WINDOW (check.sh 2026-10-27: 377 launch buys, his net +8.9099, 162 copied)")
T2 = report(A, 1 << 40, "SINCE Oct 26 13:00 UTC to now")
json.dump(dict(window=[t for t in T1], since=[t for t in T2]), open(N.W + "/data/q4.json", "w"))
