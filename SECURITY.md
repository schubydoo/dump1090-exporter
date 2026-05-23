# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities **privately** via GitHub Security
Advisories: <https://github.com/schubydoo/dump1090-exporter/security/advisories/new>.

Do **not** open a public issue for security bugs.

You should receive an acknowledgement within 72 hours. Confirmed issues
will be patched and disclosed within 30 days where reasonable.

## Supported Versions

This project is a maintained fork of
[`claws/dump1090-exporter`](https://github.com/claws/dump1090-exporter); only
releases from this fork (`schubydoo/dump1090-exporter`) receive security
updates.

| Version | Supported |
|---------|-----------|
| `0.x`   | ✅ (latest minor only) |
| upstream `22.x` and older | ❌ |

## Scope

The exporter is a read-only consumer of dump1090's JSON files / HTTP
endpoints, and it exposes a Prometheus `/metrics` HTTP server with no
authentication.

Treat the `/metrics` endpoint as **internal**: bind it to a trusted network or
front it with a reverse proxy if you need authentication. By default it binds
to `0.0.0.0` for convenience — narrow that to a loopback or LAN interface in
production deployments where the host is reachable from untrusted networks.

## Hardening checklist (recommended for users)

- Run the exporter in a container as a non-root user (the published GHCR
  image already does this).
- Restrict the exporter's network exposure to the Prometheus scraper
  (firewall / Docker network / bind to a non-public address).
- Keep the image current — Renovate ships dependency and base-image bumps as
  routine PRs, and `release.yml` publishes a fresh signed image on every tag.
- Verify image signatures with `cosign verify` against the keyless OIDC
  identity of the `release.yml` workflow before deploying.
