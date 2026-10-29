# "How much did he make today, and what would we have made?" (asked Oct 29 00:20 UTC). His landed launch buys per window
# (the UTC day, the Beirut day = UTC+2, and since the last Beirut midnight), the copy key on them (tip >= 2M at create+0/1,
# as the restart config keys; the operator-table and signer-count filters need the table and are not applied here), and
# our copy's result estimated from the live window's measured ratio: on the 162 coins the box copied (Oct 26-27) his net
# was +7.78 at a median 0.593 SOL stake and our curve +0.834 at 0.5 (07-restart section 2), i.e. our curve per SOL staked
# was 0.127 of his per SOL on the same coins (the refused copies included at 0); fixed cost 0.0031 a fill (1.5M bid +
# 0.0016) on the 77% of copies that filled live, 0.000015 on the rest. After sigs.py / fetch.py recent / parse.py.
import sys, os, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
rows = N.ours()
sigs = {x["signature"]: x for x in __import__("json").load(open(N.W + "/data/sigs_" + N.HIM + ".json"))}
have = {r["sig"] for r in rows}
miss = [s for s in sigs if s not in have]
mb = sorted(sigs[s].get("blockTime") or 0 for s in miss)
print(f"rows {len(rows)}; signatures not fetched {len(miss)}" + (f" (block times {time.strftime('%m-%d %H:%M', time.gmtime(mb[0]))} .. {time.strftime('%m-%d %H:%M', time.gmtime(mb[-1]))} UTC; "
      f"{sum(1 for s in miss if sigs[s].get('err'))} of them failed txs)" if miss else ""))
RATIO, STAKE_HIS, FILL, FIX, REF = 0.127, 0.593, 0.77, 0.0031, 0.000015
def window(lo, hi, label):
    rs = [r for r in rows if lo <= r["bt"] < hi]
    T = N.trips(rs); L = [t for t in T if t["g"] and t["s"] - t["g"][0] in (0, 1)]
    key = [t for t in L if t["tip"] >= 2e6]
    net = sum(r["d"] for r in rs) / 1e9
    print(f"\n== {label}: {time.strftime('%m-%d %H:%M', time.gmtime(lo))} - {time.strftime('%m-%d %H:%M', time.gmtime(hi))} UTC")
    print(f"   him: landed buys {len(T)} (at create+0/1 {len(L)}), failed {sum(1 for r in rs if r['err'])}, net {net:+.3f} SOL, wins {sum(1 for t in T if t['pnl'] > 0)}/{len(T)}, "
          f"median stake {sorted(t['sol'] for t in T)[len(T) // 2] / 1e9 if T else 0:.3f}")
    kn = sum(t["pnl"] for t in key); kx = sum(sorted(t["pnl"] for t in key)[:-2])
    print(f"   copy key (tip >= 2M at create+0/1): {len(key)} coins, his net on them {kn:+.3f} (without his best 2: {kx:+.3f}), wins {sum(1 for t in key if t['pnl'] > 0)}/{len(key)}")
    for stake in (0.5, 1.0):
        curve = RATIO * kn * stake / STAKE_HIS; curve_x = RATIO * kx * stake / STAKE_HIS
        cost = len(key) * (FILL * FIX + (1 - FILL) * REF)
        print(f"   our copy at {stake:.1f} SOL (estimate): curve {curve:+.2f}, fixed cost {cost:.2f} on {len(key)} copies -> net {curve - cost:+.2f} (without his best 2: {curve_x - cost:+.2f})")
D = 86400; U28 = 1793145600; assert time.strftime("%Y-%m-%d %H:%M", time.gmtime(U28)) == "2026-10-28 00:00"
window(U28, U28 + D, "UTC day Oct 28")
window(U28 - 2 * 3600, U28 + D - 2 * 3600, "Beirut day Oct 28 (UTC+2)")
window(U28 + D - 2 * 3600, int(time.time()) + 1, "Beirut Oct 29 so far")
window(U28 - D, U28, "UTC day Oct 27 (for scale)")
