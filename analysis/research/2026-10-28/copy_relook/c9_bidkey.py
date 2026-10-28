# C9. A copy key on his whole bid, tip + priority fee, instead of the tip alone. The on-chain re-check (Oct 26-28) found
# about a fifth of his high bids paid as priority fee with a low tip. His priority fee per landed launch buy is already
# in the 5-day data: the walk's transaction fee minus the 5,000-lamport signature fee (he signs alone). It equals
# cu_price x cu_limit / 1e6 from bids.json on every buy with a record (checked below). Where the on-chain agent's
# rows.jsonl overlaps (Oct 24-25), its fees are compared too. No RPC call.
# The copy: ablate.py's machinery, 0.5 SOL, 3M live costs (0.0046 a fill, 0.000015 a refusal), our measured landing
# distances, 5% bound, sold at H - 1, >= 2 of his buys on the signer in 24 h. Keys:
#   tip key (live):  tip >= 2M or size >= 2 SOL
#   bid key (X):     tip + priority >= X or size >= 2 SOL, X = 2 / 3 / 4 / 6M
# python3 -I c9_bidkey.py [rows.jsonl of the on-chain agent, optional]
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
FIX = fixed_of(3.0)
Bd = json.load(open(SP + "/dec/five/bids.json"))
chk = collections.Counter()
for r in rows:
    b = his_buy[r["m"]]; r["prio"] = max(b["fee"] - 5000, 0); r["U"] = r["tip"] + r["prio"]
    x = Bd.get(b["sig"])
    if x: chk["fee - 5000 = cu_price x cu_limit" if abs((x[1] or 0) * (x[2] or 0) // 10**6 - r["prio"]) <= 1 else "differs"] += 1
print(f"his priority fee per copy-universe buy: {dict(chk)}")
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    oc = {}
    for l in open(sys.argv[1]):
        d = json.loads(l); oc[d["sig"]] = d["fee"]
    m_ = sum(1 for r in rows if his_buy[r["m"]]["sig"] in oc and oc[his_buy[r["m"]]["sig"]] == his_buy[r["m"]]["fee"])
    n_ = sum(1 for r in rows if his_buy[r["m"]]["sig"] in oc)
    print(f"   against the on-chain agent's rows.jsonl: {n_} of his copy-universe buys in both, fee equal on {m_}")
HOTR = [r for r in rows if HOT(r)]
print(f"his buys with the operator rule: {len(HOTR)}; with tip < 2M and size < 2 SOL: {sum(1 for r in HOTR if r['tip'] < 2e6 and r['sol'] < 2)}, "
      f"of which tip + priority >= 2M: {sum(1 for r in HOTR if r['tip'] < 2e6 and r['sol'] < 2 and r['U'] >= 2e6)}")
cache = {}
def v(r):
    if r["m"] not in cache: cache[r["m"]] = value(r, 0.5, FIX, REF_LIVE)
    return cache[r["m"]]
def show(lab, sel):
    it = [(r, v(r)) for r in sel]; it = [(r, x) for r, x in it if x]
    t = line(lab, it)
    n = t["n"]; ref = sum(x["fill"] for _, x in it)
    print(f"      per copy {t['tot'] / max(n, 1):+.4f}; fills {ref:.0f} ({ref / max(n, 1):.0%} of copies); his net on them {sum(r['his'] for r, _ in it):+.2f}")
    return t
TIPK = lambda r: r["tip"] >= 2e6 or r["sol"] >= 2.0
print("\n== the keys (with the operator rule)")
show("tip key: tip >= 2M or size >= 2 (live)", [r for r in HOTR if TIPK(r)])
for X in (2e6, 3e6, 4e6, 6e6):
    show(f"bid key: tip + priority >= {X / 1e6:.0f}M or size >= 2", [r for r in HOTR if r["U"] >= X or r["sol"] >= 2.0])
for X in (3e6, 4e6, 6e6):
    show(f"tip key at {X / 1e6:.0f}M (for comparison)", [r for r in HOTR if r["tip"] >= X or r["sol"] >= 2.0])
print("\n== what the bid key adds: bid key but not the tip key (tip < 2M, size < 2, tip + priority >= X)")
for X in (2e6, 3e6, 4e6, 6e6):
    show(f"added at {X / 1e6:.0f}M", [r for r in HOTR if not TIPK(r) and r["U"] >= X])
print("   ... and what a higher bid-key threshold drops from the tip key (tip >= 2M but tip + priority < X):")
for X in (3e6, 4e6, 6e6):
    show(f"dropped at {X / 1e6:.0f}M", [r for r in HOTR if TIPK(r) and not (r["U"] >= X or r["sol"] >= 2.0)])
add = [r for r in HOTR if not TIPK(r) and r["U"] >= 2e6]
print(f"\n   the added bucket at 2M: tips {dict(sorted(collections.Counter(round(r['tip'] / 1e6, 1) for r in add).items()))}; "
      f"priority (M) {dict(sorted(collections.Counter(round(r['prio'] / 1e6, 1) for r in add).items()))}; "
      f"size {dict(sorted(collections.Counter(round(r['sol'], 2) for r in add).items()))}; his buy at create+1 {sum(1 for r in add if his_buy[r['m']]['slot'] > r['cs'])} of {len(add)}")
print("\n== are the added copies the refused ones? (refused = a landing over his price + 5%)")
def refshare(sel):
    ls = [l for r in sel for l in [legs(r, 0.5)] if l]
    return sum(sum(1 for k, _ in l if k == "ref") / len(l) for l in ls) / max(len(ls), 1)
tk = [r for r in HOTR if TIPK(r)]
reft = [r for r in tk if any(k == "ref" for k, _ in legs(r, 0.5))]
print(f"   tip-key copies: {len(tk)}, refused share of landings {refshare(tk):.0%}; copies with a refused landing {len(reft)}, his net there {sum(r['his'] for r in reft):+.2f}")
print(f"   added copies (2M): {len(add)}, refused share {refshare(add):.0%}; overlap with the tip key's refused coins: {len({r['m'] for r in add} & {r['m'] for r in reft})} (disjoint by construction: a coin is in one key or the other)")
for lab, sel in (("tip key, his priority >= 1M", [r for r in tk if r["prio"] >= 1e6]), ("tip key, his priority < 1M", [r for r in tk if r["prio"] < 1e6])):
    print(f"   {lab}: {len(sel)} copies, refused share {refshare(sel):.0%}, copy {sum(v(r)['net'] for r in sel if v(r)):+.2f}, his {sum(r['his'] for r in sel):+.2f}")
