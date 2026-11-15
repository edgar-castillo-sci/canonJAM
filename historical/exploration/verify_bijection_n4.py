import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
from collections import defaultdict
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

def group_by_stabilizer(reps, option):
    groups = defaultdict(list)
    for a in reps:
        groups[exact_stabilizer(a, option)].append(a)
    return groups

n = 4
G_bpl = generate_group(2)
G_bu = generate_group(3)

reps_bpl = list(orbit_reps(n, 2))
reps_bu = list(orbit_reps(n, 3))
print(f"BPL orbits: {len(reps_bpl)}, BU orbits: {len(reps_bu)}")

bpl_by_stab = group_by_stabilizer(reps_bpl, 2)
bu_by_stab = group_by_stabilizer(reps_bu, 3)

print(f"Stabilizer classes BPL: { {tuple(sorted(H)): len(v) for H, v in bpl_by_stab.items()} }")
print(f"Stabilizer classes BU:  { {tuple(sorted(H)): len(v) for H, v in bu_by_stab.items()} }")

# Pair orbits 1-to-1 within each stabilizer class
pairs = []
for H, bpl_list in bpl_by_stab.items():
    if H not in bu_by_stab:
        print(f"  NO BU class for {tuple(sorted(H))}")
        continue
    bu_list = bu_by_stab[H]
    if len(bpl_list) != len(bu_list):
        print(f"  COUNT MISMATCH for {tuple(sorted(H))}: BPL={len(bpl_list)}, BU={len(bu_list)}")
        continue
    for a, b in zip(bpl_list, bu_list):
        pairs.append((a, b))

print(f"Pairs: {len(pairs)}")

# Build phi
phi = {}
conflicts = 0
for a, b in pairs:
    for i in range(len(G_bpl)):
        key = array_to_chain(G_bpl[i](a.copy()))
        img = array_to_chain(G_bu[i](b.copy()))
        if key in phi and phi[key] != img:
            conflicts += 1
        phi[key] = img

bpl_chains = set(array_to_chain(x) for x in all_chains(n, 2))
bu_chains = set(array_to_chain(x) for x in all_chains(n, 3))

print(f"\nConflicts: {conflicts}")
print(f"|phi| = {len(phi)}, |X_n^BPL| = {len(bpl_chains)}")
print(f"Covers BPL: {set(phi.keys()) == bpl_chains}")
print(f"Injective: {len(phi) == len(set(phi.values()))}")
print(f"Surjective: {set(phi.values()) == bu_chains}")
