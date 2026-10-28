# C3. Sell timing risk. (1) How often our live sells land after the slot they were sent for: the live tapes
# (refused/tape) hold our sells; the copy_more wallets had fixed targets (JBokzLFR create + 5, CxyKYmQo + 12, 3yrJE1A8
# + 29: docs/19 §5-§11), so their sell slot against the target measures our sell latency. For him the target (H - 1
# from the box's table) is not in the data, so his coins are compared with his own first sell (calib_live.json).
# (2) The 5-day backtest with the sell one slot late (H instead of H - 1), on every copy or on a share p of them.
# python3 -I c3_sell_late.py <calib_live.json from calib_live.py>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
TGT = {"JBokzLFR": 5, "CxyKYmQo": 12, "3yrJE1A8": 29}
R = json.load(open(SP + "/refused/live_recs.json"))
cnt = collections.defaultdict(collections.Counter)
for r in R:
    if r["who"] not in TGT or r["status"] != "filled": continue
    p = f"{SP}/refused/tape/{r['m']}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p)); c0 = d["c0"]
    us = [x for x in d["rows"] if x[2] == US and x[3] == 0]
    if not us: cnt[r["who"]]["sell not on the tape"] += 1; continue
    off = min(us)[0] - c0 - TGT[r["who"]]
    cnt[r["who"]][off] += 1
print("== 1. our live sells against a fixed target (filled copies with a tape): slot landed - slot targeted")
tot = collections.Counter()
for w, c in cnt.items():
    n = sum(v for k, v in c.items() if isinstance(k, int))
    late = sum(v for k, v in c.items() if isinstance(k, int) and k >= 1)
    print(f"   {w:9} target +{TGT[w]:2d}: " + " ".join(f"{k:+d}:{v}" if isinstance(k, int) else f"{k}:{v}" for k, v in sorted(c.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))) +
          f"   -> late by >= 1 slot {late}/{n} = {late / max(n, 1):.0%}")
    for k, v in c.items():
        if isinstance(k, int): tot[k] += v
n = sum(tot.values()); late = sum(v for k, v in tot.items() if k >= 1); late1 = tot.get(1, 0)
P_LATE = late / n
print(f"   all: {n} sells, on target {tot.get(0, 0)}, early {sum(v for k, v in tot.items() if k < 0)}, one slot late {late1}, two or more {late - late1}: p(late) = {P_LATE:.0%}")
C = json.load(open(sys.argv[1]))["timing"]
print(f"\n   his coins (calib_live.json, {len(C)} filled copies with a tape): our sell against his first sell")
for k, v in collections.Counter(t["tk"] for t in C).most_common():
    print(f"      {k:40} {v:3d}  our net {sum(t['ours'] for t in C if t['tk'] == k):+.4f}")
print("\n== 2. the 5-day backtest (2M set, 0.5 SOL, live 3M costs): the sell one slot late")
def hk(k): return lambda r: (r["H"] - k) if r["listed"] else (hold(r) + 1 - k)
base_it = [(r, value(r, 0.5, fixed_of(3.0), REF_LIVE)) for r in LIVE2]
late_it = [(r, value(r, 0.5, fixed_of(3.0), REF_LIVE, hold_fn=hk(0))) for r in LIVE2]
late2_it = [(r, value(r, 0.5, fixed_of(3.0), REF_LIVE, hold_fn=hk(-1))) for r in LIVE2]
line("sold at H - 1 as sent (the backtest)", base_it)
line("every sell one slot late (at H)", late_it)
line("every sell two slots late (at H + 1)", late2_it)
mix = []
for (r, a), (_, b) in zip(base_it, late_it):
    if a and b: mix.append((r, {k: (1 - P_LATE) * a[k] + P_LATE * b[k] for k in a}))
line(f"a share p = {P_LATE:.0%} lands one slot late", mix)
# how often the backtest itself sells at or after his first sell (exit_at then takes the state right after his sell)
n_after = sum(1 for r in LIVE2 if r["s"] is not None and r["cs"] + max(H_live(r), 1) >= r["s"]["slot"])
n_after_H = sum(1 for r in LIVE2 if r["s"] is not None and r["cs"] + max(hk(0)(r), 1) >= r["s"]["slot"])
print(f"   in the backtest, the H - 1 sell is at or after his first sell on {n_after} of {len(LIVE2)} copies ({n_after / len(LIVE2):.0%}); at H on {n_after_H} ({n_after_H / len(LIVE2):.0%})")
d1 = sum(b["net"] - a["net"] for (r, a), (_, b) in zip(base_it, late_it) if a and b)
print(f"   one slot late costs {d1:+.2f} SOL over 5 days on {len(LIVE2)} copies ({d1 / len(LIVE2):+.4f} a copy); at p = {P_LATE:.0%}: {P_LATE * d1:+.2f}")
