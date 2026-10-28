import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpc as R
print(R.rpc("getSlot", [], cache=False))
r = R.batch([("getBalance", ["AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"]), ("getSlot", [])], cache=False)
print(r)
print("calls", R.flush_count())
