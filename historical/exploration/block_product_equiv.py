import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
from collections import defaultdict
import numpy as np
from canonjam.canonical import (generate_group, array_to_chain,
                                 chain_to_array)
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def exact_stabilizer(a, option):
    G = generate_group(option)
    key = array_to_chain(a)
    return frozenset(i for i, g in enumerate(G)
                     if array_to_chain(g(a.copy())) == key)

def orbit_reps_canonical(n, option):
    G = generate_group(option)
    seen = set()
    reps = []
    for a in all_chains(n, option):
        key = array_to_chain(a)
        if key in seen:
            continue
        orb = set(array_to_chain(g(a.copy())) for g in G)
        seen |= orb
        reps.append(a)
    return sorted(reps, key=lambda a: array_to_chain(a))

def build_bijection(n):
    G_bpl = generate_group(2)
    G_bu = generate_group(3)
    reps_bpl = orbit_reps_canonical(n, 2)
    reps_bu = orbit_reps_canonical(n, 3)
    bpl_by_stab = defaultdict(list)
    bu_by_stab = defaultdict(list)
    for a in reps_bpl:
        bpl_by_stab[exact_stabilizer(a, 2)].append(a)
    for b in reps_bu:
        bu_by_stab[exact_stabilizer(b, 3)].append(b)
    pairs = []
    for H in bpl_by_stab:
        if H not in bu_by_stab:
            continue
        for a, b in zip(bpl_by_stab[H], bu_by_stab[H]):
            pairs.append((a, b))
    phi = {}
    for a, b in pairs:
        for i in range(len(G_bpl)):
            key = array_to_chain(G_bpl[i](a.copy()))
            img = array_to_chain(G_bu[i](b.copy()))
            phi[key] = img
    return phi, pairs

phi2, _ = build_bijection(2)
G_bpl = generate_group(2)
G_bu = generate_group(3)

def phi_block(a):
    """Apply phi2 to each block of 2 layers."""
    n = a.shape[0]
    blocks = [a[i:i+2] for i in range(0, n, 2)]
    out = [chain_to_array(phi2[array_to_chain(b)]) for b in blocks]
    return np.vstack(out)

for n in [2, 4, 6]:
    fails = 0
    total = 0
    for a in all_chains(n, 2):
        for i, g_b in enumerate(G_bpl):
            lhs = phi_block(g_b(a.copy()))
            rhs = G_bu[i](phi_block(a.copy()))
            total += 1
            if not np.array_equal(lhs, rhs):
                fails += 1
    print(f"n={n}: {fails} failures out of {total} checks")
