import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
from collections import defaultdict
import numpy as np
from canonjam.canonical import generate_group, array_to_chain, canonical_key
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
    """Return orbit reps, one per orbit, ordered by canonical key."""
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
        bl = bpl_by_stab[H]
        bul = bu_by_stab[H]
        for a, b in zip(bl, bul):
            pairs.append((a, b))
    phi = {}
    for a, b in pairs:
        for i in range(len(G_bpl)):
            key = array_to_chain(G_bpl[i](a.copy()))
            img = array_to_chain(G_bu[i](b.copy()))
            phi[key] = img
    return phi, pairs

phi2, pairs2 = build_bijection(2)
phi4, pairs4 = build_bijection(4)

print(f"phi2 size: {len(phi2)}, phi4 size: {len(phi4)}")

# Check if phi4 is "phi2 applied to blocks of 2 layers"
def split_into_pairs(a):
    """Split a 4-layer chain into two 2-layer chains."""
    return (a[0:2], a[2:4])

def concat_pairs(a1, a2):
    return np.vstack([a1, a2])

match_block = 0
match_total = 0
for a_str, b_str in phi4.items():
    a = np.array([[c for c in block.split('/')] for block in [a_str]]).reshape(-1, 3)
    # Actually reconstruct array from string is easier via chain_to_array
    from canonjam.canonical import chain_to_array
    try:
        a = chain_to_array(a_str)
        b = chain_to_array(b_str)
    except Exception:
        continue
    match_total += 1
    a1, a2 = split_into_pairs(a)
    b1, b2 = split_into_pairs(b)
    phi2_a1 = phi2.get(array_to_chain(a1))
    phi2_a2 = phi2.get(array_to_chain(a2))
    if phi2_a1 is None or phi2_a2 is None:
        continue
    expected = concat_pairs(chain_to_array(phi2_a1), chain_to_array(phi2_a2))
    if array_to_chain(expected) == b_str:
        match_block += 1

print(f"phi4 = phi2 x phi2 on blocks: {match_block}/{match_total}")
