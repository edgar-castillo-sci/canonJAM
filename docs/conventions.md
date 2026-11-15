# Conventions

Minor project conventions that are not architectural decisions
(those live in `docs/adr/`).

## Filenames

English. Spanish filenames were renamed in v1.2.0
(`validacion_tabla1.py` → `validation_table1.py`, etc.). Do not
reintroduce Spanish filenames.

## Bilingual READMEs

`README.md` (English) and `README.es.md` (Spanish) are kept in sync.
Both are user-facing; other documentation (`DESIGN.md`,
`docs/adr/`, `tests/README.md`, etc.) is English-only.

## CI scripts

Live under `.github/scripts/`, not under `scripts/`. CI scripts are
infrastructure, not part of the user-facing surface.

## Commit messages

Imperative form, one "why" per commit. Format:
`type(scope): short description` followed by an explanatory body.
The body explains **why** the change was made, not just what it does.
See `git log` for examples.

## When moving a file, grep for its old path first

Files can be referenced in more than one place: CI workflows,
pre-commit hooks, `Path(__file__)` arithmetic, README examples,
docstrings. Before `git mv`, run:

```
grep -rn '<old/path>' . \
  --include='*.yml' --include='*.yaml' --include='*.toml' \
  --include='*.py' --include='*.md' --include='*.cff'
```

and update every hit in the same commit. This convention was adopted
after the v1.3.0 `scripts/` move, where the pre-commit hook failed
with exit code 2 because `.pre-commit-config.yaml` still pointed to
the old path.

