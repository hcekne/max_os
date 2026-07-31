#!/usr/bin/env sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

echo "Installed Max OS Git hooks via core.hooksPath=.githooks"
echo "The pre-commit hook now runs before each git commit in this clone."
