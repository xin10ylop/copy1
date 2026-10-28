# Q3a: his SOL flows with other wallets over his whole history, by counterparty and by day.
#   OUT = a System transfer (or createAccount) signed by him to a wallet that is not a relay tip account and not a
#         token / pump account of the same tx; IN = a System transfer to him from another wallet.
# Sources: Triton rows (all successful txs before 2026-09-24 13:11 UTC and all txs since 2026-10-24 00:00 UTC; inner
# CPI transfers of pump / pump AMM / ATA are skipped) + month rows (2026-09-24 13:11 .. 2026-10-24 13:09 UTC).
import json, os, sys, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import norm as N
HIM = N.HIM; REL = N.relays()
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
MLO, MHI = 1790255495, 1792847349
DUST = 100000
flows = []   # (bt, sig, dir, other, lamports, payer, src)
rows = [json.loads(l) for l in open(N.W + "/data/rows.jsonl")]
for r in rows:
    if MLO <= r["bt"] <= MHI or r["err"]: continue
    for s, d, l, inner, k in r["xf"]:
        if inner or l is None: continue
        if s == HIM and d != HIM and d not in REL: flows.append((r["bt"], r["sig"], "out", d, l, r["payer"], "triton", k))
        elif d == HIM and s != HIM: flows.append((r["bt"], r["sig"], "in", s, l, r["payer"], "triton", k))
mrows = [json.loads(l) for l in open(N.W + "/ds/month/AHwJSnFN.jsonl")]
for r in mrows:
    if r["err"]: continue
    mine = [t for t in r["tr"] if t[1] == HIM]
    amts = {650240}
    for t in mine: f = t[9] or 0; amts |= {t[3], f, f // 2, f - f // 2, t[10] or 0}
    trade = bool(mine) or any(p.startswith(("buy", "sell")) for p in r["pix"])
    for s, d, l in r["xf"]:
        if trade and l in amts: continue
        if s == HIM and d != HIM and d not in REL: flows.append((r["bt"], r["sig"], "out", d, l, (r["signers"] or [None])[0], "month", 2))
        elif d == HIM and s != HIM: flows.append((r["bt"], r["sig"], "in", s, l, (r["signers"] or [None])[0], "month", 2))
flows.sort()
big = [f for f in flows if f[4] >= DUST]; dust = [f for f in flows if f[4] < DUST]
print(f"flows >= 0.0001 SOL: {len(big)} (in {sum(1 for f in big if f[2]=='in')}, out {sum(1 for f in big if f[2]=='out')}); dust < 0.0001 SOL: {len(dust)} (in {sum(1 for f in dust if f[2]=='in')}, out {sum(1 for f in dust if f[2]=='out')})")
print(f"total in {sum(f[4] for f in big if f[2]=='in')/1e9:.3f} SOL, total out {sum(f[4] for f in big if f[2]=='out')/1e9:.3f} SOL")
D = collections.defaultdict(lambda: [0, 0, 0, 0])
for f in big:
    k = ts(f[0])[:10]; i = 0 if f[2] == "in" else 2; D[k][i] += 1; D[k][i + 1] += f[4]
print("by day (UTC): date  in_n  in_SOL  out_n  out_SOL")
for k in sorted(D): print(f"  {k} {D[k][0]:4d} {D[k][1]/1e9:9.3f} {D[k][2]:4d} {D[k][3]/1e9:9.3f}")
C = collections.defaultdict(lambda: dict(in_n=0, in_l=0, out_n=0, out_l=0, first=None, last=None, kinds=set()))
for f in big:
    c = C[f[3]]; c["first"] = c["first"] or f[0]; c["last"] = f[0]; c["kinds"].add(f[7])
    if f[2] == "in": c["in_n"] += 1; c["in_l"] += f[4]
    else: c["out_n"] += 1; c["out_l"] += f[4]
print("counterparties:", len(C), "| in-only", sum(1 for c in C.values() if c["in_n"] and not c["out_n"]), "| out-only", sum(1 for c in C.values() if c["out_n"] and not c["in_n"]),
      "| both", sum(1 for c in C.values() if c["out_n"] and c["in_n"]))
print("counterparties with 2+ transfers or both directions, or >= 5 SOL:")
for k, c in sorted(C.items(), key=lambda kv: -(kv[1]["in_l"] + kv[1]["out_l"])):
    if c["in_n"] + c["out_n"] >= 2 or (c["in_n"] and c["out_n"]) or c["in_l"] + c["out_l"] >= 5e9:
        print(f"  {k}  in {c['in_n']:3d} x {c['in_l']/1e9:8.3f}  out {c['out_n']:3d} x {c['out_l']/1e9:8.3f}  {ts(c['first'])[:16]} .. {ts(c['last'])[:16]}")
json.dump(dict(flows=flows, cp={k: dict(v, kinds=sorted(v["kinds"])) for k, v in C.items()}), open(N.W + "/data/flows.json", "w"))
print("first 6 flows:", [(ts(f[0]), f[2], f[3], f[4] / 1e9) for f in big[:6]])
print("last 12 flows >= 0.0001 SOL:", [(ts(f[0]), f[2], f[3][:10], f[4] / 1e9, f[6]) for f in big[-12:]])
