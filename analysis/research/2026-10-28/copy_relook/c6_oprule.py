# C6. The operator rule, on or off: oprule/options.py's copy set (his key buys, tip >= 2M or size >= 2 SOL; his buys on
# the operator counted with his month of history; the box's table lag: an operator is listed only after the first
# 4-hourly refresh that follows his first trade on it; unlisted copies sold at the default + 9), now at live costs
# (3.0M bid: 0.0046 a filled copy, 0.000015 a refusal), by day, P1 / P2, without the best 2, with and without 8ZN71X.
# Needs SP/oprule/arrival.py (= the repo's analysis/research/2026-10-26/oprule/arrival.py) and SP/oprule/op8zn.txt
# (8ZN71X's address); setup.sh puts them there.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(SP + "/oprule/arrival.py").read().split('print("by day: "')[0])
Z = open(SP + "/oprule/op8zn.txt").read().strip()
FIX = fixed_of(3.0)
for r in K2:
    bt = his_buy[r["m"]]["bt"]; r["n24"] = len(times_before(r, bt - 86400, bt))
    R_ = last_refresh(bt); r["box"] = bool(times_before(r, R_ - 7 * 86400, R_)); r["z"] = r["signer"] == Z
    r["w"] = value(r, 0.5, FIX, REF_LIVE, hold_fn=(H_live if r["box"] else (lambda r: 9)))
    r["wm"] = value(r, 0.5, hold_fn=(H_live if r["box"] else (lambda r: 9)))       # the model's costs (options.py)
RULES = (("live: >= 2 in 24 h and in the box's table", lambda r: r["n24"] >= 2 and r["box"]),
         ("no operator rule (copy_signer_min_buys = 0), table kept", lambda r: r["box"]),
         ("no operator rule and no table (every key buy)", lambda r: True),
         (">= 1 in 24 h and in the table", lambda r: r["n24"] >= 1 and r["box"]))
out = {}
for zl, zf in (("all operators", lambda r: True), ("without 8ZN71X", lambda r: not r["z"])):
    print(f"\n== {zl}")
    for lab, f in RULES:
        sel = [r for r in K2 if f(r) and zf(r)]
        out[(zl, lab)] = line(lab, [(r, r["w"]) for r in sel],
                              extra=f"  (model costs {sum(r['wm']['net'] for r in sel if r['wm']):+.2f})")
    a = out[(zl, RULES[0][0])]["bd"]; b = out[(zl, RULES[1][0])]["bd"]; c = out[(zl, RULES[2][0])]["bd"]
    print("   rule on minus off (table kept), by day: " + " ".join(f"{d} {a.get(d, 0) - b.get(d, 0):+.2f}" for d in DAYS) +
          f"   total {sum(a.values()) - sum(b.values()):+.2f}")
    print("   rule on minus every key buy, by day:    " + " ".join(f"{d} {a.get(d, 0) - c.get(d, 0):+.2f}" for d in DAYS) +
          f"   total {sum(a.values()) - sum(c.values()):+.2f}")
print("\nThe live status line printed 'operator he bought < 0 times in 24 h 0' (05-live/check-sh-2026-10-27.txt line 46): the min is 0 there.")
