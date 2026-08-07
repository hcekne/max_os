---
type: guide
status: active
---

# Standalone

Running this workspace WITHOUT the MaxOS app: a local clone driven by your
own agent — Claude Code, Codex CLI, VS Code chat, or any tool that reads
`AGENTS.md`. In hosted MaxOS runs none of this file applies: run containers
ship with the toolchain preinstalled, and missing tools can be installed on
the spot (`apt-get` / `pip` as root inside the container).

## Setup, once per clone

1. `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` — installs the
   pre-commit quality gate and writes `.maxos/local_setup_status.yaml`. Safe
   to re-run; `ready: false` means stop and fix the reported blocker.
2. `python3 AUTOMATE/Skills/tools/check_dependencies.py` — one-shot report
   of which external tools are present, with the install command for each
   gap.
3. Start your agent in the workspace folder. Claude Code finds `CLAUDE.md`,
   Copilot finds `.github/copilot-instructions.md`, Codex and most other
   tools read `AGENTS.md` directly — no startup prompt is needed.

## External dependencies

The baseline is `git`, `python3` ≥ 3.10, and a POSIX shell. Everything else
is skill-dependent:

| Needed by | Dependency | Install (macOS / Debian) |
| --- | --- | --- |
| Slide deck generation | `pandoc` | `brew install pandoc` / `apt-get install pandoc` |
| Deck logo safety check | `pillow` | `pip3 install pillow` |
| Deck visual QA (mandatory for the slide skill) | `node` ≥ 18 + Playwright + Chromium, installed workspace-local at `.maxos/visual-check/` | `brew install node` then `cd .maxos/visual-check && npm init -y && npm install playwright && npx playwright install chromium` |
| PDF rendering | `weasyprint` (+ `pandoc`) | `brew install weasyprint` / `apt-get install weasyprint` |

Word export (`md_to_docx.py`), knowledge lint, the quality gate, and the
vault validator are Python-stdlib-only and need nothing.

`check_dependencies.py` is the source of truth for what is verified. When a
new skill introduces a system dependency: add the check there, add a row
here, and note it in the skill card's `## Dependencies` section.
