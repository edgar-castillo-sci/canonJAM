"""Core canonicalization routines for JAM chains.

Given a ``k × 3`` array of tokens (a "chain"), the canonical key is the
lexicographic minimum of the orbit under the symmetry group. Two chains
are equivalent (related by a symmetry operation) if and only if they
have the same canonical key. This property reduces duplicate detection
from O(m²) pairwise comparisons to O(m) via a dictionary.

The symmetry group is G = S₃ × ℤ/2, of order 12. The S₃ factor permutes
the three columns (Wyckoff sites 1a, 1b, 1c); the ℤ/2 factor is the
vertical symmetry, which is ``flip`` for planar options (1, 2, 5) and
``sign ∘ flip`` for buckled options (3, 4, 6, 7, 8).

Two implementations of the key are provided:

- `canonical_key`: the literal definition (minimum over the 12 group
  elements). Cost: 12 group evaluations, O(k) each.
- `canonical_key_fast`: the optimal computation via column sorting.
  Cost: 2 group evaluations, O(k) each. Verified to agree with
  `canonical_key` for all 8 options and n = 2, 3.

`filter_duplicates` uses `canonical_key` internally. See ADR-0002 in
``docs/adr/`` for the rationale (not `canonical_key_fast`).
"""

import numpy as np


# ─────────────────────────────────────────────
# Basic operations
# ─────────────────────────────────────────────

def rot(a):
    """Cyclic column rotation: 0 → 1, 1 → 2, 2 → 0.

    One of the three generators of the S₃ factor. Applied three times it
    returns the identity; combined with `transp`, it generates the full
    permutation group on the three columns.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    numpy.ndarray
        A new array where the new column 0 is the old column 1, the new
        column 1 is the old column 2, and the new column 2 is the old
        column 0.

    See Also
    --------
    transp : swap columns 1 and 2.
    flip : reverse the layer order.
    sign : reflect each layer about its mid-plane.

    Examples
    --------
    >>> import numpy as np
    >>> rot(np.array([['+0', '+j', '+k']])).tolist()
    [['+j', '+k', '+0']]
    """
    return np.array(a[:, [1, 2, 0]])


def transp(a):
    """Swap columns 1 and 2.

    One of the three generators of the S₃ factor. It is an involution:
    applied twice it returns the identity.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    numpy.ndarray
        A new array where columns 1 and 2 are swapped; column 0 is
        unchanged.

    See Also
    --------
    rot : cyclic column rotation.
    flip : reverse the layer order.

    Examples
    --------
    >>> import numpy as np
    >>> transp(np.array([['+0', '+j', '+k']])).tolist()
    [['+0', '+k', '+j']]
    """
    return np.array(a[:, [0, 2, 1]])


def flip(a):
    """Reverse the order of layers.

    The "row" part of the vertical symmetry. For planar options (1, 2, 5),
    `flip` alone is the vertical involution. For buckled options (3, 4,
    6, 7, 8), it is composed with `sign` to form the correct vertical
    symmetry `sign ∘ flip`.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    numpy.ndarray
        A new array with the rows (layers) in reverse order: new row i
        is old row k-1-i.

    See Also
    --------
    sign : reflect each layer about its mid-plane.
    rot, transp : column permutations.

    Notes
    -----
    The composition `sign ∘ flip` is the vertical symmetry for buckled
    options, *not* `sign` and `flip` independently. This was confirmed
    by Dr. Jessica Arcudia and is reflected in `generate_group`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([['+0', '+j'], ['+k', '-j']])
    >>> flip(a).tolist()
    [['+k', '-j'], ['+0', '+j']]
    """
    return np.flipud(a)


def sign(a):
    """Reflect each layer about its mid-plane.

    Flips the signs of tokens, layer by layer. The behavior depends on
    the token length:

    - 2-character tokens: ``+x`` ↔ ``-x``, with two exceptions:
      ``+0`` (zero token) and ``*x`` (fixed token) are unchanged.
    - 6-character parenthesized tokens: ``(+x-y)`` ↔ ``(-x+y)``, but
      only if ``x != y``. If the two atoms are equal (``x == y``), the
      token is unchanged.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    numpy.ndarray
        A new array of the same shape, with each token sign-flipped
        according to the rules above.

    See Also
    --------
    flip : reverse the layer order.
    generate_group : the symmetry group, which uses `sign ∘ flip` for
        buckled options.

    Notes
    -----
    For buckled options the vertical symmetry is `sign ∘ flip`, not
    `sign` and `flip` independently. The point group of a buckled
    honeycomb layer contains the specular reflection (layer reversal
    combined with sign flip) but not the individual operations. See
    `generate_group` and the paper for details.

    Examples
    --------
    2-character tokens. Note that ``+0`` and ``*j`` are unchanged:

    >>> import numpy as np
    >>> sign(np.array([['+j', '-j', '+0', '*j']])).tolist()
    [['-j', '+j', '+0', '*j']]

    6-character parenthesized tokens. Different atoms are exchanged:

    >>> sign(np.array([['(+k-l)']])).tolist()
    [['(-k+l)']]

    Equal atoms yield the same token:

    >>> sign(np.array([['(+k-k)']])).tolist()
    [['(+k-k)']]
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
    """Serialize a JAM array to its canonical string form.

    Each column of the array is concatenated row by row (layer by layer),
    and the three resulting column strings are joined with ``/``. This
    produces the "chain" representation: a single string that can be used
    as a dictionary key for duplicate detection.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    str
        The chain form: ``"col0/col1/col2"``, where each column is the
        concatenation of its tokens in layer order.

    See Also
    --------
    chain_to_array : inverse operation.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    >>> array_to_chain(a)
    '+0+0/+j+j/+j+j'
    """
    parts = []
    for col in range(a.shape[1]):
        parts.append(''.join(a[:, col]))
    return '/'.join(parts)


def chain_to_array(chain):
    """Deserialize a JAM chain string to its array form.

    The inverse of `array_to_chain`. Splits the string by ``/`` into three
    column strings, parses each into tokens (2 characters per token, or 6
    characters for parenthesized tokens), and returns the resulting
    k × 3 array.

    Parameters
    ----------
    chain : str
        A JAM chain in the form ``"col0/col1/col2"``.

    Returns
    -------
    numpy.ndarray
        A k × 3 array of JAM tokens.

    See Also
    --------
    array_to_chain : inverse operation.

    Notes
    -----
    Parenthesized tokens (6 characters, e.g. ``(+k-l)``) are recognized
    by the leading ``(`` and consumed in full. All other tokens are 2
    characters.

    Examples
    --------
    >>> chain_to_array('+0+0/+j+j/+j+j').tolist()
    [['+0', '+j', '+j'], ['+0', '+j', '+j']]
    """
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
    """Return the 6 elements of S₃ as functions acting on arrays.

    The elements are the three rotations (identity, `rot`, `rot²`) and
    their compositions with `transp`, corresponding to the standard
    presentation S₃ = ⟨rot, transp⟩:

    - index 0: identity
    - index 1: rot
    - index 2: rot²
    - index 3: transp
    - index 4: rot ∘ transp
    - index 5: rot² ∘ transp

    Returns
    -------
    list of callable
        A list of 6 functions, each taking a k × 3 array and returning
        the permuted array.

    See Also
    --------
    generate_group : the full group G = S₃ × ℤ/2 of order 12.

    Examples
    --------
    >>> len(elements_S3())
    6
    """
    return [
        lambda a: a,
        lambda a: rot(a),
        lambda a: rot(rot(a)),
        lambda a: transp(a),
        lambda a: rot(transp(a)),
        lambda a: rot(rot(transp(a))),
    ]


def generate_group(optionx):
    """Return the symmetry group of the given JAM option.

    The group is G = S₃ × ℤ/2 of order 12. The S₃ factor permutes the
    three columns (Wyckoff sites 1a, 1b, 1c); the ℤ/2 factor is the
    vertical symmetry, which depends on the option:

    - Planar options (1, 2, 5): vertical symmetry is `flip` alone. The
      alphabet of these options is invariant under `sign`, so
      `sign ∘ flip` would coincide with `flip` on the chain set.
    - Buckled options (3, 4, 6, 7, 8): vertical symmetry is the
      composition `sign ∘ flip` (global reflection), not `flip` and
      `sign` independently.

    Parameters
    ----------
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    list of callable
        A list of 12 functions, each taking a k × 3 array and returning
        the transformed array.

    See Also
    --------
    elements_S3 : the 6 elements of the S₃ factor.

    Notes
    -----
    The vertical symmetry is `sign ∘ flip` for buckled options, not
    `sign` and `flip` independently. Treating them as independent would
    yield the group S₃ × ℤ/2 × ℤ/2 of order 24, which is physically
    incorrect: it would identify a buckled bilayer with its sign-reversed
    mirror image, which are not related by any spatial symmetry of the
    buckled structure. This was confirmed by Dr. Jessica Arcudia and is
    the current convention in the package.

    Examples
    --------
    >>> len(generate_group(1))  # planar
    12
    >>> len(generate_group(3))  # buckled
    12
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
    """Compute the canonical key of a JAM chain under the symmetry group.

    The canonical key is the lexicographic minimum of the orbit of `a`
    under the symmetry group of the given option. Two chains are
    equivalent — related by a symmetry operation — if and only if they
    have the same canonical key. This property is what makes duplicate
    detection O(m) via a dictionary, instead of O(m²) via pairwise
    comparison.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens. Each row is a layer, each column a
        Wyckoff site. Tokens are strings: 2-character (``+0``, ``+j``,
        ``-j``, ``*j``) or 6-character parenthesized (``(+k-k)``,
        ``(-k+l)``).
    optionx : int
        JAM option in ``1..8``. The option determines the vertical
        symmetry (see `generate_group`).

    Returns
    -------
    str
        The canonical JAM chain: the lexicographic minimum of the 12
        group evaluations of `a`, serialized by `array_to_chain`.

    See Also
    --------
    canonical_key_fast : O(k) computation via column sorting (2
        evaluations instead of 12). Verified to agree with this function
        for all 8 options and n = 2, 3. Prefer this one unless you need
        the literal definition for correspondence with the theory.
    filter_duplicates : O(m) duplicate detection using canonical keys.

    Notes
    -----
    This is the literal definition of the canonical key: the minimum
    over all 12 elements of the group. Cost: 12 group evaluations, each
    O(k). For the optimal computation in O(k) with constant 2, see
    `canonical_key_fast`.

    Examples
    --------
    Two chains equivalent under column rotation produce the same key:

    >>> import numpy as np
    >>> from canonjam import canonical_key
    >>> a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    >>> b = np.array([['+j', '+j', '+0'], ['+j', '+j', '+0']])
    >>> canonical_key(a, 1) == canonical_key(b, 1)
    True
    """
    operations = generate_group(optionx)
    chains = []
    for op in operations:
        x = op(a.copy())
        chains.append(array_to_chain(x))
    return min(chains)


def filter_duplicates(stackinglist, optionx):
    """Detect duplicates in a list of JAM chains via canonical keys.

    Two chains are duplicates if they are equivalent under the symmetry
    group of the given option. This function returns one representative
    per equivalence class, using canonical keys as dictionary keys: O(m)
    instead of the O(m²) of the pairwise method.

    Parameters
    ----------
    stackinglist : list of numpy.ndarray
        A list of k × 3 arrays, each representing a JAM chain.
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    list of numpy.ndarray
        A list of representatives, one per equivalence class. The
        representatives are the first-seen elements of their class in
        the input list (not the canonical ones); use `canonical_key` on
        a representative to get its key.

    See Also
    --------
    canonical_key : the key used internally.
    canonical_key_fast : faster key computation, not used here by
        design. If you need it, build the dictionary manually.

    Notes
    -----
    This function uses `canonical_key` (the literal definition, 12
    evaluations) internally, not `canonical_key_fast`. Rationale: the
    function performs the two-pass deduplication of the original
    pairwise method in a single call, and a ``key=`` parameter would
    have to specify which pass it applies to, leaking filter semantics
    into the interface. Users who want the fast variant can build the
    dictionary themselves; see the quickstart in the README.

    Examples
    --------
    Three identical chains collapse to one:

    >>> import numpy as np
    >>> from canonjam import filter_duplicates
    >>> a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    >>> len(filter_duplicates([a, a, a], 1))
    1
    """
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
    """Sort the columns of an array lexicographically.

    Used by `canonical_key_fast`. Because each column of a JAM chain
    serializes to a string of the same fixed length (k times the token
    length), the lexicographically minimal concatenation over all
    permutations of the columns is obtained by sorting the columns.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.

    Returns
    -------
    numpy.ndarray
        A copy of `a` with its columns sorted lexicographically.

    See Also
    --------
    canonical_key_fast : main use of this helper.

    Examples
    --------
    >>> import numpy as np
    >>> sort_cols(np.array([['+j', '+0', '+j']])).tolist()
    [['+0', '+j', '+j']]
    """
    cols = [tuple(str(x) for x in a[:, i]) for i in range(a.shape[1])]
    return np.array(sorted(cols), dtype=object).T


def canonical_key_fast(a, optionx):
    """Compute the canonical key of a JAM chain in O(k).

    The optimal computation of the canonical key: instead of the 12
    group evaluations of `canonical_key`, this function computes the
    minimum of two sorted-column concatenations:

    .. code-block:: text

        κ(a) = min( s(sort_cols(a)), s(sort_cols(v(a))) )

    where ``v`` is the non-trivial element of the ℤ/2 factor (``flip``
    for planar options, ``sign ∘ flip`` for buckled options) and ``s``
    is the chain serialization. Because each column serializes to a
    fixed-length string, sorting the columns minimizes over the S₃
    factor. Cost: 2 group evaluations, O(k) each.

    Parameters
    ----------
    a : numpy.ndarray
        A k × 3 array of JAM tokens.
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    str
        The canonical JAM chain, identical to ``canonical_key(a, optionx)``.

    See Also
    --------
    canonical_key : literal definition (12 evaluations). Use that one
        if you need direct correspondence with the theory.
    filter_duplicates : O(m) duplicate detection.

    Notes
    -----
    This is the optimal computation in the black-box model of
    column-multiset-based canonical forms: the two evaluations of ``v``
    are necessary and sufficient. Verified to agree with `canonical_key`
    for all 8 options and n = 2, 3 (see ``tests/test_canonical_fast.py``).

    Examples
    --------
    >>> import numpy as np
    >>> from canonjam import canonical_key, canonical_key_fast
    >>> a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    >>> canonical_key_fast(a, 1) == canonical_key(a, 1)
    True
    """
    if optionx in [1, 2, 5]:
        va = flip(a.copy())
    else:
        va = sign(flip(a.copy()))
    return min(
        array_to_chain(sort_cols(a)),
        array_to_chain(sort_cols(va)),
    )
