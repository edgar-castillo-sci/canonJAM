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

def stabilizer_conjclass(a, option):
    """Conjugacy class of Stab(a) in G_option, as a canonical frozenset."""
    G = generate_group(option)
    key = array_to_chain(a)
    H = frozenset(i for i, g in enumerate(G) if array_to_chain(g(a.copy())) == key)
    # Use a universal faithful sample (PL n=2 has 9 chains; the group acts
    # faithfully on X_2^PL, so it distinguishes the 12 elements).
    sample = list(all_chains(2, 1))
    def idx(k):
        for j, g in enumerate(G):
            if all(array_to_chain(g(x.copy())) == array_to_chain(k(x.copy()))
                   for x in sample):
                return j
        return None
    invs = {}
    for i, g in enumerate(G):
        for j, h in enumerate(G):
            if all(array_to_chain(g(h(x.copy()))) == array_to_chain(x)
                   for x in sample):
                invs[i] = j
                break
    conj = set()
    for i, g in enumerate(G):
        ginv = G[invs[i]]
        conj.add(frozenset(idx(lambda x, h=G[k], g=g, ginv=ginv: g(h(ginv(x))))
                            for k in H))
    return frozenset(sorted(conj, key=lambda s: tuple(sorted(s)))[0])

n = 2
reps_bpl = list(orbit_reps(n, 2))
reps_bu = list(orbit_reps(n, 3))
stabs_bpl = [stabilizer_conjclass(a, 2) for a in reps_bpl]
stabs_bu = [stabilizer_conjclass(b, 3) for b in reps_bu]

pairs = []
used = set()
for i, a in enumerate(reps_bpl):
    for j, b in enumerate(reps_bu):
        if j in used:
            continue
        if stabs_bpl[i] == stabs_bu[j]:
            pairs.append((a, b))
            used.add(j)
            break

print(f"Found {len(pairs)} pairs (expected 5)")
for a, b in pairs:
    print(f"  {array_to_chain(a)}  ->  {array_to_chain(b)}")
