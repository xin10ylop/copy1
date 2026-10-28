# Build his per-coin round trips from data/rows.jsonl (recent: since 2026-10-24 00:00 UTC) -> data/trips.json
import json, collections, struct, os, sys
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
T0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1792800000
rows = [json.loads(l) for l in open(W + "/data/rows.jsonl")]
rows = [r for r in rows if r["bt"] >= T0]; rows.sort(key=lambda r: (r["s"], r["sig"]))
def g(h): b = bytes.fromhex(h); return [struct.unpack_from("<Q", b, o)[0] for o in range(0, len(b) - 7, 8)] if h else None
def kind(r):
    if any(p.startswith("buy") for p in r["pix"]): return "buy"
    if any(p.startswith("sell") for p in r["pix"]): return "sell"
    return "other"
by = collections.defaultdict(list); fails = []
for r in rows:
    r["k"] = kind(r)
    mine = [e for e in r["tr"] if e["user"] == HIM]
    if r["k"] == "buy" and r["err"]: fails.append(r); continue
    if r["k"] in ("buy", "sell") and not r["err"] and mine: by[mine[0]["mint"]].append((r, mine))
trips = []
for m, xs in by.items():
    buys = [(r, e) for r, e in xs if r["k"] == "buy"]; sells = [(r, e) for r, e in xs if r["k"] == "sell"]
    if not buys: continue
    rb, eb = buys[0]; e0 = [e for e in eb if e["buy"]][0]
    gl = g(rb["g_slot"]); gs = g(rb["g_state"])
    tok_in = sum(e["tok"] for r, es in buys for e in es if e["buy"]); tok_out = sum(e["tok"] for r, es in sells for e in es if not e["buy"])
    t = dict(mint=m, bt=rb["bt"], buy_slot=rb["s"], buy_sig=rb["sig"], g_lo=gl[0] if gl else None, g_hi=gl[1] if gl else None, g_state=gs,
             sol=e0["sol"], max_cost=(rb.get("buyargs") or [None, None])[1], tok=e0["tok"], vsol_after=e0["vsol"], creator=e0.get("creator"),
             tip=rb["tip"], tipto=list(rb["tipto"]), prio=(rb["fee"] or 0) - 5000 * len(rb["signers"]), cup=rb["cup"], cul=rb["cul"], fee=rb["fee"],
             n_buys=len(buys), n_sells=len(sells), pnl=sum(r["d"] for r, _ in xs), buy_d=sum(r["d"] for r, _ in buys),
             closed=tok_out >= tok_in * 0.999 and tok_in > 0, sell_slots=[r["s"] for r, _ in sells], sell_sigs=[r["sig"] for r, _ in sells], sell_bts=[r["bt"] for r, _ in sells],
             sell_g=[g(r["g_slot"]) for r, _ in sells], sell_tip=[r["tip"] for r, _ in sells], sell_fee=[r["fee"] for r, _ in sells],
             ix=rb["pix"], tops=sorted(set(rb["tops"])))
    trips.append(t)
json.dump(dict(trips=trips, fails=[dict(sig=r["sig"], s=r["s"], bt=r["bt"], err=r["err"], fee=r["fee"], d=r["d"], tip=r["tip"],
                                       g_slot=g(r["g_slot"]), mints=[k for k in (r.get("pumpacc") or [])][:3]) for r in fails],
               other=[dict(sig=r["sig"], bt=r["bt"], d=r["d"], payer=r["payer"], tops=r["tops"], err=r["err"]) for r in rows if r["k"] == "other" or (r["k"] != "buy" and r["err"])]),
          open(W + "/data/trips.json", "w"))
print("trips", len(trips), "closed", sum(t["closed"] for t in trips), "fails", len(fails))
c = collections.Counter(); hs = collections.Counter(); sw = collections.Counter(); so = collections.Counter()
for t in trips:
    if t["g_lo"] is None: continue
    c[(t["buy_slot"] - t["g_lo"], t["g_hi"] - t["g_lo"])] += 1
    if t["sell_g"] and t["sell_g"][0]:
        sg = t["sell_g"][0]; hs[sg[0] - t["g_lo"]] += 1; sw[sg[1] - sg[0] if sg[1] < 1 << 60 else "inf"] += 1; so[t["sell_slots"][0] - sg[0]] += 1
print("buy at lo+k, window width:", c.most_common(6))
print("sell guard start - buy guard lo:", sorted(hs.items())[:30])
print("sell guard width:", sw.most_common(5)); print("sell landed at start + k:", sorted(so.items())[:12])
