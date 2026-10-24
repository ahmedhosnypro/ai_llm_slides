#!/usr/bin/env bash
# Commit every local change in a repo with a random message.
# Usage: scripts/commit_all.sh [repo-path]   (defaults to current directory)
set -euo pipefail

REPO="${1:-$PWD}"
cd "$REPO"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "not a git repo: $REPO" >&2
  exit 1
fi

git add -A

if git diff --cached --quiet; then
  echo "nothing to commit in $REPO"
  exit 0
fi

WORDS=(routine checkpoint snapshot wip save bank batch wave lane fleet)
msg="${WORDS[RANDOM % ${#WORDS[@]}]} $RANDOM"
git commit --quiet -m "$msg"
echo "$REPO: $msg"
