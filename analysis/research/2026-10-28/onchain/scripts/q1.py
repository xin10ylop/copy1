# Q1: per UTC day, his landed / failed buys, net SOL (his balance deltas), win rate, stake, tips, priority fees, hold.
# Month (Sep 24 13:11 - Oct 23, from the Oct-24 study's rows) against Oct 24 - Oct 28 (our Triton pull).
import json, os, time, collections, statistics as St, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
T24 = 1792800000
ours = [r for r in N.ours() if r["bt"] >= T24]; mon = [r for r in N.month() if r["bt"] < T24]
day = lambda bt: time.strftime("%m-%d", time.gmtime(bt))
STEPS = [0, 0.5, 1.0, 1.5, 1.8, 2.4, 3.2, 3.6, 4.8, 6.4, 7.2, 8.0, 12, 15, 18, 24, 30, 36, 48]
def tipb(t):
    m = t / 1e6
    for s in STEPS:
        if abs(m - s) < 0.05: return f"{s:g}"
    return "other"
def table(rows, label):
    T = N.trips(rows); D = collections.defaultdict(list); R = collections.defaultdict(list)
    for t in T: D[day(t["bt"])].append(t)
    for r in rows: R[day(r["bt"])].append(r)
    out = []
    for dd in sorted(R):
        rs = R[dd]; ts = D.get(dd, [])
        net = sum(r["d"] for r in rs) / 1e9
        lb = sum(1 for r in rs if r["k"] == "buy" and not r["err"] and r["mine"]); fb = sum(1 for r in rs if r["k"] == "buy" and r["err"])
        fcost = -sum(r["d"] for r in rs if r["err"]) / 1e9
        other = sum(r["d"] for r in rs if r["k"] == "other" and not r["err"]) / 1e9
        cl = [t for t in ts if t["closed"]]
        H = [t["sells"][0] - t["g"][0] for t in ts if t["sells"] and t["g"]]
        tips = [t["tip"] for t in ts]
        out.append(dict(day=dd, txs=len(rs), coins=len(ts), landed_buys=lb, failed_buys=fb, fail_pct=round(100 * fb / max(fb + lb, 1)), net=round(net, 3),
                        trade_pnl=round(sum(t["pnl"] for t in ts), 3), fail_cost=round(fcost, 4), nontrade=round(other, 6),
                        win=round(100 * sum(1 for t in cl if t["pnl"] > 0) / max(len(cl), 1), 1), stake_med=round(St.median([t["sol"] for t in ts]) / 1e9, 3) if ts else None,
                        stake_mean=round(St.mean([t["sol"] for t in ts]) / 1e9, 3) if ts else None,
                        tip_ge2=round(100 * sum(1 for x in tips if x >= 2e6) / max(len(tips), 1), 1), tip_med=round(St.median(tips) / 1e6, 2) if tips else None,
                        prio_pos=round(100 * sum(1 for t in ts if t["prio"] > 0) / max(len(ts), 1), 1),
                        H610=round(100 * sum(1 for h in H if h in (6, 10)) / max(len(H), 1), 1), H_n=len(H),
                        hold_med=St.median([t["sells"][0] - t["s"] for t in ts if t["sells"]]) if ts else None,
                        tipdist=collections.Counter(tipb(x) for x in tips)))
    return out, T
def show(out, label):
    print(f"== {label}")
    print(f"{'day':5} {'txs':>5} {'coins':>5} {'lbuy':>5} {'fbuy':>5} {'f%':>3} {'net':>8} {'trades':>8} {'fails':>7} {'win%':>5} {'stk_md':>6} {'stk_mn':>6} {'tip>=2M%':>8} {'tip_md':>6} {'prio>0%':>7} {'H6/10%':>6} {'hold':>4}")
    for o in out:
        print(f"{o['day']:5} {o['txs']:5d} {o['coins']:5d} {o['landed_buys']:5d} {o['failed_buys']:5d} {o['fail_pct']:3d} {o['net']:+8.3f} {o['trade_pnl']:+8.3f} {o['fail_cost']:7.4f} {o['win']:5.1f} "
              f"{o['stake_med'] or 0:6.3f} {o['stake_mean'] or 0:6.3f} {o['tip_ge2']:8.1f} {o['tip_med'] or 0:6.2f} {o['prio_pos']:7.1f} {o['H610']:6.1f} {o['hold_med'] or 0:4}")
mo, MT = table(mon, "month"); ro, RT = table(ours, "recent")
show(mo, "MONTH rows (Sep 24 13:11 UTC - Oct 23, Oct-24 study's pull)"); show(ro, "OCT 24 - 28 (Triton, to 14:56 UTC Oct 28)")
def agg(T, rows, label, days):
    cl = [t for t in T if t["closed"]]; tips = [t["tip"] for t in T]
    print(f"-- {label}: {days} days with trades; coins {len(T)}; net {sum(r['d'] for r in rows)/1e9:+.3f} SOL (balance deltas, all txs); trades {sum(t['pnl'] for t in T):+.3f}; "
          f"win {100*sum(1 for t in cl if t['pnl']>0)/max(len(cl),1):.1f}%; stake median {St.median([t['sol'] for t in T])/1e9:.3f}; tip>=2M {100*sum(1 for x in tips if x>=2e6)/len(tips):.1f}%; "
          f"prio>0 {100*sum(1 for t in T if t['prio']>0)/len(T):.1f}%")
    c = collections.Counter(tipb(x) for x in tips); tot = sum(c.values())
    print("   tip steps (M):", ", ".join(f"{k}: {v} ({100*v/tot:.1f}%)" for k, v in sorted(c.items(), key=lambda kv: (kv[0] == 'other', float(kv[0]) if kv[0] != 'other' else 0))))
    st = collections.Counter(round(t["sol"] / 1e9, 3) for t in T); print("   stake (SOL into curve) top:", st.most_common(10))
    H = collections.Counter(t["sells"][0] - t["g"][0] for t in T if t["sells"] and t["g"]); n = sum(H.values())
    print("   H = first sell slot - create slot:", ", ".join(f"{k}: {v} ({100*v/n:.1f}%)" for k, v in sorted(H.items()) if v >= max(3, n // 200)), f"(n={n})")
md = [o for o in mo if o["coins"] >= 50]
agg(MT, mon, "MONTH", len(md)); agg(RT, ours, "OCT 24-28", len(ro))
json.dump(dict(month=mo, recent=ro), open(N.W + "/data/q1.json", "w"), default=dict)
