"""
Benchmark: filtering time, original method vs canonical method.

Measures only the filtering stage (duplicate detection).
Candidate generation uses the canonical method in intermediate steps,
so that high n values are reachable without the original method being
a bottleneck at the generation stage.

Timing policy
-------------
The original method is O(m²) in the number of candidates, where m grows
rapidly with n. For small n it is fast; for large n it becomes
prohibitively slow. We measure the original method only while its
estimated time is below MAX_TIME_OLD (in seconds). Above the threshold,
we report "—" and measure only the canonical method.

The estimate is computed from the first measured level, using O(m²)
scaling:

    t_old(n) ≈ t_old(n_ref) * (m(n) / m(n_ref))²

The first level of each option is always measured for the original
method, so the estimate has a reference point.

Output
------
A timing table is printed to the console and written to
benchmark_salida.tsv next to this script.

Exit code
---------
0 if all measurements completed without error, 1 otherwise.

Override from the command line:

    python3 benchmark.py --levels 2 3 4 5 6
    python3 benchmark.py --max-time 60
"""

import argparse
import csv
import numpy as np
import sys
import os
from itertools import permutations
from time import perf_counter

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


DEFAULT_LEVELS = [2, 3, 4, 5]
DEFAULT_OPTIONS = [1, 5, 7]
DEFAULT_MAX_TIME = 30.0
OUTPUT_FILE = os.path.join(_SCRIPT_DIR, "benchmark_salida.tsv")


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


def time_original(candidates, option):
    """Measure the filtering time of the original method."""
    disc_old, conv = get_methods(option)
    canonical_candidates = [conv(c.copy()) for c in candidates]
    t0 = perf_counter()
    old_result = disc_old(canonical_candidates, option, 1)
    old_result = disc_old(old_result, option, 2)
    t1 = perf_counter()
    return t1 - t0, len(old_result)


def time_canonical(candidates, option):
    """Measure the filtering time of the canonical method."""
    t0 = perf_counter()
    new_result = filter_duplicates(candidates, option)
    t1 = perf_counter()
    return t1 - t0, len(new_result)


def benchmark_option(option, levels, max_time):
    """
    Benchmark both methods for a given option and set of levels.

    The original method is measured while its estimated time (based on
    O(m²) scaling from the first measured level) stays below max_time.
    Above that threshold, only the canonical method is measured.

    Returns a list of dicts with the results.
    """
    print(f"\n{'=' * 70}")
    print(f"Option {option}")
    print(f"{'=' * 70}\n")
    print(f"{'n':>3} {'Candidates':>12} {'Original (s)':>14} "
          f"{'Canonical (s)':>14} {'Speedup':>10}")
    print("-" * 60)

    results = []
    reference = None  # (n_ref, m_ref, t_ref)

    for n in levels:
        print(f"  Generating n={n}...", end=" ", flush=True)
        candidates = generate_candidates(n, option)
        m = len(candidates)
        print(f"{m}")

        # Always measure canonical
        t_new, _ = time_canonical(candidates, option)

        # Decide whether to measure original
        if reference is None:
            # First level: always measure to establish reference
            t_old, _ = time_original(candidates, option)
            reference = (n, m, t_old)
            t_old_str = f"{t_old:>14.3f}"
            speedup_str = f"{t_old / t_new:>9.1f}x" if t_new > 0 else "—"
            measured = True
        else:
            n_ref, m_ref, t_ref = reference
            t_old_est = t_ref * (m / m_ref) ** 2

            if t_old_est <= max_time:
                t_old, _ = time_original(candidates, option)
                t_old_str = f"{t_old:>14.3f}"
                speedup_str = f"{t_old / t_new:>9.1f}x" if t_new > 0 else "—"
                measured = True
            else:
                t_old_str = f"{'—':>14}"
                speedup_str = f"{'—':>10}"
                measured = False

        print(f"{n:>3} {m:>12} {t_old_str} "
              f"{t_new:>14.3f} {speedup_str}")

        results.append({
            "option": option,
            "n": n,
            "candidates": m,
            "t_old": t_old if measured else None,
            "t_new": t_new,
            "measured": measured,
        })

    print()
    return results


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark the filtering stage of the original pairwise "
            "method against the canonical method."
        ),
        epilog=(
            "Examples:\n"
            "  python3 benchmark.py\n"
            "  python3 benchmark.py --levels 2 3 4 5 6\n"
            "  python3 benchmark.py --options 1 5 --max-time 60\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        default=DEFAULT_LEVELS,
        help=(
            "Layer counts to benchmark (default: %(default)s). "
            "Higher levels may take a long time."
        ),
    )
    parser.add_argument(
        "--options",
        type=int,
        nargs="+",
        default=DEFAULT_OPTIONS,
        help=(
            "JAM options to benchmark (default: %(default)s). "
            "Options 1, 2, 3, 4 use libjamstd; options 5-8 use libjamtdm."
        ),
    )
    parser.add_argument(
        "--max-time",
        type=float,
        default=DEFAULT_MAX_TIME,
        help=(
            "Maximum estimated time (in seconds) for the original method. "
            "Levels where the estimate exceeds this value are skipped "
            "for the original method (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_FILE,
        help=(
            "Output TSV file path (default: benchmark_salida.tsv "
            "next to this script)."
        ),
    )
    return parser.parse_args()


def save_results(results, output_file):
    """Save benchmark results to a TSV file."""
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow([
            "option", "n", "candidates",
            "t_old", "t_new", "speedup", "measured",
        ])
        for r in results:
            if r["measured"] and r["t_new"] > 0:
                speedup = f"{r['t_old'] / r['t_new']:.2f}"
                t_old = f"{r['t_old']:.4f}"
            else:
                speedup = "—"
                t_old = "—"
            writer.writerow([
                r["option"], r["n"], r["candidates"],
                t_old, f"{r['t_new']:.4f}", speedup, r["measured"],
            ])


if __name__ == "__main__":
    args = parse_args()

    print("=" * 70)
    print("Benchmark: original method vs canonical method")
    print("=" * 70)
    print()
    print("Measures only the filtering stage (duplicate detection).")
    print("Candidate generation uses the canonical method in intermediate steps.")
    print(f"Levels: {args.levels}")
    print(f"Options: {args.options}")
    print(f"Max estimated time for original method: {args.max_time} s")
    print()

    all_results = []

    for option in args.options:
        results = benchmark_option(option, args.levels, args.max_time)
        all_results.extend(results)

    save_results(all_results, args.output)

    print(f"Results saved to: {args.output}")
    print("=" * 70)
    print("Done.")
    sys.exit(0)
