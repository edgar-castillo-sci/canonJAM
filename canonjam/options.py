"""Single-layer rows and alphabet definitions for the 8 JAM options.

Each JAM option is characterized by two things: the set of valid
single-layer rows (a subset of permutations of a base token set) and the
vertical symmetry (``flip`` for planar options, ``sign ∘ flip`` for
buckled). This module provides the row sets; the vertical symmetry is
handled by :func:`canonjam.canonical.generate_group`.

The 8 options, with their base tokens and row counts:

===========  ==============================================  =========  ============
Option       Base tokens                                     # rows     Type
===========  ==============================================  =========  ============
1 (PL)       ``+0``, ``+j``, ``+j``                          3          planar
2 (BPL)      ``+0``, ``+j``, ``+k``                          6          planar
3 (BU)       ``+0``, ``+j``, ``-j``                          6          buckled
4 (BBU)      two bases: (``+0``, ``+j``, ``-k``) and         12         buckled
             (``+0``, ``-j``, ``+k``)
5            ``+0``, ``*j``, ``(+k-k)``                       6          planar
6            ``*j``, ``+k``, ``-k``                          6          buckled
7            two bases: (``+0``, ``*j``, ``(+k-l)``) and     12         buckled
             (``+0``, ``*j``, ``(-k+l)``)
8            two bases: (``*j``, ``+k``, ``-l``) and         12         buckled
             (``*j``, ``-k``, ``+l``)
===========  ==============================================  =========  ============

Options 5-8 are the "extended" options with site-occupancy tokens
(``*j`` and ``(+x-y)``). Only options 1-4 have closed-form counts in the
published paper; the extended options are covered in the current
manuscript.

This module is self-contained: it depends only on the standard library
(``itertools``). It does not import from :mod:`canonjam.canonical`, and
does not require ``numpy``.
"""

from itertools import permutations

_BASE_TOKENS = {
    1: ['+0', '+j', '+j'],
    2: ['+0', '+j', '+k'],
    3: ['+0', '+j', '-j'],
    5: ['+0', '*j', '(+k-k)'],
    6: ['*j', '+k', '-k'],
}

_TWO_BASES = {
    4: [['+0', '+j', '-k'], ['+0', '-j', '+k']],
    7: [['+0', '*j', '(+k-l)'], ['+0', '*j', '(-k+l)']],
    8: [['*j', '+k', '-l'], ['*j', '-k', '+l']],
}


def base_tokens_for_option(optionx):
    """Return the base tokens of a single layer for a single-base option.

    For the five single-base options (1, 2, 3, 5, 6), returns the list of
    three tokens that, when permuted, generate all valid single-layer
    rows. For the three two-base options (4, 7, 8), raises ``ValueError``
    because there is no single base set; use `base_sets_for_option`
    instead.

    Parameters
    ----------
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    list of str
        The three base tokens of one layer, before permutation.

    Raises
    ------
    ValueError
        If `optionx` is a two-base option (4, 7, 8). Use
        `base_sets_for_option` for those.

    See Also
    --------
    base_sets_for_option : works for all 8 options.
    rows_for_option : the fully permuted single-layer rows.

    Examples
    --------
    >>> base_tokens_for_option(1)
    ['+0', '+j', '+j']
    >>> base_tokens_for_option(3)
    ['+0', '+j', '-j']
    """
    if optionx in _BASE_TOKENS:
        return list(_BASE_TOKENS[optionx])
    raise ValueError(f"Option {optionx} has multiple base sets; "
                     f"use base_sets_for_option() instead.")


def base_sets_for_option(optionx):
    """Return the base token sets of a single layer for any JAM option.

    Unlike `base_tokens_for_option`, this function works for all 8
    options. For single-base options it returns a list with one base set;
    for two-base options it returns a list with two base sets.

    Parameters
    ----------
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    list of list of str
        A list of base token sets. Length 1 for single-base options
        (1, 2, 3, 5, 6), length 2 for two-base options (4, 7, 8).

    Raises
    ------
    ValueError
        If `optionx` is not in ``1..8``.

    See Also
    --------
    base_tokens_for_option : convenience wrapper for single-base options.
    rows_for_option : the fully permuted single-layer rows.

    Examples
    --------
    Single-base option:
    >>> base_sets_for_option(2)
    [['+0', '+j', '+k']]

    Two-base option:
    >>> base_sets_for_option(4)
    [['+0', '+j', '-k'], ['+0', '-j', '+k']]
    """
    if optionx in _BASE_TOKENS:
        return [list(_BASE_TOKENS[optionx])]
    if optionx in _TWO_BASES:
        return [list(b) for b in _TWO_BASES[optionx]]
    raise ValueError(f"Invalid option: {optionx}")


def rows_for_option(optionx):
    """Return all valid single-layer rows for the given JAM option.

    A single-layer row is a triple of tokens (one per Wyckoff site
    ``1a``, ``1b``, ``1c``) that is a permutation of one of the base
    token sets of the option. This function returns all distinct
    permutations, deduplicated (relevant when the base has repeated
    tokens, as in option 1).

    The result is the input alphabet for the canonicalization: a chain of
    ``k`` layers is a ``k × 3`` array whose rows are drawn from this set.

    Parameters
    ----------
    optionx : int
        JAM option in ``1..8``.

    Returns
    -------
    list of tuple of str
        All distinct single-layer rows of the option, as tuples of three
        tokens. The number of rows is 3 (option 1), 6 (options 2, 3, 5,
        6), or 12 (options 4, 7, 8).

    Raises
    ------
    ValueError
        If `optionx` is not in ``1..8``.

    See Also
    --------
    base_sets_for_option : the underlying base token sets.
    canonjam.filter_duplicates : the main user of this function.

    Notes
    -----
    The rows are returned as tuples (not lists) so they can be used
    directly as dictionary keys or in :func:`itertools.product`. The
    order of the list is not specified; do not rely on it.

    Examples
    --------
    Option 1 has repeated tokens (``+j``, ``+j``), so the 6 permutations
    collapse to 3 distinct rows:

    >>> len(rows_for_option(1))
    3

    Option 2 has all distinct tokens, so all 6 permutations are distinct:

    >>> len(rows_for_option(2))
    6

    Option 4 has two base sets, each with distinct tokens, so 12 rows:

    >>> len(rows_for_option(4))
    12
    """
    rows = []
    for base in base_sets_for_option(optionx):
        rows.extend(list(p) for p in set(permutations(base, 3)))
    return rows
