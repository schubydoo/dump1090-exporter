# Changelog

All notable changes to this fork (`schubydoo/dump1090-exporter`) will be
documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases are
automated by [Release Please](https://github.com/googleapis/release-please)
from Conventional Commit messages on `master`.

## [0.3.3](https://github.com/schubydoo/dump1090-exporter/compare/v0.3.2...v0.3.3) (2026-08-22)


### Bug Fixes

* **deps:** constrain orjson &lt;3.12 to keep musl armv7 wheels ([#102](https://github.com/schubydoo/dump1090-exporter/issues/102)) ([5a3ac32](https://github.com/schubydoo/dump1090-exporter/commit/5a3ac321bc3774302f530cb7c269b323e8d25ba1))


### Dependencies

Sixty-two dependency commits landed since 0.3.2. Repeated bumps of the same
component are collapsed into one entry, linking the last update in the series.

* centralize Renovate config via shared preset ([#64](https://github.com/schubydoo/dump1090-exporter/issues/64)) ([260b853](https://github.com/schubydoo/dump1090-exporter/commit/260b853b3a76442d642d86af66206d25aea415e8))
* **ci:** update docker/login-action action to v4.6.0 ([#80](https://github.com/schubydoo/dump1090-exporter/issues/80)) ([7a07f21](https://github.com/schubydoo/dump1090-exporter/commit/7a07f2191a7fa82e8de130a14b7ac8919b0d468a)) (3 bumps)
* **ci:** update docker/setup-buildx-action action to v4.3.0 ([#104](https://github.com/schubydoo/dump1090-exporter/issues/104)) ([1fed49d](https://github.com/schubydoo/dump1090-exporter/commit/1fed49d1a0801d515d383b7570699909a27c9ec7))
* **ci:** update github-actions ([#74](https://github.com/schubydoo/dump1090-exporter/issues/74)) ([1ca25dc](https://github.com/schubydoo/dump1090-exporter/commit/1ca25dc78fbe9a5b68919ff3e98176e81153a7f0)) (3 grouped updates)
* **ci:** update github/codeql-action action to v4.37.7 ([#96](https://github.com/schubydoo/dump1090-exporter/issues/96)) ([25577ad](https://github.com/schubydoo/dump1090-exporter/commit/25577ade68b29a3f7863503f27f00bd4bb9a8fd6)) (8 bumps)
* **deps:** lock file maintenance ([#99](https://github.com/schubydoo/dump1090-exporter/issues/99)) ([2e13d8b](https://github.com/schubydoo/dump1090-exporter/commit/2e13d8becd0bd6b49c6fafadb07fc107d44b681e)) (12 refreshes)
* **deps:** update actions/checkout action to v7 ([#49](https://github.com/schubydoo/dump1090-exporter/issues/49)) ([d7e67cd](https://github.com/schubydoo/dump1090-exporter/commit/d7e67cd2a4d0c453e3480fd1fe4e33f3af617c16))
* **deps:** update astral-sh/setup-uv action to v10 ([#95](https://github.com/schubydoo/dump1090-exporter/issues/95)) ([e5835b0](https://github.com/schubydoo/dump1090-exporter/commit/e5835b0e51b3dde1a6d4a2a98104b82edc452fa5)) (2 bumps)
* **deps:** update astral-sh/uv ([#55](https://github.com/schubydoo/dump1090-exporter/issues/55)) ([f736d53](https://github.com/schubydoo/dump1090-exporter/commit/f736d53ac93c7793b943f9d52dbccda68a51806b)) (3 bumps)
* **deps:** update demo stack ([#67](https://github.com/schubydoo/dump1090-exporter/issues/67)) ([5f2133d](https://github.com/schubydoo/dump1090-exporter/commit/5f2133d1f3f63bb215f8bd002de898082487d330)) (2 bumps)
* **deps:** update dependency uv to v0.12.5 ([#98](https://github.com/schubydoo/dump1090-exporter/issues/98)) ([940ca59](https://github.com/schubydoo/dump1090-exporter/commit/940ca592e6158a0675c0957325781bb32d2ba331)) (10 bumps)
* **deps:** update docker/dockerfile docker tag to v1.26 ([#84](https://github.com/schubydoo/dump1090-exporter/issues/84)) ([bfc7ec1](https://github.com/schubydoo/dump1090-exporter/commit/bfc7ec100a747d356a10e6b4b01af5a56e916534)) (3 bumps)
* **deps:** update grafana/grafana docker tag to v13.2.0 ([#101](https://github.com/schubydoo/dump1090-exporter/issues/101)) ([1f44afe](https://github.com/schubydoo/dump1090-exporter/commit/1f44afee536f2536b9ee0bbf7a5d0cd8bbcb376c)) (4 bumps)
* **deps:** update prom/prometheus docker tag to v3.14.0 ([#100](https://github.com/schubydoo/dump1090-exporter/issues/100)) ([6ab087c](https://github.com/schubydoo/dump1090-exporter/commit/6ab087cbb232df8420f81662d3bb111ed71fb145)) (3 bumps)
* **deps:** update python:3.14-alpine docker digest to 05b2b8b ([#94](https://github.com/schubydoo/dump1090-exporter/issues/94)) ([0497f99](https://github.com/schubydoo/dump1090-exporter/commit/0497f9939d7348f85f887409a3bb154a744f7a53)) (5 digest refreshes)
* retire renovate-uv-shas.yml workflow (replaced by Renovate CE postUpgradeTask) ([#72](https://github.com/schubydoo/dump1090-exporter/issues/72)) ([0a2e4ef](https://github.com/schubydoo/dump1090-exporter/commit/0a2e4ef714fc7b6ce07093f19322cea266ffe953))

## [0.3.2](https://github.com/schubydoo/dump1090-exporter/compare/v0.3.1...v0.3.2) (2026-06-08)


### Miscellaneous

* release 0.3.2 ([a204ae8](https://github.com/schubydoo/dump1090-exporter/commit/a204ae8a2fc458a9358214092fc2357ab12ef480))

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
