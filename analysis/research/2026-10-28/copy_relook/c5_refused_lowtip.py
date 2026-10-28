# C5. (a) One untested second copy: after a refusal, buy again only when his tip >= 8M AND the price at the refusal
# was within 10% of his price AND the second buy still lands at create + 1 (his buy at create + 0; create + 1 is the
# last slot the tapes hold in full), with a short hold (sold at create + 5). The second buy lands D' positions into
# create + 1 (the live next-slot landings, recon.py -> live_landing.json), bound his price + 10% (and + 5% as a check);
# a refused second buy costs 0.000015. Only the refused landings of the 2M copy set get it; its value is weighted by
# the refused share of the copy's 10 landings.
# (b) His low-tip buys the key skips (tip < 2M, size < 2 SOL), keyed on size >= 1.0 SOL AND tip >= 1.5M, operator rule
# kept: copied at 0.5 and 1.0 SOL (5% bound, H - 1). Also the wider 1.0-1.8M group by size, for context.
# Live 3M costs everywhere. P1 Oct 21-23, P2 Oct 24-25, [without the best 2].
# python3 -I c5_refused_lowtip.py OUTDIR/live_landing.json
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "base.py")).read())
LL = json.load(open(sys.argv[1])); LNEXT = LL["LNEXT"]
FIX = fixed_of(3.0)
print("== (a) a second copy after a refusal (tip >= 8M, refusal price <= his + 10%, lands at create + 1, sold at create + 5)")
def second(r, bound, hold_to):
    b = his_buy[r["m"]]
    if b["slot"] != r["cs"] or r["tip"] < 8e6: return None
    ls = [D for D in dec if entry_at(r, D) and (entry_at(r, D)[0] / entry_at(r, D)[1]) / r["hisp"] - 1 > 0.05]
    if not ls: return None
    elig = [D for D in ls if (entry_at(r, D)[0] / entry_at(r, D)[1]) / r["hisp"] - 1 <= 0.10]
    if not elig: return None
    vs = []
    for j in LNEXT:
        xs = [x for x in r["seq"] if (x[0], x[1]) <= (r["cs"] + 1, j)]
        en = (xs[-1][2], xs[-1][3]) if xs else None
        if not en: continue
        if (en[0] / en[1]) / r["hisp"] - 1 > bound: vs.append(-REF_LIVE); continue
        ex = exit_at(r["seq"], r["cs"], hold_to(r), r["s"])
        c = curve_of(en, ex, 0.5) if ex else None
        if c is not None: vs.append(c - FIX)
    if not vs: return None
    w = len(elig) / len([D for D in dec if entry_at(r, D)])          # the share of landings this rule re-buys
    return dict(net=w * sum(vs) / len(vs), w=w)
for bound in (0.10, 0.05):
    for hl, hf in (("create + 5", lambda r: 5), ("H - 1", lambda r: max(H_live(r), 2))):
        it = [(r, second(r, bound, hf)) for r in LIVE2]
        it = [(r, v) for r, v in it if v]
        lab = f"bound +{bound:.0%}, sold {hl}" + ("  (the rule as specified)" if bound == 0.10 and hl == "create + 5" else "")
        line(lab, it, extra=f"  re-bought landings {sum(v['w'] for _, v in it):.1f}")
print("\n== (b) his low-tip buys: tip < 2M and size < 2 SOL, operator rule kept (>= 2 in 24 h)")
LOW = [r for r in rows if HOT(r) and r["tip"] < 2e6 and r["sol"] < 2.0]
print(f"   {len(LOW)} such buys; tips: {dict(sorted(collections.Counter(round(r['tip'] / 1e6, 1) for r in LOW).items()))}")
for lab, f in (("size >= 1.0 AND tip >= 1.5M", lambda r: r["sol"] >= 1.0 and r["tip"] >= 1.5e6),
               ("size >= 1.0, any tip", lambda r: r["sol"] >= 1.0),
               ("tip 1.5-1.8M, any size", lambda r: r["tip"] >= 1.5e6),
               ("all of them", lambda r: True)):
    sel = [r for r in LOW if f(r)]
    print(f"  {lab}: {len(sel)} buys, his net {sum(r['his'] for r in sel):+.2f}")
    for s in (0.5, 1.0):
        line(f"copy at {s} SOL", [(r, value(r, s, FIX, REF_LIVE)) for r in sel])
print("\n   the size of his 1.5-1.8M-tip buys (all signers, no operator rule): " + str(dict(sorted(collections.Counter(round(r['sol'], 2) for r in rows if 1.5e6 <= r['tip'] < 2e6).items()))))
ALL = [r for r in rows if 1.5e6 <= r["tip"] < 2e6 and r["sol"] >= 1.0]
print(f"   size >= 1.0 AND tip 1.5-1.8M without the operator rule: {len(ALL)} buys, his net {sum(r['his'] for r in ALL):+.2f}")
for s in (0.5, 1.0):
    line(f"copy at {s} SOL (no operator rule)", [(r, value(r, s, FIX, REF_LIVE)) for r in ALL])
