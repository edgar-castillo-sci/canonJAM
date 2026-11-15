# ─────────────────────────────────────────────
# check03_full_matrix.py
# ─────────────────────────────────────────────
"""Check 3: full M(G) and B(G) with exact rational entries."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import table_of_marks, invert_fraction_matrix

M = table_of_marks(wrong=False)
B = invert_fraction_matrix(M.tolist())

print("M(G) =")
for row in M.tolist():
    print("  ", row)
print("\nB(G) = M(G)^-1 (exact):")
for row in B:
    print("  ", [str(x) for x in row])

ok = all(sum(M[i, k] * B[k][j] for k in range(10)) == (1 if i == j else 0)
         for i in range(10) for j in range(10))
print("\nM·B = I:", ok)
sys.exit(0 if ok else 1)
