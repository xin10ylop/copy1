# Shared base for copy_relook/: the 5-day copy backtest of him exactly as five/copy/ablate.py builds it (Oct 21-25 tapes,
# his landed launch buys at create + 0/1, our measured landing distances D behind him, 5% bound, sold at the table hold
# H - 1 / his modal first sell - 1 / +9), with the P&L split into the curve part and the fixed part:
#   curve = what the round trip returns minus the stake, on the constant-product curve (our buy's own price impact, our
#           tokens left in the curve until the exit, pump's 1.25% fee each way): the model's pnl_s() + its fixed costs;
#   fixed = the cost of a filled copy that does not scale with the stake: the buy tip (our bid) + the sell tip, priority
#           and base fees. The scripts' model uses 0.003 + 0.0005 + 2 x 0.00001 = 0.00352; live, check.sh's fees column
#           averaged 0.00465 at the 3.0M bid and 0.00958 at 8.0M (live_parse.py), i.e. the bid + 0.0016.
# A refused copy (bound) costs only its fee: 0.0001 in the scripts, 0.000015 measured live (every refused buy).
# exec this file: exec(open(<dir>/base.py).read()). It execs SP/dec/copy/ablate.py (identical to the repo's
# analysis/research/2026-10-25/five/copy/ablate.py) up to its tables, so every loader is the original one.
import json, sys, collections, io, contextlib, bisect, statistics as st, datetime, math, random, os
SP = "/tmp/claude-0/-home-user-rugsnipe/972c43cf-f494-5af4-b87a-fe32117a83be/scratchpad"
ARGV = list(sys.argv)
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(SP + "/dec/copy/ablate.py").read().split("live = [r for r in rows")[0])
sys.argv = ARGV                                             # the loaders overwrite sys.argv
MODEL_FIX = TIP + SELL_TIP + 2 * BASE                       # 0.00352
LIVE_NONBID = 0.0016                                        # live fees minus the bid, per filled copy (live_parse.py)
def fixed_of(bid_m): return bid_m / 1000.0 + LIVE_NONBID    # 3.0M -> 0.0046, 8.0M -> 0.0096
REF_MODEL = 0.0001; REF_LIVE = 0.000015
KEY2 = lambda r: r["tip"] >= 2e6 or r["sol"] >= 2.0
LIVE2 = [r for r in rows if KEY2(r) and HOT(r)]             # ablate.py's "tip >= 2M or size >= 2": 298 copies, +8.02
P1 = ("10-21", "10-22", "10-23"); P2 = ("10-24", "10-25")
def curve_of(en, ex, stake):
    """the round trip's SOL back minus the stake (pump fee in, tips and tx fees out); None if the exit cannot absorb"""
    v = pnl_s(en, ex, stake)
    return None if v is None else v + MODEL_FIX
def legs(r, stake=0.5, prem=0.05, hold_fn=None, D_list=None, entry_fn=None):
    """one leg per landing distance D: ('ref', 0) refused by the bound, ('fill', curve) filled; None legs skipped as
    ablate.val() skips them (no state at the entry or the exit)"""
    hold_fn = hold_fn or H_live; out = []
    for D in (D_list or dec):
        en = (entry_fn or entry_at)(r, D)
        if not en: continue
        if (en[0] / en[1]) / r["hisp"] - 1 > prem: out.append(("ref", 0.0)); continue
        ex = exit_at(r["seq"], r["cs"], max(hold_fn(r), 1), r["s"])
        c = curve_of(en, ex, stake) if ex else None
        if c is not None: out.append(("fill", c))
    return out
def agg(ls, fix=MODEL_FIX, ref=REF_MODEL):
    """mean over the legs: net, curve part, fixed part, refused part, fill fraction"""
    if not ls: return None
    n = len(ls); fl = [c for k, c in ls if k == "fill"]
    cur = sum(fl) / n; fx = fix * len(fl) / n; rf = ref * (n - len(fl)) / n
    return dict(net=cur - fx - rf, curve=cur, fixed=fx, ref=rf, fill=len(fl) / n)
def value(r, stake=0.5, fix=MODEL_FIX, ref=REF_MODEL, **kw):
    return agg(legs(r, stake, **kw), fix, ref)
def by_day(items):
    """items: [(row, value_dict)] -> {day: net}"""
    d = collections.defaultdict(float)
    for r, v in items: d[r["day"]] += v["net"]
    return d
def without_best(nets, k=2):
    xs = sorted(nets, reverse=True); return sum(xs[k:])
def intraday_dd(items):
    """worst running drawdown inside a UTC day, copies in the time order of his buys (each booked at his buy)"""
    worst = 0.0; byd = collections.defaultdict(list)
    for r, v in sorted(items, key=lambda x: his_buy[x[0]["m"]]["bt"]): byd[r["day"]].append(v["net"])
    per = {}; low = 0.0
    for d, xs in byd.items():
        run = peak = w = 0.0
        for x in xs:
            run += x; peak = max(peak, run); w = min(w, run - peak); low = min(low, run)
        per[d] = w; worst = min(worst, w)
    return worst, per, low                                  # peak-to-trough, per day, lowest running day P&L from 0
def line(lab, items, extra=""):
    """one table line: n, total, P1 / P2, without best 2 (total, P1, P2), worst day, by day"""
    items = [(r, v) for r, v in items if v is not None]
    bd = by_day(items); nets = [v["net"] for _, v in items]
    p1 = [v["net"] for r, v in items if r["day"] in P1]; p2 = [v["net"] for r, v in items if r["day"] in P2]
    tot = sum(nets)
    s = (f"   {lab:46} n {len(items):4d} total {tot:+6.2f} [w/o best2 {without_best(nets):+6.2f}]  P1 {sum(p1):+6.2f} [{without_best(p1):+6.2f}]"
         f"  P2 {sum(p2):+6.2f} [{without_best(p2):+6.2f}]  worst day {min(bd.get(d, 0.0) for d in DAYS):+5.2f}  by day "
         + " ".join(f"{bd.get(d, 0.0):+5.2f}" for d in DAYS))
    print(s + extra)
    return dict(n=len(items), tot=tot, p1=sum(p1), p2=sum(p2), p1x=without_best(p1), p2x=without_best(p2), bd=dict(bd))
def tipb(r):
    t = r["tip"]
    return "<2M" if t < 2e6 else "2-4M" if t < 4e6 else "4-8M" if t < 8e6 else "8M+"
def sizeb(r):
    s = r["sol"]
    return "<0.7" if s < 0.7 else "0.7-1.1" if s < 1.1 else "1.1-2" if s < 2.0 else "2+"
# ---- a second price-impact model, for the stake questions only (sensitivity): the other traders' SOL amounts fixed
# instead of their token amounts. pnl_s() keeps their tokens fixed, so every later buyer pays more SOL because our buy
# moved the price, and our exit gets that back: it flatters a bigger stake. Here the curve's SOL at the exit is the
# tape's plus our SOL in, so our own impact is not repaid by the traders behind us.
def curve_solfixed(en, ex, stake):
    v0, t0 = en; k = v0 * t0; s_in = stake * 1e9 / (1 + FEE); q = t0 - k / (v0 + s_in)
    vr, tr = ex; kx = vr * tr; v1 = vr + s_in; t1 = kx / v1
    out = (v1 - kx / (t1 + q)) * (1 - FEE)
    return out / 1e9 - stake
def legs_impact(r, stake=0.5, prem=0.05, hold_fn=None, D_list=None, impact="token"):
    if impact == "token": return legs(r, stake, prem, hold_fn, D_list)
    hold_fn = hold_fn or H_live; out = []
    for D in (D_list or dec):
        en = entry_at(r, D)
        if not en: continue
        if (en[0] / en[1]) / r["hisp"] - 1 > prem: out.append(("ref", 0.0)); continue
        ex = exit_at(r["seq"], r["cs"], max(hold_fn(r), 1), r["s"])
        if ex and curve_of(en, ex, stake) is not None: out.append(("fill", curve_solfixed(en, ex, stake)))
    return out
SLOT_S = 0.4                                                # seconds a slot (docs: about 0.4 s)
def t_buy(r): return his_buy[r["m"]]["bt"]
def t_exit(r, hold_fn=None):
    b = his_buy[r["m"]]; h = max((hold_fn or H_live)(r), 1)
    return b["bt"] + max(r["cs"] + h - b["slot"], 1) * SLOT_S
# ---- one landing per copy instead of the mean over the 10 D legs: a real copy lands once, so the per-copy mean
# understates the spread of days and drawdowns. sim_risk draws one leg per copy, nsim times.
def leg_nets(r, stake, fix, ref, **kw):
    return [(c - fix) if k == "fill" else -ref for k, c in legs(r, stake, **kw)]
def sim_risk(sel, stake_fn, fix, ref=REF_LIVE, nsim=300, seed=7, **kw):
    rng = random.Random(seed)
    L_ = [(r, leg_nets(r, stake_fn(r), fix, ref, **kw)) for r in sorted(sel, key=t_buy)]
    L_ = [(r, l) for r, l in L_ if l]
    tots, wdays, dds, lows = [], [], [], []
    for _ in range(nsim):
        byd = collections.defaultdict(list)
        for r, l in L_: byd[r["day"]].append(rng.choice(l))
        tot = 0.0; wd = 0.0; dd = 0.0; lo = 0.0
        for d, xs in byd.items():
            run = peak = 0.0
            for x in xs:
                run += x; peak = max(peak, run); dd = min(dd, run - peak); lo = min(lo, run)
            tot += run; wd = min(wd, run)
        tots.append(tot); wdays.append(wd); dds.append(dd); lows.append(lo)
    q = lambda v, p: sorted(v)[int(p * (len(v) - 1))]
    return dict(tot_med=q(tots, 0.5), tot_p05=q(tots, 0.05), tot_p95=q(tots, 0.95), wday_med=q(wdays, 0.5), wday_p05=q(wdays, 0.05),
                dd_med=q(dds, 0.5), dd_p05=q(dds, 0.05), low_med=q(lows, 0.5), low_p05=q(lows, 0.05))
def fmt_risk(x):
    return (f"one landing per copy ({300} draws): 5 days median {x['tot_med']:+.2f} (5-95% {x['tot_p05']:+.2f} .. {x['tot_p95']:+.2f}); "
            f"worst day median {x['wday_med']:+.2f} (5% {x['wday_p05']:+.2f}); worst intraday drawdown median {x['dd_med']:+.2f} (5% {x['dd_p05']:+.2f}); "
            f"lowest running day P&L median {x['low_med']:+.2f} (5% {x['low_p05']:+.2f})")
