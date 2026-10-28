# Page getSignaturesForAddress for an address, newest first. Pages with a `before` cursor are cached (stable);
# the head page is fetched once and saved as data/head_<addr>.json (re-used on reruns).
#   run.sh sigs.py ADDR [MAX_PAGES] [STOP_BT]  -> data/sigs_<addr>.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
D = os.path.join(R.W, "data")
def all_sigs(addr, max_pages=1000, stop_bt=None, before=None, limit=1000, head_cache=True):
    out = []
    hp = os.path.join(D, f"head_{addr}.json")
    for pg in range(max_pages):
        o = {"limit": limit}
        if before: o["before"] = before
        if before is None and head_cache:
            if os.path.exists(hp): page = json.load(open(hp))
            else:
                page = R.rpc("getSignaturesForAddress", [addr, o], cache=False) or []
                json.dump(page, open(hp, "w"))
        else:
            page = R.rpc("getSignaturesForAddress", [addr, o], cache=True) or []
        out += page
        if len(page) < limit: break
        if stop_bt and (page[-1].get("blockTime") or 0) < stop_bt: break
        before = page[-1]["signature"]
    return out
if __name__ == "__main__":
    a = sys.argv[1]; mp = int(sys.argv[2]) if len(sys.argv) > 2 else 1000; sb = int(sys.argv[3]) if len(sys.argv) > 3 else None
    s = all_sigs(a, mp, sb)
    json.dump(s, open(os.path.join(D, f"sigs_{a}.json"), "w"))
    bts = [x.get("blockTime") or 0 for x in s]
    print(a[:8], "sigs", len(s), "errs", sum(1 for x in s if x.get("err")), "newest", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(max(bts))),
          "oldest", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(min(b for b in bts if b) if any(bts) else 0)), "calls", R.flush_count())
