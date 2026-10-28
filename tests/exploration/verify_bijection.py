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

def find_with_stabilizer(n, option, H):
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
G_bpl = generate_group(2)
G_bu = generate_group(3)
reps_bpl = list(orbit_reps(n, 2))
stabs_bpl = [exact_stabilizer(a, 2) for a in reps_bpl]

pairs = []
for a, H in zip(reps_bpl, stabs_bpl):
    b = find_with_stabilizer(n, 3, H)
    if b is not None:
        pairs.append((a, b))

print(f"Pairs: {len(pairs)}")

# Build phi as a dict chain -> chain, extending by equivariance
phi = {}
conflicts = []
for a, b in pairs:
    for i in range(len(G_bpl)):
        key = array_to_chain(G_bpl[i](a.copy()))
        img = array_to_chain(G_bu[i](b.copy()))
        if key in phi and phi[key] != img:
            conflicts.append((key, phi[key], img))
        phi[key] = img

print(f"\nDomain size: {len(phi)}")
print(f"Conflicts (two extensions disagree): {len(conflicts)}")
for c in conflicts[:5]:
    print(f"  {c}")

# Check that phi is a bijection onto X_n^BU
bu_chains = set(array_to_chain(x) for x in all_chains(n, 3))
bpl_chains = set(array_to_chain(x) for x in all_chains(n, 2))
print(f"\n|X_n^BPL| = {len(bpl_chains)}, |X_n^BU| = {len(bu_chains)}")
print(f"phi covers BPL domain: {set(phi.keys()) == bpl_chains}")
print(f"phi images are in BU: {set(phi.values()).issubset(bu_chains)}")
print(f"|phi images| = {len(set(phi.values()))}")
print(f"phi is injective: {len(phi) == len(set(phi.values()))}")
print(f"phi is surjective: {set(phi.values()) == bu_chains}")

# Verify equivariance: phi(g . a) == g . phi(a)
equiv_ok = True
for a, b in pairs:
    for i in range(len(G_bpl)):
        lhs = phi[array_to_chain(G_bpl[i](a.copy()))]
        rhs = array_to_chain(G_bu[i](b.copy()))
        if lhs != rhs:
            equiv_ok = False
            print(f"  EQUIV FAIL: g={i}, a={array_to_chain(a)}")
            break
print(f"\nEquivariance: {'PASS' if equiv_ok and not conflicts else 'FAIL'}")
