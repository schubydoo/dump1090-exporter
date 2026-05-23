#!/usr/bin/env bash
# Refresh the per-arch UV_SHA256_* ARGs in the Dockerfile to match the
# version currently pinned in `ARG UV_VERSION=...`. Run this after Renovate
# (or you) bumps UV_VERSION so the sha256-verify step in the Docker build
# stays valid.
#
# Why this exists: Renovate's PyPI manager bumps UV_VERSION fine, but it
# doesn't know about our three companion SHA ARGs. Until we have a custom
# datasource or postUpgradeTasks support, this is a one-command refresh.
#
# Usage:
#   tools/update-uv-shas.sh             # update ./Dockerfile in place
#   tools/update-uv-shas.sh path/to/Dockerfile
#
# Requires: bash, curl, jq, sed.

set -euo pipefail

dockerfile="${1:-Dockerfile}"

if [ ! -f "$dockerfile" ]; then
    echo "error: $dockerfile not found" >&2
    exit 1
fi

version=$(grep -E '^ARG UV_VERSION=' "$dockerfile" | head -1 | cut -d= -f2)
if [ -z "$version" ]; then
    echo "error: could not find 'ARG UV_VERSION=' in $dockerfile" >&2
    exit 1
fi

echo "refreshing uv SHA256 ARGs for version $version"

manifest_url="https://github.com/astral-sh/uv/releases/download/${version}/dist-manifest.json"
manifest=$(curl -fsSL "$manifest_url")

for target in x86_64-unknown-linux-musl aarch64-unknown-linux-musl armv7-unknown-linux-musleabihf; do
    sha=$(echo "$manifest" | jq -r --arg t "uv-${target}.tar.gz" '.artifacts[$t].checksums.sha256')
    if [ -z "$sha" ] || [ "$sha" = "null" ]; then
        echo "error: no sha256 for ${target} in ${manifest_url}" >&2
        exit 1
    fi
    case "$target" in
        x86_64-unknown-linux-musl) arg=UV_SHA256_AMD64 ;;
        aarch64-unknown-linux-musl) arg=UV_SHA256_ARM64 ;;
        armv7-unknown-linux-musleabihf) arg=UV_SHA256_ARMV7 ;;
    esac
    echo "  ${arg}=${sha}"
    # GNU sed and BSD sed differ on -i; use a temp file to be portable.
    sed "s|^ARG ${arg}=.*|ARG ${arg}=${sha}|" "$dockerfile" > "${dockerfile}.tmp"
    mv "${dockerfile}.tmp" "$dockerfile"
done

echo "done."
