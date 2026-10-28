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

def apply_arr(g, a):
    """Apply group element g to array a, return array."""
    return g(a.copy())

def orbit_reps(n, option):
    G = generate_group(option)
    seen = set()
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(apply_arr(g, a)) for g in G)
        seen |= orb
        yield a

def stabilizer_indices(a, G):
    key = array_to_chain(a)
    return frozenset(i for i, g in enumerate(G)
                     if array_to_chain(apply_arr(g, a)) == key)

def element_index(G, k, sample):
    """Identify group element k (function) with an index in G."""
    for j, g in enumerate(G):
        if all(array_to_chain(apply_arr(g, x)) ==
               array_to_chain(apply_arr(k, x)) for x in sample):
            return j
    return None

def stabilizer_conjclass(a, option):
    """Canonical form of the conjugacy class of Stab(a) in G."""
    G = generate_group(option)
    H = stabilizer_indices(a, G)
    # Sample of chains big enough to distinguish group elements
    sample = list(all_chains(2, option))[:20] if option in [2, 3] else [a]
    # Actually build sample from current n
    # (we pass it in via closure; simpler: use n=2 chains, faithful)
    sample = list(all_chains(2, 1))[:20]  # universal sample for PL, faithful
    # Find inverse for each g
    invs = {}
    for i, g in enumerate(G):
        for j, h in enumerate(G):
            if all(array_to_chain(apply_arr(g, apply_arr(h, x))) ==
                   array_to_chain(x) for x in sample):
                invs[i] = j
                break
    conjugates = set()
    for i, g in enumerate(G):
        ginv = G[invs[i]]
        conj = frozenset(
            element_index(G,
                lambda x, h=G[k], g=g, ginv=ginv: g(h(ginv(x))),
                sample)
            for k in H
        )
        conjugates.add(conj)
    return frozenset(sorted(conjugates, key=lambda s: tuple(sorted(s)))[0])

def stabilizer_dist(n, option):
    dist = Counter()
    for a in orbit_reps(n, option):
        dist[stabilizer_conjclass(a, option)] += 1
    return dist

for n in [2, 4]:
    d_bpl = stabilizer_dist(n, 2)
    d_bu = stabilizer_dist(n, 3)
    print(f"\nn={n}")
    print(f"  BPL: {dict(d_bpl)}")
    print(f"  BU:  {dict(d_bu)}")
    print(f"  Match? {d_bpl == d_bu}")
