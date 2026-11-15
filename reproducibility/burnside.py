import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
import numpy as np
from canonjam import generate_group
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def burnside_table(n, option):
    G = generate_group(option)
    counts = [0] * len(G)
    for a in all_chains(n, option):
        for i, g in enumerate(G):
            if np.array_equal(g(a.copy()), a):
                counts[i] += 1
    return counts

for n in range(2, 13):
    counts = burnside_table(n, 1)
    total = sum(counts)
    orbits = total // len(counts)
    print(f"n={n:2d}  |Fix| = {counts}  sum = {total:8d}  orbits = {orbits}")
