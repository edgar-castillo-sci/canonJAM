"""
Validation: original pairwise method vs canonical method.

For each JAM option and each number of layers, this script:
  1. Generates all candidates using the original method.
  2. Filters them with the original pairwise method.
  3. Filters them with the canonical method.
  4. Verifies that both produce the same equivalence classes.

Output: a summary per option, with a final pass/fail.
Exit code: 0 if all pass, 1 if any fail.

Default validation levels: n=2 and n=3 are sufficient to verify that
both methods produce the same equivalence classes. For n=4, the
original method starts to be slow (~0.5-2 s per option). For n>=5, it
becomes prohibitively slow (minutes). The validation does not need
large n; it only needs to cover the cases where the fiber structure
is non-trivial.

The levels can be overridden from the command line:

    python3 validacion.py --levels 2 3 4
"""

import argparse
import numpy as np
import sys
import os
from itertools import permutations

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from xjam.libjamstd import (
        disc_equivalents as disc_old_std,
        conv2pseudocanonic as conv_std,
    )
    from xjam.libjamtdm import (
        disc_equivalents as disc_old_tdm,
        conv2pseudocanonic as conv_tdm,
    )
except ImportError as exc:
    raise SystemExit(
        "This comparison script requires xjam2, which is optional and "
        "not a dependency of canonJAM. See tests/comparison/README.md.\n"
        f"Underlying error: {exc}"
    ) from exc
from canonjam import (
    canonical_key,
    filter_duplicates,
    rows_for_option,
)


DEFAULT_LEVELS = [2, 3]


def get_methods(option):
    """Return the appropriate old-method functions for the given option."""
    if option in [1, 2, 3, 4]:
        return disc_old_std, conv_std
    return disc_old_tdm, conv_tdm


def generate_candidates(n, option):
    """Generate all candidates for n layers, replicating x.jam's logic."""
    disc_old, conv = get_methods(option)

    single = [np.array(r) for r in rows_for_option(option)]
    uniques = single.copy()

    candidates = single
    for level in range(2, n + 1):
        if level == 2:
            candidates = [
                np.vstack([a, b]) for a in uniques for b in single
            ]
        else:
            down = [np.vstack([a, b]) for a in uniques for b in single]
            up = [np.vstack([b, a]) for a in uniques for b in single]
            candidates = down + up

        canonical = [conv(c) for c in candidates]
        uniques = disc_old(canonical, option, 1)
        uniques = disc_old(uniques, option, 2)

    return candidates


def validate(option, n):
    """Validate both methods for a given option and number of layers."""
    disc_old, conv = get_methods(option)

    candidates = generate_candidates(n, option)

    # Original method
    canonical_candidates = [conv(c.copy()) for c in candidates]
    old_result = disc_old(canonical_candidates, option, 1)
    old_result = disc_old(old_result, option, 2)

    # Canonical method
    new_result = filter_duplicates(candidates, option)

    # Compare counts
    if len(old_result) != len(new_result):
        return False, f"count mismatch ({len(old_result)} vs {len(new_result)})"

    # Compare classes
    old_keys = set(canonical_key(c, option) for c in old_result)
    new_keys = set(canonical_key(c, option) for c in new_result)

    if old_keys != new_keys:
        return False, "class mismatch"

    return True, len(old_result)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Validate the canonical method against the original "
            "pairwise method for all JAM options."
        ),
        epilog=(
            "Example: python3 validacion.py --levels 2 3 4"
        ),
    )
    parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        default=DEFAULT_LEVELS,
        help=(
            "Layer counts to validate (default: %(default)s). "
            "n>=4 becomes slow for the original method; "
            "n>=5 is prohibitively slow."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    layers = args.levels

    print("=" * 60)
    print("Validation: original method vs canonical method")
    print("=" * 60)
    print(f"Levels: {layers}")
    print()

    all_pass = True

    for option in range(1, 9):
        print(f"Option {option}:")

        for n in layers:
            passed, info = validate(option, n)
            mark = "PASS" if passed else "FAIL"

            if passed:
                print(f"  n={n}: {mark} ({info} classes)")
            else:
                print(f"  n={n}: {mark} ({info})")
                all_pass = False

        print()

    print("=" * 60)
    if all_pass:
        print("Result: ALL PASS")
        sys.exit(0)
    else:
        print("Result: SOME FAILED")
        sys.exit(1)
