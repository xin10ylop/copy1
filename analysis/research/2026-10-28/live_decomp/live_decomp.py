#!/usr/bin/env python3
"""The live copies of him, decomposed (2026-10-28, 07-restart/README.md section 2).

Parses the `== 1 him` table of 05-live/check-sh-2026-10-27.txt (377 of his launch buys, newest first, Beirut time)
and splits the 162 copies by what decided them: curve P&L against tips and fees, the 3.0M / 8.0M bid, the Beirut day,
his tip bucket, his size, where the copy landed, slots held. The stake of a filled copy is OUR NET / our %.
Run from the repo root: python3 -I analysis/research/2026-10-28/live_decomp/live_decomp.py
"""
import collections
import re
import statistics as st
import sys

PASTE = "05-live/check-sh-2026-10-27.txt"
ROW = re.compile(r"\s+(\d\d:\d\d:\d\d)\s+(\S+)\s+([+-]\d+\.\d+)\s+(?:([+-]\d+\.\d+)\s+)?(?:([+-]\d+\.\d+)%\s+)?COPIED\s+"
                 r"(\S+)\s+(\S+)M\s+\+(\d)\s+(filled|refused|not landed)\s*(.*)$")


def rows(path: str) -> list[dict]:
    lines = open(path).read().splitlines()
    a = next(i for i, l in enumerate(lines) if l.startswith("== 1 him"))
    b = next(i for i, l in enumerate(lines) if i > a and l.startswith("== 2 "))
    out = []
    for l in lines[a + 3:b]:
        if "COPIED" not in l:
            continue
        m = ROW.match(l)
        if not m:
            print("unparsed:", l, file=sys.stderr)
            continue
        t, coin, its, our, pct, hissol, histip, hisslot, res, rest = m.groups()
        d = dict(t=t, coin=coin, its=float(its), our=float(our) if our else 0.0, pct=float(pct) if pct else None,
                 hissol=float(hissol), tip=float(histip), hslot=int(hisslot), res=res, landed=None, behind=None,
                 held=None, bid=None, fees=0.0, stake=None)
        toks = rest.split()
        if toks:
            d["landed"] = "its" if toks[0] == "its" else toks[0]
            bi = next((i for i, x in enumerate(toks) if re.fullmatch(r"\d+\.\dM", x)), None)
            if bi is not None:
                d["bid"] = float(toks[bi][:-1])
                d["fees"] = float(toks[bi + 1]) if bi + 1 < len(toks) else 0.0
                ints = [int(x) for x in toks[:bi] if x.isdigit()]
                if res == "filled":
                    d["held"] = ints[-1] if ints else None
                    d["behind"] = ints[0] if len(ints) == 2 else None
                else:
                    d["behind"] = ints[0] if ints else None
        if d["pct"]:
            d["stake"] = d["our"] / (d["pct"] / 100)
        out.append(d)
    # newest first: the clock jumps up at midnight Beirut
    day, prev = "Oct 27", None
    for d in out:
        tm = int(d["t"][:2]) * 60 + int(d["t"][3:5])
        if prev is not None and tm > prev:
            day = "Oct 26"
        prev = tm
        d["day"] = day
    return out


def grp(f: list[dict], key, title: str) -> None:
    print(title)
    g = collections.defaultdict(list)
    for d in f:
        g[key(d)].append(d)
    for k in sorted(g, key=str):
        v = g[k]
        n = len(v)
        net = sum(x["our"] for x in v)
        fees = sum(x["fees"] for x in v)
        its = sum(x["its"] for x in v)
        w = sum(x["our"] > 0 for x in v)
        ss = [x["stake"] for x in v if x["stake"]]
        print(f"  {str(k):16s} n {n:3d} won {w:3d} ournet {net:+.4f} fees {fees:.4f} curve {net + fees:+.4f} "
              f"his {its:+.4f} avgstake {st.mean(ss) if ss else 0:.3f} per copy {net / n:+.4f}")


def tip_bucket(d: dict) -> str:
    return "2-4M" if d["tip"] < 4.5 else ("4.8-7.2M" if d["tip"] < 8 else "8M+")


def size_bucket(d: dict) -> str:
    s = d["hissol"]
    return "<0.7" if s < 0.7 else ("0.7-1.1" if s < 1.1 else ("1.1-2" if s < 2 else "2+"))


def main() -> None:
    cop = rows(PASTE)
    filled = [d for d in cop if d["res"] == "filled"]
    refused = [d for d in cop if d["res"] == "refused"]
    print(f"copied {len(cop)}: filled {len(filled)}, refused {len(refused)}, not landed "
          f"{sum(d['res'] == 'not landed' for d in cop)}")
    net, fees = sum(d["our"] for d in filled), sum(d["fees"] for d in filled)
    print(f"filled: OUR NET {net:+.4f}  tips and fees {fees:.4f}  curve P&L {net + fees:+.4f}")
    stakes = [d["stake"] for d in filled if d["stake"]]
    print(f"stake: n {len(stakes)} median {st.median(stakes):.3f} mean {st.mean(stakes):.3f} "
          f"min {min(stakes):.3f} max {max(stakes):.3f}")
    grp(filled, lambda d: d["bid"], "by our bid (M):")
    grp(filled, lambda d: d["day"], "by Beirut day:")
    grp(filled, lambda d: (d["day"], d["bid"]), "by day x bid:")
    grp(filled, tip_bucket, "by his tip:")
    grp(filled, size_bucket, "by his size (SOL):")
    grp(filled, lambda d: d["landed"], "by where we landed (its slot / +1):")
    grp(filled, lambda d: d["hslot"], "by his buy slot (create + k):")
    grp(filled, lambda d: d["held"], "by slots held:")
    s = sorted(filled, key=lambda d: d["our"])
    print(f"filled net without the best 2: {sum(d['our'] for d in s[:-2]):+.4f}; without the worst 2: "
          f"{sum(d['our'] for d in s[2:]):+.4f}")
    print("worst 8:")
    for d in s[:8]:
        print(f"   {d['t']} {d['coin']} {d['day']} our {d['our']:+.4f} ({d['pct']}%) his {d['its']:+.4f} tip {d['tip']}M "
              f"at +{d['hslot']} landed {d['landed']} held {d['held']} bid {d['bid']}M")
    print("best 5:")
    for d in s[-1:-6:-1]:
        print(f"   {d['t']} {d['coin']} {d['day']} our {d['our']:+.4f} ({d['pct']}%) his {d['its']:+.4f} tip {d['tip']}M "
              f"at +{d['hslot']} landed {d['landed']} held {d['held']} bid {d['bid']}M")
    grp(refused, lambda d: d["bid"], "refused, by our bid (his net on them):")
    grp(refused, tip_bucket, "refused, by his tip:")
    grp(refused, lambda d: d["landed"], "refused, by where we landed:")


if __name__ == "__main__":
    main()
