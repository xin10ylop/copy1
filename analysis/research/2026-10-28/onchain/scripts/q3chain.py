# Follow his outgoing SOL (Aug 23 - Sep 3) hop by hop (each hop: the wallet's next transaction, its largest System
# transfer out) up to 8 hops, for 12 sampled deposits; and walk back the funding of 12 sampled sweepers (their first
# inbound >= 0.1 SOL) up to 6 hops. Does any chain reach a wallet that later sweeps to him, or a known exchange?
import sys, os, json, time, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
HIM = P.HIM
F = json.load(open(os.path.join(R.W, "data", "flows.json")))
senders = {f[3] for f in F["flows"] if f[2] == "in" and f[4] >= 1e8}
recips = {f[3] for f in F["flows"] if f[2] == "out" and f[4] >= 1e8}
big = [f for f in F["flows"] if f[4] >= 1e9 and 1787443200 <= f[0] < 1788480000]
outs = [f for f in big if f[2] == "out"]; ins = [f for f in big if f[2] == "in"]
random.seed(11); so = random.sample(outs, 12); si = random.sample(ins, 12)
ts = lambda bt: time.strftime("%m-%d %H:%M:%S", time.gmtime(bt))
def nxt(addr, after_sig):
    page = R.rpc("getSignaturesForAddress", [addr, {"limit": 1000, "until": after_sig}], cache=True) or []
    return [x["signature"] for x in reversed(page)]
print("== forward chains")
for f in so:
    a, sig, amt, path = f[3], f[1], f[4], []
    for hop in range(8):
        later = nxt(a, sig)
        if not later: path.append(f"{a[:8]}(stops, {len(later)} later txs)"); break
        t = R.rpc("getTransaction", [later[0], R.TXO1], cache=True); c = P.compact_any(t, a)
        outs_ = sorted([(l, d) for s, d, l, inner, k in c["xf"] if s == a and d != a], reverse=True)
        tag = ("SWEEPER" if a in senders else "") + ("RECIP" if a in recips and hop > 0 else "")
        if c["my_trades"]: path.append(f"{a[:8]}{tag}(pump trade, {len(later)} later txs)"); break
        if not outs_: path.append(f"{a[:8]}{tag}(next tx: {','.join(sorted(p[:8] for p in c['progs']))}, {len(later)} later txs)"); break
        path.append(f"{a[:8]}{tag}->{outs_[0][0]/1e9:.3f}@{c['bt']-f[0]}s"); a, sig = outs_[0][1], later[0]
    print(" ", ts(f[0]), f"{amt/1e9:.3f} SOL:", " | ".join(path))
print("== funding of sweepers, walked back")
def first_in(a):
    s = []; before = None
    for _ in range(4):
        o = {"limit": 1000}
        if before: o["before"] = before
        page = R.rpc("getSignaturesForAddress", [a, o], cache=True) or []
        s += page
        if len(page) < 1000: break
        before = page[-1]["signature"]
    for x in reversed(s[-6:]):
        t = R.rpc("getTransaction", [x["signature"], R.TXO1], cache=True)
        if not t: continue
        c = P.compact_any(t, a)
        g = [(l, src) for src, d, l, inner, k in c["xf"] if d == a and src != a and l >= 1e8]
        if g: return max(g)[1], max(g)[0], c["bt"], len(s)
    return None, None, None, len(s)
for f in si:
    a, path = f[3], []
    for hop in range(6):
        src, l, bt, n = first_in(a)
        tag = "(him)" if src == HIM else ("SWEEPER" if src in senders else "") + ("RECIP" if src in recips else "")
        if not src: path.append(f"{a[:8]}(no inbound >= 0.1 SOL in its first 6 txs; {n} txs)"); break
        path.append(f"{a[:8]}<-{src[:8]}{tag} {l/1e9:.3f} {time.strftime('%Y-%m-%d', time.gmtime(bt))}")
        if src == HIM: break
        a = src
    print(" ", ts(f[0]), f"{f[4]/1e9:.3f} SOL from {f[3][:8]}:", " | ".join(path))
print("calls", R.flush_count())
