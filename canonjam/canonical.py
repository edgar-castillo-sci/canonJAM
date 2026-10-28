"""Canonicalization of JAM strings for duplicate detection."""

import numpy as np


# ─────────────────────────────────────────────
# Basic operations
# ─────────────────────────────────────────────

def rot(a):
    """Cyclic column rotation: 0→1, 1→2, 2→0."""
    return np.array(a[:, [1, 2, 0]])


def transp(a):
    """Swap columns 1 and 2."""
    return np.array(a[:, [0, 2, 1]])


def flip(a):
    """Invert the order of layers."""
    return np.flipud(a)


def sign(a):
    """
    Sign change. Reflects each layer about its mid-plane.

    - 2-character tokens: +x ↔ -x (except +0 and *x)
    - 6-character tokens: (+x-y) ↔ (-x+y) only if x != y
    """
    y = np.copy(a)
    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            s = y[i, j]
            if len(s) == 2:
                letter = s[1]
                sign_char = s[0]
                if letter != '0' and sign_char != '*':
                    if sign_char == '+':
                        y[i, j] = '-' + letter
                    elif sign_char == '-':
                        y[i, j] = '+' + letter
            elif len(s) == 6:
                sign1, letter1 = s[1], s[2]
                sign2, letter2 = s[3], s[4]
                if letter1 != letter2:
                    if sign1 == '+':
                        y[i, j] = '(-' + letter1 + '+' + letter2 + ')'
                    elif sign1 == '-':
                        y[i, j] = '(+' + letter1 + '-' + letter2 + ')'
    return y


# ─────────────────────────────────────────────
# Array ↔ chain conversion
# ─────────────────────────────────────────────

def array_to_chain(a):
    """Convert an array of tokens to its JAM string representation."""
    parts = []
    for col in range(a.shape[1]):
        parts.append(''.join(a[:, col]))
    return '/'.join(parts)


def chain_to_array(chain):
    """Convert a JAM string to an array of tokens."""
    blocks = chain.split('/')
    columns = []
    for block in blocks:
        tokens = []
        i = 0
        while i < len(block):
            if block[i] == '(':
                tokens.append(block[i:i+6])
                i += 6
            else:
                tokens.append(block[i:i+2])
                i += 2
        columns.append(tokens)
    return np.array(columns).T


# ─────────────────────────────────────────────
# Group construction
# ─────────────────────────────────────────────

def elements_S3():
    """Return the 6 elements of S_3 as functions."""
    return [
        lambda a: a,
        lambda a: rot(a),
        lambda a: rot(rot(a)),
        lambda a: transp(a),
        lambda a: rot(transp(a)),
        lambda a: rot(rot(transp(a))),
    ]


def generate_group(optionx):
    """
    Generate the group of operations for the given option.

    Planar options (1, 2, 5): no buckling. The group is S3 × {e, flip},
    with 12 elements. Sign does not apply (option 5's alphabet is sign-invariant,
    so sign·flip ≡ flip on X_5).

    Buckled options (3, 4, 6, 7, 8): the relevant vertical symmetry is the
    composition sign·flip (global reflection). The group is
    S3 × {e, sign·flip}, with 12 elements.
    """
    S3 = elements_S3()

    if optionx in [1, 2, 5]:
        Z2_vertical = [
            lambda a: a,
            lambda a: flip(a.copy())
        ]
    else:
        Z2_vertical = [
            lambda a: a,
            lambda a: sign(flip(a.copy()))
        ]

    operations = []
    for s in S3:
        for v in Z2_vertical:
            def op(a, s=s, v=v):
                return v(s(a))
            operations.append(op)

    return operations


# ─────────────────────────────────────────────
# Canonical key
# ─────────────────────────────────────────────

def canonical_key(a, optionx):
    """Compute the canonical key of a under the group of the given option."""
    operations = generate_group(optionx)
    chains = []
    for op in operations:
        x = op(a.copy())
        chains.append(array_to_chain(x))
    return min(chains)


def filter_duplicates(stackinglist, optionx):
    """Detect duplicates using canonical keys."""
    dicc = {}
    for a in stackinglist:
        key = canonical_key(a, optionx)
        if key not in dicc:
            dicc[key] = a
    return list(dicc.values())

# ─────────────────────────────────────────────
# Optimal computation of κ
# ─────────────────────────────────────────────

def sort_cols(a):
    """Return a copy of a with its columns sorted lexicographically."""
    cols = [tuple(a[:, i]) for i in range(a.shape[1])]
    return np.array(sorted(cols), dtype=object).T


def canonical_key_fast(a, optionx):
    """Optimal computation of κ via column sorting.

    Computes κ(a) = min(σ(sort_cols(a)), σ(sort_cols(v(a)))), where v is
    the non-trivial element of the Z/2 factor (flip for planar options,
    sign∘flip for buckled options). This is O(k) with a constant of 2,
    instead of the 12 group evaluations of `canonical_key`.

    Verified to agree with `canonical_key` for all 8 options and n=2,3;
    see tests/test_canonical_fast.py.
    """
    if optionx in [1, 2, 5]:
        va = flip(a.copy())
    else:
        va = sign(flip(a.copy()))
    return min(
        array_to_chain(sort_cols(a)),
        array_to_chain(sort_cols(va)),
    )
