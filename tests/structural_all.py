import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import product
import numpy as np
from canonjam.canonical import generate_group, flip, sign
from canonjam import rows_for_option

def all_chains(n, option):
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)

def v_of(a, option):
    # Opciones 1-2: flip puro. Opciones 3-8: sign∘flip.
    if option in [1, 2]:
        return flip(a.copy())
    return sign(flip(a.copy()))

def sorted_cols(a):
    return tuple(sorted(tuple(a[:, i]) for i in range(3)))

def key_prime(a, option):
    return min(sorted_cols(a), sorted_cols(v_of(a, option)))

KNOWN = {
    1: {2: 2, 3: 4}, 2: {2: 5, 3: 21}, 3: {2: 5, 3: 21}, 4: {2: 16, 3: 144},
    5: {2: 5, 3: 21}, 6: {2: 5, 3: 21}, 7: {2: 16, 3: 144}, 8: {2: 16, 3: 144},
}

for option in range(1, 9):
    G = generate_group(option)
    for n in [2, 3]:
        chains = list(all_chains(n, option))
        inv_ok = all(key_prime(g(a.copy()), option) == key_prime(a, option)
                     for a in chains for g in G)
        n_keys = len(set(key_prime(a, option) for a in chains))
        match = (n_keys == KNOWN[option][n])
        print(f"option={option} n={n}: inv={inv_ok} keys={n_keys} "
              f"orbits={KNOWN[option][n]} match={match}")
