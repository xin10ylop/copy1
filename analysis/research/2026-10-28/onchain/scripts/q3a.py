# Q3a: every SOL movement into or out of his wallet outside pump trades, over his whole history:
#   Triton rows (2025-01-16 .. 2026-09-24 13:11 UTC successful txs, and every tx since 2026-10-24 00:00 UTC)
#   + the Oct-24 study's month rows (2026-09-24 13:11 .. 2026-10-24 13:09 UTC, every tx).
# Also: transfers inside his trade txs that do not go to pump (curve, fee recipients, creator vault) or a relay tip account.
import json, os, sys, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
HIM = N.HIM
REL = N.relays()
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
MLO, MHI = 1790255495, 1792847349
rows = [json.loads(l) for l in open(N.W + "/data/rows.jsonl")]
mrows = [json.loads(l) for l in open(N.W + "/ds/month/AHwJSnFN.jsonl")]
ev = []   # (bt, sig, payer, kind, his_delta, transfers[(src,dst,lamports,inner,kind)], tops, src)
odd_in_trades = []
for r in rows:
    if MLO <= r["bt"] <= MHI: continue
    trade = any(p.startswith(("buy", "sell")) for p in r["pix"])
    if not trade:
        ev.append((r["bt"], r["sig"], r["payer"], "other", r["d"], r["xf"], sorted(set(r["tops"])), "triton", r["err"], r["fee"]))
    else:
        mine = [e for e in r["tr"] if e["user"] == HIM]
        amts = set()
        for e in mine: f = e.get("fee") or 0; amts |= {e["sol"], f, f // 2, f - f // 2, e.get("cfee") or 0}
        for s, d, l, inner, k in r["xf"]:
            if inner:  continue           # pump's own CPI transfers (curve, fees, creator vault, ATA rent)
            if s == HIM and d in REL: continue
            odd_in_trades.append((r["bt"], r["sig"], s, d, l, k))
for r in mrows:
    trade = bool([t for t in r["tr"] if t[1] == HIM]) or any(p.startswith(("buy", "sell")) for p in r["pix"])
    if not trade:
        ev.append((r["bt"], r["sig"], (r["signers"] or [None])[0], "other", r["d"], [[s, d, l, None, 2] for s, d, l in r["xf"]], sorted({c[0] for c in r["calls"]}), "month", r["err"], r["fee"]))
    else:
        mine = [t for t in r["tr"] if t[1] == HIM]
        amts = {650240}
        for t in mine: f = t[9] or 0; amts |= {t[3], f, f // 2, f - f // 2, t[10] or 0}
        for s, d, l in r["xf"]:
            if s == HIM and (d in REL or l in amts): continue
            if d == HIM and l in amts: continue
            odd_in_trades.append((r["bt"], r["sig"], s, d, l, 2))
ev.sort()
print("non-trade transactions in his history:", len(ev))
big = [e for e in ev if abs(e[4]) > 100000 or (e[2] == HIM)]
print("those he paid for, or moving > 0.0001 SOL of his:", len(big))
for e in big:
    xs = [(s[:8], d[:8], l) for s, d, l, *_ in e[5]]
    print(" ", ts(e[0]), e[7], "payer", e[2], "his d", e[4], "fee", e[9], "err", e[8] is not None, "progs", [p[:8] for p in e[6]], "xfers", xs[:6], e[1][:20])
dust = [e for e in ev if e not in big]
print("dust / spam received (other payers, |d| <= 0.0001 SOL):", len(dust), "total", sum(e[4] for e in dust), "lamports; payers", len({e[2] for e in dust}),
      "by month", sorted(collections.Counter(ts(e[0])[:7] for e in dust).items()))
print("unexpected transfers inside trade txs:", len(odd_in_trades))
c = collections.Counter((s == HIM, d if s == HIM else s) for bt, sig, s, d, l, k in odd_in_trades)
for (out, other), n in c.most_common(25):
    ls = [l for bt, sig, s, d, l, k in odd_in_trades if (d if s == HIM else s) == other]
    print("  ", "OUT to" if out else "IN from", other, n, "amounts", collections.Counter(ls).most_common(4), ts(min(bt for bt, sig, s, d, l, k in odd_in_trades if (d if s == HIM else s) == other))[:10])
json.dump(dict(events=ev, odd=odd_in_trades), open(N.W + "/data/q3a.json", "w"))
