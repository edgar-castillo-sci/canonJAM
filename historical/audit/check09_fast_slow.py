# ─────────────────────────────────────────────
# check09_fast_slow.py
# ─────────────────────────────────────────────
"""Check 9: canonical_key vs canonical_key_fast."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import all_chains
from canonjam import canonical_key, canonical_key_fast

ok = True
for option in range(1, 9):
    for n in [2, 3]:
        for a in all_chains(n, option):
            fast = canonical_key_fast(a, option)
            slow = canonical_key(a, option)
            if fast != slow:
                print(f"MISMATCH option={option} n={n} "
                      f"a={a.tolist()}: fast={fast!r} slow={slow!r}")
                ok = False
print("PASS for all options and n=2,3" if ok else "FAIL")
sys.exit(0 if ok else 1)
