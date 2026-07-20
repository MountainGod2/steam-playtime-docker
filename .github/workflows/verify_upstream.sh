#!/usr/bin/env bash

set -euo pipefail

if [[ "$#" -ne 2 || -z "$1" || -z "$2" ]]; then
    printf '%s\n' "::error::Unable to determine upstream branch name!" >&2
    exit 1
fi

remote_name="$1"
branch_name="$2"
upstream_branch="$remote_name/$branch_name"

git fetch "$remote_name"

if ! upstream_sha="$(git rev-parse "$upstream_branch")"; then
    printf '%s\n' "::error::Unable to determine upstream branch name!" >&2
    exit 1
fi

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
