# ─────────────────────────────────────────────
# check14_transpose.py
# ─────────────────────────────────────────────
"""Check 14: the linear relation between marks β_X and orbit coefficients a.

The paper (§2.3, §5.2) writes β_X = M a and a = B β_X. The correct
relation, given M_{ij} = β_{G/U_i}(U_j), is β_X = M^T a and a = B^T β_X.

Strategy: for X = G/U_i (single orbit type), a = e_i, so β_X must equal
row i of M. We compute β_X directly from the action on cosets of U_i
(g·(g'U_i) = g'U_i  ⇔  (g')⁻¹gg' ∈ U_i), never using the mark formula,
so this is not circular. The wrong convention M a = column i of M fails
on every non-diagonal row.

Also validates a composite case X = G/U_2 ⊔ G/U_6 via linearity.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import (U_REPS, G_ELEMENTS, g_mul, g_inv,
                    left_cosets, table_of_marks, invert_fraction_matrix)


def beta_on_coset_direct(U_i, U_j):
    """β_{G/U_i}(U_j) = #{U_j-fixed cosets of U_i}, computed from the
    action. Independent of the mark formula."""
    cosets = left_cosets(U_i)
    count = 0
    for C in cosets:
        fixed = True
        for h in U_j:
            hC = frozenset(g_mul(h, x) for x in C)
            if hC != C:
                fixed = False
                break
        if fixed:
            count += 1
    return count


M = table_of_marks(wrong=False)
B = np.array([[float(x) for x in row]
              for row in invert_fraction_matrix(M.tolist())])

ok = True

# Part 1: β for X = G/U_i must equal row i of M, verified by M^T e_i
print("Part 1: β_{G/U_i} == M^T e_i (row i of M), direct computation")
for i in range(1, 11):
    U_i = U_REPS[i]
    beta_i = np.array([beta_on_coset_direct(U_i, U_REPS[j])
                       for j in range(1, 11)])
    if not np.array_equal(beta_i, M[i - 1]):
        print(f"  FAIL: i={i}, direct β = {beta_i.tolist()}, "
              f"row {i} of M = {M[i - 1].tolist()}")
        ok = False
print(f"  → 10/10 verified")

# Part 2: M^T e_i = row i, M e_i = column i, and they differ for every i
print("\nPart 2: M^T e_i (correct) vs M e_i (paper's convention)")
differ = 0
for i in range(1, 11):
    e_i = np.zeros(10); e_i[i - 1] = 1
    if not np.array_equal(M.T @ e_i, M[i - 1]):
        print(f"  FAIL: M^T e_{i} does not equal row {i} of M")
        ok = False
    if not np.array_equal(M @ e_i, M[i - 1]):
        differ += 1
print(f"  → M e_i ≠ row i of M for {differ}/10 values of i")
if differ == 0:
    print("  FAIL: M a and M^T a agree on all singletons (no counterexample)")
    ok = False

# Show one explicit counterexample
e_6 = np.zeros(10); e_6[5] = 1
print(f"\n  Explicit counterexample (i=6, X=G/U_6):")
print(f"    M^T e_6 = {M.T @ e_6}  (correct; matches direct β)")
print(f"    M   e_6 = {M @ e_6}  (paper's convention; wrong)")

# Part 3: composite X = G/U_2 ⊔ G/U_6, a = e_2 + e_6
print("\nPart 3: composite X = G/U_2 ⊔ G/U_6")
a = np.zeros(10); a[1] = 1; a[5] = 1
beta_X = np.array([beta_on_coset_direct(U_REPS[2], U_REPS[j]) +
                   beta_on_coset_direct(U_REPS[6], U_REPS[j])
                   for j in range(1, 11)])
correct = M.T @ a
wrong = M @ a
print(f"  direct β_X    = {beta_X.tolist()}")
print(f"  M^T a (correct) = {correct.tolist()}  "
      f"{'MATCH' if np.array_equal(correct, beta_X) else 'MISMATCH'}")
print(f"  M   a (paper)   = {wrong.tolist()}  "
      f"{'MATCH' if np.array_equal(wrong, beta_X) else 'MISMATCH'}")
if not np.array_equal(correct, beta_X):
    ok = False
if np.array_equal(wrong, beta_X):
    print("  FAIL: paper's convention also matches — counterexample too weak")
    ok = False

# Part 4: a = B^T β_X (recover the coefficients)
a_recovered = B.T @ beta_X
if not np.allclose(a_recovered, a):
    print(f"\n  FAIL: B^T β_X = {a_recovered.tolist()}, expected {a.tolist()}")
    ok = False
else:
    print(f"  B^T β_X = {a_recovered.tolist()}  (matches a = e_2 + e_6)")

print("\nPASS: β_X = M^T a (correct) holds; β_X = M a (paper) fails"
      if ok else "\nFAIL")
sys.exit(0 if ok else 1)
