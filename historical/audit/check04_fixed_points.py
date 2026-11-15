# ─────────────────────────────────────────────
# check04_fixed_points.py
# ─────────────────────────────────────────────
"""Check 4: |Fix(g)| per conjugacy class (Table 5.2)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fixed_counts_table

options = {1: "PL", 2: "BPL", 3: "BU", 4: "BBU"}

# Expected values from the paper's Table 5.2 at n=3
expected_n3 = {
    "PL":  dict(e=27,   v=9,   tau=1, tau_v=3,  omega=0, omega_v=0),
    "BPL": dict(e=216,  v=36,  tau=0, tau_v=0,  omega=0, omega_v=0),
    "BU":  dict(e=216,  v=0,   tau=0, tau_v=12, omega=0, omega_v=0),
    "BBU": dict(e=1728, v=0,   tau=0, tau_v=0,  omega=0, omega_v=0),
}

ok = True
for opt, name in options.items():
    for n in [2, 3, 4]:
        counts = fixed_counts_table(n, opt)
        print(f"{name} n={n}: {counts}")
        if n == 3:
            exp = expected_n3[name]
            if counts != exp:
                print(f"  MISMATCH: expected {exp}")
                ok = False
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
