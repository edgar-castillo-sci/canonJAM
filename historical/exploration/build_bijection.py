import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
import numpy as np
from canonjam.canonical import generate_group, array_to_chain, canonical_key
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def orbit_reps(n, option):
    G = generate_group(option)
    seen = set()
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(g(a.copy())) for g in G)
        seen |= orb
        yield a

def stabilizer_indices(a, G):
    key = array_to_chain(a)
    return frozenset(i for i, g in enumerate(G)
                     if array_to_chain(g(a.copy())) == key)

n = 2
G = generate_group(2)
reps_bpl = list(orbit_reps(n, 2))
reps_bu = list(orbit_reps(n, 3))

# Pair by matching stabilizer
pairs = []
used = set()
for a in reps_bpl:
    Ha = stabilizer_indices(a, G)
    for b in reps_bu:
        if id(b) in used:
            continue
        Hb = stabilizer_indices(b, G)
        if Ha == Hb:
            pairs.append((a, b))
            used.add(id(b))
            break

print(f"Found {len(pairs)} pairs (expected 5)")
for a, b in pairs:
    print(f"  {array_to_chain(a)}  ->  {array_to_chain(b)}")
