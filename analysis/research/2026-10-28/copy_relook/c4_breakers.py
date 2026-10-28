# C4. Circuit breakers for the copies, on the copies' own timeline (a breaker only knows the copies whose exit came
# before the next buy). The 5-day 2M copy set, 0.5 SOL, live 3M costs; and check.sh's live him table (real OUR NET,
# the exit placed at the buy + held slots x 0.4 s).
#   (a) pause 60 min after 3 consecutive filled copies each losing >= 15%
#   (b) pause 60 min after 2 copies dumped >= 30% within 30 min
#   (c) a day stop for the copies alone at -0.5 / -1.0 SOL (UTC day, realized)
#   (d) skip an operator for 3 h after one of its coins dumped >= 30% inside our hold
# A 5-day copy is a mean over its 10 landings; it counts as filled when most of them fill, and its loss is the mean over
# the filled ones. Also: do dumps cluster in time, or by operator? (2,000 label shuffles.)
# python3 -I c4_breakers.py <live_rows.json from live_parse.py>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
FIX = fixed_of(3.0); STAKE = 0.5
C = []
for r in LIVE2:
    ls = legs(r, STAKE)
    if not ls: continue
    v = agg(ls, FIX, REF_LIVE); fl = [c - FIX for k, c in ls if k == "fill"]
    pct = (sum(fl) / len(fl)) / STAKE if fl else None
    C.append(dict(tb=t_buy(r), te=t_exit(r), day=r["day"], net=v["net"], filled=v["fill"] >= 0.5, pct=pct, op=r["signer"], m=r["m"]))
def live_copies(path):
    out = []
    for x in json.load(open(path)):
        if x["bot"] != "COPIED" or x.get("result") not in ("filled", "refused"): continue
        hh, mm, ss = map(int, x["t"].split(":")); dd = int(x["day"][3:])
        tb = datetime.datetime(2026, 10, dd, hh, mm, ss, tzinfo=datetime.timezone(datetime.timedelta(hours=2))).timestamp()
        held = x.get("held") or 0
        utc = datetime.datetime.fromtimestamp(tb, datetime.timezone.utc).strftime("%m-%d")
        f = x["result"] == "filled"
        out.append(dict(tb=tb, te=tb + max(held, 1) * SLOT_S, day=utc, net=x["ours"], filled=f, pct=x["pct"] if f else None, op=None, m=x["coin"]))
    return sorted(out, key=lambda c: c["tb"])
def run(cs, rule, X=None):
    """walk the copies in buy order; return the skipped ones"""
    cs = sorted(cs, key=lambda c: c["tb"]); taken, skipped = [], []; pause_until = -1; op_block = {}
    for c in cs:
        known = sorted([x for x in taken if x["te"] < c["tb"]], key=lambda x: x["te"])
        skip = c["tb"] < pause_until
        if rule == "a" and not skip:
            fk = [x for x in known if x["filled"]]
            if len(fk) >= 3 and all(x["pct"] is not None and x["pct"] <= -0.15 for x in fk[-3:]):
                end = fk[-1]["te"] + 3600
                if c["tb"] < end: skip = True; pause_until = end
        if rule == "b" and not skip:
            dm = [x for x in known if x["filled"] and x["pct"] is not None and x["pct"] <= -0.30]
            if len(dm) >= 2 and dm[-1]["te"] - dm[-2]["te"] <= 1800:
                end = dm[-1]["te"] + 3600
                if c["tb"] < end: skip = True; pause_until = end
        if rule == "c" and not skip:
            if sum(x["net"] for x in known if x["day"] == c["day"]) <= -X: skip = True
        if rule == "d" and not skip and c["op"] is not None:
            for x in known:
                if x["op"] == c["op"] and x["filled"] and x["pct"] is not None and x["pct"] <= -0.30 and c["tb"] < x["te"] + 3 * 3600: skip = True
        (skipped if skip else taken).append(c)
    return taken, skipped
def report(lab, cs):
    base_bd = collections.defaultdict(float)
    for c in cs: base_bd[c["day"]] += c["net"]
    days = sorted(base_bd)
    print(f"\n== {lab}: {len(cs)} copies, net {sum(c['net'] for c in cs):+.3f}; by day " + " ".join(f"{d} {base_bd[d]:+.2f}" for d in days))
    for rl, X, nm in (("a", None, "(a) 3 losses >= 15% in a row -> 60 min"), ("b", None, "(b) 2 dumps >= 30% in 30 min -> 60 min"),
                      ("c", 0.5, "(c) day stop -0.5"), ("c", 1.0, "(c) day stop -1.0"), ("d", None, "(d) operator out 3 h after a dump")):
        if rl == "d" and cs and cs[0]["op"] is None: print(f"   {nm:42} (no operator in the live table)"); continue
        tk, sk = run(cs, rl, X)
        bd = collections.defaultdict(float)
        for c in tk: bd[c["day"]] += c["net"]
        saves = -sum(c["net"] for c in sk if c["net"] < 0); costs = sum(c["net"] for c in sk if c["net"] > 0)
        print(f"   {nm:42} skips {len(sk):3d}  saves {saves:+.3f}  forgoes {costs:+.3f}  net change {saves - costs:+.3f}  -> {sum(c['net'] for c in tk):+.3f}  by day "
              + " ".join(f"{bd[d]:+.2f}" for d in days))
report("5-day backtest (Oct 21-25 UTC)", C)
report("live, check.sh him table (Oct 26 13:00 - Oct 27 07:50 UTC)", live_copies(sys.argv[1]))
# clustering of dumps
print("\n== do dumps (a filled copy losing >= 30%) cluster? 5-day backtest")
F = sorted([c for c in C if c["filled"]], key=lambda c: c["tb"])
lab = [c["pct"] <= -0.30 for c in F]
print(f"   filled copies {len(F)}, dumps {sum(lab)} ({sum(lab) / len(F):.1%}); losses >= 15%: {sum(c['pct'] <= -0.15 for c in F)}")
def stats(lab):
    nxt = sum(1 for i in range(1, len(F)) if lab[i] and lab[i - 1]); prev = sum(1 for i in range(1, len(F)) if lab[i - 1])
    near = sum(1 for i in range(len(F)) if lab[i] and any(lab[j] and abs(F[j]["tb"] - F[i]["tb"]) <= 1800 for j in range(len(F)) if j != i))
    ops = collections.Counter(F[i]["op"] for i in range(len(F)) if lab[i]); rep = sum(v for v in ops.values() if v >= 2)
    return nxt / max(prev, 1), near, rep
p_next, near, rep = stats(lab)
rng = random.Random(11); sims = [stats(rng.sample(lab, len(lab))) for _ in range(2000)]
print(f"   P(dump | the previous filled copy dumped) {p_next:.1%} against the base {sum(lab) / len(F):.1%}; shuffles: median {st.median(s[0] for s in sims):.1%}, "
      f"share of shuffles >= observed {sum(1 for s in sims if s[0] >= p_next) / len(sims):.2f}")
print(f"   dumps with another dump within 30 min: {near}; shuffles median {st.median(s[1] for s in sims)}, share >= observed {sum(1 for s in sims if s[1] >= near) / len(sims):.2f}")
print(f"   dumps on an operator with 2+ dumps: {rep}; shuffles median {st.median(s[2] for s in sims)}, share >= observed {sum(1 for s in sims if s[2] >= rep) / len(sims):.2f}")
L = [c for c in live_copies(sys.argv[1]) if c["filled"]]
ll = [c["pct"] <= -0.30 for c in L]
nx = sum(1 for i in range(1, len(L)) if ll[i] and ll[i - 1]); pv = sum(1 for i in range(1, len(L)) if ll[i - 1])
nr = sum(1 for i in range(len(L)) if ll[i] and any(ll[j] and abs(L[j]["tb"] - L[i]["tb"]) <= 1800 for j in range(len(L)) if j != i))
sims = []
for _ in range(2000):
    s_ = rng.sample(ll, len(ll))
    sims.append(sum(1 for i in range(len(L)) if s_[i] and any(s_[j] and abs(L[j]["tb"] - L[i]["tb"]) <= 1800 for j in range(len(L)) if j != i)))
print(f"   live: filled {len(L)}, dumps {sum(ll)}; P(dump | previous dumped) {nx}/{pv}; dumps with another within 30 min {nr} "
      f"(shuffles median {st.median(sims)}, share >= observed {sum(1 for s in sims if s >= nr) / len(sims):.3f})")
print("   live dumps (Beirut): " + ", ".join(datetime.datetime.fromtimestamp(c["tb"], datetime.timezone(datetime.timedelta(hours=2))).strftime("%d %H:%M") + f" {c['m']} {c['pct']:+.0%}" for c in L if c["pct"] <= -0.30))
