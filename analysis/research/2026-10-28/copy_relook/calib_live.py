# The backtest's model against our real copies of him, coin by coin, on the live tapes (refused/tape: every trade of
# create .. create + 3, each later slot's closing trade, his ATA's trades; our buy and sell are on them for most coins).
# For each filled copy in check.sh's him table that has a tape with our buy and sell on it:
#   real     = check.sh's OUR NET + fees (the curve part, after pump's fee, before tips and fees)
#   chain    = the same from the tape's own trade amounts (our sells' SOL x (1 - 1.25%) - our buy's SOL x (1 + 1.25%))
#   model@real = the backtest's valuation (pnl_s's curve, our tokens left in the curve) at our real entry (the state
#                just before our buy) and our real sell slot, sold at that slot's END (the backtest's exit), the tape
#                taken without our own trades (later reserves corrected for our tokens), at our real stake
#   model@bt = the backtest's own assumptions on the same coin: our buy D positions behind his in his slot (the 5-day
#              deciles), 5% bound (a refused leg is 0), sold at the end of our real sell slot (the box's H - 1 there)
# Also the sell timing (Part C3): our sell slot against his first sell on the coin.
# python3 -I calib_live.py <live_rows.json from live_parse.py>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
R = json.load(open(sys.argv[1]))
mine = json.load(open(SP + "/refused/live.json"))["mine"]
pref = collections.defaultdict(list)
for m in mine: pref[m[:8]].append(m)
def st_(x): return (x[6] if x[6] > 0 else K // x[7], x[7])
out = []; miss = collections.Counter(); timing = collections.Counter(); tim_rows = []
for r in R:
    if r["bot"] != "COPIED" or r.get("result") != "filled": continue
    ms = pref.get(r["coin"], [])
    if len(ms) != 1: miss["no live buy record" if not ms else "prefix not unique"] += 1; continue
    m = ms[0]; p = f"{SP}/refused/tape/{m}.json"
    if not os.path.exists(p): miss["no tape"] += 1; continue
    d = json.load(open(p)); rows = [x for x in d["rows"] if x[7] > 0]; c0 = d["c0"]
    hb = [x for x in rows if x[2] == A and x[3] == 1 and x[0] <= c0 + 1]
    ub = [x for x in rows if x[2] == US and x[3] == 1]; us = [x for x in rows if x[2] == US and x[3] == 0]
    if not hb or not ub: miss["his or our buy not on the tape"] += 1; continue
    h = min(hb, key=lambda x: (x[0], x[1])); b = min(ub, key=lambda x: (x[0], x[1])); q = b[5]
    hs = [x for x in rows if x[2] == A and x[3] == 0]; hs1 = min(hs, key=lambda x: (x[0], x[1])) if hs else None
    sell_slot = (min(us, key=lambda x: (x[0], x[1]))[0] if us else (b[0] + r["held"] if r.get("held") is not None else None))
    if sell_slot is None: miss["no sell slot"] += 1; continue
    # sell timing against his first sell
    if hs1:
        if sell_slot < hs1[0]: tk = "before his first sell's slot"
        elif sell_slot == hs1[0]:
            tk = ("in his sell's slot, before it" if us and (min(us)[0], min(us)[1]) < (hs1[0], hs1[1]) else "in his sell's slot, after it")
        else: tk = "a slot or more after his first sell"
    else: tk = "he did not sell on the tape"
    timing[tk] += 1
    tim_rows.append(dict(coin=r["coin"], tk=tk, ours=r["ours"], sell_off=sell_slot - c0, his_off=(hs1[0] - c0) if hs1 else None,
                         buy_off=b[0] - c0, his_buy_off=h[0] - c0))
    # the tape without us: drop our trades, correct the reserves between our buy and our last sell for our q tokens
    last_us = max(((x[0], x[1]) for x in us), default=(10**12, 0))
    seq = []
    for x in rows:
        if x[2] == US: continue
        v, t = st_(x)
        if (b[0], b[1]) < (x[0], x[1]) < last_us: v, t = v * t // (t + q), t + q
        seq.append((x[0], x[1], v, t, x[2], x[3], x[4]))
    stake = r["stake"]
    en_real = state_before(seq, b[0], b[1])
    s_his = None
    if hs1:
        hv, ht = st_(hs1)
        if (b[0], b[1]) < (hs1[0], hs1[1]) < last_us: hv, ht = hv * ht // (ht + q), ht + q
        s_his = dict(slot=hs1[0], fill=[0, 0, hv, ht])
    ex = exit_at(seq, c0, sell_slot - c0, s_his)
    m_real = curve_of(en_real, ex, stake) if en_real and ex else None
    chain = sum(x[4] for x in us) / 1e9 * (1 - FEE) - b[4] / 1e9 * (1 + FEE) if us else None
    hisp = st_(h)[0] / st_(h)[1]
    legs_ = []
    for D in dec:
        xs = [x for x in seq if (x[0], x[1]) <= (h[0], h[1] + D) and x[0] <= h[0]]
        en = (xs[-1][2], xs[-1][3]) if xs else None
        if not en: continue
        if (en[0] / en[1]) / hisp - 1 > 0.05: legs_.append(0.0); continue
        c = curve_of(en, ex, stake) if ex else None
        if c is not None: legs_.append(c)
    m_bt = sum(legs_) / len(legs_) if legs_ else None
    out.append(dict(coin=r["coin"], day=r["day"], t=r["t"], real=r["curve"], ours=r["ours"], fees=r["fees"], chain=chain,
                    m_real=m_real, m_bt=m_bt, stake=stake, landed=r["landed"], hisbuy=r["hisbuy"], tip=r["tip"], sol=r["sol"]))
print(f"filled copies of him in the paste matched to a live tape: {len(out)}; not matched: {dict(miss)}")
ok = [o for o in out if o["m_real"] is not None and o["chain"] is not None and o["m_bt"] is not None]
print(f"with every valuation: {len(ok)} (Beirut {min(o['day'] + ' ' + o['t'] for o in ok)} .. {max(o['day'] + ' ' + o['t'] for o in ok)})")
def s(k, xs): return sum(o[k] for o in xs)
print(f"   real (check.sh curve) {s('real', ok):+.4f}   chain (tape amounts) {s('chain', ok):+.4f}   model at our real entry and sell slot {s('m_real', ok):+.4f}"
      f"   model with the backtest's landing {s('m_bt', ok):+.4f}")
print(f"   per fill: model@real - real {(s('m_real', ok) - s('real', ok)) / len(ok):+.4f}   model@bt - real {(s('m_bt', ok) - s('real', ok)) / len(ok):+.4f}"
      f"   chain - real {(s('chain', ok) - s('real', ok)) / len(ok):+.4f}   (fees {s('fees', ok):.4f}, real net {s('ours', ok):+.4f})")
for lab, f in (("landed in his slot", lambda o: o["landed"] == "its"), ("landed a slot later", lambda o: o["landed"] != "its"),
               ("his buy create + 0", lambda o: o["hisbuy"] == 0), ("his buy create + 1", lambda o: o["hisbuy"] == 1)):
    xs = [o for o in ok if f(o)]
    if xs: print(f"   {lab:22} n {len(xs):3d} real {s('real', xs):+.4f} model@real {s('m_real', xs):+.4f} model@bt {s('m_bt', xs):+.4f}  "
                 f"(model@bt - real per fill {(s('m_bt', xs) - s('real', xs)) / len(xs):+.4f})")
xs = sorted(ok, key=lambda o: o["m_real"] - o["real"])
print("   largest model@real - real gaps: " + "; ".join(f"{o['coin']} real {o['real']:+.3f} model {o['m_real']:+.3f}" for o in xs[-4:]))
print("   smallest: " + "; ".join(f"{o['coin']} real {o['real']:+.3f} model {o['m_real']:+.3f}" for o in xs[:4]))
print("\n== sell timing (C3): where our sell landed against his first sell on the coin (filled copies with a tape)")
for k, n in timing.most_common():
    xs = [t for t in tim_rows if t["tk"] == k]
    print(f"   {k:40} {n:3d}  our net {sum(t['ours'] for t in xs):+.4f}")
d_ = collections.Counter((t["sell_off"] - t["his_off"]) for t in tim_rows if t["his_off"] is not None)
print("   our sell slot - his first sell slot: " + " ".join(f"{k:+d}:{v}" for k, v in sorted(d_.items())))
print("   our sell slot after the create: " + " ".join(f"+{k}:{v}" for k, v in sorted(collections.Counter(t["sell_off"] for t in tim_rows).items())))
json.dump(dict(rows=out, timing=tim_rows), open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "calib_live.json"), "w"))
