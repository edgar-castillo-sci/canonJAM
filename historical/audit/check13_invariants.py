# ─────────────────────────────────────────────
# check13_invariants.py
# ─────────────────────────────────────────────
"""Check 13: S3_TO_CANONJAM is a computed (not fitted) group isomorphism.

Canonjam's ops act contragrediently (new[m] = old[σ⁻¹(m)]), so the map
in common.py uses an inverse-compensated match. The right statement to
test is at the level of *array actions*, not tuple labels:

    ops[φ(i)](ops[φ(j)](a)) == ops[φ(s3_compose(i,j))](a)

for every array a and all i, j. This is what we check, together with:

  (a) φ is a bijection on {0, …, 5}.
  (b) φ(identity) = identity.
  (c) φ sends each S3_LIST element to the ops index whose array action
      has the correct contragredient behaviour.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import S3_LIST, S3_TO_CANONJAM, s3_compose, s3_inverse
from canonjam import elements_S3

ops = elements_S3()
arr = np.array([[0, 1, 2]])

ok = True

# (a) bijection
if sorted(S3_TO_CANONJAM.values()) != list(range(6)):
    print(f"FAIL (a): not a bijection: {S3_TO_CANONJAM}")
    ok = False

# (b) identity ↦ identity
if S3_TO_CANONJAM[0] != 0:
    print(f"FAIL (b): φ(0) = {S3_TO_CANONJAM[0]} != 0")
    ok = False

# (c) contragredient correspondence:
#     ops[φ(i)]([0,1,2]) must equal S3_LIST[s3_inverse(i)]
for i in range(6):
    got = tuple(int(x) for x in ops[S3_TO_CANONJAM[i]](arr.copy())[0])
    want = tuple(S3_LIST[s3_inverse(i)])
    if got != want:
        print(f"FAIL (c): i={i}, φ(i)={S3_TO_CANONJAM[i]}: "
              f"ops acts as {got}, expected {want}")
        ok = False

# Homomorphism at the level of array actions:
#     ops[φ(i)](ops[φ(j)](a)) == ops[φ(i∘j)](a)
for i in range(6):
    for j in range(6):
        lhs = ops[S3_TO_CANONJAM[i]](ops[S3_TO_CANONJAM[j]](arr.copy()))
        rhs = ops[S3_TO_CANONJAM[s3_compose(i, j)]](arr.copy())
        if not np.array_equal(lhs, rhs):
            print(f"FAIL (hom): i={i}, j={j}: "
                  f"lhs={tuple(int(x) for x in lhs[0])}, "
                  f"rhs={tuple(int(x) for x in rhs[0])}")
            ok = False

print("PASS: φ is a bijection, preserves identity, respects the "
      "contragredient correspondence, and is a homomorphism of "
      "array actions" if ok else "FAIL")
sys.exit(0 if ok else 1)
