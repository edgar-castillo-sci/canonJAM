## [1.2.1] - 2026-10-27

### Changed

- `.github/workflows/tests.yml`: `fail-fast: false`. Previously, a
  failure in one Python version cancelled the others and hid their
  status (only the first to fail reported the real error; the rest
  appeared as `cancelled`). With `fail-fast: false`, all five jobs
  report their own status.
- `CITATION.cff`: DOI updated to `10.5281/zenodo.23720442` (version
  DOI for v1.2.0). The concept DOI (`10.5281/zenodo.23471387`)
  remains in the README badge, where it always resolves to the
  latest version.
- `README.md`: the test badge now points to the GitHub Actions
  workflow badge, so it reflects the actual state of `main` instead
  of the hardcoded `tests-33 passing`.

### Added

- `.pre-commit-config.yaml` and `scripts/check_requires_python.py`:
  validate that `pyproject.toml` declares `requires-python` in the
  form `>=3.X,<4` with `10 <= X <= (current minor + 2)`. Rejects
  both typos like `>=3.19` (impossible, this is what broke the
  `99857bc` CI run) and stale values like `>=3.9` (EOL).
  Activate with `pip install pre-commit && pre-commit install`.

## [1.2.0] - 2026-10-27

### Added

- `canonjam/options.py`: single-layer rows per JAM option, exposed as
  `rows_for_option`, `base_sets_for_option`, `base_tokens_for_option`.
  Makes the package self-sufficient for the row sets and removes the
  package's indirect dependence on `tests/validacion.py`.
- `tests/comparison/` directory with the three scripts that compare
  against the original pairwise method: `validation.py`, `full_report.py`,
  `benchmark.py` (renamed from `tests/validacion.py`,
  `tests/reporte_completo.py`, `tests/benchmark.py`).
- `tests/comparison/README.md`: explains that these scripts require
  `xjam2`, which is not distributed with canonJAM.
- `.gitignore` covering `__pycache__`, `*.egg-info`, generated outputs
  (`*_salida.txt`, `*_salida.tsv`), and the optional `xjam/`, `xjam2/`
  directories.

### Changed

- Renamed `tests/validacion_tabla1.py` → `tests/validation_table1.py`
  and `tests/escalabilidad.py` → `tests/scalability.py`. All filenames
  in `tests/` are now in English.
- All self-contained reproducibility scripts under `tests/` and
  `tests/exploration/` now import `rows_for_option` from `canonjam`
  instead of from `tests/validacion.py`. They no longer require
  `xjam2` to run.
- The three comparison scripts under `tests/comparison/` now fail with
  a clear message when `xjam2` is not installed, instead of raising
  `ModuleNotFoundError`.
- `examples/x_canonical.py`: fail with a clear message if `xjam2` is
  not installed (instead of `ModuleNotFoundError`).
- `examples/pipeline.py`: uses `rows_for_option` from `canonjam`
  instead of a local copy.
- `README.md`, `README.es.md`, `tests/README.md`: reorganize the
  reproducibility section into self-contained vs. comparison, add an
  explicit "Integration with xjam2 (monkey patching)" section, and
  clarify that canonJAM does not vendor or modify `xjam2`.

### Fixed

- `generate_group` and `canonical_key_fast` treat option 5 as
  planar-type (`v = flip`), as stated in Section 3.3 of the paper
  (options 1, 2, 5 are planar; 3, 4, 6, 7, 8 are buckled). No change
  in results because the option 5 alphabet is sign-invariant, but this
  makes code and paper consistent and avoids silent breakage if the
  alphabet changes.
- `tests/test_canonical_fast.py`: imports `rows_for_option` from
  `canonjam` instead of using a local copy. The local copy returned
  one row per option, so the test was run on 1-2 chains per option at
  n=2, not on all permutations. After the fix, it runs on all
  permutations for n=2,3 (5,655 chains instead of ~15), so the
  "verified for all 8 options and n=2,3" claim in the README is now
  accurate.

### Removed

- `tests/exploration/validation.py` (duplicate of `tests/validacion.py`;
  removed after the reorganization).

### Notes

- `canonJAM` does not vendor or modify `xjam2`. Only its public API is
  used, and only in the comparison scripts and the optional integration
  example.

## [1.1.0] - 2026-10-21

### Added

- `canonical_key_fast`: optimal computation of κ via column sorting.
  O(k) with a constant of 2. Verified to agree with `canonical_key`
  for all 8 options and n=2,3.
- `sort_cols` helper.
- 8 reproducibility scripts under `tests/`:
  `validacion_tabla1.py`, `escalabilidad.py`, `recursion_check.py`,
  `burnside.py`, `burnside_all.py`, `structural.py`,
  `structural_all.py`, `kappa_equal_kappa_prime.py`.
- 10 exploration scripts under `tests/exploration/` for the BPL/BU
  dichotomy and the classification of G-sets.
- "Reproducing the theoretical results" section in README, mapping
  each script to the result it reproduces.
- `tests/test_canonical_fast.py`: parametrized tests verifying
  `canonical_key_fast == canonical_key` for all 8 options and n=2,3.

### Changed

- Version bumped to 1.1.0.
- README reorganized: scientific basis, reproducibility section,
  exploration scripts.
- `tests/README.md` reorganized into three categories: formal tests,
  reproducibility scripts, exploration scripts.
- Test suite now includes 33 tests (was 25).

### Notes

- `canonical_key` remains the literal definition (minimum over the
  12 group elements) and is the function used by the benchmarks, for
  direct correspondence with the theory. `canonical_key_fast` is the
  optimal computation via column sorting.
