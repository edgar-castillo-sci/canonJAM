# canonjam/options.py
"""Single-layer rows for each JAM option (1-8).

Self-contained: depends only on the standard library. Does NOT import
xjam, and is safe to use without xjam installed.
"""

from itertools import permutations


_BASE_TOKENS = {
    1: ['+0', '+j', '+j'],
    2: ['+0', '+j', '+k'],
    3: ['+0', '+j', '-j'],
    5: ['+0', '*j', '(+k-k)'],
    6: ['*j', '+k', '-k'],
}

# Options with two independent base row sets (buckled Janus variants)
_TWO_BASES = {
    4: [['+0', '+j', '-k'], ['+0', '-j', '+k']],
    7: [['+0', '*j', '(+k-l)'], ['+0', '*j', '(-k+l)']],
    8: [['*j', '+k', '-l'], ['*j', '-k', '+l']],
}


def base_tokens_for_option(optionx):
    """Base tokens of one layer, before permutation (single-base options)."""
    if optionx in _BASE_TOKENS:
        return list(_BASE_TOKENS[optionx])
    raise ValueError(f"Option {optionx} has multiple base sets; "
                     f"use base_sets_for_option() instead.")


def base_sets_for_option(optionx):
    """Base token sets of one layer, before permutation (all options)."""
    if optionx in _BASE_TOKENS:
        return [list(_BASE_TOKENS[optionx])]
    if optionx in _TWO_BASES:
        return [list(b) for b in _TWO_BASES[optionx]]
    raise ValueError(f"Invalid option: {optionx}")


def rows_for_option(optionx):
    """Return all valid single-layer rows of the given JAM option."""
    rows = []
    for base in base_sets_for_option(optionx):
        rows.extend(list(p) for p in set(permutations(base, 3)))
    return rows
