# ─────────────────────────────────────────────
# check05_burnside.py
# ─────────────────────────────────────────────
"""Check 5: Burnside sum vs closed forms (Theorem 5.5)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fixed_counts_table

def burnside_sum(n, option):
    c = fixed_counts_table(n, option)
    total = (c["e"] + c["v"]
             + 3 * c["tau"] + 3 * c["tau_v"]
             + 2 * c["omega"] + 2 * c["omega_v"])
    assert total % 12 == 0, \
        f"non-integer orbit count for option={option} n={n}: {total}/12"
    return total // 12

def closed_form(n, option):
    if option == 1:  # PL
        if n % 2 == 0:
            return (3**(n//2) + 1) * (3**(n//2) + 3) // 12
        return (3**((n-1)//2) + 1)**2 // 4
    if option in (2, 3):  # BPL, BU
        if n % 2 == 0:
            return (6**n + 4 * 6**(n//2)) // 12
        return (6**n + 6**((n+1)//2)) // 12
    if option == 4:  # BBU
        if n % 2 == 0:
            return (12**n + 4 * 12**(n//2)) // 12
        return 12**(n - 1)
    raise ValueError(option)

ok = True
for option in [1, 2, 3, 4]:
    for n in [2, 3, 4, 5]:
        b, c = burnside_sum(n, option), closed_form(n, option)
        match = (b == c)
        print(f"option={option} n={n}: Burnside={b}, closed={c}, "
              f"{'OK' if match else 'MISMATCH'}")
        ok = ok and match
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
