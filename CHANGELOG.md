# Changelog

All notable changes to this fork (`schubydoo/dump1090-exporter`) will be
documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases are
automated by [Release Please](https://github.com/googleapis/release-please)
from Conventional Commit messages on `master`.

## [0.2.0](https://github.com/schubydoo/dump1090-exporter/compare/v0.1.0...v0.2.0) (2026-05-23)


### Features

* **cli:** add --version flag and startup version log ([#15](https://github.com/schubydoo/dump1090-exporter/issues/15)) ([09a6218](https://github.com/schubydoo/dump1090-exporter/commit/09a621853b4974824dad8f8127178436dc05d56a))


### Bug Fixes

* **docker:** install project non-editable so the venv survives stage copy ([#14](https://github.com/schubydoo/dump1090-exporter/issues/14)) ([0a1c1bf](https://github.com/schubydoo/dump1090-exporter/commit/0a1c1bf8bf1ca445ce6e817f11452372e6cedbea))
* **docker:** install uv from a hash-verified binary, not pip ([#25](https://github.com/schubydoo/dump1090-exporter/issues/25)) ([49f9af3](https://github.com/schubydoo/dump1090-exporter/commit/49f9af38033f5f766313267317e61c50c4ae033d))
* **docker:** pin Python base image by digest (closes Scorecard alerts) ([#24](https://github.com/schubydoo/dump1090-exporter/issues/24)) ([905eb62](https://github.com/schubydoo/dump1090-exporter/commit/905eb62cf14ab700b1e4cb8b2d232c15b1a7f867))


### Build System & Dependencies

* **demo:** pin demo stack images and group them in renovate ([#12](https://github.com/schubydoo/dump1090-exporter/issues/12)) ([b4bcefc](https://github.com/schubydoo/dump1090-exporter/commit/b4bcefce6033b7cad06aeda874c2d94922ee2733))
* **docker:** switch to alpine and beef up image-smoke ([#16](https://github.com/schubydoo/dump1090-exporter/issues/16)) ([6836d12](https://github.com/schubydoo/dump1090-exporter/commit/6836d12350a46f8b2262a7b58159ec8bdc0871c8))
* modernize Dockerfile with multi-stage uv-based build ([#3](https://github.com/schubydoo/dump1090-exporter/issues/3)) ([e53ae40](https://github.com/schubydoo/dump1090-exporter/commit/e53ae400ec264b1bc63be67ed4168e91864b14ec))

## [0.1.0] - 2026-05-23

Initial release under the `schubydoo/dump1090-exporter` fork. Brings the
project up to current Python tooling, security baseline, and release
automation without adding new features.

### Build System & Dependencies

- Migrate from `setup.py` + `requirements*.txt` + `asynctest` +
  `black`/`isort`/`pylint` to `pyproject.toml` + `uv` + `ruff` + `mypy` +
  `pytest`/`pytest-asyncio`.
- Drop Python 3.6–3.10 (EOL or imminent EOL); supported versions are now
  3.11, 3.12, 3.13.
- Bump `aiohttp` and `aioprometheus` to current versions.
- Rewrite the Dockerfile as a multi-stage `uv`-based build on
  `python:3.13-slim`, with OCI labels, a non-root user (UID 1000), and a
  `HEALTHCHECK` against `/metrics`. Image is published multi-arch
  (`linux/amd64,linux/arm64,linux/arm/v7`) to GHCR with SBOM, provenance,
  and a cosign keyless signature on every tag.

### Continuous Integration

- Add modern CI (`ci.yml`, `lint.yml`), comprehensive security workflows
  (`security.yml` — CodeQL / Gitleaks / Trivy filesystem / zizmor /
  Dependency Review), OSSF Scorecard, and a Conventional Commits PR-title
  validator.
- All third-party actions pinned to commit SHAs; Renovate (`renovate.json`)
  manages them as grouped weekly PRs and auto-merges patch-level dev tooling
  bumps.
- Release Please automates version bumps and `CHANGELOG.md` writes from
  Conventional Commit messages; tagged releases publish to GHCR via
  `release.yml`.

### Refactoring

- Drop the deprecated `asyncio.get_event_loop()` / `run_forever()` pattern
  for `asyncio.run()` with signal-driven shutdown.
- Replace blanket `except Exception` in the scraper loops with explicit
  `Dump1090Error`, `OSError`, and `ValueError` handling.
- Use `aiohttp.ClientTimeout` instead of the deprecated `timeout=` keyword.
- Type hints modernized to PEP 604 unions and `collections.abc`.

### Notes

This fork is **not** a successor to the upstream project — it is a
maintained, up-to-date variant. Credit and attribution go to Chris Laws
(`claws/dump1090-exporter`) for the original implementation.
