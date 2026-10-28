import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
from collections import Counter
import numpy as np
from canonjam.canonical import generate_group, array_to_chain
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def orbit_size(a, G):
    return len(set(array_to_chain(g(a.copy())) for g in G))

def orbit_size_distribution(n, option):
    G = generate_group(option)
    seen = set()
    sizes = Counter()
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(g(a.copy())) for g in G)
        seen |= orb
        sizes[len(orb)] += 1
    return sizes

for n in [2, 4]:
    for option in [2, 3]:
        dist = orbit_size_distribution(n, option)
        name = "BPL" if option == 2 else "BU"
        print(f"n={n} {name}: orbit size distribution = {dict(sorted(dist.items()))}")
