"""
Benchmark: filtering time, original method vs canonical method.

Measures only the filtering stage (duplicate detection).
Candidate generation uses the canonical method in intermediate steps,
so that high n values are reachable without the original method being
a bottleneck at the generation stage. The candidate generation logic
itself lives in ``_helpers.py``.

Timing policy
-------------
The original method is O(m^2) in the number of candidates, where m grows
rapidly with n. For small n it is fast; for large n it becomes
prohibitively slow. We measure the original method only while its
estimated time is below MAX_TIME_OLD (in seconds). Above the threshold,
we report "—" and measure only the canonical method.

The estimate is computed from the first measured level, using O(m^2)
scaling:

    t_old(n) ~= t_old(n_ref) * (m(n) / m(n_ref))^2

The first level of each option is always measured for the original
method, so the estimate has a reference point.

Output
------
A timing table is printed to the console and written to
``benchmark_output.tsv`` next to this script.

Exit code
---------
0 if all measurements completed without error, 1 otherwise.

Override from the command line:

    python3 benchmark.py --levels 2 3 4 5 6
    python3 benchmark.py --max-time 60
"""

import argparse
import csv
import os
import sys
from time import perf_counter

from _helpers import generate_candidates, get_methods

from canonjam import filter_duplicates

DEFAULT_LEVELS = [2, 3, 4, 5]
DEFAULT_OPTIONS = [1, 5, 7]
DEFAULT_MAX_TIME = 30.0
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "benchmark_output.tsv"
)


def time_original(candidates, option):
    """Measure the filtering time of the original method.

    Parameters
    ----------
    candidates : list of numpy.ndarray
        Candidate chains at the target level.
    option : int
        JAM option in 1..8.

    Returns
    -------
    tuple
        ``(elapsed_seconds, number_of_unique_structures)``.
    """
    disc_old, conv = get_methods(option)
    canonical_candidates = [conv(c.copy()) for c in candidates]
    t0 = perf_counter()
    old_result = disc_old(canonical_candidates, option, 1)
    old_result = disc_old(old_result, option, 2)
    t1 = perf_counter()
    return t1 - t0, len(old_result)


def time_canonical(candidates, option):
    """Measure the filtering time of the canonical method.

    Parameters
    ----------
    candidates : list of numpy.ndarray
        Candidate chains at the target level.
    option : int
        JAM option in 1..8.

    Returns
    -------
    tuple
        ``(elapsed_seconds, number_of_unique_structures)``.
    """
    t0 = perf_counter()
    new_result = filter_duplicates(candidates, option)
    t1 = perf_counter()
    return t1 - t0, len(new_result)


def benchmark_option(option, levels, max_time):
    """Benchmark both methods for a given option and set of levels.

    The original method is measured while its estimated time (based on
    O(m^2) scaling from the first measured level) stays below ``max_time``.
    Above that threshold, only the canonical method is measured.

    Parameters
    ----------
    option : int
        JAM option in 1..8.
    levels : list of int
        Layer counts to benchmark.
    max_time : float
        Maximum estimated time (in seconds) for the original method.

    Returns
    -------
    list of dict
        One dict per level with keys: ``option``, ``n``, ``candidates``,
        ``t_old`` (float or None), ``t_new`` (float), ``measured`` (bool).
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
            _n_ref, m_ref, t_ref = reference
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
            "Output TSV file path (default: benchmark_output.tsv "
            "next to this script)."
        ),
    )
    return parser.parse_args()


def save_results(results, output_file):
    """Save benchmark results to a TSV file.

    Parameters
    ----------
    results : list of dict
        As returned by ``benchmark_option``.
    output_file : str
        Path to write.
    """
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
