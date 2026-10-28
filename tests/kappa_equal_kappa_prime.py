import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
import numpy as np
from canonjam.canonical import generate_group, flip, sign, array_to_chain
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def v_of(a, option):
    if option in [1, 2]:
        return flip(a.copy())
    return sign(flip(a.copy()))

def sort_cols(a):
    cols = sorted([tuple(a[:, i]) for i in range(3)])
    return np.array(cols).T

def kappa_literal(a, option):
    G = generate_group(option)
    return min(array_to_chain(g(a.copy())) for g in G)

def kappa_fast(a, option):
    return min(array_to_chain(sort_cols(a)),
               array_to_chain(sort_cols(v_of(a, option))))

ok = True
for option in range(1, 9):
    for n in [2, 3]:
        for a in all_chains(n, option):
            if kappa_literal(a, option) != kappa_fast(a, option):
                print(f"MISMATCH option={option} n={n} a={array_to_chain(a)}")
                ok = False
if ok:
    print("kappa == kappa' for all options and n=2,3")
