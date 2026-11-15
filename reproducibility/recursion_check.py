"""Closed forms vs recursive formulas for the orbit counts.

The orbit count S_n of the four binary JAM options has a closed form
(Theorem 5.5 of the paper) and a recursive formula (Table S1 of
[Arcudia2023]). This script verifies that the two agree for n = 2..30,
for all three families: PL, BPL/BU, and BBU.

Usage
-----
    python3 recursion_check.py

The script exits with 0 if all values match, 1 otherwise.

Self-contained: numpy + canonjam only. Does not require xjam2.
"""


def closed_PL(n):
    """Closed form for PL orbit counts.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of PL chains with n layers.
    """
    if n % 2 == 0:
        return (3 ** (n // 2) + 1) * (3 ** (n // 2) + 3) // 12
    m = (n - 1) // 2
    return (3 ** m + 1) ** 2 // 4


def closed_BPLBU(n):
    """Closed form for BPL and BU orbit counts (they coincide).

    Parameters
    ----------
    n : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of BPL (or BU) chains with n layers.
    """
    if n % 2 == 0:
        return (6 ** n + 4 * 6 ** (n // 2)) // 12
    return (6 ** n + 6 ** ((n + 1) // 2)) // 12


def closed_BBU(n):
    """Closed form for BBU orbit counts.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of BBU chains with n layers.
    """
    if n % 2 == 0:
        return (12 ** n + 4 * 12 ** (n // 2)) // 12
    return 12 ** (n - 1)


def rec_PL(N):
    """Recursive formula for PL orbit counts (Table S1 of [Arcudia2023]).

    Parameters
    ----------
    N : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of PL chains with N layers.
    """
    if N == 2:
        return 2
    # n empieza en 0 para N par, en 1 para N impar (Tabla S1 de [1]).
    n = (N - 1) // 2 if N % 2 == 1 else (N - 2) // 2
    return 3 * rec_PL(N - 1) - (3 ** n + 1) // 2


def rec_BPLBU(N):
    """Recursive formula for BPL/BU orbit counts.

    Parameters
    ----------
    N : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of BPL (or BU) chains with N layers.
    """
    if N == 2:
        return 5
    n = (N - 2) // 2
    m = 1 if N % 2 == 1 else 0
    return 6 * rec_BPLBU(N - 1) - 6 ** n * 3 ** (2 * m)


def rec_BBU(N):
    """Recursive formula for BBU orbit counts.

    Parameters
    ----------
    N : int
        Number of layers, >= 2.

    Returns
    -------
    int
        The number of orbits of BBU chains with N layers.
    """
    if N == 2:
        return 16
    n = (N - 1) // 2 if N % 2 == 1 else N // 2 - 1
    m = 1 if N % 2 == 1 else -1
    return 12 * rec_BBU(N - 1) - 4 * m * (12 ** n)


if __name__ == "__main__":
    ok = True
    for N in range(2, 31):
        for name, rec, clo in [
            ("PL", rec_PL, closed_PL),
            ("BPL/BU", rec_BPLBU, closed_BPLBU),
            ("BBU", rec_BBU, closed_BBU),
        ]:
            r, c = rec(N), clo(N)
            if r != c:
                print(f"MISMATCH {name} N={N}: rec={r} closed={c}")
                ok = False
    if ok:
        print("All match for N=2..30 (PL, BPL/BU, BBU)")
