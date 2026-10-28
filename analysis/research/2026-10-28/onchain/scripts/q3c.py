# Q3c: who deployed his guard programs: program -> ProgramData -> upgrade authority, and the deploy transactions.
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
from sigs import all_sigs
HIM = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"
PROGS = {"slot guard": "A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp", "state guard": "8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez",
         "DeFG8i8z's program": "BYdq7NJXWHnTzzCogT6VByrPXvUQwkD5PuZQLS8JvZtw"}
out = {}
for name, p in PROGS.items():
    a = R.rpc("getAccountInfo", [p, {"encoding": "jsonParsed"}], cache=True)["value"]
    pd = a["data"]["parsed"]["info"]["programData"]
    b = R.rpc("getAccountInfo", [pd, {"encoding": "jsonParsed", "dataSlice": {"offset": 0, "length": 45}}], cache=True)["value"]
    info = b["data"]["parsed"]["info"] if isinstance(b["data"], dict) else None
    if info is None:
        import base64, parse as P
        raw = base64.b64decode(b["data"][0]); slot = int.from_bytes(raw[4:12], "little"); auth = P.b58e(raw[13:45]) if raw[12] == 1 else None
        info = dict(slot=slot, authority=auth)
    # oldest signatures of the ProgramData account = the deploy / upgrades
    s = all_sigs(pd, max_pages=5, head_cache=False)
    deploys = []
    for x in s[-5:][::-1] + s[:3]:
        t = R.rpc("getTransaction", [x["signature"], R.TXO1], cache=True)
        deploys.append(dict(sig=x["signature"], slot=x["slot"], time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(x["blockTime"])), payer=t["transaction"]["message"]["accountKeys"][0] if t else None, err=x.get("err") is not None))
    out[name] = dict(program=p, programData=pd, owner=a["owner"], authority=info.get("authority"), last_deploy_slot=info.get("slot"), programData_sigs=len(s), deploys=deploys)
    print(name, p, "| programData", pd, "| upgrade authority", info.get("authority"), "| last deployed slot", info.get("slot"), "| programData sigs", len(s))
    for d in deploys: print("    ", d["time"], d["slot"], "payer", d["payer"], "err", d["err"], d["sig"][:20])
json.dump(out, open(os.path.join(R.W, "data", "q3c.json"), "w"), indent=1)
print("calls", R.flush_count())
