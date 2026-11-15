import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
import numpy as np
from canonjam.canonical import generate_group, array_to_chain
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

def exact_stabilizer(a, option):
    G = generate_group(option)
    key = array_to_chain(a)
    return frozenset(i for i, g in enumerate(G)
                     if array_to_chain(g(a.copy())) == key)

def find_with_stabilizer(n, option, H):
    """Return a chain in X_n^option with exact stabilizer H."""
    G = generate_group(option)
    seen = set()
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(g(a.copy())) for g in G)
        seen |= orb
        if exact_stabilizer(a, option) == H:
            return a
    return None

n = 2
reps_bpl = list(orbit_reps(n, 2))
stabs_bpl = [exact_stabilizer(a, 2) for a in reps_bpl]

print(f"BPL exact stabilizers (n={n}):")
for a, H in zip(reps_bpl, stabs_bpl):
    print(f"  {array_to_chain(a)}  stab={sorted(H)}")

print(f"\nBuilding bijection:")
pairs = []
for a, H in zip(reps_bpl, stabs_bpl):
    b = find_with_stabilizer(n, 3, H)
    if b is None:
        print(f"  NO MATCH for {array_to_chain(a)} with stab {sorted(H)}")
    else:
        pairs.append((a, b))
        print(f"  {array_to_chain(a)}  ->  {array_to_chain(b)}")

print(f"\nFound {len(pairs)} pairs (expected 5)")
