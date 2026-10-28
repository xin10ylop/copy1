# Profile wallets linked to him by SOL transfers: signature count (to 3 pages), first / last activity, balance, and a
# sample of their transactions (first 2, newest 3, 3 spread): pump trades by the wallet, guard programs, who funded it.
#   run.sh profile_w.py LABEL ADDR [ADDR...]  -> data/prof_<LABEL>.json
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
from sigs import all_sigs
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
GUARDS = {"A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp", "8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez"}
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"; PAMM = "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"
def profile(a, pages=3):
    s = all_sigs(a, max_pages=pages, head_cache=False, before=None) if False else None
    out = []; before = None
    for pg in range(pages):
        o = {"limit": 1000}
        if before: o["before"] = before
        page = R.rpc("getSignaturesForAddress", [a, o], cache=True) or []
        out += page
        if len(page) < 1000: break
        before = page[-1]["signature"]
    s = out
    bal = R.rpc("getBalance", [a], cache=True)["value"]
    if not s: return dict(addr=a, n=0, bal=bal)
    idx = sorted(set([len(s) - 1, len(s) - 2, 0, 1, 2] + [len(s) * k // 4 for k in (1, 2, 3)]))
    idx = [i for i in idx if 0 <= i < len(s)]
    sel = [s[i]["signature"] for i in idx]
    txs = R.txs1(sel)
    smp = []
    for x, t in zip(sel, txs):
        if not t: continue
        c = P.compact_any(t, a)
        smp.append(c)
    first = smp[0] if smp else None
    fund = None
    for c in sorted(smp, key=lambda c: c["s"]):
        for src, dst, lam, inner, k in c["xf"]:
            if dst == a and src != a and lam and lam >= 1000000: fund = (src, lam, c["bt"]); break
        if fund: break
    return dict(addr=a, n=len(s), capped=len(s) >= pages * 1000, first_bt=s[-1]["blockTime"], last_bt=s[0]["blockTime"], bal=bal,
                errs=sum(1 for x in s if x.get("err")), sample=len(smp), pump_trades=sum(1 for c in smp if c["my_trades"]),
                pump_any=sum(1 for c in smp if PUMP in c["progs"] or PAMM in c["progs"]), guard=sum(1 for c in smp if c["progs"] & GUARDS),
                with_him=sum(1 for c in smp if c["him"]), payers=collections.Counter(c["payer"][:8] for c in smp).most_common(3), funder=fund,
                progs=collections.Counter(p[:8] for c in smp for p in c["progs"]).most_common(8))
if __name__ == "__main__":
    lab = sys.argv[1]; addrs = sys.argv[2:]
    if len(addrs) == 1 and os.path.exists(addrs[0]): addrs = json.load(open(addrs[0]))
    res = {}
    for a in addrs:
        try: res[a] = profile(a)
        except Exception as e: res[a] = dict(addr=a, error=R.red(e)[:100])
        p = res[a]
        ts = lambda bt: time.strftime("%Y-%m-%d", time.gmtime(bt)) if bt else "-"
        print(f"{a} n={p.get('n')}{'+' if p.get('capped') else ''} {ts(p.get('first_bt'))}..{ts(p.get('last_bt'))} bal={p.get('bal', 0)/1e9:.4f} sample={p.get('sample')} pump={p.get('pump_any')} own_pump_trades={p.get('pump_trades')} guard={p.get('guard')} with_him={p.get('with_him')} funder={(p.get('funder') or [None])[0]} progs={p.get('progs')}", flush=True)
    json.dump(res, open(os.path.join(R.W, "data", f"prof_{lab}.json"), "w"), indent=1)
    print("calls", R.flush_count())
