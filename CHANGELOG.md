# Changelog

All notable changes to this fork (`schubydoo/dump1090-exporter`) will be
documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases are
automated by [Release Please](https://github.com/googleapis/release-please)
from Conventional Commit messages on `master`.

## [0.3.1](https://github.com/schubydoo/dump1090-exporter/compare/v0.3.0...v0.3.1) (2026-05-26)


### Bug Fixes

* **grafana:** restore stat tile values and All-instance query ([#29](https://github.com/schubydoo/dump1090-exporter/issues/29)) ([654fe0a](https://github.com/schubydoo/dump1090-exporter/commit/654fe0a94fb72ce7f3b0645cba68f123e2f2bce2))

## [0.3.0](https://github.com/schubydoo/dump1090-exporter/compare/v0.2.0...v0.3.0) (2026-05-24)


### Features

* **grafana:** modernize dashboard for Grafana 10+ ([#27](https://github.com/schubydoo/dump1090-exporter/issues/27)) ([0933466](https://github.com/schubydoo/dump1090-exporter/commit/0933466ac98ea4505be0a6eb0e39f45f23729cc9))

## [0.2.0](https://github.com/schubydoo/dump1090-exporter/compare/v0.1.0...v0.2.0) - 2026-05-23

**First published release of the modernized fork.** `v0.1.0` was a
placeholder version in the manifest; this is the first tag with a real
multi-arch GHCR image, an automated release pipeline, and a security
baseline. If you're coming from upstream `claws/dump1090-exporter 22.x`,
this is the snapshot to upgrade to.

### Highlights for consumers

- **Multi-arch container image** published to GHCR for every release:
  `ghcr.io/schubydoo/dump1090-exporter:0.2.0` (and `:0.2`, `:0`, `:latest`).
  Built for `linux/amd64`, `linux/arm64`, and `linux/arm/v7` — covers
  amd64 hosts, modern Raspberry Pi (4/5, CM4, Zero 2W in 64-bit mode), and
  older 32-bit Pis. Signed keyless via cosign; SLSA provenance + SBOM
  attestations attached. ~80 MB compressed on `python:3.14-alpine`.
- **`--version` CLI flag** (and a matching startup log line) so you can
  identify which exporter version is actually running in a container or
  service.
- **Same metric names as upstream.** No renames; existing Grafana dashboards
  (including the long-standing [dashboard 768](https://grafana.com/grafana/dashboards/768))
  keep working untouched.
- **Same CLI surface as upstream** plus `--version`. Existing deployments
  drop in as-is.

### Highlights for maintainers / contributors

- **Python support:** 3.11, 3.12, 3.13 (test matrix). The published Docker
  image runs on Python 3.14. Upstream dropped 3.6–3.10 here as part of the
  modernization — those versions are EOL or imminent EOL.
- **Toolchain:** `pyproject.toml` + `uv` + `ruff` + `mypy` + `pytest` /
  `pytest-asyncio`. `setup.py`, `requirements*.txt`, `Makefile`, `.pylintrc`,
  `.coveragerc`, and the dead `asynctest` dep are gone.
- **Test coverage** raised from 68% (upstream) to 90%+ with new unit tests
  for the geometry helpers, every `_fetch` error branch, `process_stats` /
  `process_aircraft` edge cases, and the CLI. An 85% floor in
  `pyproject.toml` catches future regressions.
- **CI** — modern workflows with every third-party action pinned to a
  commit SHA:
  - `ci.yml` — plan job that trims the matrix on docs-only PRs, full
    3 OS × 3 Python on master push, sdist+wheel build, and an image-smoke
    job that cross-builds `arm64`+`armv7` and curls `/metrics` against
    the bundled golden-data fixtures.
  - `lint.yml` — ruff + mypy.
  - `security.yml` — CodeQL, Gitleaks, Trivy filesystem, zizmor,
    Dependency Review, all in one consolidated file with file-level gating.
  - `scorecard.yml` — OSSF Scorecard.
  - `pr-title.yml` — Conventional Commit title validator.
  - `release.yml` — multi-arch GHCR publish + cosign sign + SBOM on tag
    push.
  - `release-please.yml` — automated release PRs on master push.
  - `renovate-uv-shas.yml` — auto-refreshes the per-arch uv SHA256 ARGs
    in the Dockerfile whenever Renovate bumps `UV_VERSION`, so the
    hash-pinned uv install stays current without manual intervention.
- **Supply chain** — image is built from a digest-pinned `python:3.14-alpine`
  base, and `uv` is fetched as a per-arch static binary verified by SHA256
  (no `pip install` in the build path). Closes every Scorecard
  Pinned-Dependencies finding.
- **Dependency management:** Renovate config with grouped/auto-merge rules
  for ruff / pytest / aio-stack / docker actions / security tooling /
  astral-sh-uv / demo-stack / release-automation. A custom regex manager
  tracks the Dockerfile's `UV_VERSION`.
- **Repo settings:** declarative via Probot Settings (`.github/settings.yml`)
  — labels (including `autorelease:*` so Release Please's chips survive),
  squash-merge defaults, branch protection.

### Refactoring (no behavioural change)

- Replace deprecated `asyncio.get_event_loop()` / `run_forever()` with
  `asyncio.run()` and signal-driven shutdown (SIGINT/SIGTERM on Linux,
  KeyboardInterrupt fallback on Windows).
- Drop blanket `except Exception` in the scraper loops for explicit
  `Dump1090Error`, `OSError`, `ValueError` handling — real bugs no longer
  get swallowed.
- Switch to `aiohttp.ClientTimeout` (the `timeout=` kwarg is deprecated
  upstream).
- Type hints modernized to PEP 604 unions and `collections.abc`.

### Notes

- This fork is **not** a successor to the upstream project — it is a
  maintained, up-to-date variant. Credit and attribution go to Chris Laws
  (`claws/dump1090-exporter`) for the original implementation.
- PyPI publishing is intentionally deferred — only the GHCR image and the
  GitHub source distribution are produced today.

### Conventional Commit details

Auto-generated from squash-merged PRs since `v0.1.0` (the manifest seed):

#### Features

* **cli:** add `--version` flag and startup version log
  ([#15](https://github.com/schubydoo/dump1090-exporter/pull/15))

#### Bug Fixes

* **docker:** install uv from a hash-verified binary, not pip
  ([#25](https://github.com/schubydoo/dump1090-exporter/pull/25))
* **docker:** pin Python base image by digest
  ([#24](https://github.com/schubydoo/dump1090-exporter/pull/24))
* **docker:** install project non-editable so the venv survives the
  inter-stage copy
  ([#14](https://github.com/schubydoo/dump1090-exporter/pull/14))

#### Build System & Dependencies

* **docker:** switch to alpine and beef up image-smoke
  ([#16](https://github.com/schubydoo/dump1090-exporter/pull/16))
* **demo:** pin demo stack images and group them in renovate
  ([#12](https://github.com/schubydoo/dump1090-exporter/pull/12))
* modernize Dockerfile with multi-stage uv-based build
  ([#3](https://github.com/schubydoo/dump1090-exporter/pull/3))

(`chore`, `ci`, `docs`, `refactor`, `style`, and `test` commits are
hidden from this section by design — see `release-please-config.json`.)

## [0.1.0] - 2026-05-23

Manifest-only placeholder; never tagged or published. Used as the starting
point for Release Please. See `v0.2.0` for the first real release.
