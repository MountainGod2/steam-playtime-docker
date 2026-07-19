#!/usr/bin/env bash

set -euo pipefail

if ! upstream_branch="$(
    git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
)"; then
    printf '%s\n' "::error::Unable to determine upstream branch name!" >&2
    exit 1
fi

remote_name="${upstream_branch%%/*}"

git fetch "$remote_name"

upstream_sha="$(git rev-parse "$upstream_branch")"
head_sha="$(git rev-parse HEAD)"

if [[ "$head_sha" != "$upstream_sha" ]]; then
    printf '%s\n' \
        "[HEAD SHA] $head_sha != $upstream_sha [UPSTREAM SHA]" >&2
    printf '%s\n' \
        "::error::Upstream has changed, aborting release..." >&2
    exit 1
fi

printf '%s\n' \
    "Verified upstream branch has not changed, continuing with release..."
