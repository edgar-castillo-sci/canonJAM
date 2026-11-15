import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from canonjam import filter_duplicates
from canonjam import rows_for_option

def gen_candidates_canonical(n, option):
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
        uniques = filter_duplicates(candidates, option)
    return candidates

for n in [6, 8, 10, 12]:
    t0 = time.perf_counter()
    cands = gen_candidates_canonical(n, 1)
    t_gen = time.perf_counter() - t0
    m = len(cands)
    t0 = time.perf_counter()
    unique = filter_duplicates(cands, 1)
    t_filt = time.perf_counter() - t0
    print(f"n={n}: m={m}, classes={len(unique)}, gen={t_gen:.2f}s, filter={t_filt:.2f}s", flush=True)
