#!/usr/bin/env sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STATUS_DIR=".maxos"
STATUS_FILE="$STATUS_DIR/local_setup_status.yaml"
HOOK_FILE=".githooks/pre-commit"
INSTALL_SCRIPT="AUTOMATE/Skills/tools/install_git_hooks.sh"
SETUP_SCRIPT="AUTOMATE/Skills/tools/ensure_local_setup.sh"
QUALITY_GATE_SCRIPT="AUTOMATE/Skills/tools/maxos_quality_gate.py"
KNOWLEDGE_LINT_SCRIPT="AUTOMATE/Skills/tools/knowledge_lint.py"
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
hook_file_executable: $([ -x "$HOOK_FILE" ] && printf true || printf false)
install_script_executable: $([ -x "$INSTALL_SCRIPT" ] && printf true || printf false)
setup_script_executable: $([ -x "$SETUP_SCRIPT" ] && printf true || printf false)
python3_available: $([ -n "$python_path" ] && printf true || printf false)
python3_path: "$python_path"
quality_gate_available: $([ -f "$QUALITY_GATE_SCRIPT" ] && printf true || printf false)
knowledge_lint_available: $([ -f "$KNOWLEDGE_LINT_SCRIPT" ] && printf true || printf false)
install_command: "sh $INSTALL_SCRIPT"
quality_gate_command: "python3 $QUALITY_GATE_SCRIPT --root ."
EOF
}

if ! command -v python3 >/dev/null 2>&1; then
  write_status false "python3 is required for Max OS quality gates"
  echo "Max OS local setup failed: python3 is required." >&2
  exit 1
fi

if [ ! -f "$HOOK_FILE" ]; then
  write_status false "$HOOK_FILE is missing"
  echo "Max OS local setup failed: $HOOK_FILE is missing." >&2
  exit 1
fi

if [ ! -f "$INSTALL_SCRIPT" ]; then
  write_status false "$INSTALL_SCRIPT is missing"
  echo "Max OS local setup failed: $INSTALL_SCRIPT is missing." >&2
  exit 1
fi

if [ ! -f "$QUALITY_GATE_SCRIPT" ]; then
  write_status false "quality gate script is missing"
  echo "Max OS local setup failed: quality gate script is missing." >&2
  exit 1
fi

if [ ! -f "$KNOWLEDGE_LINT_SCRIPT" ]; then
  write_status false "knowledge lint script is missing"
  echo "Max OS local setup failed: knowledge lint script is missing." >&2
  exit 1
fi

chmod +x "$HOOK_FILE" "$INSTALL_SCRIPT" "$SETUP_SCRIPT"

current_hooks_path="$(git config --get core.hooksPath || true)"
if [ "$current_hooks_path" != ".githooks" ] || [ ! -x "$HOOK_FILE" ]; then
  sh "$INSTALL_SCRIPT" >/dev/null
fi

current_hooks_path="$(git config --get core.hooksPath || true)"
if [ "$current_hooks_path" != ".githooks" ] || [ ! -x "$HOOK_FILE" ]; then
  write_status false "git hooks are not installed correctly"
  echo "Max OS local setup failed: git hooks are not installed correctly." >&2
  exit 1
fi

write_status true "local setup ready"
echo "Max OS local setup ready."
echo "Status: $STATUS_FILE"
