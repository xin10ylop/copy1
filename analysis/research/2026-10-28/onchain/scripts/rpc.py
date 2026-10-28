# Triton JSON-RPC client. URL from env TRITON_URL (never printed; errors redacted). Every raw response cached under
# ../cache/<sha1>.json; every request (batched or not) counted in ../calls.json.
import json, os, time, hashlib, urllib.request, threading
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = os.environ.get("TRITON_URL", "").strip()  # empty: offline (cache only)
TOKEN = (URL.rstrip("/").rsplit("/", 1)[-1] if URL else "\x00none")
CACHE = os.path.join(W, "cache"); os.makedirs(CACHE, exist_ok=True)
CNT = os.path.join(W, "calls.json")
_lock = threading.Lock()
_n = [0]
def red(s):
    s = str(s)
    return s.replace(URL, "<url>").replace(TOKEN, "<token>")
def _bump(k):
    with _lock:
        _n[0] += k
def flush_count():
    with _lock:
        tot = json.load(open(CNT))["total"] if os.path.exists(CNT) else 0
        tot += _n[0]; _n[0] = 0
        json.dump({"total": tot}, open(CNT, "w"))
        return tot
def _key(method, params): return hashlib.sha1(json.dumps([method, params], sort_keys=True).encode()).hexdigest()
def _path(method, params): return os.path.join(CACHE, _key(method, params) + ".json")
def _post(body):
    for i in range(7):
        try:
            req = urllib.request.Request(URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            if i == 6: raise RuntimeError(red(e)) from None
            time.sleep(1.5 * (i + 1))
def rpc(method, params, cache=True):
    p = _path(method, params)
    if cache and os.path.exists(p): return json.load(open(p))
    for i in range(5):
        j = _post({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}); _bump(1)
        if "error" in j:
            if i == 4: raise RuntimeError(red(j["error"])[:300])
            time.sleep(2 * (i + 1)); continue
        break
    res = j.get("result")
    if cache and res is not None:
        json.dump(res, open(p + ".tmp", "w")); os.replace(p + ".tmp", p)
    return res
def batch(calls, cache=True):
    """calls: list of (method, params). Returns list of results (None on error / missing). One HTTP POST, len(todo) calls."""
    out = [None] * len(calls); todo = []
    for k, (m, pa) in enumerate(calls):
        p = _path(m, pa)
        if cache and os.path.exists(p): out[k] = json.load(open(p))
        else: todo.append(k)
    tries = 0
    while todo and tries < 5:
        tries += 1
        body = [{"jsonrpc": "2.0", "id": k, "method": calls[k][0], "params": calls[k][1]} for k in todo]
        j = _post(body); _bump(len(todo))
        if isinstance(j, dict): j = [j]
        again = []
        got = {r.get("id"): r for r in j if isinstance(r, dict)}
        for k in todo:
            r = got.get(k)
            if r is None or "error" in r:
                if r is not None and (r.get("error") or {}).get("code") == -32015: continue  # version-1 tx: fetch with TXO1
                again.append(k); continue
            res = r.get("result"); out[k] = res
            if cache and res is not None:
                p = _path(*calls[k]); json.dump(res, open(p + ".tmp", "w")); os.replace(p + ".tmp", p)
        todo = again
        if todo: time.sleep(1.5 * tries)
    return out
TXO = {"encoding": "json", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}
def tx(sig): return rpc("getTransaction", [sig, TXO])
def txs(sigs): return batch([("getTransaction", [s, TXO]) for s in sigs])
TXO1 = {"encoding": "json", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}
def gettx(sig):
    """cached tx under either option set (v0 first; version-1 transactions need TXO1)"""
    p0 = _path("getTransaction", [sig, TXO]); p1 = _path("getTransaction", [sig, TXO1])
    if os.path.exists(p0): return json.load(open(p0))
    if os.path.exists(p1): return json.load(open(p1))
    return None
def txs1(sigs): return batch([("getTransaction", [s, TXO1]) for s in sigs])
