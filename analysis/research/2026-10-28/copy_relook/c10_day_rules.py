# C10. Day rules for the copies, asked Oct 28 ("stop the day at +1 SOL? start/stop times?"): on the copies' own
# timeline (a rule only knows the copies whose exit came before the next buy, as c4), the 5-day 2M copy set at the
# restart's settings (1.0 SOL, the 1.5M bid: fixed 0.0031 a fill) and at the live ones (0.5 SOL, 3M: 0.0046):
#   (a) a daily profit target T: once the realized day P&L reaches T, no more copies that UTC day
#   (b) a trailing day stop X: once the realized day P&L falls X below its peak, no more copies that day
#   (c) hours of the day: the copies' P&L by UTC hour (Beirut = UTC + 2) and by 4-hour block, his own buys by hour;
#       the only honest test: pick the losing blocks on P1 (Oct 21-23), score them on P2 (Oct 24-25)
# Each copy's net is the mean over its 10 landings (deterministic path), and then one landing per copy drawn 300
# times (the spread a real day has). The live him table (check.sh, Oct 26-27, real OUR NET) walked the same way.
# python3 -I c10_day_rules.py <live_rows.json from live_parse.py>
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
def copies(stake, fix):
    out = []
    for r in LIVE2:
        ls = legs(r, stake)
        if not ls: continue
        v = agg(ls, fix, REF_LIVE)
        out.append(dict(tb=t_buy(r), te=t_exit(r), day=r["day"], net=v["net"], legs=leg_nets(r, stake, fix, REF_LIVE), m=r["m"]))
    return sorted(out, key=lambda c: c["tb"])
def live_copies(path):
    out = []
    for x in json.load(open(path)):
        if x["bot"] != "COPIED" or x.get("result") not in ("filled", "refused"): continue
        hh, mm, ss = map(int, x["t"].split(":")); dd = int(x["day"][3:])
        tb = datetime.datetime(2026, 10, dd, hh, mm, ss, tzinfo=datetime.timezone(datetime.timedelta(hours=2))).timestamp()
        held = x.get("held") or 0
        utc = datetime.datetime.fromtimestamp(tb, datetime.timezone.utc).strftime("%m-%d")
        out.append(dict(tb=tb, te=tb + max(held, 1) * SLOT_S, day=utc, net=x["ours"], legs=[x["ours"]], m=x["coin"], its=x["its"]))
    return sorted(out, key=lambda c: c["tb"])
def walk(cs, rule, X, nets=None):
    """copies in buy order; realized = the day's copies whose exit came before this buy. returns (taken, skipped)"""
    taken, skipped = [], []; stopped = set()
    for i, c in enumerate(cs):
        n = nets[i] if nets else c["net"]
        if c["day"] in stopped: skipped.append((c, n)); continue
        known = [(x, m) for x, m in taken if x["day"] == c["day"] and x["te"] < c["tb"]]
        run = peak = 0.0
        for x, m in sorted(known, key=lambda t: t[0]["te"]):
            run += m; peak = max(peak, run)
        if rule == "target" and run >= X: stopped.add(c["day"]); skipped.append((c, n)); continue
        if rule == "trail" and peak > 0 and run <= peak - X: stopped.add(c["day"]); skipped.append((c, n)); continue
        taken.append((c, n))
    return taken, skipped
def report(lab, cs, rules, draws=300):
    days = sorted({c["day"] for c in cs})
    base = sum(c["net"] for c in cs); bd = collections.defaultdict(float)
    for c in cs: bd[c["day"]] += c["net"]
    print(f"\n== {lab}: {len(cs)} copies, net {base:+.2f}; by day " + " ".join(f"{d} {bd[d]:+.2f}" for d in days))
    print(f"   {'rule':28} {'skips':>5} {'forgone':>8} {'-> total':>9}  by day" + " " * (6 * len(days) - 6) + "  one landing per copy: median [5%..95%] of the change")
    rng = random.Random(3)
    for rule, X, nm in rules:
        tk, sk = walk(cs, rule, X)
        bdr = collections.defaultdict(float)
        for c, n in tk: bdr[c["day"]] += n
        forg = sum(n for _, n in sk)
        ch = []
        for _ in range(draws):
            nets = [rng.choice(c["legs"]) for c in cs]
            t2, s2 = walk(cs, rule, X, nets)
            ch.append(-sum(n for _, n in s2))
        ch.sort(); q = lambda p: ch[int(p * (len(ch) - 1))]
        print(f"   {nm:28} {len(sk):5d} {forg:+8.3f} {sum(n for _, n in tk):+9.3f}  " + " ".join(f"{bdr[d]:+5.2f}" for d in days)
              + f"   {q(0.5):+.3f} [{q(0.05):+.3f} .. {q(0.95):+.3f}]")
RULES_1 = [("target", t, f"(a) day target +{t:.2f}") for t in (0.5, 1.0, 1.5, 2.0, 3.0)] + [("trail", x, f"(b) trailing stop -{x:.2f}") for x in (0.5, 1.0, 1.5)]
RULES_05 = [("target", t, f"(a) day target +{t:.2f}") for t in (0.25, 0.5, 0.75, 1.0, 1.5)] + [("trail", x, f"(b) trailing stop -{x:.2f}") for x in (0.25, 0.5, 0.75)]
C1 = copies(1.0, fixed_of(1.5)); C05 = copies(0.5, fixed_of(3.0))
report("5-day backtest at the restart's settings: 1.0 SOL, 1.5M bid", C1, RULES_1)
report("5-day backtest at the live settings: 0.5 SOL, 3M bid", C05, RULES_05)
LV = live_copies(sys.argv[1])
report("live, check.sh him table (Oct 26 13:00 - Oct 27 07:50 UTC), real OUR NET at 0.5", LV, RULES_05, draws=1)
# (c) hours
def hour(c, tz=0): return int(datetime.datetime.fromtimestamp(c["tb"], datetime.timezone(datetime.timedelta(hours=tz))).strftime("%H"))
print("\n== (c) the copies by hour of the day (restart settings, 1.0 SOL): UTC hour (Beirut = +2), n copies, net, by day; his landed launch buys that hour (all keys, 5 days)")
his_h = collections.Counter(int(datetime.datetime.fromtimestamp(his_buy[r["m"]]["bt"], datetime.timezone.utc).strftime("%H")) for r in rows if r["m"] in his_buy)
byh = collections.defaultdict(list)
for c in C1: byh[hour(c)].append(c)
for h in range(24):
    cs = byh.get(h, []); bd = collections.defaultdict(float)
    for c in cs: bd[c["day"]] += c["net"]
    print(f"   {h:02d} UTC ({(h + 2) % 24:02d} Beirut)  copies {len(cs):3d}  net {sum(c['net'] for c in cs):+6.2f}  "
          + " ".join(f"{bd.get(d, 0.0):+5.2f}" for d in DAYS) + f"   his buys {his_h.get(h, 0):3d}")
print("\n== (c) by 4-hour block (UTC): P1 (Oct 21-23) and P2 (Oct 24-25), each also without its best 2 copies")
blk = lambda c: hour(c) // 4
for b in range(6):
    cs = [c for c in C1 if blk(c) == b]; p1 = [c["net"] for c in cs if c["day"] in P1]; p2 = [c["net"] for c in cs if c["day"] in P2]
    print(f"   {4 * b:02d}-{4 * b + 3:02d} UTC ({(4 * b + 2) % 24:02d}-{(4 * b + 5) % 24:02d} Beirut)  n {len(cs):3d}  P1 {sum(p1):+6.2f} [{without_best(p1):+6.2f}] on {len(p1):3d}   P2 {sum(p2):+6.2f} [{without_best(p2):+6.2f}] on {len(p2):3d}")
bad = [b for b in range(6) if sum(c["net"] for c in C1 if blk(c) == b and c["day"] in P1) < 0]
p2_bad = [c["net"] for c in C1 if blk(c) in bad and c["day"] in P2]
print(f"   blocks losing on P1: {[f'{4 * b:02d}-{4 * b + 3:02d}' for b in bad]} -> skipping them on P2 changes P2 by {-sum(p2_bad):+.2f} on {len(p2_bad)} copies [w/o their best 2: {-without_best(p2_bad):+.2f}]")
worst = sorted(range(6), key=lambda b: sum(c["net"] for c in C1 if blk(c) == b and c["day"] in P1))[:2]
p2_w = [c["net"] for c in C1 if blk(c) in worst and c["day"] in P2]
print(f"   the 2 worst P1 blocks: {[f'{4 * b:02d}-{4 * b + 3:02d}' for b in worst]} -> skipping them on P2 changes P2 by {-sum(p2_w):+.2f} on {len(p2_w)} copies")
print("\n== (c) live copies by Beirut hour: n, our net (0.5 SOL), his net on the same coins")
bl = collections.defaultdict(list)
for c in LV: bl[hour(c, 2)].append(c)
for h in sorted(bl):
    cs = bl[h]
    print(f"   {h:02d} Beirut ({(h - 2) % 24:02d} UTC)  copies {len(cs):3d}  ours {sum(c['net'] for c in cs):+6.3f}  his {sum(c['its'] for c in cs):+6.2f}")
