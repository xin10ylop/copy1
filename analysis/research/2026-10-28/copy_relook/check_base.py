# Sanity check: base.py's split P&L must give ablate.py's +8.02 (298 copies) with the model's own costs.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")).read())
items = [(r, value(r)) for r in LIVE2]
items = [(r, v) for r, v in items if v]
print(f"2M key, model costs: n {len(items)} net {sum(v['net'] for _, v in items):+.4f} curve {sum(v['curve'] for _, v in items):+.4f} "
      f"fixed {sum(v['fixed'] for _, v in items):.4f} refused {sum(v['ref'] for _, v in items):.4f} fills {sum(v['fill'] for _, v in items):.1f}")
bd = by_day(items); print("by day", " ".join(f"{d} {bd[d]:+.2f}" for d in DAYS))
