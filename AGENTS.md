# dump1090-exporter

Prometheus exporter for [`dump1090`](https://github.com/flightaware/dump1090) —
scrapes its JSON stats and re-exposes them as Prometheus metrics. Python.

**This is a maintained fork** of [`claws/dump1090-exporter`](https://github.com/claws/dump1090-exporter)
(Chris Laws), whose upstream is unmaintained. This fork modernizes tooling,
security baseline, and release pipeline **without changing exporter behaviour** —
keep behavioural parity; credit for the original design belongs upstream.

## Build · test · lint

```
uv sync --extra dev
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy src/dump1090exporter
```

The last line mirrors CI. Works with the `dump1090` mutability fork, `dump1090-fa`, and `readsb`.

## Hard rules

- **Behavioural parity with upstream** — this fork modernizes packaging/CI/security, not the
  exporter's metrics or scraping behaviour. A metrics-surface change needs an explicit reason.
- **Conventional Commits** — PR titles are enforced (`pr-title.yml`); release-please drives
  versioning + CHANGELOG. Never hand-edit `CHANGELOG.md` or the release manifest.
- **GitHub Actions are SHA-pinned**; Renovate manages dependency + action bumps.
- CI gates: unit tests on Linux/macOS/Windows × Python 3.11/3.12/3.13, `ruff` + `mypy` lint,
  security + Scorecard. Coverage ~90%.

## Release

A multi-arch image (`amd64`/`arm64`/`arm/v7`) publishes to GHCR on every release.
Default and PR target branch is **`master`**.
