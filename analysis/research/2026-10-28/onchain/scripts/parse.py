# Compact rows from cached raw transactions of his wallet. Pump trade events decoded from the self-CPI event ix.
#   python3 -I parse.py  -> data/rows.jsonl (every cached tx of his signature list)
import sys, os, json, struct, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"; SYS = "11111111111111111111111111111111"; CB = "ComputeBudget111111111111111111111111111111"
SLOTG = "A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp"; STATEG = "8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez"
TAG = bytes.fromhex("e445a52e51cb9a1d"); TRADE = bytes.fromhex("bddb7fd34ee661ee"); CREATEV = bytes.fromhex("1b72a94ddeeb6376")
IX = {bytes.fromhex(v): k for k, v in dict(create="181ec828051c0777", create_v2="d6904cec5f8b31b4", buy="66063d1201daebea",
      buy_exact_sol_in="38fc74089edfcd5f", sell="33e685a4017f83ad").items()}
A58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"; IDX = {c: i for i, c in enumerate(A58)}
def b58d(d):
    n = 0
    for c in d: n = n * 58 + IDX[c]
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * (len(d) - len(d.lstrip("1"))) + raw
def b58e(b):
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = A58[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\x00"))) + s
u64 = lambda b, o: struct.unpack_from("<Q", b, o)[0]
def trade(d):
    # TradeEvent payload (after TAG + disc): mint, sol, tok, is_buy, user, ts, vsol, vtok, real_sol, real_tok, fee_recipient, fee_bps, fee, creator, cfee_bps, cfee
    e = dict(mint=b58e(d[0:32]), sol=u64(d, 32), tok=u64(d, 40), buy=d[48] == 1, user=b58e(d[49:81]), vsol=u64(d, 89), vtok=u64(d, 97),
             rsol=u64(d, 105), rtok=u64(d, 113))
    if len(d) >= 121 + 32 + 16 + 32 + 16:
        e.update(fee=u64(d, 153 + 8), creator=b58e(d[169:201]), cfee=u64(d, 201 + 8))
    return e
def compact(t):
    m = t["transaction"]["message"]; meta = t["meta"] or {}
    la = meta.get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    nsig = m["header"]["numRequiredSignatures"]
    hi = ks.index(HIM) if HIM in ks else None
    tokacc = {b["accountIndex"] for b in (meta.get("preTokenBalances") or []) + (meta.get("postTokenBalances") or [])}
    r = dict(sig=t["transaction"]["signatures"][0], s=t["slot"], bt=t.get("blockTime"), v=str(t.get("version")),
             err=(json.dumps(meta["err"], separators=(",", ":"))[:90] if meta.get("err") is not None else None), fee=meta.get("fee"),
             payer=ks[0], signers=ks[:nsig], d=(meta["postBalances"][hi] - meta["preBalances"][hi]) if hi is not None else 0,
             him_signer=HIM in ks[:nsig], tops=[], pix=[], tr=[], tip=0, tipto={}, cup=None, cul=None, g_slot=None, g_state=None, xf=[],
             nkeys=len(ks), tok=[])
    def walk():
        for i, ix in enumerate(m["instructions"]): yield ix, False, i
        for g in meta.get("innerInstructions") or []:
            for ix in g["instructions"]: yield ix, True, g["index"]
    for ix, inner, oi in walk():
        p = ks[ix["programIdIndex"]]; acc = ix.get("accounts") or []
        if not inner: r["tops"].append(p)
        if p == CB and not inner:
            d = b58d(ix.get("data", ""))
            if d[:1] == b"\x03" and len(d) >= 9: r["cup"] = u64(d, 1)
            if d[:1] == b"\x02" and len(d) >= 5: r["cul"] = struct.unpack_from("<I", d, 1)[0]
        elif p == SYS:
            d = b58d(ix.get("data", ""))
            if len(d) < 4: continue
            kind = struct.unpack_from("<I", d, 0)[0]
            if kind == 2 and len(d) >= 12 and len(acc) >= 2: src, dst, lam = ks[acc[0]], ks[acc[1]], u64(d, 4)
            elif kind == 0 and len(d) >= 12 and len(acc) >= 2: src, dst, lam = ks[acc[0]], ks[acc[1]], u64(d, 4)  # createAccount
            elif kind == 3 and len(acc) >= 2: src, dst, lam = ks[acc[0]], ks[acc[1]], None  # createAccountWithSeed (amount after seed)
            elif kind == 11 and len(d) >= 12 and len(acc) >= 3: src, dst, lam = ks[acc[0]], ks[acc[2]], u64(d, 4)  # transferWithSeed
            else: continue
            if HIM in (src, dst): r["xf"].append([src, dst, lam, int(inner), kind])
            if not inner and src == HIM and kind == 2 and dst != HIM and acc[1] not in tokacc:
                r["tip"] += lam; r["tipto"][dst] = r["tipto"].get(dst, 0) + lam
        elif p == PUMP:
            d = b58d(ix.get("data", ""))
            if inner and d[:8] == TAG and d[8:16] == TRADE:
                try: r["tr"].append(trade(d[16:]))
                except Exception: pass
            elif inner and d[:8] == TAG and d[8:16] == CREATEV: r["pix"].append("CREATE_EVENT")
            elif not inner and d[:8] in IX:
                r["pix"].append(IX[d[:8]])
                if IX[d[:8]].startswith("buy") and len(d) >= 24: r["buyargs"] = [u64(d, 8), u64(d, 16)]
                if IX[d[:8]].startswith("sell") and len(d) >= 24: r["sellargs"] = [u64(d, 8), u64(d, 16)]
                r.setdefault("pumpacc", [ks[a] for a in acc[:6]])
            elif not inner: r["pix"].append("pump:" + d[:8].hex())
        elif p == SLOTG and not inner:
            d = b58d(ix.get("data", "")); r["g_slot"] = d.hex()
        elif p == STATEG and not inner:
            d = b58d(ix.get("data", "")); r["g_state"] = d.hex()
    for b in (meta.get("postTokenBalances") or []) + (meta.get("preTokenBalances") or []):
        if b.get("owner") == HIM: r["tok"].append([b["mint"], b["accountIndex"], b["uiTokenAmount"]["amount"]])
    r["pre_bal"] = meta["preBalances"][hi] if hi is not None else None; r["post_bal"] = meta["postBalances"][hi] if hi is not None else None
    r["logs_err"] = [l for l in (meta.get("logMessages") or []) if "rror" in l or "failed" in l][:3] if meta.get("err") is not None else []
    return r
if __name__ == "__main__":
    S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
    n = miss = 0
    with open(os.path.join(R.W, "data", "rows.jsonl"), "w") as f:
        for x in S:
            t = R.gettx(x["signature"])
            if not t: miss += 1; continue
            f.write(json.dumps(compact(t), separators=(",", ":")) + "\n"); n += 1
    print("rows", n, "not fetched", miss)
def compact_any(t, who):
    """small summary of any tx from the point of view of wallet `who`"""
    m = t["transaction"]["message"]; meta = t["meta"] or {}
    la = meta.get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    progs = {ks[i["programIdIndex"]] for i in m["instructions"]}
    xf = []; trades = []
    def walk():
        for ix in m["instructions"]: yield ix, False
        for g in meta.get("innerInstructions") or []:
            for ix in g["instructions"]: yield ix, True
    for ix, inner in walk():
        p = ks[ix["programIdIndex"]]; acc = ix.get("accounts") or []
        if p == SYS:
            d = b58d(ix.get("data", ""))
            if len(d) >= 12 and struct.unpack_from("<I", d, 0)[0] in (0, 2) and len(acc) >= 2:
                xf.append((ks[acc[0]], ks[acc[1]], u64(d, 4), int(inner), struct.unpack_from("<I", d, 0)[0]))
        elif p == PUMP and inner:
            d = b58d(ix.get("data", ""))
            if d[:8] == TAG and d[8:16] == TRADE:
                try: trades.append(trade(d[16:]))
                except Exception: pass
    return dict(sig=t["transaction"]["signatures"][0], s=t["slot"], bt=t.get("blockTime"), payer=ks[0], progs=progs, xf=xf,
                my_trades=[e for e in trades if e["user"] == who], him=HIM in ks, err=meta.get("err") is not None)
