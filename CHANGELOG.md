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

* centralize Renovate config via shared preset ([#64](https://github.com/schubydoo/dump1090-exporter/issues/64)) ([260b853](https://github.com/schubydoo/dump1090-exporter/commit/260b853b3a76442d642d86af66206d25aea415e8))
* **ci:** update docker/login-action action to v4.5.1 ([#75](https://github.com/schubydoo/dump1090-exporter/issues/75)) ([d50c81d](https://github.com/schubydoo/dump1090-exporter/commit/d50c81dcf943c190e5711d6e717914a4e104e9c3))
* **ci:** update docker/login-action action to v4.5.2 ([#77](https://github.com/schubydoo/dump1090-exporter/issues/77)) ([e1d6e6c](https://github.com/schubydoo/dump1090-exporter/commit/e1d6e6cb953828569e3d052c7ef85fda453f736f))
* **ci:** update docker/login-action action to v4.6.0 ([#80](https://github.com/schubydoo/dump1090-exporter/issues/80)) ([7a07f21](https://github.com/schubydoo/dump1090-exporter/commit/7a07f2191a7fa82e8de130a14b7ac8919b0d468a))
* **ci:** update docker/setup-buildx-action action to v4.3.0 ([#104](https://github.com/schubydoo/dump1090-exporter/issues/104)) ([1fed49d](https://github.com/schubydoo/dump1090-exporter/commit/1fed49d1a0801d515d383b7570699909a27c9ec7))
* **ci:** update github-actions ([#66](https://github.com/schubydoo/dump1090-exporter/issues/66)) ([d473b90](https://github.com/schubydoo/dump1090-exporter/commit/d473b90e722d4079fa1160d41c89a52891ecbcbb))
* **ci:** update github-actions ([#74](https://github.com/schubydoo/dump1090-exporter/issues/74)) ([1ca25dc](https://github.com/schubydoo/dump1090-exporter/commit/1ca25dc78fbe9a5b68919ff3e98176e81153a7f0))
* **ci:** update github/codeql-action action to v4.37.3 ([#71](https://github.com/schubydoo/dump1090-exporter/issues/71)) ([e7e5f16](https://github.com/schubydoo/dump1090-exporter/commit/e7e5f16a3a2cfc7bf59e4675e80e3412a13a7133))
* **ci:** update github/codeql-action action to v4.37.4 ([#81](https://github.com/schubydoo/dump1090-exporter/issues/81)) ([6feb4bf](https://github.com/schubydoo/dump1090-exporter/commit/6feb4bfb90f810090ccca16c185f8c55ae015c5f))
* **ci:** update github/codeql-action action to v4.37.5 ([#86](https://github.com/schubydoo/dump1090-exporter/issues/86)) ([dc5951c](https://github.com/schubydoo/dump1090-exporter/commit/dc5951cfe80cb278c01e7b53604c523cb13b318a))
* **ci:** update github/codeql-action action to v4.37.6 ([#87](https://github.com/schubydoo/dump1090-exporter/issues/87)) ([fd991b7](https://github.com/schubydoo/dump1090-exporter/commit/fd991b7099dc8b5e83b6e692881bc2eca272e290))
* **ci:** update github/codeql-action action to v4.37.7 ([#96](https://github.com/schubydoo/dump1090-exporter/issues/96)) ([25577ad](https://github.com/schubydoo/dump1090-exporter/commit/25577ade68b29a3f7863503f27f00bd4bb9a8fd6))
* **deps:** lock file maintenance ([#43](https://github.com/schubydoo/dump1090-exporter/issues/43)) ([4e3f7f8](https://github.com/schubydoo/dump1090-exporter/commit/4e3f7f83760a3de467aea22333dd7fd09630c097))
* **deps:** lock file maintenance ([#45](https://github.com/schubydoo/dump1090-exporter/issues/45)) ([83b1181](https://github.com/schubydoo/dump1090-exporter/commit/83b1181293ef68ae78f24e3034f04f81a2a815ba))
* **deps:** lock file maintenance ([#50](https://github.com/schubydoo/dump1090-exporter/issues/50)) ([89df707](https://github.com/schubydoo/dump1090-exporter/commit/89df707706e0ecefba251401f7ff2a41e6180edc))
* **deps:** lock file maintenance ([#52](https://github.com/schubydoo/dump1090-exporter/issues/52)) ([ff1a996](https://github.com/schubydoo/dump1090-exporter/commit/ff1a996d83d96df1a5960afb596d80a493e3b085))
* **deps:** lock file maintenance ([#58](https://github.com/schubydoo/dump1090-exporter/issues/58)) ([d926a85](https://github.com/schubydoo/dump1090-exporter/commit/d926a8587d377e731980b0ef63210ae832d55ed2))
* **deps:** lock file maintenance ([#60](https://github.com/schubydoo/dump1090-exporter/issues/60)) ([38b183a](https://github.com/schubydoo/dump1090-exporter/commit/38b183aa26e3aca19c48c233da34f5d5ac899008))
* **deps:** lock file maintenance ([#62](https://github.com/schubydoo/dump1090-exporter/issues/62)) ([5f5009d](https://github.com/schubydoo/dump1090-exporter/commit/5f5009d13b80ba035834aefa4806f2201bcbc5e0))
* **deps:** lock file maintenance ([#63](https://github.com/schubydoo/dump1090-exporter/issues/63)) ([b115940](https://github.com/schubydoo/dump1090-exporter/commit/b115940490ce8193eab68d77f66a7ab8748856a4))
* **deps:** lock file maintenance ([#76](https://github.com/schubydoo/dump1090-exporter/issues/76)) ([beb361b](https://github.com/schubydoo/dump1090-exporter/commit/beb361b66291aafb70bced3e32d60d8c0d3ad304))
* **deps:** lock file maintenance ([#85](https://github.com/schubydoo/dump1090-exporter/issues/85)) ([0ca2f60](https://github.com/schubydoo/dump1090-exporter/commit/0ca2f60897a8f9822042edf87a78c953f67ff923))
* **deps:** lock file maintenance ([#93](https://github.com/schubydoo/dump1090-exporter/issues/93)) ([bd6dbdc](https://github.com/schubydoo/dump1090-exporter/commit/bd6dbdc352b267f91af92d358ec9dc5b694d13a9))
* **deps:** lock file maintenance ([#99](https://github.com/schubydoo/dump1090-exporter/issues/99)) ([2e13d8b](https://github.com/schubydoo/dump1090-exporter/commit/2e13d8becd0bd6b49c6fafadb07fc107d44b681e))
* **deps:** pin docker/dockerfile docker tag to 0adf442 ([#65](https://github.com/schubydoo/dump1090-exporter/issues/65)) ([3aa71ca](https://github.com/schubydoo/dump1090-exporter/commit/3aa71cab2c07996a682bb473759f77ccef780289))
* **deps:** update actions/checkout action to v7 ([#49](https://github.com/schubydoo/dump1090-exporter/issues/49)) ([d7e67cd](https://github.com/schubydoo/dump1090-exporter/commit/d7e67cd2a4d0c453e3480fd1fe4e33f3af617c16))
* **deps:** update astral-sh/setup-uv action to v10 ([#95](https://github.com/schubydoo/dump1090-exporter/issues/95)) ([e5835b0](https://github.com/schubydoo/dump1090-exporter/commit/e5835b0e51b3dde1a6d4a2a98104b82edc452fa5))
* **deps:** update astral-sh/setup-uv action to v9 ([#69](https://github.com/schubydoo/dump1090-exporter/issues/69)) ([eefb858](https://github.com/schubydoo/dump1090-exporter/commit/eefb858cf165241b1f3c4eb4c67408142cdfa87e))
* **deps:** update astral-sh/uv ([#47](https://github.com/schubydoo/dump1090-exporter/issues/47)) ([8772812](https://github.com/schubydoo/dump1090-exporter/commit/877281223f1540e3c86d6e0769655483a77cba04))
* **deps:** update astral-sh/uv ([#55](https://github.com/schubydoo/dump1090-exporter/issues/55)) ([f736d53](https://github.com/schubydoo/dump1090-exporter/commit/f736d53ac93c7793b943f9d52dbccda68a51806b))
* **deps:** update astral-sh/uv to v0.11.20 ([#42](https://github.com/schubydoo/dump1090-exporter/issues/42)) ([86b37de](https://github.com/schubydoo/dump1090-exporter/commit/86b37decafa797c9b78fd37e46d86b979797c73a))
* **deps:** update demo stack ([#51](https://github.com/schubydoo/dump1090-exporter/issues/51)) ([6270c38](https://github.com/schubydoo/dump1090-exporter/commit/6270c386a3d883b14ff698388773fe14d9ea228d))
* **deps:** update demo stack ([#67](https://github.com/schubydoo/dump1090-exporter/issues/67)) ([5f2133d](https://github.com/schubydoo/dump1090-exporter/commit/5f2133d1f3f63bb215f8bd002de898082487d330))
* **deps:** update dependency uv to v0.11.29 ([#59](https://github.com/schubydoo/dump1090-exporter/issues/59)) ([e388224](https://github.com/schubydoo/dump1090-exporter/commit/e388224ade461bfdfbf12db91568f830518f804e))
* **deps:** update dependency uv to v0.11.31 ([#68](https://github.com/schubydoo/dump1090-exporter/issues/68)) ([6b24734](https://github.com/schubydoo/dump1090-exporter/commit/6b2473490776e1402de554ee8cacea5504376ad8))
* **deps:** update dependency uv to v0.11.32 ([#73](https://github.com/schubydoo/dump1090-exporter/issues/73)) ([82b1cfc](https://github.com/schubydoo/dump1090-exporter/commit/82b1cfc528ebee4bd11fc30d71d4bcf54974796c))
* **deps:** update dependency uv to v0.11.33 ([#78](https://github.com/schubydoo/dump1090-exporter/issues/78)) ([f56ba9d](https://github.com/schubydoo/dump1090-exporter/commit/f56ba9d240bbd58dda5c1d8686da3e57021329e3))
* **deps:** update dependency uv to v0.12.0 ([#79](https://github.com/schubydoo/dump1090-exporter/issues/79)) ([cc4e330](https://github.com/schubydoo/dump1090-exporter/commit/cc4e33045444ee07b1f9d361cd6fece2b4e014ae))
* **deps:** update dependency uv to v0.12.1 ([#83](https://github.com/schubydoo/dump1090-exporter/issues/83)) ([20a0652](https://github.com/schubydoo/dump1090-exporter/commit/20a06529dc048bc7b31ad415f4ec3480dba540ea))
* **deps:** update dependency uv to v0.12.2 ([#90](https://github.com/schubydoo/dump1090-exporter/issues/90)) ([dd6c083](https://github.com/schubydoo/dump1090-exporter/commit/dd6c083d4b2686e597046b1a0f077a983a29aa22))
* **deps:** update dependency uv to v0.12.3 ([#92](https://github.com/schubydoo/dump1090-exporter/issues/92)) ([6d90a97](https://github.com/schubydoo/dump1090-exporter/commit/6d90a97419fe85d100068348525c9330eeff6252))
* **deps:** update dependency uv to v0.12.4 ([#97](https://github.com/schubydoo/dump1090-exporter/issues/97)) ([0cf29b9](https://github.com/schubydoo/dump1090-exporter/commit/0cf29b969a2bbc6e0af7974a7b01214c7adffff8))
* **deps:** update dependency uv to v0.12.5 ([#98](https://github.com/schubydoo/dump1090-exporter/issues/98)) ([940ca59](https://github.com/schubydoo/dump1090-exporter/commit/940ca592e6158a0675c0957325781bb32d2ba331))
* **deps:** update docker/dockerfile docker tag to v1.25 ([#48](https://github.com/schubydoo/dump1090-exporter/issues/48)) ([66ee360](https://github.com/schubydoo/dump1090-exporter/commit/66ee3609ee0cef3f95cc8d77749c0a375788fe27))
* **deps:** update docker/dockerfile docker tag to v1.26 ([#84](https://github.com/schubydoo/dump1090-exporter/issues/84)) ([bfc7ec1](https://github.com/schubydoo/dump1090-exporter/commit/bfc7ec100a747d356a10e6b4b01af5a56e916534))
* **deps:** update github-actions (non-major) ([#54](https://github.com/schubydoo/dump1090-exporter/issues/54)) ([0ebddca](https://github.com/schubydoo/dump1090-exporter/commit/0ebddca9f222a73fbbb5a6dbd36b7342c10b2f62))
* **deps:** update github/codeql-action action to v4.36.3 ([#53](https://github.com/schubydoo/dump1090-exporter/issues/53)) ([2cdbf52](https://github.com/schubydoo/dump1090-exporter/commit/2cdbf52e0321a1f2bbe5505a95681692136100ca))
* **deps:** update github/codeql-action action to v4.37.0 ([#57](https://github.com/schubydoo/dump1090-exporter/issues/57)) ([d396fb2](https://github.com/schubydoo/dump1090-exporter/commit/d396fb2d5b54f2cee4972e4ee6c1c0f097e16618))
* **deps:** update github/codeql-action action to v4.37.1 ([#61](https://github.com/schubydoo/dump1090-exporter/issues/61)) ([0a69abc](https://github.com/schubydoo/dump1090-exporter/commit/0a69abc959feb3625238b8afe204952edc8e8a98))
* **deps:** update grafana/grafana docker tag to v13.1.2 ([#88](https://github.com/schubydoo/dump1090-exporter/issues/88)) ([3fa52e4](https://github.com/schubydoo/dump1090-exporter/commit/3fa52e4dc88d5067da495fe94398f4f1fa67cc25))
* **deps:** update grafana/grafana docker tag to v13.1.3 ([#91](https://github.com/schubydoo/dump1090-exporter/issues/91)) ([81dd336](https://github.com/schubydoo/dump1090-exporter/commit/81dd336447d449c4c0f70832eccc3d3c50643192))
* **deps:** update grafana/grafana docker tag to v13.2.0 ([#101](https://github.com/schubydoo/dump1090-exporter/issues/101)) ([1f44afe](https://github.com/schubydoo/dump1090-exporter/commit/1f44afee536f2536b9ee0bbf7a5d0cd8bbcb376c))
* **deps:** update grafana/grafana:13.1.1 docker digest to 7cb8c64 ([#70](https://github.com/schubydoo/dump1090-exporter/issues/70)) ([38da94a](https://github.com/schubydoo/dump1090-exporter/commit/38da94a2f9a2088b306167f2d8a33c5d2fc9923a))
* **deps:** update prom/prometheus docker tag to v3.13.1 ([#56](https://github.com/schubydoo/dump1090-exporter/issues/56)) ([100915a](https://github.com/schubydoo/dump1090-exporter/commit/100915ac7bc23f607afa79812b1d466b10f792f1))
* **deps:** update prom/prometheus docker tag to v3.13.2 ([#82](https://github.com/schubydoo/dump1090-exporter/issues/82)) ([5ef66d2](https://github.com/schubydoo/dump1090-exporter/commit/5ef66d271cb661f7c8715f0ef84c8bce1352a2ad))
* **deps:** update prom/prometheus docker tag to v3.14.0 ([#100](https://github.com/schubydoo/dump1090-exporter/issues/100)) ([6ab087c](https://github.com/schubydoo/dump1090-exporter/commit/6ab087cbb232df8420f81662d3bb111ed71fb145))
* **deps:** update python:3.14-alpine docker digest to 003970a ([#44](https://github.com/schubydoo/dump1090-exporter/issues/44)) ([50631bb](https://github.com/schubydoo/dump1090-exporter/commit/50631bb602abb6702cf0d4c347294928d9875067))
* **deps:** update python:3.14-alpine docker digest to 05b2b8b ([#94](https://github.com/schubydoo/dump1090-exporter/issues/94)) ([0497f99](https://github.com/schubydoo/dump1090-exporter/commit/0497f9939d7348f85f887409a3bb154a744f7a53))
* **deps:** update python:3.14-alpine docker digest to 2673086 ([#46](https://github.com/schubydoo/dump1090-exporter/issues/46)) ([02af113](https://github.com/schubydoo/dump1090-exporter/commit/02af1134ef8a68a28e21538aae8af5cc269d66eb))
* **deps:** update python:3.14-alpine docker digest to a132151 ([#89](https://github.com/schubydoo/dump1090-exporter/issues/89)) ([995af3c](https://github.com/schubydoo/dump1090-exporter/commit/995af3c361bd282faf529805d3ff341d45546a9c))
* **deps:** update python:3.14-alpine docker digest to c5c7233 ([#41](https://github.com/schubydoo/dump1090-exporter/issues/41)) ([fb408a1](https://github.com/schubydoo/dump1090-exporter/commit/fb408a111b61c2e8aac4ca79d4eb6937a22327e4))
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
