# ─────────────────────────────────────────────
# check15_burnside_convention.py
# ─────────────────────────────────────────────
"""Check 15: Burnside's lemma requires ROW SUMS of B, not the first row.

Paper (§5.3) claims:
  "the first row of B(G) applied to β_X gives the total number of orbits"

This is false. Under the correct convention β_X = M^T a, we have
a = B^T β_X, so:

  (C1) |X/G| = Σ_i a_{U_i}(X) = (row sums of B) · β_X   ← Burnside
  (C2) a_{U_1}(X) = (col 1 of B) · β_X, not (row 1 of B) · β_X

Three parts:
  Part 1 — verify C1 on X = G/U_i for all i.
  Part 2 — verify C1 on X = G/U_2 ⊔ G/U_6 (composite).
  Part 3 — show that row 1 of B does NOT give a_{U_1} (paper's convention
           is wrong), and that col 1 of B DOES (correct convention).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import (U_REPS, G_ELEMENTS, g_mul, g_inv,
                    left_cosets, table_of_marks, invert_fraction_matrix)


M = table_of_marks(wrong=False)
B = np.array([[float(x) for x in row]
              for row in invert_fraction_matrix(M.tolist())])
rowsums   = B.sum(axis=1)
first_row = B[0, :]
first_col = B[:, 0]


def beta_on_coset_direct(U_i, U_j):
    """β_{G/U_i}(U_j) computed from the action, not the mark formula."""
    count = 0
    for C in left_cosets(U_i):
        if all(frozenset(g_mul(h, x) for x in C) == C for h in U_j):
            count += 1
    return count


def beta_X_for_coset(U_i):
    return np.array([beta_on_coset_direct(U_i, U_REPS[j])
                     for j in range(1, 11)])


# ─────────────────────────────────────────────
# Part 1 — row sums reproduce Burnside on singletons
# ─────────────────────────────────────────────
print("Part 1: rowsums(B)·β_X = |X/G| for X = G/U_i (expected 1)")
ok_c1_singletons = True
paper_first_row_wrong_somewhere = False

for i in range(1, 11):
    beta_X = beta_X_for_coset(U_REPS[i])
    rs = rowsums   @ beta_X
    fr = first_row @ beta_X
    if not np.isclose(rs, 1.0):
        print(f"  FAIL: i={i}, rowsums·β_X = {rs:.4f}, expected 1")
        ok_c1_singletons = False
    if not np.isclose(fr, 1.0):
        paper_first_row_wrong_somewhere = True
    print(f"  i={i:2d}: rowsums={rs:.4f}, first_row={fr:.4f}  "
          f"({'rowsums OK' if np.isclose(rs, 1) else 'FAIL'} | "
          f"first_row {'≠' if not np.isclose(fr, 1) else '='} Burnside)")


# ─────────────────────────────────────────────
# Part 2 — row sums reproduce Burnside on a composite
# ─────────────────────────────────────────────
print("\nPart 2: composite X = G/U_2 ⊔ G/U_6, expected |X/G| = 2")
beta_X = beta_X_for_coset(U_REPS[2]) + beta_X_for_coset(U_REPS[6])
rs = rowsums   @ beta_X
fr = first_row @ beta_X
cs = B.sum(axis=0) @ beta_X
print(f"  rowsums·β_X   = {rs:.4f}  (correct, expected 2)")
print(f"  first_row·β_X = {fr:.4f}  (paper's claim, wrong)")
print(f"  colsums·β_X   = {cs:.4f}  (not Burnside)")
if not np.isclose(rs, 2.0):
    print("  FAIL: rowsums did not give 2")
    ok_c1_singletons = False
if not np.isclose(fr, 2.0):
    paper_first_row_wrong_somewhere = True


# ─────────────────────────────────────────────
# Part 3 — a_{U_1}: paper's row-1 vs correct col-1
# ─────────────────────────────────────────────
print("\nPart 3: a_{U_1}(X) for X = G/U_i (expected δ_{i,1})")
print("  row1(B)·β_X = 1/|U_i| (paper's convention; wrong)")
print("  col1(B)·β_X = δ_{i,1} (correct convention)")
ok_col1 = True
for i in range(1, 11):
    beta_X = beta_X_for_coset(U_REPS[i])
    r1 = first_row @ beta_X
    c1 = first_col @ beta_X
    expected = 1.0 if i == 1 else 0.0
    if not np.isclose(c1, expected):
        ok_col1 = False
    print(f"  i={i:2d}: row1·β={r1:.4f}, col1·β={c1:.4f}, "
          f"expected={expected:.1f}  "
          f"({'row1≡a' if np.isclose(r1, expected) else 'row1≠a'}, "
          f"{'col1≡a' if np.isclose(c1, expected) else 'col1≠a'})")


# ─────────────────────────────────────────────
# Verdict
# ─────────────────────────────────────────────
print()
ok = ok_c1_singletons and paper_first_row_wrong_somewhere and ok_col1
if ok:
    print("PASS: row sums of B reproduce Burnside; first row does NOT; "
          "col 1 of B (not row 1) gives a_{U_1}")
else:
    if not ok_c1_singletons:
        print("FAIL: rowsums did not reproduce Burnside")
    if not paper_first_row_wrong_somewhere:
        print("FAIL: paper's first-row claim also matched — counterexample too weak")
    if not ok_col1:
        print("FAIL: col 1 of B did not give a_{U_1}")
sys.exit(0 if ok else 1)
