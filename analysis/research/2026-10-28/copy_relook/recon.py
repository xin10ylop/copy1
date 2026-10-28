# Part B: the live copy against the 5-day backtest. The same copy set as ablate.py's +8.02 (his tip >= 2M or size >= 2 SOL,
# >= 2 of his buys on the signer in 24 h, 5% bound, sold at H - 1), with
#   1. the stake ladder x our bid, the curve P&L split from the fixed cost per filled copy (live fees: bid + 0.0016);
#   2. where the copy lands: his slot (the backtest: D positions behind him, D = our measured deciles) or the next slot
#      (D' positions into it, D' = the live next-slot landings of our copies of him), split by his buy slot;
#   3. the backtest re-run with the landing measured live (refused/live.json + refused/tape: position behind him when in
#      his slot, the share landing a slot later, D' there).
# python3 -I recon.py OUTDIR   (writes OUTDIR/live_landing.json, which c5 and c8 read)
# Price impact: the constant-product curve. Our buy of `stake` moves the price we pay (tokens q = t0 - k / (v0 + s_in)),
# our tokens stay in the curve until the exit (the exit state is the tape's, shifted by our q: out = vr q / (tr - q)),
# 1.25% pump fee each way. Other traders' amounts are taken from the tape unchanged (they do not react to our size).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
STAKES = (0.25, 0.3, 0.5, 0.75, 1.0, 1.5)
BIDS = (3.0, 8.0)
# ---- the live landings of our copies of him (Oct 26 04:34 - Oct 27 00:22 UTC, the 60-slot tapes of refused/)
mine = json.load(open(SP + "/refused/live.json"))["mine"]
same, nxt, offs = [], [], collections.Counter()
for m, atts in mine.items():
    p = f"{SP}/refused/tape/{m}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p)); c0 = d["c0"]
    hb = [x for x in d["rows"] if x[2] == A and x[3] == 1 and x[0] <= c0 + 1]
    if not hb: continue
    h = min(hb, key=lambda x: (x[0], x[1])); a0 = min(atts, key=lambda a: (a["slot"], a["idx"] or 0))
    if a0.get("code") not in (None, "6042"): continue
    off = a0["slot"] - h[0]; offs[off] += 1
    if off == 0: same.append((a0["idx"] or 0) - h[1])
    elif off == 1: nxt.append(a0["idx"] or 0)
def deciles(v):
    v = sorted(v); return [v[int(len(v) * q)] for q in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95)]
LSAME, LNEXT = deciles(same), deciles(nxt)
p_next = sum(n for o, n in offs.items() if o >= 1) / sum(offs.values())
print(f"live landings of our copies of him (landed or refused, with a tape): {sum(offs.values())}; slot offset {dict(sorted(offs.items()))}; "
      f"a slot or more later {p_next:.0%}")
print(f"   in his slot, positions behind him: median {st.median(same)}  deciles {LSAME}")
print(f"   the next slot, our index in it:    median {st.median(nxt)}  deciles {LNEXT}")
print(f"   the backtest's D (our 5-day at-create landings, positions after the create): deciles {dec}")
def entry_next(r, j, pess=True):
    """our copy lands in his slot + 1 at index j. His create + 0 buys: create + 1 is fully on the tape. His create + 1
    buys: create + 2 has only its closing trade, so the end of create + 2 (pess) or the end of his slot (optimistic)."""
    b = his_buy[r["m"]]; ns = b["slot"] + 1
    if ns <= r["cs"] + 1:
        xs = [x for x in r["seq"] if (x[0], x[1]) <= (ns, j)]
    else:
        xs = [x for x in r["seq"] if x[0] <= (ns if pess else b["slot"])]
    return (xs[-1][2], xs[-1][3]) if xs else None
def H_next(r):
    b = his_buy[r["m"]]; h = H_live(r)
    return max(h, b["slot"] + 2 - r["cs"])          # never sell before the slot after our landing
def entry_same_live(r, D): return entry_at(r, D)
OUTD = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
json.dump(dict(LSAME=LSAME, LNEXT=LNEXT, p_next=p_next), open(os.path.join(OUTD, "live_landing.json"), "w"))
print("\n== 1. the stake x our bid (the 2M copy set as ablate.py: 298 copies, our measured D, his slot)")
print("   fixed cost per filled copy: model 0.00352; live 3.0M 0.0046, 8.0M 0.0096 (bid + 0.0016). A refused copy: 0.000015 live.")
print(f"   {'stake':>5} {'bid':>4} {'curve':>7} {'fixed':>6} {'refused':>7} {'net':>7} {'worst day':>9} {'/copy':>7} {'/filled':>8}  by day " + " ".join(DAYS))
tab = {}
for s in STAKES:
    L_ = [(r, legs(r, s)) for r in LIVE2]
    L_ = [(r, l) for r, l in L_ if l]
    for lab, fx, rf in (("model", MODEL_FIX, REF_MODEL),) + tuple((f"{b:.0f}M", fixed_of(b), REF_LIVE) for b in BIDS):
        it = [(r, agg(l, fx, rf)) for r, l in L_]
        cur = sum(v["curve"] for _, v in it); fxx = sum(v["fixed"] for _, v in it); rff = sum(v["ref"] for _, v in it)
        nf = sum(v["fill"] for _, v in it); net = sum(v["net"] for _, v in it); bd = by_day(it)
        tab[(s, lab)] = dict(net=net, worst=min(bd.values()), per=net / len(it), curve=cur, fixed=fxx, n=len(it), nf=nf)
        print(f"   {s:5.2f} {lab:>5} {cur:+7.2f} {fxx:6.2f} {rff:7.3f} {net:+7.2f} {min(bd.values()):+9.2f} {net / len(it):+7.4f} {net / nf:+8.4f}  " + " ".join(f"{bd[d]:+5.2f}" for d in DAYS))
print(f"   fills per copy {nf / len(it):.2f}; curve per filled copy at 0.5 SOL: {tab[(0.5, '3M')]['curve'] / tab[(0.5, '3M')]['nf']:+.4f}; "
      f"break-even stake (curve per filled copy = fixed) is where the curve per SOL staked x stake = bid + 0.0016:")
for b in BIDS:
    for s in STAKES:
        t = tab[(s, f"{b:.0f}M")]
        if t["net"] > 0: print(f"     bid {b:.0f}M: the smallest positive stake on the ladder is {s} SOL (net {t['net']:+.2f})"); break
print("\n   the same, split by period (P1 Oct 21-23, P2 Oct 24-25) and without each period's best 2 copies [in brackets]:")
for s in STAKES:
    L_ = [(r, legs(r, s)) for r in LIVE2]
    for b in BIDS:
        line(f"stake {s:.2f}, bid {b:.0f}M", [(r, agg(l, fixed_of(b), REF_LIVE)) for r, l in L_ if l])
print("\n   the brief's fixed costs (0.0045 at 3M, 0.0095 at 8M: the paste's median fees) at 0.3 and 0.5 SOL:")
for s in (0.3, 0.5):
    L_ = [(r, legs(r, s)) for r in LIVE2]
    for fx in (0.0045, 0.0095):
        line(f"stake {s:.2f}, fixed {fx:.4f}", [(r, agg(l, fx, REF_LIVE)) for r, l in L_ if l])
print("\n== 1b. the same ladder with the other price-impact model (the traders behind us keep their SOL, not their tokens)")
print(f"   {'stake':>5} {'bid':>4} {'curve':>7} {'net':>7} {'worst day':>9} {'/copy':>7}   token-fixed net (the scripts' model)")
for s in STAKES:
    L_ = [(r, legs_impact(r, s, impact="sol")) for r in LIVE2]
    L_ = [(r, l) for r, l in L_ if l]
    for b in BIDS:
        it = [(r, agg(l, fixed_of(b), REF_LIVE)) for r, l in L_]
        net = sum(v["net"] for _, v in it); bd = by_day(it)
        print(f"   {s:5.2f} {b:3.0f}M {sum(v['curve'] for _, v in it):+7.2f} {net:+7.2f} {min(bd.values()):+9.2f} {net / len(it):+7.4f}   {tab[(s, f'{b:.0f}M')]['net']:+7.2f}")
print("\n== 2. where the copy lands, by his buy slot (0.5 SOL, live 3M cost 0.0046, refused 0.000015)")
def vset(sel, entry_fn, D_list, hold_fn=None, fix=fixed_of(3.0)):
    return [(r, value(r, 0.5, fix, REF_LIVE, D_list=D_list, entry_fn=entry_fn, hold_fn=hold_fn)) for r in sel]
for slab, sel in (("all", LIVE2), ("his buy at create + 0", [r for r in LIVE2 if his_buy[r["m"]]["slot"] == r["cs"]]),
                  ("his buy at create + 1", [r for r in LIVE2 if his_buy[r["m"]]["slot"] == r["cs"] + 1])):
    print(f" {slab}: {len(sel)} copies, his net {sum(r['his'] for r in sel):+.2f}")
    line("his slot, backtest D (5-day deciles)", vset(sel, entry_at, dec))
    line("his slot, D = live same-slot deciles", vset(sel, entry_at, LSAME))
    line("next slot, D' = live next-slot deciles (pess.)", vset(sel, lambda r, j: entry_next(r, j, True), LNEXT, H_next))
    line("next slot, D' live deciles (c+1 optimistic)", vset(sel, lambda r, j: entry_next(r, j, False), LNEXT, H_next))
print("\n== 3. the backtest with the landing measured live: his slot at the live positions (share 1 - p), the next slot")
print(f"   at the live D' (share p = {p_next:.0%}); 0.5 SOL; costs as live")
for b in BIDS:
    it = []
    for r in LIVE2:
        a = value(r, 0.5, fixed_of(b), REF_LIVE, D_list=LSAME)
        n_ = value(r, 0.5, fixed_of(b), REF_LIVE, D_list=LNEXT, entry_fn=lambda r, j: entry_next(r, j, True), hold_fn=H_next)
        if a is None or n_ is None: continue
        it.append((r, {k: (1 - p_next) * a[k] + p_next * n_[k] for k in a}))
    t = line(f"live landing, bid {b:.0f}M", it)
    print(f"      curve {sum(v['curve'] for _, v in it):+.2f} fixed {sum(v['fixed'] for _, v in it):.2f} fills {sum(v['fill'] for _, v in it):.0f}  per copy {t['tot'] / t['n']:+.4f}")

print("\n== 4. the backtest step by step toward the live setup (0.5 SOL), against the live window's per-fill numbers")
P_LATE = 0.16                      # c3_sell_late.py: 16 of 100 live sells with a fixed target landed 1+ slot late
LIVE_FIX = 0.8817 / 125            # live fees per fill, both bids (64 fills at 3.0M, 61 at 8.0M)
def hk0(r): return r["H"] if r["listed"] else hold(r) + 1
def step(fix, ref, land_live, late):
    it = []
    for r in LIVE2:
        parts = []
        for hf, wh in ((H_live, 1 - late), (hk0, late)):
            if wh == 0: continue
            if land_live:
                a = value(r, 0.5, fix, ref, D_list=LSAME, hold_fn=hf)
                hn = (lambda r, hf=hf: max(hf(r), his_buy[r["m"]]["slot"] + 2 - r["cs"]))
                n_ = value(r, 0.5, fix, ref, D_list=LNEXT, entry_fn=lambda r, j: entry_next(r, j, True), hold_fn=hn)
                if a is None or n_ is None: parts = None; break
                parts.append((wh, {k: (1 - p_next) * a[k] + p_next * n_[k] for k in a}))
            else:
                a = value(r, 0.5, fix, ref, hold_fn=hf)
                if a is None: parts = None; break
                parts.append((wh, a))
        if parts: it.append((r, {k: sum(w * v[k] for w, v in parts) for k in parts[0][1]}))
    return it
STEPS = (("ablate.py as published (model costs 0.00352, measured D, his slot)", MODEL_FIX, REF_MODEL, False, 0.0),
         ("+ live fixed costs at 3.0M (0.0046 a fill)", fixed_of(3.0), REF_LIVE, False, 0.0),
         ("+ live landing (live positions, 31% next slot)", fixed_of(3.0), REF_LIVE, True, 0.0),
         ("+ 16% of sells one slot late", fixed_of(3.0), REF_LIVE, True, P_LATE),
         ("+ the live bid mix (half the fills at 8.0M: 0.00705 a fill)", LIVE_FIX, REF_LIVE, True, P_LATE))
for lab, fx, rf, ll, lt in STEPS:
    it = step(fx, rf, ll, lt)
    t = line(lab, it)
    nf = sum(v["fill"] for _, v in it); cur = sum(v["curve"] for _, v in it)
    p2 = [(r, v) for r, v in it if r["day"] in P2]; nf2 = sum(v["fill"] for _, v in p2)
    print(f"      fills {nf:.0f}, curve per fill {cur / nf:+.4f}, net per fill {t['tot'] / nf:+.4f};  P2 only: {len(p2)} copies, {nf2:.0f} fills, "
          f"curve per fill {sum(v['curve'] for _, v in p2) / nf2:+.4f}, net per fill {sum(v['net'] for _, v in p2) / nf2:+.4f}")
print("   live (check.sh, Oct 26 13:00 - Oct 27 07:50 UTC): 125 fills, curve +0.8342 (+0.0067 a fill), fees 0.8817 (0.0071 a fill), net -0.0475 (-0.0004 a fill)")
