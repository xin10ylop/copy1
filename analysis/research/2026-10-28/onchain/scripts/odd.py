# His recent txs that are not the usual trade shape: other fee payers, other programs. Prints transfers and his delta.
import sys, os, json, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
S = json.load(open(os.path.join(R.W, "data", f"sigs_{HIM}.json")))
lo = int(sys.argv[1]) if len(sys.argv) > 1 else 1792800000; hi = int(sys.argv[2]) if len(sys.argv) > 2 else 1 << 40
rec = [x for x in S if lo <= (x["blockTime"] or 0) < hi]
STD = {"11111111111111111111111111111111", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P", "8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez",
       "A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "ComputeBudget111111111111111111111111111111",
       "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}
for x in rec:
    t = R.gettx(x["signature"])
    if not t: print("MISSING", x["signature"]); continue
    m = t["transaction"]["message"]; meta = t["meta"]; la = meta.get("loadedAddresses") or {}
    ks = m["accountKeys"] + la.get("writable", []) + la.get("readonly", [])
    tops = [ks[i["programIdIndex"]] for i in m["instructions"]]
    if ks[0] == HIM and set(tops) <= STD and "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P" in tops: continue
    i = ks.index(HIM); d = meta["postBalances"][i] - meta["preBalances"][i]
    print(time.strftime("%m-%d %H:%M:%S", time.gmtime(t["blockTime"])), t["slot"], "v", t.get("version"), "payer", ks[0][:12], "signers", m["header"]["numRequiredSignatures"],
          "err", meta["err"] is not None, "his d", d, "tops", [p[:8] for p in tops], "nkeys", len(ks), x["signature"][:16])
