# ADR-0005: Versioning, DOI policy, and Zenodo metadata

## Status

Accepted (2026-11-15)

## Context

`canonJAM` is archived on Zenodo via GitHub release integration.
That integration has one specific pitfall: if `.zenodo.json`
contains a `version` field, Zenodo labels the archived record with
that field, **not** with the git tag. During v1.2.1, the field was
present with a stale value (`1.1.0`) and produced a duplicate
"1.1.0" record alongside the real v1.1.0 record from Oct 22. The
correction required manual metadata editing on Zenodo (record
23720668).

Separately, the release process (SemVer, CHANGELOG, two DOIs) needs
to be documented so that releases are reproducible by future
maintainers.

## Decision

**Versioning.** SemVer. `MAJOR.MINOR.PATCH`. A release that
introduces a change to the public API (removal, rename, semantic
change) bumps MAJOR; a release that adds features or significant
reorganization bumps MINOR; a release with only bug fixes bumps
PATCH. The `__version__` in `canonjam/__init__.py` and the version
in `pyproject.toml` are always kept in sync.

**CHANGELOG.** One entry per release, under `CHANGELOG.md`. Past
entries are **not rewritten** when files move or APIs change: the
history describes the state at the time of the release. A move or
rename produces a new entry that describes the move, not a
retroactive edit of older entries.

**Zenodo DOIs.** Two DOIs per artifact:

- A **concept DOI** (assigned when the first version is archived)
  always resolves to the latest version. Used in README badges and
  in "Cite this" sections.
- A **version DOI** (assigned per release) identifies the exact
  release. Used in `CITATION.cff`.

**Zenodo metadata.** `.zenodo.json` **does not contain a `version`
field**. The git tag is the single source of truth for the version
label. The `.zenodo.json` contains title, description, creators,
license, keywords, and `related_identifiers`, and nothing that
duplicates what the release tag already encodes.

## Consequences

**Gains.**

- No duplicate Zenodo records from stale `version` fields.
- Version label always matches the tag; no manual metadata
  correction needed at release time.
- Concept DOI always resolves to the latest version, so README
  badges stay valid across releases.
- CHANGELOG remains an honest historical record; users can look up
  what changed at each release without being confused by
  retroactive edits.

**Losses.**

- The maintainer must remember **not** to re-add `version` to
  `.zenodo.json` (the pre-commit config does not check this today;
  adding a check is a future improvement).
- If a tag must be re-cut (rare), the version DOI of the bad tag
  cannot be undone; a new tag is required. Accepted: this is a
  general constraint of Zenodo, not specific to `canonJAM`.
- `related_identifiers` currently points only to the JAM paper
  ([Arcudia2023]). When the columnar G-sets paper and the Lean repo
  are archived, they should be added as `isSupplementedBy` /
  `isSupplementedBy`. Not in scope for v1.3.0.
