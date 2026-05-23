# Contributing

Thanks for your interest in `dump1090-exporter`.

## Quick start

```bash
git clone https://github.com/schubydoo/dump1090-exporter
cd dump1090-exporter
uv sync --extra dev
uv run pytest
```

## Pull-request expectations

- Branch from `master`; open the PR back against `master`. No stacking — use
  GitHub's "Update branch" button to rebase open PRs after a sibling merges.
- One PR = one logical change. Keep diffs focused and reviewable.
- **Conventional Commits for the squash-merge subject** (see
  [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)).
  Release Please reads these to bump the version and write the `CHANGELOG.md`.
  The merge-commit subject is what counts; individual commits on the branch are
  flattened into it.
- Commit messages: imperative subject ≤72 chars (`feat(metrics): ...`,
  `fix(exporter): ...`), body only if context is needed. **Signed commits
  required** (GitHub must show "Verified"). SSH or GPG signing both work — see
  [GitHub's docs](https://docs.github.com/en/authentication/managing-commit-signature-verification).
- Run `uv run ruff check && uv run ruff format --check && uv run mypy src/dump1090exporter && uv run pytest`
  before pushing.

### Conventional Commits prefixes

| Prefix | Section in CHANGELOG | Triggers release? |
|---|---|---|
| `feat:` | Features | minor bump |
| `fix:` | Bug Fixes | patch bump |
| `perf:` | Performance | patch bump |
| `feat!:` or `BREAKING CHANGE:` body | Features (breaking) | major bump |
| `docs:` | Documentation | no |
| `test:` | Tests | no |
| `refactor:` | Refactoring | no |
| `build:` | Build System | no |
| `ci:` | Continuous Integration | no |
| `chore:` | Miscellaneous | no |

Optional scopes in parens (`feat(metrics): ...`) are encouraged.

## Releases

Releases are automated by
[Release Please](https://github.com/googleapis/release-please-action). Each
push to `master` re-evaluates the open commits; if there's at least one
`feat:`, `fix:`, or `perf:` since the last tag, Release Please opens (or
updates) a **release PR** that bumps `__version__` in
`src/dump1090exporter/__init__.py`, updates `CHANGELOG.md`, and edits
`.release-please-manifest.json`. Merging that PR tags the commit (e.g.
`v0.1.1`) and fires `release.yml`, which builds the multi-arch image and
pushes it to GHCR.

PyPI publishing is **not** configured today.

Practical implications:

- Don't edit `CHANGELOG.md` by hand for routine PRs — Release Please rewrites
  it from commit messages.
- Don't bump `__version__` by hand — Release Please owns it.
- Pure `docs:`, `ci:`, `chore:` work won't trigger a release on its own; it
  rides along with the next `feat:`/`fix:` commit.

## CI / GitHub Actions

The CI surface lives in `.github/workflows/`:

| File | Purpose | Triggers |
|---|---|---|
| `ci.yml` | Unit tests across Linux/macOS/Windows × Python 3.11/3.12/3.13, plus an sdist+wheel build job | push to master, pull_request |
| `lint.yml` | `ruff check`, `ruff format --check`, `mypy` | push, pull_request |
| `security.yml` | CodeQL + Gitleaks + Trivy filesystem + zizmor + Dependency Review | push, pull_request, weekly cron |
| `scorecard.yml` | OSSF Scorecard | weekly cron, push to master, branch protection rule changes |
| `pr-title.yml` | Conventional Commit PR title validator | pull_request |
| `release-please.yml` | Opens / updates the release PR | push to master |
| `release.yml` | Builds + pushes the multi-arch GHCR image on `v*` tag push | tag push, manual dispatch |

## Dependency management

Dependencies are managed by [Renovate](https://github.com/renovatebot/renovate)
via `renovate.json`. Patch bumps for dev tooling (ruff/pytest/mypy/pre-commit)
auto-merge; everything else opens a grouped PR for review.

GitHub Actions are pinned to commit SHAs and updated in lockstep groups
(docker/* majors, security tooling, astral-sh/uv across the action and the
image, etc.).

## Filing issues

Bug reports and feature requests are welcome at
<https://github.com/schubydoo/dump1090-exporter/issues>. Include the exporter
version, Python version, and a minimal reproduction where possible.
