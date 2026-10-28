# Program 7SVCZWEj (deployed 2026-10-22 by 4yN2vFSi): authority, size, and every signature that touches it, with payers.
import sys, os, json, time, collections, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R, parse as P
from sigs import all_sigs
ts = lambda bt: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
for p in sys.argv[1:]:
    a = R.rpc("getAccountInfo", [p, {"encoding": "jsonParsed"}], cache=True)["value"]
    pd = a["data"]["parsed"]["info"]["programData"] if isinstance(a["data"], dict) else None
    b = R.rpc("getAccountInfo", [pd, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 45}}], cache=True)["value"] if pd else None
    raw = base64.b64decode(b["data"][0]) if b else b""
    auth = P.b58e(raw[13:45]) if len(raw) >= 45 and raw[12] == 1 else None
    print(p, "owner", a["owner"], "programData", pd, "authority", auth, "last deploy slot", int.from_bytes(raw[4:12], "little") if raw else None, "programData lamports", b["lamports"] if b else None, "space", b.get("space") if b else None)
    s = all_sigs(p, max_pages=50, head_cache=False)
    payers = collections.Counter(); first = {}
    for i in range(0, len(s), 50):
        for x, t in zip(s[i:i + 50], R.txs1([y["signature"] for y in s[i:i + 50]])):
            if t: k = t["transaction"]["message"]["accountKeys"][0]; payers[k] += 1; first.setdefault(k, x["blockTime"])
    print("   sigs", len(s), ts(s[-1]["blockTime"]) if s else "", "..", ts(s[0]["blockTime"]) if s else "", "payers:", [(k, v) for k, v in payers.most_common(10)])
print("calls", R.flush_count())
