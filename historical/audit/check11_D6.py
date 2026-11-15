# ─────────────────────────────────────────────
# check11_D6.py
# ─────────────────────────────────────────────
"""Check 11: explicit S3 × Z/2 ≅ D6."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import g_mul, g_inv, closure, G_ELEMENTS, C_G, TAU_G, V_G

r = g_mul(C_G, V_G)
s = TAU_G

def order(g):
    x = (0, 0)
    for k in range(1, 100):
        x = g_mul(x, g)
        if x == (0, 0):
            return k
    return None

ok = (order(r) == 6 and order(s) == 2
      and g_mul(g_mul(s, r), s) == g_inv(r))
gen = closure({r, s})
ok = ok and (gen == closure(set(G_ELEMENTS)))

print(f"order(r)={order(r)}, order(s)={order(s)}, "
      f"s·r·s = r^-1: {g_mul(g_mul(s, r), s) == g_inv(r)}")
print(f"<r, s> = G: {gen == closure(set(G_ELEMENTS))}")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
