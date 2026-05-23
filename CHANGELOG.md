# Changelog

All notable changes to this fork (`schubydoo/dump1090-exporter`) will be
documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases are
automated by [Release Please](https://github.com/googleapis/release-please)
from Conventional Commit messages on `master`.

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
