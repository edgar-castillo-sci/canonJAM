"""
Full validation report: canonical keys produced by both methods.

For each JAM option and each number of layers, this script:
  1. Generates all candidates using the original method.
  2. Filters them with the original pairwise method.
  3. Filters them with the canonical method.
  4. Computes the canonical key of every unique structure.
  5. Compares the two sets of keys.

Output: a detailed report written to reporte_completo_salida.txt,
with a summary on the console.

Exit code: 0 if all pass, 1 if any fail.

Default levels: n=2 and n=3 are sufficient to compare the full set of
canonical keys. Larger n makes the original method prohibitively slow
without adding new information about equivalence.

Override from the command line:

    python3 reporte_completo.py --levels 2 3 4
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
OUTPUT_FILE = os.path.join(_SCRIPT_DIR, "reporte_completo_salida.txt")


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


def report_option(option, n, out):
    """Write a detailed report for a given option and number of layers."""
    disc_old, conv = get_methods(option)

    candidates = generate_candidates(n, option)

    canonical_candidates = [conv(c.copy()) for c in candidates]
    old_result = disc_old(canonical_candidates, option, 1)
    old_result = disc_old(old_result, option, 2)

    new_result = filter_duplicates(candidates, option)

    old_keys = set(canonical_key(c, option) for c in old_result)
    new_keys = set(canonical_key(c, option) for c in new_result)

    identical = old_keys == new_keys

    out.write(f"\n{'=' * 70}\n")
    out.write(f"Option {option}, n = {n}\n")
    out.write(f"{'=' * 70}\n")
    out.write(f"Candidates: {len(candidates)}\n")
    out.write(f"Original method: {len(old_result)} structures, "
              f"{len(old_keys)} unique keys\n")
    out.write(f"Canonical method: {len(new_result)} structures, "
              f"{len(new_keys)} unique keys\n")
    out.write(f"Sets identical? {'YES' if identical else 'NO'}\n\n")

    if identical:
        out.write(f"Canonical keys ({len(old_keys)}):\n")
        for k in sorted(old_keys):
            out.write(f"  {k}\n")
    else:
        common = sorted(old_keys & new_keys)
        only_old = sorted(old_keys - new_keys)
        only_new = sorted(new_keys - old_keys)

        out.write(f"Common keys ({len(common)}):\n")
        for k in common:
            out.write(f"  {k}\n")

        out.write(f"\nOnly in original ({len(only_old)}):\n")
        for k in only_old:
            out.write(f"  {k}\n")

        out.write(f"\nOnly in canonical ({len(only_new)}):\n")
        for k in only_new:
            out.write(f"  {k}\n")

    return identical


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a full validation report comparing the canonical "
            "method against the original pairwise method."
        ),
        epilog=(
            "Example: python3 reporte_completo.py --levels 2 3 4"
        ),
    )
    parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        default=DEFAULT_LEVELS,
        help=(
            "Layer counts to report (default: %(default)s). "
            "n>=4 becomes slow for the original method; "
            "n>=5 is prohibitively slow."
        ),
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_FILE,
        help=(
            "Output file path (default: reporte_completo_salida.txt "
            "next to this script)."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    levels = args.levels

    print("=" * 60)
    print("Full validation report")
    print("=" * 60)
    print(f"Levels: {levels}")
    print(f"Output: {args.output}")
    print()

    all_pass = True

    out = open(args.output, "w")
    out.write("FULL VALIDATION REPORT\n")
    out.write("Original method vs canonical method\n")
    out.write(f"Options: 1-8. Levels: {levels}\n")

    # Summary table
    out.write(f"\n{'=' * 70}\n")
    out.write("SUMMARY\n")
    out.write(f"{'=' * 70}\n")
    out.write(f"{'Option':>8} {'n':>3} {'Original':>10} "
              f"{'Canonical':>10} {'Identical':>12}\n")
    out.write("-" * 50 + "\n")

    results = []
    for option in range(1, 9):
        for n in levels:
            disc_old, conv = get_methods(option)
            candidates = generate_candidates(n, option)
            canonical_candidates = [conv(c.copy()) for c in candidates]
            old_result = disc_old(canonical_candidates, option, 1)
            old_result = disc_old(old_result, option, 2)
            new_result = filter_duplicates(candidates, option)
            old_keys = set(canonical_key(c, option) for c in old_result)
            new_keys = set(canonical_key(c, option) for c in new_result)
            mark = "YES" if old_keys == new_keys else "NO"
            out.write(f"{option:>8} {n:>3} {len(old_keys):>10} "
                      f"{len(new_keys):>10} {mark:>12}\n")
            results.append((option, n, old_keys == new_keys))

    out.write("\n")
    if all(r[2] for r in results):
        out.write("Result: ALL PASS\n")
    else:
        out.write("Result: SOME FAILED\n")
        all_pass = False

    # Detailed report
    out.write(f"\n{'=' * 70}\n")
    out.write("DETAIL BY OPTION\n")
    out.write(f"{'=' * 70}\n")

    for option in range(1, 9):
        for n in levels:
            if not report_option(option, n, out):
                all_pass = False

    out.close()

    # Print summary to console
    with open(args.output) as f:
        for i, line in enumerate(f):
            if i < 50:
                print(line, end="")

    print(f"\n... see {args.output} for full details")
    print("=" * 60)
    if all_pass:
        print("Result: ALL PASS")
        sys.exit(0)
    else:
        print("Result: SOME FAILED")
        sys.exit(1)
