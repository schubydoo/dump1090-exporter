# syntax=docker/dockerfile:1.28@sha256:bb22d9815c728170f72750f4e5b0d672e06176142e1d602c7e66c050100b7e5b

# Pinned uv release. Renovate's PyPI regex manager (renovate.json) bumps
# UV_VERSION on the next master scan. The per-arch SHA256 hashes below
# must update IN LOCKSTEP — refresh them with `tools/update-uv-shas.sh`
# (or by hand from
# https://github.com/astral-sh/uv/releases/download/<ver>/dist-manifest.json).
ARG UV_VERSION=0.12.23
ARG UV_SHA256_AMD64=1cff8783850e794470aadb73f54b749542a511fc57b0ce6468b64bd3852e0ade
ARG UV_SHA256_ARM64=b536543cc4d50661986b165c76ee8aa9056e4fa332edcd153ff2e98760f9359b
ARG UV_SHA256_ARMV7=f5c941f2a7fa078ffcbc58654ec1b37de98e2a93a24cd3deb19c1acdd66ff533

# --------------------------------------------------------------------------
# 1. builder — install the project + its locked deps into a venv at /app/.venv
# --------------------------------------------------------------------------
# Pin the base image by digest (tag AND sha256) so Scorecard's
# Pinned-Dependencies check is satisfied and supply-chain attacks via tag
# repointing are blocked. Renovate's docker manager bumps tag + digest in
# the same PR.
FROM python:3.14-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72 AS builder

# ARGs declared before the first FROM are "global" — they substitute into
# the FROM line(s) but are invisible to RUN inside the stage unless
# re-declared here.
ARG UV_VERSION
ARG UV_SHA256_AMD64
ARG UV_SHA256_ARM64
ARG UV_SHA256_ARMV7

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Install uv by downloading the per-arch static binary from GitHub releases
# and verifying its SHA256. Replaces the previous `pip install uv==<ver>`
# which Scorecard flagged (pipCommand not pinned by hash — the install
# pulled uv + transitive deps from PyPI without `--require-hashes`).
#
# Picks the right artifact via `uname -m` because buildx executes the RUN
# inside the target-arch builder. Astral's official tarballs are statically
# linked against musl, which matches the alpine base.
RUN set -eux; \
    case "$(uname -m)" in \
        x86_64) target="x86_64-unknown-linux-musl"; expected="${UV_SHA256_AMD64}" ;; \
        aarch64) target="aarch64-unknown-linux-musl"; expected="${UV_SHA256_ARM64}" ;; \
        armv7l) target="armv7-unknown-linux-musleabihf"; expected="${UV_SHA256_ARMV7}" ;; \
        *) echo "Unsupported architecture: $(uname -m)" >&2; exit 1 ;; \
    esac; \
    cd /tmp; \
    wget -q -O uv.tar.gz "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-${target}.tar.gz"; \
    echo "${expected}  uv.tar.gz" | sha256sum -c -; \
    tar -xzf uv.tar.gz; \
    mv "uv-${target}/uv" "uv-${target}/uvx" /usr/local/bin/; \
    rm -rf "uv-${target}" uv.tar.gz; \
    uv --version

WORKDIR /app

# Install deps first (cache-friendly), then the project itself.
# `--no-editable` is critical: by default uv installs the local project as an
# editable .pth link into the venv pointing at /app/src/dump1090exporter. The
# runtime stage only copies /app/.venv across, so /app/src/ is missing and the
# editable link breaks at import time. --no-editable bakes a regular wheel
# install into site-packages instead.
COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable --no-install-project

COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


# --------------------------------------------------------------------------
# 2. runtime — alpine final image with just Python + the prebuilt venv
# --------------------------------------------------------------------------
# Same digest as the builder — keep them in lockstep so the venv built
# against builder's libpython matches runtime's. Renovate's docker manager
# bumps every `python:X.Y-alpine@sha256:...` reference in a single PR.
FROM python:3.14-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72 AS runtime

LABEL org.opencontainers.image.title="dump1090exporter" \
      org.opencontainers.image.description="Prometheus metrics exporter for the dump1090 Mode S decoder." \
      org.opencontainers.image.source="https://github.com/schubydoo/dump1090-exporter" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.authors="Schuby <schubydoo@users.noreply.github.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

# Non-root user; UID/GID 1000 is stable so bind-mounted volume permissions
# are predictable on hosts that map UIDs 1:1 (e.g. balena devices).
RUN addgroup -S -g 1000 d1090exp \
    && adduser -S -u 1000 -G d1090exp -H -h /app -s /sbin/nologin d1090exp

WORKDIR /app

COPY --from=builder --chown=d1090exp:d1090exp /app/.venv /app/.venv

USER d1090exp

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:9105/metrics', timeout=3).status == 200 else 1)" \
        || exit 1

ENTRYPOINT ["python", "-m", "dump1090exporter"]
CMD ["--help"]
