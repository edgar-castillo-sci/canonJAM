"""Benchmark: literal vs fast canonical filter (no xjam2 required).

Generates candidate sets with the canonical-dedup generator
(same as scalability.py), then measures the filter time of both
implementations for each (option, k):

    t_lit  = time of filter_duplicates(S, option)          # literal key
    t_fast = time of a fast filter using canonical_key_fast

Also reports m (candidate count) and nclasses, and asserts that both
filters produce the same number of classes (sanity check; the full
key-by-key check is covered by kappa_equal_kappa_prime.py for n=2,3).

BBU k=5 (option 7, k=5) is included as its own row: the literal
filter is skipped there (t_lit = "---") because it is prohibitively
slow and not required for the table.

Output: benchmark_fast.csv next to this script, columns
    option,k,m,t_lit,t_fast,nclasses

Usage:
    python3 benchmark_fast.py
    python3 benchmark_fast.py --options 1 5 --levels 2 3 4
    python3 benchmark_fast.py --no-bbu5
"""

import argparse
import csv
import os
import sys
import time

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, os.path.dirname(_SCRIPT_DIR))

import numpy as np
from canonjam import (
    canonical_key_fast,
    filter_duplicates,
    rows_for_option,
)

OUTPUT_FILE = os.path.join(_SCRIPT_DIR, "benchmark_fast.csv")

REPS_SMALL = 3          # median of 3 runs for small candidate sets
REPS_LARGE = 1          # single run for large ones (BBU k=5)
LARGE_THRESHOLD = 5000


# ---------------------------------------------------------------------------
# Generation (self-contained, identical logic to scalability.py)
# ---------------------------------------------------------------------------

def gen_candidates_canonical(n, option, dedup=None):
    """Generate all candidates for n layers using canonical dedup in
    intermediate steps.

    `dedup` is a callable (chains, option) -> unique chains. Defaults to
    `filter_duplicates` (literal key). Pass `filter_fast` to use the
    optimal key in the intermediate dedup (much faster for BBU k=5;
    the final candidate set S is the same up to isomorphism).
    """
    if dedup is None:
        dedup = filter_duplicates

    single = [np.array(r) for r in rows_for_option(option)]
    uniques = single.copy()
    candidates = single
    for level in range(2, n + 1):
        if level == 2:
            candidates = [np.vstack([a, b]) for a in uniques for b in single]
        else:
            down = [np.vstack([a, b]) for a in uniques for b in single]
            up = [np.vstack([b, a]) for a in uniques for b in single]
            candidates = down + up
        uniques = dedup(candidates, option)
    return candidates


# ---------------------------------------------------------------------------
# Fast filter (mirrors filter_duplicates semantics, uses optimal key)
# ---------------------------------------------------------------------------

def filter_fast(chains, optionx):
    seen = set()
    out = []
    for c in chains:
        k = canonical_key_fast(c, optionx)
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------

def timeit(fn, reps):
    ts = []
    result = None
    for _ in range(reps):
        t0 = time.perf_counter()
        result = fn()
        ts.append(time.perf_counter() - t0)
    ts.sort()
    return ts[len(ts) // 2], result


def benchmark_row(option, k, do_lit=True):
    # BBU k=5 generation may be slow if the intermediate dedup uses the
    # literal key; use the fast dedup there.
    if option == 7 and k >= 5:
        S = gen_candidates_canonical(k, option, dedup=filter_fast)
    else:
        S = gen_candidates_canonical(k, option)

    m = len(S)
    reps = REPS_LARGE if m > LARGE_THRESHOLD else REPS_SMALL

    t_fast, uniq_fast = timeit(lambda: filter_fast(S, option), reps)
    nclass_fast = len(uniq_fast)

    if do_lit:
        t_lit, uniq_lit = timeit(lambda: filter_duplicates(S, option), reps)
        nclass_lit = len(uniq_lit)
        assert nclass_lit == nclass_fast, (
            f"nclasses mismatch: option={option} k={k} "
            f"lit={nclass_lit} fast={nclass_fast}"
        )
    else:
        t_lit = None
        nclass_lit = None

    return {
        "option": option, "k": k, "m": m,
        "t_lit": t_lit, "t_fast": t_fast,
        "nclasses": nclass_fast, "nclasses_lit": nclass_lit,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--options", type=int, nargs="+", default=[1, 5, 7])
    p.add_argument("--levels", type=int, nargs="+", default=[2, 3, 4, 5])
    p.add_argument("--no-bbu5", action="store_true",
                   help="Skip the BBU k=5 row (option 7, k=5)")
    p.add_argument("--output", default=OUTPUT_FILE)
    return p.parse_args()


def main():
    args = parse_args()

    print("Benchmark: literal vs fast canonical filter")
    print(f"Options: {args.options}")
    print(f"Levels:  {args.levels}")
    print(f"Output:  {args.output}")
    print("-" * 60)

    rows = []
    for opt in args.options:
        for k in args.levels:
            is_bbu5 = (opt == 7 and k == 5)
            if is_bbu5 and args.no_bbu5:
                continue

            print(f"option={opt} k={k}...", end=" ", flush=True)
            r = benchmark_row(opt, k, do_lit=not is_bbu5)
            if r["t_lit"] is not None:
                print(f"m={r['m']}  t_lit={r['t_lit']:.4f}s  "
                      f"t_fast={r['t_fast']:.4f}s  nclass={r['nclasses']}",
                      flush=True)
            else:
                print(f"m={r['m']}  t_lit=---  "
                      f"t_fast={r['t_fast']:.4f}s  nclass={r['nclasses']}",
                      flush=True)
            rows.append(r)

    with open(args.output, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["option", "k", "m", "t_lit", "t_fast", "nclasses"])
        for r in rows:
            w.writerow([
                r["option"], r["k"], r["m"],
                f"{r['t_lit']:.4f}" if r["t_lit"] is not None else "---",
                f"{r['t_fast']:.4f}",
                r["nclasses"],
            ])

    print("-" * 60)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
