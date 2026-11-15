# ─────────────────────────────────────────────
# common.py
# ─────────────────────────────────────────────
"""Shared infrastructure for session-1 validation of ve_OaM.tex."""

import numpy as np
from fractions import Fraction
from canonjam import generate_group, elements_S3, rows_for_option
from itertools import product


# ─────────────────────────────────────────────
# Abstract group S3 × Z/2
# ─────────────────────────────────────────────

S3_LIST = [
    (0, 1, 2),   # e
    (1, 0, 2),   # (01)
    (2, 1, 0),   # (02)
    (0, 2, 1),   # (12)
    (1, 2, 0),   # (012)
    (2, 0, 1),   # (021)
]

def s3_compose(i, j):
    return S3_LIST.index(tuple(S3_LIST[i][S3_LIST[j][k]] for k in range(3)))

def s3_inverse(i):
    s = S3_LIST[i]
    return S3_LIST.index(tuple(sorted(range(3), key=lambda k: s[k])))

G_ELEMENTS = [(i, z) for i in range(6) for z in range(2)]

def g_mul(a, b):
    return (s3_compose(a[0], b[0]), a[1] ^ b[1])

def g_inv(a):
    return (s3_inverse(a[0]), a[1])

def g_id():
    return (0, 0)

def closure(elements):
    S = set(elements)
    changed = True
    while changed:
        changed = False
        for a in list(S):
            for b in list(S):
                c = g_mul(a, b)
                if c not in S:
                    S.add(c)
                    changed = True
    return frozenset(S)

def all_conjugates(H):
    return set(frozenset(g_mul(g_mul(a, h), g_inv(a)) for h in H)
               for a in G_ELEMENTS)

def normalizer(H):
    return frozenset(a for a in G_ELEMENTS
                     if frozenset(g_mul(g_mul(a, h), g_inv(a)) for h in H) == H)

def left_cosets(H):
    return set(frozenset(g_mul(g, h) for h in H) for g in G_ELEMENTS)


# ─────────────────────────────────────────────
# Group-element mapping 
# ─────────────────────────────────────────────

def _build_s3_to_canonjam():
    """Compute the bijection S3_LIST → canonjam.elements_S3() that is a
    group homomorphism, not an anti-homomorphism.

    Subtlety: canonjam's ops act *contragrediently*. For a permutation σ
    (as a function on positions), `rot(a) = a[:, [1,2,0]]` means
    new[m] = old[σ⁻¹(m)], so the *array* `ops[i]([0,1,2])` equals the
    tuple σ_i⁻¹, not σ_i. Therefore, to identify ops[i] with S3_LIST[j]
    (so that σ_i = S3_LIST[j] as permutations), we must match
    cj_acts[i] against S3_LIST[j]⁻¹ = S3_LIST[s3_inverse(j)].

    The inverse-compensated match restores the homomorphism property:
        ops[φ(i)](ops[φ(j)](a)) == ops[φ(s3_compose(i,j))](a)
    for every a, i, j. This is what check13_invariants asserts.
    """
    ops = elements_S3()
    arr = np.array([[0, 1, 2]])
    cj_acts = [tuple(int(x) for x in op(arr.copy())[0]) for op in ops]
    mapping = {i: cj_acts.index(tuple(S3_LIST[s3_inverse(i)]))
               for i in range(6)}
    assert sorted(mapping.values()) == list(range(6)), \
        f"not a bijection: {mapping}"
    return mapping

S3_TO_CANONJAM = _build_s3_to_canonjam()

def element_to_index(s_idx, z):
    """Index in generate_group(option)'s 12-element list."""
    return 2 * S3_TO_CANONJAM[s_idx] + z


# Paper's U1..U10 reps (v = (e,1), tau = (01), c = (012))
V_G   = (0, 1)
TAU_G = (1, 0)
C_G   = (4, 0)

U_REPS = {
    1:  closure({g_id()}),
    2:  closure({V_G}),
    3:  closure({TAU_G}),
    4:  closure({g_mul(TAU_G, V_G)}),
    5:  closure({C_G}),
    6:  closure({V_G, TAU_G}),
    7:  closure({(1,0), (2,0), (3,0), (4,0), (5,0)}),
    8:  closure({C_G, g_mul(TAU_G, V_G)}),
    9:  closure({g_mul(C_G, V_G)}),
    10: closure(set(G_ELEMENTS)),
}


# ─────────────────────────────────────────────
# Table of marks — paper's formula vs Pfeiffer's
# ─────────────────────────────────────────────

def mark_correct(U_i, U_j):
    """Correct β_{G/U_i}(U_j) = # left cosets of U_i fixed by U_j."""
    count = 0
    for C in left_cosets(U_i):
        ok = True
        for h in U_j:
            hC = frozenset(g_mul(h, x) for x in C)
            if hC != C:
                ok = False
                break
        if ok:
            count += 1
    return count

def mark_wrong(U_i, U_j):
    """Paper's draft formula: |N(U_i):U_i| if U_j ≲ U_i, else 0.
    (Missing the multiplicity factor |{U_i^g : U_j ≤ U_i^g}|.)"""
    ratio = len(normalizer(U_i)) // len(U_i)
    for H in all_conjugates(U_j):
        if H <= U_i:
            return ratio
    return 0

def table_of_marks(wrong=False):
    fn = mark_wrong if wrong else mark_correct
    return np.array([[fn(U_REPS[i], U_REPS[j])
                      for j in range(1, 11)] for i in range(1, 11)])


# ─────────────────────────────────────────────
# Fixed-point counts on X_n
# ─────────────────────────────────────────────

CONJ_CLASSES = [
    ("e",       (0, 0), 1),
    ("v",       (0, 1), 1),
    ("tau",     (1, 0), 3),
    ("tau_v",   (1, 1), 3),
    ("omega",   (4, 0), 2),
    ("omega_v", (4, 1), 2),
]

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def fixed_count(n, option, s_idx, z):
    ops = generate_group(option)
    op = ops[element_to_index(s_idx, z)]
    return sum(1 for a in all_chains(n, option)
               if np.array_equal(op(a.copy()), a))

def fixed_counts_table(n, option):
    return {name: fixed_count(n, option, s, z)
            for name, (s, z), _ in CONJ_CLASSES}


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

def invert_fraction_matrix(M):
    """Exact inverse of a rational matrix via Gauss-Jordan."""
    n = len(M)
    A = [[Fraction(M[i][j]) for j in range(n)] +
         [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = next(k for k in range(i, n) if A[k][i] != 0)
        A[i], A[pivot] = A[pivot], A[i]
        p = A[i][i]
        A[i] = [x / p for x in A[i]]
        for k in range(n):
            if k != i and A[k][i] != 0:
                f = A[k][i]
                A[k] = [A[k][j] - f * A[i][j] for j in range(2 * n)]
    return [[A[i][n + j] for j in range(n)] for i in range(n)]
