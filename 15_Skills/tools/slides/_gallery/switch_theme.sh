#!/usr/bin/env bash
# Copy the chosen theme variant into theme.css so the build script picks it up.
# Usage: ./switch_theme.sh default | dmg | <other>
set -euo pipefail

cd "$(dirname "$0")"

choice="${1:-default}"
src="theme-${choice}.css"

if [[ ! -f "$src" ]]; then
  echo "No such theme: $src" >&2
  echo "Available:" >&2
  ls theme-*.css 2>/dev/null | sed 's/^/  /' >&2
  exit 1
fi

cp "$src" theme.css
echo "Active theme: $choice ($src -> theme.css)"
