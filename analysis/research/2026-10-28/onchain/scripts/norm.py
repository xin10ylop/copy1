# Normalised rows for both sources: month rows (Sep 24 13:11 - Oct 24 13:09 UTC, the Oct-24 study's Helius pull, in
# ds/month/AHwJSnFN.jsonl) and our Triton rows (data/rows.jsonl). One row per tx of his signature list.
import json, os, struct, collections
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
SLOTG = "A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp"
TIPS = json.load(open(W + "/ds/rivalpnl/tip_accounts.json"))
def g(h):
    if not h: return None
    b = bytes.fromhex(h); return [struct.unpack_from("<Q", b, o)[0] for o in range(0, min(len(b), 16) - 7, 8)]
def ours():
    out = []
    for l in open(W + "/data/rows.jsonl"):
        r = json.loads(l)
        mine = [(e["mint"], e["buy"], e["sol"], e["tok"]) for e in r["tr"] if e["user"] == HIM]
        k = "buy" if any(p.startswith("buy") for p in r["pix"]) else "sell" if any(p.startswith("sell") for p in r["pix"]) else "other"
        out.append(dict(sig=r["sig"], s=r["s"], bt=r["bt"], err=r["err"], fee=r["fee"], d=r["d"], k=k, mine=mine, tip=r["tip"],
                        prio=(r["fee"] or 0) - 5000 * len(r["signers"]), g=g(r["g_slot"]), payer=r["payer"], src="triton",
                        tipto=list(r["tipto"]), maxcost=(r.get("buyargs") or [None, None])[1]))
    return out
def relays():
    """relay tip accounts: the known list + top-level System-transfer destinations of his pump buy/sell txs seen 3+ times"""
    s = set(TIPS); c = collections.Counter()
    for l in open(W + "/data/rows.jsonl"):
        r = json.loads(l)
        if any(p.startswith(("buy", "sell")) for p in r["pix"]): c.update(r["tipto"])
    return s | {d for d, n in c.items() if n >= 3}
def month():
    R = relays(); out = []
    for l in open(W + "/ds/month/AHwJSnFN.jsonl"):
        r = json.loads(l)
        mine = [(t[0], bool(t[2]), t[3], t[4]) for t in r["tr"] if t[1] == HIM]
        k = ("buy" if mine[0][1] else "sell") if mine else ("buy" if any(p.startswith("buy") for p in r["pix"]) else "sell" if any(p.startswith("sell") for p in r["pix"]) else "other")
        extra = sum(l for s, d, l in r["xf"] if s == HIM and d in R and d not in TIPS)
        gs = next((h for p, h, na in r["calls"] if p == SLOTG), None)
        out.append(dict(sig=r["sig"], s=r["s"], bt=r["bt"], err=r["err"], fee=r["fee"], d=r["d"], k=k, mine=mine, tip=(r["tip"] or 0) + extra,
                        prio=(r["fee"] or 0) - 5000 * len(r["signers"]), g=g(gs), payer=(r["signers"] or [None])[0], src="month", tipto=None, maxcost=None))
    return out
def trips(rows):
    """per coin: first landed buy, its tip / prio / sol, all landed sells; pnl = sum of his balance deltas on the coin's landed txs"""
    by = collections.defaultdict(list)
    for r in sorted(rows, key=lambda r: (r["s"], r["sig"])):
        if r["err"] or not r["mine"] or r["k"] not in ("buy", "sell"): continue
        by[r["mine"][0][0]].append(r)
    T = []
    for m, xs in by.items():
        b = [x for x in xs if x["k"] == "buy"]; s = [x for x in xs if x["k"] == "sell"]
        if not b: continue
        b0 = b[0]; e = [x for x in b0["mine"] if x[1]][0]
        ti = sum(t[3] for x in b for t in x["mine"] if t[1]); to = sum(t[3] for x in s for t in x["mine"] if not t[1])
        T.append(dict(mint=m, bt=b0["bt"], s=b0["s"], sol=e[2], tip=b0["tip"], prio=b0["prio"], g=b0["g"], maxcost=b0["maxcost"], tipto=b0["tipto"],
                      pnl=sum(x["d"] for x in xs) / 1e9, closed=ti > 0 and to >= 0.999 * ti, sells=[x["s"] for x in s], nb=len(b), ns=len(s), sell_tips=[x["tip"] for x in s], sell_prio=[x["prio"] for x in s]))
    return T
