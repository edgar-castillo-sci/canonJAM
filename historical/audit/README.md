> **Historical record.** This directory was originally
> `tests/validation_session1/`. It documents a single validation session
> against a draft manuscript; the findings F1–F5 were folded into the
> implementation and the paper. The checks are not part of the library's
> test suite and are not maintained.

# Validation — Session 1

Definitive working record of the automated checks behind the corrections
to `ve_OaM.tex`. **This directory is not part of the paper.** It is the
reproducible evidence trail for every numeric and structural claim about
`G = S_3 × Z/2`, the table of marks `M(G)`, the Burnside matrix `B(G)`,
and the eight canonical JAM options.

## Status: 16/16 PASS

Last full run: **16 checks, 16 PASS**. Five findings (F1–F5) require
paper edits; all numerical claims of the paper are verified.

---

## Quick start

```bash
cd tests/validation_session1
python3 run_all.py             # 16 checks, per-check status
python3 run_all.py | tail -20  # summary only
```

Expected summary (see §Observed outputs for full transcripts):

```
check01_marks.py: PASS
check02_row_vs_col.py: PASS
check03_full_matrix.py: PASS
check04_fixed_points.py: PASS
check05_burnside.py: PASS
check06_orbits.py: PASS
check07_chiral.py: PASS
check08_bpl_bu.py: PASS
check09_fast_slow.py: PASS
check10_extended.py: PASS
check11_D6.py: PASS
check12_subgroups.py: PASS
check13_invariants.py: PASS
check14_transpose.py: PASS
check15_burnside_convention.py: PASS
check16_projection.py: PASS
```

`run_all.py` exits `0` iff every script exits `0`. `check01` exits `0`
deliberately: its job is to *report* a correctable discrepancy — the
`NOTE:` line is the actionable output.

---

## File map

| File | Purpose |
|---|---|
| `common.py` | Group `S_3 × Z/2` (abstract), subgroup reps `U_1..U_10`, both mark formulas (`mark_correct` / `mark_wrong`), the *computed* `S3_TO_CANONJAM` mapping, exact-rational matrix inverse |
| `check01_marks.py` | Compare the paper's mark formula with Pfeiffer's, entry-by-entry |
| `check02_row_vs_col.py` | Distinguish first row vs first column of `M(G)` |
| `check03_full_matrix.py` | Emit full `M(G)` and `B(G)` for Appendix C |
| `check04_fixed_points.py` | Fixed-point counts per conjugacy class (Table 5.2) |
| `check05_burnside.py` | Closed forms of Thm 5.5 vs direct Burnside sum |
| `check06_orbits.py` | Brute-force class counts vs Table 8.1 |
| `check07_chiral.py` | Sign-twisted Burnside split (Thm 5.6) |
| `check08_bpl_bu.py` | Prop. 4.19 BPL/BU dichotomy |
| `check09_fast_slow.py` | `canonical_key` vs `canonical_key_fast` (Thm 4.10) |
| `check10_extended.py` | Extended options 5–8 and `q = |Σ_1|` |
| `check11_D6.py` | `S_3 × Z/2 ≅ D_6` (Lemma 4.2) |
| `check12_subgroups.py` | Table 5.1 (subgroup order / normalizer / class size) |
| `check13_invariants.py` | `S3_TO_CANONJAM` is a *computed* group homomorphism |
| `check14_transpose.py` | `β_X = M^T a` (correct) vs `β_X = M a` (paper) |
| `check15_burnside_convention.py` | Burnside uses rowsums of `B`, not the first row |
| `check16_projection.py` | Definition 3.1 "projection" — three readings |
| `run_all.py` | Aggregate runner |

---

## Conventions used in this directory

### C.1 — Group `S_3 × Z/2` and its action on JAM arrays

Abstract group `S_3 × Z/2`, order 12. `S_3` acts on the three columns;
`Z/2 = {0, 1}` acts on the layer order (and, for buckled-type options,
on token signs). Elements in `common.py` are pairs `(s, z)`,
`s ∈ {0..5}` index into

```
S3_LIST = [ (0,1,2), (1,0,2), (2,1,0), (0,2,1), (1,2,0), (2,0,1) ]
```

read contragrediently (`new = old[σ⁻¹]`), matching `rot(a) = a[:,[1,2,0]]`.
Composition is `g_mul((s,z),(s',z')) = (s3_compose(s,s'), z ⊕ z')`.

`canonjam.canonical.elements_S3()` uses a different order:

```
canonjam[0] = id         canonjam[3] = transp    (1 2)
canonjam[1] = rot        canonjam[4] = rot·transp  (0 1)
canonjam[2] = rot²       canonjam[5] = rot²·transp (0 2)
```

`common._build_s3_to_canonjam()` computes the bijection **at import
time** by matching each `S3_LIST[i]` to its inverse action on `[0,1,2]`
under `canonjam`'s elements (inverse compensates the contragredient
convention). `check13` asserts the result is a group isomorphism. **No
hand-written mapping survives anywhere in this directory.**

### C.2 — Subgroup representatives `U_1 … U_10`

Ordered by increasing subgroup order (Table 5.1 of the paper). Verified
by `check12` against `|U|`, `|N_G(U)|`, and class size:

| `i` | Representative | `\|U_i\|` | `\|N_G(U_i)\|` | Class size |
|---|---|---|---|---|
| 1  | `{e}` | 1 | 12 | 1 |
| 2  | `⟨v⟩` | 2 | 12 | 1 |
| 3  | `⟨τ⟩` | 2 | 4  | 3 |
| 4  | `⟨τv⟩` | 2 | 4  | 3 |
| 5  | `⟨c⟩` | 3 | 12 | 1 |
| 6  | `⟨v, τ⟩` | 4 | 4  | 3 |
| 7  | `S_3 × {e}` | 6 | 12 | 1 |
| 8  | `⟨c, τv⟩` | 6 | 12 | 1 |
| 9  | `⟨cv⟩` | 6 | 12 | 1 |
| 10 | `G` | 12 | 12 | 1 |

### C.3 — Convention for `M(G)` and `B(G)`

Standard convention (Kerber 2002, Pfeiffer 1997): `M(G)_{ij} =
β_{G/U_i}(U_j)`, with the correct Pfeiffer formula

$$\beta_{G/U_i}(U_j) = \bigl|\{U_i^g : g \in G,\, U_j \le U_i^g\}\bigr| \cdot |N_G(U_i) : U_i|.$$

Numerical entries:

- `M[0, :]` = `(12, 0, …, 0)` — first row, `U_1 = {e}`
- `M[:, 0]` = `(12, 6, 6, 6, 4, 3, 2, 2, 2, 1)` — first column = `|G : U_i|`
- `diag(M)` = `(12, 6, 2, 2, 4, 1, 2, 2, 2, 1)` — = `|N_G(U_i) : U_i|`

`B(G) = M(G)^{-1}`, exact over `ℚ` via `common.invert_fraction_matrix`.

### C.4 — Relation between `β_X` and orbit coefficients `a_X`

**Correct**: `β_X = Mᵀ a_X`, equivalently `a_X = Bᵀ β_X`.
**Paper's draft**: `β_X = M a_X`, `a_X = B β_X` (wrong — see F3).

Under the correct convention:

- `|X/G| = Σᵢ a_{U_i}(X) = (row sums of B) · β_X` — this is Burnside.
- `a_{U_1}(X) = (first column of B) · β_X`.
- The paper's claim that "the first row of `B` gives `|X/G|`" is false
  (see F4).

### C.5 — Direct computation of `β_X` (independence from `M`)

`check14` and `check15` compute `β_X(U_j)` **without** using the mark
formula, by counting `U_j`-fixed left cosets of `U_i` directly:

```python
def beta_on_coset_direct(U_i, U_j):
    count = 0
    for C in left_cosets(U_i):              # all |G|/|U_i| cosets
        if all(frozenset(g_mul(h, x) for x in C) == C for h in U_j):
            count += 1
    return count
```

So `check14`'s and `check15`'s conclusions are independent of
`mark_correct`. If `mark_correct` had a bug, `check14` would still
detect it.

---

## Findings requiring paper edits (F1–F5)

### F1 — §2.3 mark formula: **four** entries wrong, not one (`check01`)

The draft formula

$$\beta_{G/U_i}(U_j) = \begin{cases}|N_G(U_i) : U_i| & U_j \lesssim U_i \\ 0 & \text{otherwise}\end{cases}$$

is missing the multiplicity factor `|{U_i^g : U_j ≤ U_i^g}|`. Comparison
against Pfeiffer's formula yields **four** differing entries:

| `(i, j)` | draft value | correct value |
|---|---|---|
| (3, 1) | 2 | 6 |
| (4, 1) | 2 | 6 |
| (6, 1) | 1 | 3 |
| (6, 2) | 1 | 3 |

Where the multiplicity factor is 3, not 1:

- For `i ∈ {3, 4, 6}` (the non-normal classes), the class size is 3.
  When `U_1 = {e}` is `U_j`, it is contained in every conjugate of
  `U_i`, so `|{U_i^g : {e} ≤ U_i^g}| = 3`. Produces the
  `(3,1), (4,1), (6,1)` differences.
- For `i = 6` and `j = 2`, `U_2 = ⟨v⟩` is central in `G`, hence
  contained in every conjugate of `U_6 = ⟨v, τ⟩`. Again factor 3,
  producing `(6,2)`.

**What to write**: state Pfeiffer's formula in full. Do not patch only
`(6,2)` — the missing factor applies to **every** non-normal `U_i`.

**Reference**: Kerber 2002 §2.3; Pfeiffer 1997, Prop. 1.2.

### F2 — Prop. 5.3 row/column mix-up (`check02`)

Paper: *"its first row is `(12, 6, 6, 6, 4, 3, 2, 2, 2, 1)`."*

Computed:

```
M[0, :]  = [12, 0, 0, 0, 0, 0, 0, 0, 0, 0]        ← row
M[:, 0]  = [12, 6, 6, 6, 4, 3, 2, 2, 2, 1]        ← column
diag(M)  = [12, 6, 2, 2, 4, 1, 2, 2, 2, 1]
```

The vector `(12, 6, 6, 6, 4, 3, 2, 2, 2, 1)` is the **first column**,
not the first row. Numeric values are correct; only the word "row" is
wrong. Replace with "its first **column** is".

### F3 — §2.3 / §5.2 transpose in `β_X = M a` (`check14`)

Paper writes `β_X = M a_X` and `a_X = B β_X`. Correct:
`β_X = Mᵀ a_X`, `a_X = Bᵀ β_X`.

**Basis proof**: for `X = G/U_i`, `a_X = e_i`, so `β_X` must equal row
`i` of `M`. `check14` verifies `β_X = Mᵀ e_i` from the coset action for
all `i ∈ {1, …, 10}` — **all ten match** — while `M e_i = column i of M
≠ row i of M` for all ten `i`.

**Counterexample 1** — `i = 6`, `X = G/U_6`, `a = e_6`:

```
direct β_X (coset action):    [3, 3, 1, 1, 0, 1, 0, 0, 0, 0]
Mᵀ e_6   (correct):           [3, 3, 1, 1, 0, 1, 0, 0, 0, 0]  ✓
M   e_6   (paper's convention): [0, 0, 0, 0, 0, 1, 0, 0, 0, 1]  ✗
```

**Counterexample 2** — `X = G/U_2 ⊔ G/U_6`, `a = e_2 + e_6`:

```
direct β_X:        [9, 9, 1, 1, 0, 1, 0, 0, 0, 0]
Mᵀ a (correct):    [9, 9, 1, 1, 0, 1, 0, 0, 0, 0]  ✓
M   a (paper):     [0, 6, 0, 0, 0, 4, 0, 0, 2, 2]  ✗
Bᵀ β_X recovered:  [0, 1, 0, 0, 0, 1, 0, 0, 0, 0]  (= e_2 + e_6) ✓
```

Linear maps are determined by their actions on a basis (`{e_i}` spans
`ℚ^10`), and by linearity on direct sums. The 10/10 basis check plus
counterexample 2 proves `β_X = Mᵀ a_X` for every finite `G`-set.

**What to write**: replace `β_X = M a`, `a = B β_X` with
`β_X = Mᵀ a`, `a = Bᵀ β_X` in §2.3 and §5.2.

### F4 — §5.3 "first row of `B(G)`" (`check15`)

Paper: *"the first row of `B(G)` applied to `β_X` gives the total number
of orbits."* Three errors:

**1. Burnside's lemma uses row sums, not the first row.**

```
rowsums(B) = (1/12, 1/12, 1/4, 1/4, 1/6, 0, 0, 0, 1/6, 0)
colsums(B) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
first row  = (1/12, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

For every `X = G/U_i`, `rowsums · β_X = 1` (all ten, `check15` Part 1).
For `X = G/U_2 ⊔ G/U_6`, `rowsums · β_X = 2` (Part 2). Both match direct
Burnside sums.

**2. First row of `B` gives `1/|U_i|`, not `|X/G|`.**

`first_row · β_{G/U_i} = 1/|U_i|`. Sample: `i=2 → 0.5`, `i=6 → 0.25`,
`i=10 → 0.0833`. Coincides with `|X/G|` (`= 1`) only for `i = 1`.

**3. Even under the paper's (wrong) convention, "first row gives
`a_{U_1}`" is false.** Under the correct `a = Bᵀ β_X`, it is the
**first column** of `B` that extracts `a_{U_1}`:

```
col_1(B) · β_{G/U_i} = δ_{i,1}   for all i ∈ {1, …, 10}
```

Verified in `check15` Part 3 (all ten). Under the paper's convention,
`row_1(B) · β_{G/U_i} = 1/|U_i|`, never `δ_{i,1}` for `i > 1`.

**What to write**: replace "first row of `B(G)`" with "the vector of row
sums of `B(G)`" (equivalently `B · 1`). If the paper ever claims "the
first row extracts orbits with trivial stabilizer", that claim belongs
to the **first column** of `B`.

### F5 — Definition 3.1 "projection" condition (`check16`)

Draft: *"for every `i ∈ {1, …, r}`, the projection `Σ_k → Σ, w ↦ w_i`,
is surjective onto its image."* Three readings, tested on all 8 options:

| Reading | Status | Evidence |
|---|---|---|
| (i) surjective onto *its own* image | **vacuously true** | Every function is surjective onto its image; empty condition |
| (ii) `image(π_i)` **independent of `i`** | **true for all 8 options** | `check16` prints per-option images; all three equal |
| (iii) `image(π_i) = Σ` (full ambient alphabet) | **false for all 8 options** | Each option uses a strict subset of the 11-token ambient `Σ` |

**Token census** from `check16`:

| Option | `\|image(π_i)\|` | Image |
|---|---|---|
| 1 (PL)  | 2 | `{+0, +j}` |
| 2 (BPL) | 3 | `{+0, +j, +k}` |
| 3 (BU)  | 3 | `{+0, +j, -j}` |
| 4 (BBU) | 5 | `{+0, ±j, ±k}` |
| 5       | 3 | `{+0, *j, (+k-k)}` |
| 6       | 3 | `{*j, +k, -k}` |
| 7       | 4 | `{+0, *j, (+k-l), (-k+l)}` |
| 8       | 5 | `{*j, ±k, ±l}` |

**Decision needed**: adopt (ii) and rewrite; or drop the condition.
Reading (i) is vacuous and should not be kept; (iii) is false and should
not be adopted.

---

## Observed outputs (verbatim)

Pasted directly from the last `run_all.py` execution. These are the
canonical values to compare against if you rerun the checks.

### `check01_marks.py`

```
Differing (i, j, wrong, correct):
  (3, 1): wrong=2, correct=6
  (4, 1): wrong=2, correct=6
  (6, 1): wrong=1, correct=3
  (6, 2): wrong=1, correct=3

Total differences: 4
NOTE: checklist predicted [(6, 2)], found [(3, 1), (4, 1), (6, 1), (6, 2)].
```

### `check02_row_vs_col.py`

```
M[0, :]  (row for U1) = [12, 0, 0, 0, 0, 0, 0, 0, 0, 0]
M[:, 0]  (column U1)  = [12, 6, 6, 6, 4, 3, 2, 2, 2, 1]
diag(M)               = [12, 6, 2, 2, 4, 1, 2, 2, 2, 1]
PASS
```

### `check03_full_matrix.py`

```
M(G) =
   [12, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   [6, 6, 0, 0, 0, 0, 0, 0, 0, 0]
   [6, 0, 2, 0, 0, 0, 0, 0, 0, 0]
   [6, 0, 0, 2, 0, 0, 0, 0, 0, 0]
   [4, 0, 0, 0, 4, 0, 0, 0, 0, 0]
   [3, 3, 1, 1, 0, 1, 0, 0, 0, 0]
   [2, 0, 2, 0, 2, 0, 2, 0, 0, 0]
   [2, 0, 0, 2, 2, 0, 0, 2, 0, 0]
   [2, 2, 0, 0, 2, 0, 0, 0, 2, 0]
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

B(G) = M(G)^-1 (exact):
   ['1/12', '0', '0', '0', '0', '0', '0', '0', '0', '0']
   ['-1/12', '1/6', '0', '0', '0', '0', '0', '0', '0', '0']
   ['-1/4', '0', '1/2', '0', '0', '0', '0', '0', '0', '0']
   ['-1/4', '0', '0', '1/2', '0', '0', '0', '0', '0', '0']
   ['-1/12', '0', '0', '0', '1/4', '0', '0', '0', '0', '0']
   ['1/2', '-1/2', '-1/2', '-1/2', '0', '1', '0', '0', '0', '0']
   ['1/4', '0', '-1/2', '0', '-1/4', '0', '1/2', '0', '0', '0']
   ['1/4', '0', '0', '-1/2', '-1/4', '0', '0', '1/2', '0', '0']
   ['1/12', '-1/6', '0', '0', '-1/4', '0', '0', '0', '1/2', '0']
   ['-1/2', '1/2', '1/2', '1/2', '1/2', '-1', '-1/2', '-1/2', '-1/2', '1']

M·B = I: True
```

Derived quantities (from `check15`):

```
rowsums(B) = [1/12, 1/12, 1/4, 1/4, 1/6, 0, 0, 0, 1/6, 0]
colsums(B) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
first row  = [1/12, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

### `check04_fixed_points.py`

```
PL n=2: {'e': 9, 'v': 3, 'tau': 1, 'tau_v': 3, 'omega': 0, 'omega_v': 0}
PL n=3: {'e': 27, 'v': 9, 'tau': 1, 'tau_v': 3, 'omega': 0, 'omega_v': 0}
PL n=4: {'e': 81, 'v': 9, 'tau': 1, 'tau_v': 9, 'omega': 0, 'omega_v': 0}
BPL n=2: {'e': 36, 'v': 6, 'tau': 0, 'tau_v': 6, 'omega': 0, 'omega_v': 0}
BPL n=3: {'e': 216, 'v': 36, 'tau': 0, 'tau_v': 0, 'omega': 0, 'omega_v': 0}
BPL n=4: {'e': 1296, 'v': 36, 'tau': 0, 'tau_v': 36, 'omega': 0, 'omega_v': 0}
BU n=2: {'e': 36, 'v': 6, 'tau': 0, 'tau_v': 6, 'omega': 0, 'omega_v': 0}
BU n=3: {'e': 216, 'v': 0, 'tau': 0, 'tau_v': 12, 'omega': 0, 'omega_v': 0}
BU n=4: {'e': 1296, 'v': 36, 'tau': 0, 'tau_v': 36, 'omega': 0, 'omega_v': 0}
BBU n=2: {'e': 144, 'v': 12, 'tau': 0, 'tau_v': 12, 'omega': 0, 'omega_v': 0}
BBU n=3: {'e': 1728, 'v': 0, 'tau': 0, 'tau_v': 0, 'omega': 0, 'omega_v': 0}
BBU n=4: {'e': 20736, 'v': 144, 'tau': 0, 'tau_v': 144, 'omega': 0, 'omega_v': 0}
PASS
```

### `check05_burnside.py`

```
option=1 n=2: Burnside=2, closed=2, OK
option=1 n=3: Burnside=4, closed=4, OK
option=1 n=4: Burnside=10, closed=10, OK
option=1 n=5: Burnside=25, closed=25, OK
option=2 n=2: Burnside=5, closed=5, OK
option=2 n=3: Burnside=21, closed=21, OK
option=2 n=4: Burnside=120, closed=120, OK
option=2 n=5: Burnside=666, closed=666, OK
option=3 n=2: Burnside=5, closed=5, OK
option=3 n=3: Burnside=21, closed=21, OK
option=3 n=4: Burnside=120, closed=120, OK
option=3 n=5: Burnside=666, closed=666, OK
option=4 n=2: Burnside=16, closed=16, OK
option=4 n=3: Burnside=144, closed=144, OK
option=4 n=4: Burnside=1776, closed=1776, OK
option=4 n=5: Burnside=20736, closed=20736, OK
PASS
```

### `check06_orbits.py`

```
option=1 n=2: 2 (expected 2) OK
option=1 n=3: 4 (expected 4) OK
option=1 n=4: 10 (expected 10) OK
option=1 n=5: 25 (expected 25) OK
option=2 n=2: 5 (expected 5) OK
option=2 n=3: 21 (expected 21) OK
option=2 n=4: 120 (expected 120) OK
option=2 n=5: 666 (expected 666) OK
option=3 n=2: 5 (expected 5) OK
option=3 n=3: 21 (expected 21) OK
option=3 n=4: 120 (expected 120) OK
option=3 n=5: 666 (expected 666) OK
option=4 n=2: 16 (expected 16) OK
option=4 n=3: 144 (expected 144) OK
option=4 n=4: 1776 (expected 1776) OK
option=4 n=5: skipped (too large)
PASS
```

### `check07_chiral.py`

```
option=1 n=2: direct=(ach=2, chir=0), formula=(ach=2, chir=0) OK
option=1 n=3: direct=(ach=3, chir=1), formula=(ach=3, chir=1) OK
option=1 n=4: direct=(ach=6, chir=4), formula=(ach=6, chir=4) OK
option=2 n=2: direct=(ach=4, chir=1), formula=(ach=4, chir=1) OK
option=2 n=3: direct=(ach=6, chir=15), formula=(ach=6, chir=15) OK
option=2 n=4: direct=(ach=24, chir=96), formula=(ach=24, chir=96) OK
option=3 n=2: direct=(ach=4, chir=1), formula=(ach=4, chir=1) OK
option=3 n=3: direct=(ach=6, chir=15), formula=(ach=6, chir=15) OK
option=3 n=4: direct=(ach=24, chir=96), formula=(ach=24, chir=96) OK
option=4 n=2: direct=(ach=8, chir=8), formula=(ach=8, chir=8) OK
option=4 n=3: direct=(ach=0, chir=144), formula=(ach=0, chir=144) OK
option=4 n=4: direct=(ach=96, chir=1680), formula=(ach=96, chir=1680) OK
PASS
```

### `check08_bpl_bu.py`

```
n=2: |Fix_BPL(v)|=6, |Fix_BU(v)|=6, stab multisets EQUAL
n=3: |Fix_BPL(v)|=36, |Fix_BU(v)|=0, stab multisets DIFFER
n=4: |Fix_BPL(v)|=36, |Fix_BU(v)|=36, stab multisets EQUAL
PASS
```

### `check09_fast_slow.py`

```
PASS for all options and n=2,3
```

### `check10_extended.py`

```
Option 5: q=6 (OK)
  n=2: 5 (expected 5) OK
  n=3: 21 (expected 21) OK
  n=4: 120 (expected 120) OK
Option 6: q=6 (OK)
  n=2: 5 (expected 5) OK
  n=3: 21 (expected 21) OK
  n=4: 120 (expected 120) OK
Option 7: q=12 (OK)
  n=2: 16 (expected 16) OK
  n=3: 144 (expected 144) OK
  n=4: skipped (n=4 too large for brute force)
Option 8: q=12 (OK)
  n=2: 16 (expected 16) OK
  n=3: 144 (expected 144) OK
  n=4: skipped (n=4 too large for brute force)
PASS
```

### `check11_D6.py`

```
order(r)=6, order(s)=2, s·r·s = r^-1: True
<r, s> = G: True
PASS
```

### `check12_subgroups.py`

```
U 1: |U|= 1 (exp  1), |N|=12 (exp 12), class= 1 (exp  1) OK
U 2: |U|= 2 (exp  2), |N|=12 (exp 12), class= 1 (exp  1) OK
U 3: |U|= 2 (exp  2), |N|= 4 (exp  4), class= 3 (exp  3) OK
U 4: |U|= 2 (exp  2), |N|= 4 (exp  4), class= 3 (exp  3) OK
U 5: |U|= 3 (exp  3), |N|=12 (exp 12), class= 1 (exp  1) OK
U 6: |U|= 4 (exp  4), |N|= 4 (exp  4), class= 3 (exp  3) OK
U 7: |U|= 6 (exp  6), |N|=12 (exp 12), class= 1 (exp  1) OK
U 8: |U|= 6 (exp  6), |N|=12 (exp 12), class= 1 (exp  1) OK
U 9: |U|= 6 (exp  6), |N|=12 (exp 12), class= 1 (exp  1) OK
U10: |U|=12 (exp 12), |N|=12 (exp 12), class= 1 (exp  1) OK
PASS
```

### `check13_invariants.py`

```
PASS: φ is a bijection, preserves identity, respects the contragredient
      correspondence, and is a homomorphism of array actions
```

### `check14_transpose.py`

```
Part 1: β_{G/U_i} == M^T e_i (row i of M), direct computation
  → 10/10 verified

Part 2: M^T e_i (correct) vs M e_i (paper's convention)
  → M e_i ≠ row i of M for 10/10 values of i

  Explicit counterexample (i=6, X=G/U_6):
    M^T e_6 = [3. 3. 1. 1. 0. 1. 0. 0. 0. 0.]  (correct; matches direct β)
    M   e_6 = [0. 0. 0. 0. 0. 1. 0. 0. 0. 1.]  (paper's convention; wrong)

Part 3: composite X = G/U_2 ⊔ G/U_6
  direct β_X    = [9, 9, 1, 1, 0, 1, 0, 0, 0, 0]
  M^T a (correct) = [9.0, 9.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]  MATCH
  M   a (paper)   = [0.0, 6.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 2.0, 2.0]  MISMATCH
  B^T β_X = [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]  (matches a = e_2 + e_6)

PASS: β_X = M^T a (correct) holds; β_X = M a (paper) fails
```

### `check15_burnside_convention.py`

```
Part 1: rowsums(B)·β_X = |X/G| for X = G/U_i (expected 1)
  i= 1: rowsums=1.0000, first_row=1.0000  (rowsums OK | first_row = Burnside)
  i= 2: rowsums=1.0000, first_row=0.5000  (rowsums OK | first_row ≠ Burnside)
  i= 3: rowsums=1.0000, first_row=0.5000  (rowsums OK | first_row ≠ Burnside)
  i= 4: rowsums=1.0000, first_row=0.5000  (rowsums OK | first_row ≠ Burnside)
  i= 5: rowsums=1.0000, first_row=0.3333  (rowsums OK | first_row ≠ Burnside)
  i= 6: rowsums=1.0000, first_row=0.2500  (rowsums OK | first_row ≠ Burnside)
  i= 7: rowsums=1.0000, first_row=0.1667  (rowsums OK | first_row ≠ Burnside)
  i= 8: rowsums=1.0000, first_row=0.1667  (rowsums OK | first_row ≠ Burnside)
  i= 9: rowsums=1.0000, first_row=0.1667  (rowsums OK | first_row ≠ Burnside)
  i=10: rowsums=1.0000, first_row=0.0833  (rowsums OK | first_row ≠ Burnside)

Part 2: composite X = G/U_2 ⊔ G/U_6, expected |X/G| = 2
  rowsums·β_X   = 2.0000  (correct, expected 2)
  first_row·β_X = 0.7500  (paper's claim, wrong)
  colsums·β_X   = -0.0000  (not Burnside)

Part 3: a_{U_1}(X) for X = G/U_i (expected δ_{i,1})
  row1(B)·β_X = 1/|U_i| (paper's convention; wrong)
  col1(B)·β_X = δ_{i,1} (correct convention)
  i= 1: row1·β=1.0000, col1·β=1.0000, expected=1.0  (row1≡a, col1≡a)
  i= 2: row1·β=0.5000, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 3: row1·β=0.5000, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 4: row1·β=0.5000, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 5: row1·β=0.3333, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 6: row1·β=0.2500, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 7: row1·β=0.1667, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 8: row1·β=0.1667, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i= 9: row1·β=0.1667, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)
  i=10: row1·β=0.0833, col1·β=0.0000, expected=0.0  (row1≠a, col1≡a)

PASS: row sums of B reproduce Burnside; first row does NOT; col 1 of B
      (not row 1) gives a_{U_1}
```

### `check16_projection.py`

```
Full ambient alphabet Σ (11 tokens):
  ['(+k-k)', '(+k-l)', '(-k+l)', '*j', '+0', '+j', '+k', '+l', '-j', '-k', '-l']

Option 1:
  image(π_1) = ['+0', '+j']
  image(π_2) = ['+0', '+j']
  image(π_3) = ['+0', '+j']
  Option uses 2 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 2:
  image(π_1) = ['+0', '+j', '+k']
  image(π_2) = ['+0', '+j', '+k']
  image(π_3) = ['+0', '+j', '+k']
  Option uses 3 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 3:
  image(π_1) = ['+0', '+j', '-j']
  image(π_2) = ['+0', '+j', '-j']
  image(π_3) = ['+0', '+j', '-j']
  Option uses 3 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 4:
  image(π_1) = ['+0', '+j', '+k', '-j', '-k']
  image(π_2) = ['+0', '+j', '+k', '-j', '-k']
  image(π_3) = ['+0', '+j', '+k', '-j', '-k']
  Option uses 5 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 5:
  image(π_1) = ['(+k-k)', '*j', '+0']
  image(π_2) = ['(+k-k)', '*j', '+0']
  image(π_3) = ['(+k-k)', '*j', '+0']
  Option uses 3 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 6:
  image(π_1) = ['*j', '+k', '-k']
  image(π_2) = ['*j', '+k', '-k']
  image(π_3) = ['*j', '+k', '-k']
  Option uses 3 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 7:
  image(π_1) = ['(+k-l)', '(-k+l)', '*j', '+0']
  image(π_2) = ['(+k-l)', '(-k+l)', '*j', '+0']
  image(π_3) = ['(+k-l)', '(-k+l)', '*j', '+0']
  Option uses 4 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False
Option 8:
  image(π_1) = ['*j', '+k', '+l', '-k', '-l']
  image(π_2) = ['*j', '+k', '+l', '-k', '-l']
  image(π_3) = ['*j', '+k', '+l', '-k', '-l']
  Option uses 5 distinct tokens, full Σ has 11
  (i)   surjective onto its image: TRIVIALLY TRUE (no constraint)
  (ii)  image independent of i:    True
  (iii) image = full Σ:            False

Summary for the author:
  (i) is vacuous.
  (ii) holds for all 8 options (verify above).
  (iii) holds for 0/8 options (each option uses a strict subset of Σ).

PASS: interpretation (ii) holds universally; (i) and (iii) as written
      provide no usable constraint
```

---

## Design principles

1. **No fitted constants.** Every literal in `common.py` is one of:
   - a **paper claim** (e.g. `EXPECTED` in `check12` = Table 5.1) —
     what the test checks;
   - **structurally verified data** (e.g. `U_REPS`, `S3_TO_CANONJAM`),
     guarded by `check12` / `check13`;
   - **generated at import time** from `canonjam` (the group
     operations themselves).

   No constant is "known to work" without a test that would fail if it
   were wrong.

2. **Structural invariants over spot checks.** `check13` tests
   composition, not just pointwise matching. `check14` tests on a
   **basis** (`{e_i}` spans `ℚ^10`) plus linearity on a direct sum,
   proving the relation for every finite `G`-set. `check15` tests
   **both** the correct statement (rowsums work) and the false one
   (first row fails).

3. **Independence from `M` where it matters.** `check14` and `check15`
   compute `β_X` directly from the coset action. If `mark_correct` had
   a bug, these checks would still detect the transpose error.

4. **Nonzero exit on failure.** Every script exits `0` on PASS and `1`
   on FAIL; `run_all.py` collapses to a single status.

5. **Self-documenting output.** Every script prints intermediate values
   (not just PASS/FAIL), so this record can quote exact numbers and any
   divergence is immediately visible.

---

## Runtime

| Script | Typical wall time |
|---|---|
| 01, 02, 03, 05, 08, 09, 11, 12, 13, 14, 15, 16 | < 1 s each |
| 04 | ~3–5 s (includes BBU `n = 4`: 20736 chains × 12 elements) |
| 06 | ~30–40 s (BBU `n = 5` skipped; PL/BPL/BU/BBU up to `n = 4`) |
| 07 | ~5 s |
| 10 | ~10 s (options 7, 8 at `n = 4` skipped) |
| `run_all.py` | ~60 s total |

Measured on AMD Ryzen 5 4600H at 4.00 GHz, Python 3.14.7.

---

## Dependencies

- `numpy` — array operations
- `canonjam` — `canonical_key`, `generate_group`, `rows_for_option`
- Standard library: `sys`, `os`, `fractions`, `itertools`, `subprocess`

No other dependencies. `canonjam` must be importable (either `pip
install -e .` from the repo root or `PYTHONPATH=.`).

---

## Cross-reference: paper sections ↔ checks

| Paper section | Check(s) |
|---|---|
| §2.3 mark formula | 01, 03, 14 |
| §2.3 / §5.2 `β_X = M a` | 14 |
| §2.3 "first row of `B`" | 15 |
| §2.4 chiral split (sign-twisted Burnside) | 07 |
| §3 Def. 3.1 "projection" | 16 |
| §3.1 group = `S_3 × Z/2` | 11, 13 |
| §4.1 `κ = κ′` (Thm 4.10) | 09 |
| §4.3 BPL/BU dichotomy (Prop. 4.19) | 08 |
| §5.1 Table 5.1 subgroups | 12 |
| §5.2 Prop. 5.3 (row/column) | 02, 03 |
| §5.3 Table 5.2 (fixed points) | 04 |
| §5.3 Thm 5.5 (closed forms) | 05 |
| §5.3 Burnside via `B` | 15 |
| §6 extended options 5–8 | 10 |
| §8 Table 8.1 (class counts) | 06 |

---

## What to do next

1. Apply the five edits (F1–F5) to `ve_OaM.tex` using the values in
   this README.
2. Insert `M(G)` and `B(G)` from `check03` into a new Appendix C.
3. Add the caption note to Table 5.2 (`q = |Σ_k| = 3, 6, 6, 12` for
   PL, BPL, BU, BBU).
4. Rerun `python3 run_all.py` — must remain 16/16 PASS.
