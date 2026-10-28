# Comparison scripts (require xjam2)

These scripts compare the canonical filter against the original
pairwise method of the JAM framework. The original method lives in
**xjam2**, which is **not** a dependency of canonJAM and is **not**
distributed with this repository.

They will fail with a clear error if `xjam2` is not installed.

## Why is xjam2 not a dependency?

`xjam2` is developed by a third party and is not licensed for
redistribution. canonJAM uses only its public API (function names),
which is why we do not copy or vendor any of its code.

## Install xjam2

From source:

    pip install git+https://github.com/Theochem-merida/xjam2.git

Or use a local copy:

    export PYTHONPATH=/path/to/xjam2:$PYTHONPATH

## If you don't need xjam2

The self-contained reproducibility scripts (no xjam2 required) live
one level up in `tests/`:

    tests/validation_table1.py
    tests/scalability.py
    tests/burnside.py
    tests/burnside_all.py
    tests/structural.py
    tests/structural_all.py
    tests/kappa_equal_kappa_prime.py
    tests/recursion_check.py

They reproduce the class counts, the closed forms, the structural
theorems, and the κ = κ' check, using only `numpy` and `canonjam`.
