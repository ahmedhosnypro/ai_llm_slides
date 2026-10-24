#!/usr/bin/env bash
# Commit every local change in a repo with a random message, then push.
# Usage: scripts/commit_all.sh [repo-path] [remote] [branch]   (defaults: cwd / origin / current branch)
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

REMOTE="${2:-origin}"
BRANCH="${3:-$(git rev-parse --abbrev-ref HEAD)}"
if git push --quiet "$REMOTE" "$BRANCH" 2>/dev/null; then
  echo "$REPO: pushed to $REMOTE/$BRANCH"
else
  echo "$REPO: WARNING push to $REMOTE/$BRANCH failed (commit kept locally)" >&2
fi
