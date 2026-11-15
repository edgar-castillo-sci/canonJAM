# ─────────────────────────────────────────────
# check02_row_vs_col.py
# ─────────────────────────────────────────────
"""Check 2: first row vs first column of M, diagonal entries."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import table_of_marks

M = table_of_marks(wrong=False)

print("M[0, :]  (row for U1) =", list(int(x) for x in M[0, :]))
print("M[:, 0]  (column U1)  =", list(int(x) for x in M[:, 0]))
print("diag(M)               =", [int(M[i, i]) for i in range(10)])

ok = (list(int(x) for x in M[0, :]) == [12, 0, 0, 0, 0, 0, 0, 0, 0, 0] and
      list(int(x) for x in M[:, 0]) == [12, 6, 6, 6, 4, 3, 2, 2, 2, 1] and
      [int(M[i, i]) for i in range(10)] == [12, 6, 2, 2, 4, 1, 2, 2, 2, 1])

print("PASS" if ok else
      "FAIL (the paper's sentence must be corrected: the "
      "(12,6,6,6,4,3,2,2,2,1) vector is the first *column*, not row)")
sys.exit(0 if ok else 1)
