"""Shared helpers for the comparison scripts (require xjam2).

The three comparison scripts (benchmark.py, full_report.py,
validation.py) need to replicate the candidate generation logic of
x.jam without depending on it. That logic and the dispatch between
libjamstd (options 1-4) and libjamtdm (options 5-8) are identical in
all three, so they live here. Each script imports what it needs; the
import of this module is the single point where xjam2 is required.

Requires xjam2, which is optional and not a dependency of canonJAM.
If xjam2 is not importable, importing this module raises SystemExit
with a message pointing to tests/comparison/README.md.
"""

import numpy as np

from canonjam import rows_for_option

try:
    from xjam.libjamstd import (
        conv2pseudocanonic as conv_std,
    )
    from xjam.libjamstd import (
        disc_equivalents as disc_old_std,
    )
    from xjam.libjamtdm import (
        conv2pseudocanonic as conv_tdm,
    )
    from xjam.libjamtdm import (
        disc_equivalents as disc_old_tdm,
    )
except ImportError as exc:
    raise SystemExit(
        "This comparison script requires xjam2, which is optional and "
        "not a dependency of canonJAM. See tests/comparison/README.md.\n"
        f"Underlying error: {exc}"
    ) from exc


def get_methods(option):
    """Return the appropriate old-method functions for the given option.

    Options 1-4 use ``libjamstd``; options 5-8 use ``libjamtdm``. The two
    modules expose the same interface (``disc_equivalents`` and
    ``conv2pseudocanonic``), so this dispatch is the only place that
    distinguishes them.

    Parameters
    ----------
    option : int
        JAM option in 1..8.

    Returns
    -------
    tuple
        ``(disc_equivalents, conv2pseudocanonic)`` from the appropriate
        module.
    """
    if option in [1, 2, 3, 4]:
        return disc_old_std, conv_std
    return disc_old_tdm, conv_tdm


def generate_candidates(n, option):
    """Generate all candidates for n layers, replicating x.jam's logic.

    Starting from the single-layer rows, iteratively stacks pairs of
    blocks (down and up) and deduplicates at each level using the
    original pairwise method. Returns the candidate set at level ``n``,
    before the final filtering that the caller will measure.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.
    option : int
        JAM option in 1..8.

    Returns
    -------
    list of numpy.ndarray
        All candidate chains at level ``n``, as ``k x 3`` arrays.
    """
    disc_old, conv = get_methods(option)

    single = [np.array(r) for r in rows_for_option(option)]
    uniques = single.copy()

    candidates = single
    for level in range(2, n + 1):
        if level == 2:
            candidates = [
                np.vstack([a, b]) for a in uniques for b in single
            ]
        else:
            down = [np.vstack([a, b]) for a in uniques for b in single]
            up = [np.vstack([b, a]) for a in uniques for b in single]
            candidates = down + up

        canonical = [conv(c) for c in candidates]
        uniques = disc_old(canonical, option, 1)
        uniques = disc_old(uniques, option, 2)

    return candidates
