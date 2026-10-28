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

def stabilizer(a, G):
    key = array_to_chain(a)
    return frozenset(i for i, g in enumerate(G)
                     if array_to_chain(g(a.copy())) == key)

def orbit_representatives(n, option):
    G = generate_group(option)
    seen = set()
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(g(a.copy())) for g in G)
        seen |= orb
        yield a

def stabilizer_distribution(n, option):
    G = generate_group(option)
    dist = Counter()
    for a in orbit_representatives(n, option):
        dist[stabilizer(a, G)] += 1
    return dist

def normalize(dist):
    # Remap frozensets of indices to canonical strings by sorting the index tuples
    return Counter({tuple(sorted(s)): c for s, c in dist.items()})

for n in [2, 4]:
    d_bpl = normalize(stabilizer_distribution(n, 2))
    d_bu = normalize(stabilizer_distribution(n, 3))
    print(f"\nn={n}")
    print(f"  BPL stabilizer dist: {dict(d_bpl)}")
    print(f"  BU  stabilizer dist: {dict(d_bu)}")
    print(f"  Match? {d_bpl == d_bu}")
