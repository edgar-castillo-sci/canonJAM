"""
Validation: original pairwise method vs canonical method.

For each JAM option and each number of layers, this script:
  1. Generates all candidates using the original method.
  2. Filters them with the original pairwise method.
  3. Filters them with the canonical method.
  4. Verifies that both produce the same equivalence classes.

Output: a summary per option, with a final pass/fail. The candidate
generation logic itself lives in ``_helpers.py``.

Exit code: 0 if all pass, 1 if any fail.

Default validation levels: n=2 and n=3 are sufficient to verify that
both methods produce the same equivalence classes. For n=4, the
original method starts to be slow (~0.5-2 s per option). For n>=5, it
becomes prohibitively slow (minutes). The validation does not need
large n; it only needs to cover the cases where the fiber structure
is non-trivial.

The levels can be overridden from the command line:

    python3 validation.py --levels 2 3 4
"""

import argparse
import sys

from _helpers import generate_candidates, get_methods

from canonjam import canonical_key, filter_duplicates

DEFAULT_LEVELS = [2, 3]


def validate(option, n):
    """Validate both methods for a given option and number of layers.

    Parameters
    ----------
    option : int
        JAM option in 1..8.
    n : int
        Number of layers, >= 2.

    Returns
    -------
    tuple
        ``(passed, info)``. ``passed`` is a bool; ``info`` is the number
        of classes if passed, or a description of the mismatch otherwise.
    """
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
    old_keys = {canonical_key(c, option) for c in old_result}
    new_keys = {canonical_key(c, option) for c in new_result}

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
            "Example: python3 validation.py --levels 2 3 4"
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
