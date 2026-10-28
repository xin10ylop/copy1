# The live copies of him (05-live/check-sh-2026-10-27.txt, section "== 1 him", 377 rows), parsed into one record per
# row, then summed: stake (= OUR NET / our %), the fixed cost per filled copy by our bid, the curve P&L (OUR NET + fees),
# and the result by his tip bucket, his size bucket, his buy slot (create + 0 / + 1), our landing slot (his slot / + 1),
# and the slots held. Times are Beirut (UTC+2). Run from the repo root: python3 -I <this> [paste] [out.json]
import re, sys, json, collections, statistics as st
P = sys.argv[1] if len(sys.argv) > 1 else "05-live/check-sh-2026-10-27.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else None
L = open(P).read().splitlines()
a = next(i for i, l in enumerate(L) if l.startswith("== 1 him"))
b = next(i for i, l in enumerate(L) if i > a and l.startswith("== 2 "))
row = re.compile(r"^\s+(\d\d):(\d\d):(\d\d)\s+(\S+)\s+(holding|[+-]\d+\.\d+)\s+(?:([+-]\d+\.\d+)\s+)?(?:([+-]\d+\.\d+)%\s+)?"
                 r"(skip: tip/size low|COPIED|copied, not sent|not seen)\s+(\d+\.\d+)\s+(\d+\.\d+)M(?:\s+\+(\d))?\s*(.*)$")
recs, prev, day = [], None, "10-27"
for l in L[a:b]:
    m = row.match(l)
    if not m: continue
    hh, mm, ss, coin, its, ours, pct, bot, sol, tip, buy, rest = m.groups()
    t = int(hh) * 60 + int(mm)
    if prev is not None and t > prev: day = "10-26"           # newest first: the clock jumps up at midnight
    prev = t
    r = dict(t=f"{hh}:{mm}:{ss}", day=day, coin=coin, its=float(its), ours=float(ours) if ours else None,
             pct=float(pct) / 100 if pct else None, bot=bot, sol=float(sol), tip=float(tip), hisbuy=int(buy) if buy is not None else None)
    toks = rest.split()
    if bot == "COPIED":
        r["result"] = "not landed" if rest.startswith("not landed") else toks[0]
        if r["result"] in ("filled", "refused"):
            r["landed"] = "its" if rest.split()[1] == "its" else rest.split()[1]
            m2 = re.search(r"(its slot|\+\d slot)\s+(\d+)?\s*(\d+)?\s+(\d+\.\d+)M\s+(\d+\.\d+)", rest)
            if m2:
                _, x1, x2, bid, fee = m2.groups()
                r["bid"] = float(bid); r["fees"] = float(fee)
                if r["result"] == "filled":
                    if r["landed"] == "its": r["behind"] = int(x1) if x1 else None; r["held"] = int(x2) if x2 else None
                    else: r["behind"] = None; r["held"] = int(x1) if x1 else None
                else:
                    r["behind"] = int(x1) if (x1 and r["landed"] == "its") else None
            r["exit"] = toks[-1] if r["result"] == "filled" else None
        elif r["result"] == "not":
            r["result"] = "not landed"
        if r["result"] == "not landed":
            m3 = re.search(r"(\d+\.\d+)M", rest); r["bid"] = float(m3.group(1)) if m3 else None
    recs.append(r)
print(f"parsed {len(recs)} rows; by the bot: {collections.Counter(r['bot'] for r in recs)}")
F = [r for r in recs if r["bot"] == "COPIED" and r.get("result") == "filled"]
bad = [r for r in F if "fees" not in r]
print("filled rows without fees parsed:", [(r["t"], r["coin"]) for r in bad])
for r in F:
    r["stake"] = abs(r["ours"] / r["pct"]) if r["pct"] else None
    r["curve"] = r["ours"] + r["fees"]
S = [r["stake"] for r in F if r["stake"]]
print(f"\nfilled copies {len(F)}: stake median {st.median(S):.3f} mean {st.mean(S):.3f} min {min(S):.3f} max {max(S):.3f}; "
      f"stakes < 0.45 SOL: {sum(1 for x in S if x < 0.45)}")
print(f"   OUR NET {sum(r['ours'] for r in F):+.4f} = curve {sum(r['curve'] for r in F):+.4f} - fees {sum(r['fees'] for r in F):.4f}")
print("\nfixed cost (fees column) per filled copy, by our bid:")
for bid in sorted({r["bid"] for r in F}):
    xs = [r for r in F if r["bid"] == bid]
    fe = [r["fees"] for r in xs]
    print(f"   bid {bid:.1f}M: n {len(xs):3d} fees {sum(fe):.4f} mean {st.mean(fe):.5f} median {st.median(fe):.4f} "
          f"(fees - bid: mean {st.mean(fe) - bid / 1000:.5f})  curve {sum(r['curve'] for r in xs):+.4f}  net {sum(r['ours'] for r in xs):+.4f}  "
          f"net/copy {sum(r['ours'] for r in xs) / len(xs):+.4f}  his {sum(r['its'] for r in xs):+.4f}")
def grp(lab, key):
    print(f"\n{lab} (filled copies; his = ITS NET on the same coins):")
    g = collections.defaultdict(list)
    for r in F: g[key(r)].append(r)
    for k in sorted(g):
        xs = g[k]
        print(f"   {k:14} n {len(xs):3d} net {sum(r['ours'] for r in xs):+.4f} curve {sum(r['curve'] for r in xs):+.4f} fees {sum(r['fees'] for r in xs):.4f} "
              f"won {sum(1 for r in xs if r['ours'] > 0):3d} his {sum(r['its'] for r in xs):+.4f}  by day " +
              " ".join(f"{d} {sum(r['ours'] for r in xs if r['day'] == d):+.3f}" for d in ("10-26", "10-27")))
tipb = lambda r: "z <2M (size key)" if r["tip"] < 2.0 else "a 2-4M" if r["tip"] < 4.0 else "b 4.8-7.2M" if r["tip"] < 8.0 else "c 8M+"
sizeb = lambda r: "a <0.7" if r["sol"] < 0.7 else "b 0.7-1.1" if r["sol"] < 1.1 else "c 1.1-2" if r["sol"] < 2.0 else "d 2+"
grp("by his tip", tipb)
grp("by his size", sizeb)
grp("by his buy slot", lambda r: f"create+{r['hisbuy']}")
grp("by our landing slot", lambda r: f"landed {r['landed']}")
grp("his buy slot x our landing", lambda r: f"c+{r['hisbuy']} / {r['landed']}")
grp("by our bid x landing", lambda r: f"{r['bid']:.0f}M / {r['landed']}")
grp("by day", lambda r: r["day"])
H = [r["held"] for r in F if r.get("held") is not None]
print(f"\nslots held: n {len(H)} median {st.median(H)} distribution {sorted(collections.Counter(H).items())}")
dumps = [r for r in F if r["pct"] is not None and r["pct"] <= -0.15]
print(f"filled copies losing >= 15%: {len(dumps)}, net {sum(r['ours'] for r in dumps):+.4f}; >= 30%: "
      f"{sum(1 for r in F if r['pct'] <= -0.30)}, net {sum(r['ours'] for r in F if r['pct'] <= -0.30):+.4f}")
for r in sorted(F, key=lambda r: r["ours"])[:8]:
    print(f"   worst: {r['day']} {r['t']} {r['coin']} ours {r['ours']:+.4f} ({r['pct']:+.1%}) his {r['its']:+.4f} tip {r['tip']}M size {r['sol']} c+{r['hisbuy']} landed {r['landed']} held {r.get('held')} bid {r['bid']}")
R = [r for r in recs if r["bot"] == "COPIED" and r.get("result") == "refused"]
print(f"\nrefused {len(R)}: his {sum(r['its'] for r in R):+.4f}; by landing " + str(collections.Counter(r["landed"] for r in R)))
sk = [r for r in recs if r["bot"] == "skip: tip/size low"]
print(f"skipped tip/size low {len(sk)}: his {sum(r['its'] for r in sk):+.4f}; with size >= 1.0 and tip >= 1.5M: "
      f"{sum(1 for r in sk if r['sol'] >= 1.0 and r['tip'] >= 1.5)} his {sum(r['its'] for r in sk if r['sol'] >= 1.0 and r['tip'] >= 1.5):+.4f}; "
      f"size >= 1.0 any tip: {sum(1 for r in sk if r['sol'] >= 1.0)} his {sum(r['its'] for r in sk if r['sol'] >= 1.0):+.4f}")
print("   skipped by tip: " + "  ".join(f"{t}M n {sum(1 for r in sk if r['tip'] == t)} his {sum(r['its'] for r in sk if r['tip'] == t):+.3f}" for t in sorted({r['tip'] for r in sk})))
if OUT: json.dump(recs, open(OUT, "w"), indent=0)
