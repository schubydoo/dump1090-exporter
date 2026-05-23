# syntax=docker/dockerfile:1.7

# Pinned uv release used to install the project into a virtualenv. Renovate
# tracks this via the `ghcr.io/astral-sh/uv` Dockerfile manager.
ARG UV_VERSION=0.11.14
ARG PYTHON_VERSION=3.13

# --------------------------------------------------------------------------
# 1. builder — install the project + its locked deps into a venv at /app/.venv
# --------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM python:${PYTHON_VERSION}-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1

# uv is a single static binary; copy it from the official uv image.
COPY --from=uv /uv /usr/local/bin/uv

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
# 2. runtime — slim final image with just Python + the prebuilt venv
# --------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ARG PYTHON_VERSION

LABEL org.opencontainers.image.title="dump1090exporter" \
      org.opencontainers.image.description="Prometheus metrics exporter for the dump1090 Mode S decoder." \
      org.opencontainers.image.source="https://github.com/schubydoo/dump1090-exporter" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.authors="Schuby <schubydoo@users.noreply.github.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

# Non-root user; UID/GID are stable so volume permissions are predictable.
RUN groupadd --system --gid 1000 d1090exp \
    && useradd --system --uid 1000 --gid d1090exp --shell /usr/sbin/nologin d1090exp

WORKDIR /app

COPY --from=builder --chown=d1090exp:d1090exp /app/.venv /app/.venv

USER d1090exp

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:9105/metrics', timeout=3).status == 200 else 1)" \
        || exit 1

ENTRYPOINT ["python", "-m", "dump1090exporter"]
CMD ["--help"]
