---
type: skill
status: active
tags: [setup, standalone, tooling]
---

# Skill - Set Up Standalone MaxOS

Prepare a local clone to run without the MaxOS app. Hosted runs do not use
this skill: their containers already provide the baseline toolchain and allow
missing tools to be installed inside the runner.

## Trigger

- The owner has cloned Max OS to their own computer.
- A standalone agent reports missing setup or tool dependencies.

## Steps

1. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`. It installs the
   pre-commit quality gate and writes `.maxos/local_setup_status.yaml`; stop
   and fix any `ready: false` blocker.
2. Run `python3 AUTOMATE/Skills/tools/check_dependencies.py` and install only
   dependencies required by the intended skills.
3. Start the AI tool in the workspace root. Codex reads `AGENTS.md`; Claude
   reads `CLAUDE.md`; Gemini reads `.gemini/GEMINI.md`; Copilot reads
   `.github/copilot-instructions.md`.

## Baseline

The baseline is Git, Python 3.10 or later, and a POSIX shell. Optional skills
declare their own dependencies. `check_dependencies.py` is the executable
source of truth and prints the appropriate install command for each gap.

## Quality checks

- [ ] `.maxos/local_setup_status.yaml` reports `ready: true`.
- [ ] The intended skill's declared dependencies pass the dependency check.
- [ ] The pre-commit hook runs the Max OS quality gate.
