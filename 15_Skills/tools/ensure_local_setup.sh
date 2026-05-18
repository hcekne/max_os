#!/usr/bin/env sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STATUS_DIR=".maxos"
STATUS_FILE="$STATUS_DIR/local_setup_status.yaml"
mkdir -p "$STATUS_DIR"

write_status() {
  ready="$1"
  message="$2"
  hooks_path="$(git config --get core.hooksPath || true)"
  python_path="$(command -v python3 || true)"
  checked_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  cat > "$STATUS_FILE" <<EOF
version: 1
ready: $ready
checked_at: "$checked_at"
message: "$message"
git_repo: true
hooks_path_configured: $([ "$hooks_path" = ".githooks" ] && printf true || printf false)
hooks_path: "$hooks_path"
hook_file_executable: $([ -x ".githooks/pre-commit" ] && printf true || printf false)
python3_available: $([ -n "$python_path" ] && printf true || printf false)
python3_path: "$python_path"
quality_gate_available: $([ -f "15_Skills/tools/maxos_quality_gate.py" ] && printf true || printf false)
install_command: "sh 15_Skills/tools/install_git_hooks.sh"
quality_gate_command: "python3 15_Skills/tools/maxos_quality_gate.py --root ."
EOF
}

if ! command -v python3 >/dev/null 2>&1; then
  write_status false "python3 is required for Max OS quality gates"
  echo "Max OS local setup failed: python3 is required." >&2
  exit 1
fi

if [ ! -f ".githooks/pre-commit" ]; then
  write_status false ".githooks/pre-commit is missing"
  echo "Max OS local setup failed: .githooks/pre-commit is missing." >&2
  exit 1
fi

if [ ! -f "15_Skills/tools/maxos_quality_gate.py" ]; then
  write_status false "quality gate script is missing"
  echo "Max OS local setup failed: quality gate script is missing." >&2
  exit 1
fi

current_hooks_path="$(git config --get core.hooksPath || true)"
if [ "$current_hooks_path" != ".githooks" ] || [ ! -x ".githooks/pre-commit" ]; then
  sh 15_Skills/tools/install_git_hooks.sh >/dev/null
fi

write_status true "local setup ready"
echo "Max OS local setup ready."
echo "Status: $STATUS_FILE"
