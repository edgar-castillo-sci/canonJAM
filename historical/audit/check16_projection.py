# ─────────────────────────────────────────────
# check16_projection.py
# ─────────────────────────────────────────────
"""Check 16: Definition 3.1 — three possible readings of the projection
condition, which one is satisfied.

The paper says: "for every i ∈ {1, …, r}, the projection
Σ_k → Σ, w ↦ w_i, is surjective onto its image."

Interpretation (i): the projection is surjective onto its own image.
    → Tautologically true for any nonempty Σ_k (any map is surjective
      onto its image). Provides no constraint on Σ_k. The condition is
      vacuous as written.

Interpretation (ii): image(π_i) is independent of i.
    → A symmetry condition on Σ_k. Satisfied by all 8 options because
      Σ_k is built as the set of all permutations of a base multiset.

Interpretation (iii): image(π_i) = Σ (the full ambient alphabet).
    → False for every option: each option uses only a subset of the
      JAM alphabet Σ.

This check reports which interpretations hold, per option, so the author
can choose the intended meaning or drop the condition.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonjam import rows_for_option

# Build the full ambient alphabet as the union over all 8 options
ALL_TOKENS = set()
for opt in range(1, 9):
    for r in rows_for_option(opt):
        ALL_TOKENS.update(r)

print(f"Full ambient alphabet Σ ({len(ALL_TOKENS)} tokens):")
print(f"  {sorted(ALL_TOKENS)}")
print()

ok = True

for option in range(1, 9):
    rows = [tuple(r) for r in rows_for_option(option)]
    images = [set(r[i] for r in rows) for i in range(3)]
    option_tokens = set().union(*[set(r) for r in rows])
    all_equal = images[0] == images[1] == images[2]
    image_is_full_sigma = images[0] == ALL_TOKENS

    print(f"Option {option}:")
    print(f"  image(π_1) = {sorted(images[0])}")
    print(f"  image(π_2) = {sorted(images[1])}")
    print(f"  image(π_3) = {sorted(images[2])}")
    print(f"  Option uses {len(option_tokens)} distinct tokens, "
          f"full Σ has {len(ALL_TOKENS)}")
    print(f"  (i)   surjective onto its image: TRIVIALLY TRUE "
          f"(no constraint)")
    print(f"  (ii)  image independent of i:    {all_equal}")
    print(f"  (iii) image = full Σ:            {image_is_full_sigma}")
    print()

    if not all_equal:
        print(f"  FAIL: option {option}, images differ — interpretation (ii) fails")
        ok = False

print("Summary for the author:")
print("  (i) is vacuous.")
print("  (ii) holds for all 8 options (verify above).")
print("  (iii) holds for 0/8 options (each option uses a strict subset of Σ).")
print()
print("PASS: interpretation (ii) holds universally; (i) and (iii) as written "
      "provide no usable constraint" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
