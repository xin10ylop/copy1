# C8. Our bid: the fixed cost per filled copy, and what the bid buys in landing.
#   1. fixed cost by bid: the live fees column = the bid + 0.0016 (live_parse.py: 3.0M 0.00465, 8.0M 0.00958 a fill).
#   2. what the bid bought live, on our copies of him: check.sh's bid per copy matched to the live tapes (refused/tape;
#      Oct 26 04:34 - Oct 27 00:22 UTC): the share landing in his slot and the positions behind him there.
#   3. what our tip bought in the 5-day data (our at-create fires, not copies: walk_4g49xG + bids.json): positions after
#      the create, by our tip.
#   4. the value of a landing distance on the 2M copy set (tipworth.py's method: every copy D positions behind him, his
#      slot), and the break-even extra tip per filled copy against our measured deciles; then each bid's net with its
#      fixed cost, at the landing it was measured to buy (3M, 8M) or at the 3M landing (1.0M, 1.5M: not measured).
# python3 -I c8_bid.py OUTDIR/live_rows.json OUTDIR/live_landing.json
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "base.py")).read())
LL = json.load(open(sys.argv[2]))
print("== 1. fixed cost per filled copy = bid + 0.0016 (live mean of fees - bid over 125 fills)")
for b in (1.0, 1.5, 3.0, 8.0): print(f"   bid {b:.1f}M: {fixed_of(b):.4f} SOL a fill; over the 5-day set's 232 fills {232 * fixed_of(b):.2f} SOL")
print("\n== 2. live, our copies of him by our bid (paste bid x live tape landing)")
LR = json.load(open(sys.argv[1]))
mine = json.load(open(SP + "/refused/live.json"))["mine"]; pref = collections.defaultdict(list)
for m in mine: pref[m[:8]].append(m)
by = collections.defaultdict(lambda: dict(n=0, same=0, pos=[], nxt=[]))
for x in LR:
    if x["bot"] != "COPIED" or x.get("result") not in ("filled", "refused") or not x.get("bid"): continue
    ms = pref.get(x["coin"], [])
    if len(ms) != 1 or not os.path.exists(f"{SP}/refused/tape/{ms[0]}.json"): continue
    d = json.load(open(f"{SP}/refused/tape/{ms[0]}.json")); c0 = d["c0"]
    hb = [y for y in d["rows"] if y[2] == A and y[3] == 1 and y[0] <= c0 + 1]
    if not hb: continue
    h = min(hb, key=lambda y: (y[0], y[1])); a0 = min(mine[ms[0]], key=lambda a: (a["slot"], a["idx"] or 0))
    g = by[x["bid"]]; g["n"] += 1
    if a0["slot"] == h[0]: g["same"] += 1; g["pos"].append((a0["idx"] or 0) - h[1])
    elif a0["slot"] == h[0] + 1: g["nxt"].append(a0["idx"] or 0)
for b, g in sorted(by.items()):
    print(f"   bid {b:.1f}M: {g['n']} copies with a tape; in his slot {g['same']} ({g['same'] / g['n']:.0%}), positions behind him there: median "
          f"{st.median(g['pos']) if g['pos'] else None}, mean {st.mean(g['pos']) if g['pos'] else 0:.0f}; next slot {len(g['nxt'])}, index median {st.median(g['nxt']) if g['nxt'] else None}")
print("   check.sh TIP TEST (him, from Oct 26 18:20 Beirut): 3.0M 56 copies, in its slot 36, d_avg 156; 8.0M 79 copies, in its slot 52, d_avg 149")
print("\n== 3. the 5-day data: our at-create fires by our tip (landed or failed 6042 at create + 0/1)")
crm = {m: (d["cs"], d["create"]["idx"]) for m, d in coins.items()}
Bd = json.load(open(SP + "/dec/five/bids.json"))
g3 = collections.defaultdict(lambda: dict(c0=[], c1=0))
for r in W[US]:
    if r["kind"] != "buy" or r["m"] not in crm or not (r["ok"] or r.get("code") == 6042): continue
    b = Bd.get(r["sig"])
    if not b: continue
    cs, ci = crm[r["m"]]; t = round(b[0] / 1e6, 1)
    if r["slot"] == cs: g3[t]["c0"].append(r["idx"] - ci)
    elif r["slot"] == cs + 1: g3[t]["c1"] += 1
for t in sorted(g3):
    g = g3[t]; n = len(g["c0"]) + g["c1"]
    if n < 20: continue
    xs = sorted(g["c0"])
    print(f"   our tip {t:4.1f}M: {n:4d} landings; in the create slot {len(xs) / n:.0%}, positions after the create: median {st.median(xs) if xs else None}, "
          f"p25 {xs[len(xs) // 4] if xs else None}, p75 {xs[3 * len(xs) // 4] if xs else None}")
print("\n== 4. the 2M copy set, 0.5 SOL: value by landing distance (his slot), live 3M fixed cost")
def tot(D_list, fix):
    it = [(r, value(r, 0.5, fix, REF_LIVE, D_list=D_list)) for r in LIVE2]; it = [(r, v) for r, v in it if v]
    return sum(v["net"] for _, v in it), sum(v["fill"] for _, v in it)
B0, F0 = tot(dec, fixed_of(3.0))
print(f"   measured deciles {dec}: {B0:+.2f} SOL, {F0:.0f} fills")
for D in (0, 5, 10, 20, 45, 90, 125, 150, 200):
    T_, F_ = tot([D], fixed_of(3.0))
    print(f"   D = {D:3d}: {T_:+6.2f}  fills {F_:5.0f}  gain vs measured {T_ - B0:+.2f}  break-even extra tip {(T_ - B0) / max(F_, 1) * 1e3:+.1f}M a filled copy")
for sh in (7, 20):
    T_, F_ = tot([max(d - sh, 0) for d in dec], fixed_of(3.0))
    print(f"   every decile {sh} positions closer: {T_:+.2f} (gain {T_ - B0:+.2f}, {(T_ - B0) / max(F_, 1) * 1e3:+.2f}M a fill: what {sh} positions are worth)")
print("\n   each bid at its landing (the live mix: his slot at the live positions, share p next slot; recon.py section 3):")
p = LL["p_next"]
def entry_next(r, j):
    b = his_buy[r["m"]]; ns = b["slot"] + 1
    xs = [x for x in r["seq"] if (x[0], x[1]) <= (ns, j)] if ns <= r["cs"] + 1 else [x for x in r["seq"] if x[0] <= ns]
    return (xs[-1][2], xs[-1][3]) if xs else None
def H_next(r): return max(H_live(r), his_buy[r["m"]]["slot"] + 2 - r["cs"])
def mixed(fix, Dsame, pn):
    it = []
    for r in LIVE2:
        a = value(r, 0.5, fix, REF_LIVE, D_list=Dsame)
        n_ = value(r, 0.5, fix, REF_LIVE, D_list=LL["LNEXT"], entry_fn=entry_next, hold_fn=H_next)
        if a and n_: it.append((r, {k: (1 - pn) * a[k] + pn * n_[k] for k in a}))
    return it
for b, lab in ((1.0, "1.0M (landing assumed = the live 3M/8M mix; not measured)"), (1.5, "1.5M (same assumption)"),
               (3.0, "3.0M"), (8.0, "8.0M (7 positions closer: TIP TEST d_avg 149 vs 156)")):
    Ds = [max(d - 7, 0) for d in LL["LSAME"]] if b == 8.0 else LL["LSAME"]
    line(lab, mixed(fixed_of(b), Ds, p))
print("\n   each live bid at the landing measured for it on the tapes (section 2; small samples):")
def dec10(v):
    v = sorted(v); return [v[int(len(v) * q)] for q in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95)]
for b in (3.0, 8.0):
    g = by[b]; pn = 1 - g["same"] / g["n"]
    Ds = dec10(g["pos"]); Ln = dec10(g["nxt"])
    it = []
    for r in LIVE2:
        a = value(r, 0.5, fixed_of(b), REF_LIVE, D_list=Ds)
        n_ = value(r, 0.5, fixed_of(b), REF_LIVE, D_list=Ln, entry_fn=entry_next, hold_fn=H_next)
        if a and n_: it.append((r, {k: (1 - pn) * a[k] + pn * n_[k] for k in a}))
    line(f"{b:.1f}M: next slot {pn:.0%}, his-slot D {Ds[4]}-{Ds[5]} mid", it)
