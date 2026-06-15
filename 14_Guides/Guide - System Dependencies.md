---
type: guide
date: 2026-05-19
status: active
tags: [guide, setup, dependencies, tooling, agent-reference]
---

# Guide - System Dependencies

What software the system needs installed for every Max OS skill and tool to run cleanly. Read this guide before running any of the skills listed in `SKILLS.md` for the first time on a new machine.

This guide is **mandatory reading for any agent (human or AI)** working in this repo on a fresh clone or a system where the tools have not been verified. Skipping it leads to silent failure modes: scripts that fall back to degraded behaviour, visual QA that reports green without actually rendering, and PDFs that look right in HTML but fail to export.

---

## TL;DR — what to install on a fresh macOS clone

```bash
# Baseline (must have)
brew install python@3 node pandoc weasyprint
python3 -m pip install --user --break-system-packages pillow

# Visual QA for slide decks (installs Playwright into the workspace)
cd "$(git rev-parse --show-toplevel)" && mkdir -p .maxos/visual-check && cd .maxos/visual-check
npm init -y && npm install playwright
npx playwright install chromium

# Verify everything is wired
sh "$(git rev-parse --show-toplevel)/15_Skills/tools/ensure_local_setup.sh"
python3 "$(git rev-parse --show-toplevel)/15_Skills/tools/check_dependencies.py"
```

If `check_dependencies.py` reports everything OK, the agent can run any skill in this repo without falling back to a degraded path.

---

## Mandatory baseline (always required)

These must be on `$PATH` for the system to function at all.

| Dependency | macOS install | Used by |
| --- | --- | --- |
| `git` | Pre-installed on macOS (Xcode CLT) | Everything; the repo is git-tracked. |
| `python3` ≥ 3.10 | `brew install python@3` | Every Python tool in `15_Skills/tools/`. |
| `bash` / `sh` | Pre-installed | The setup and install scripts. |

Quality-gate-side baseline:

| Dependency | Notes |
| --- | --- |
| Pre-commit hooks | Run `sh 15_Skills/tools/ensure_local_setup.sh` once after cloning. Writes `.maxos/local_setup_status.yaml` and registers `.githooks` as the hooks path so the knowledge-lint and whitespace gate run before each commit. |

---

## Skill / tool dependency matrix

| Skill or tool | External dependency | Install command | Failure mode if missing |
| --- | --- | --- | --- |
| **Slide deck generation** (`Skill - Slide Deck Generation`, `15_Skills/tools/slides/build_deck.py`) | `pandoc` | `brew install pandoc` | Falls back to the inline Markdown subset parser. Most slides still render, but features like advanced tables and pipe-table-with-formatting can degrade. Visually inspect every slide. |
| **Slide deck logo safety check** (`build_deck.py` pre-build pass) | `pillow` (Python) | `pip3 install --user --break-system-packages pillow` (or `brew install pillow`) | Logo-vs-slide-background mismatch warnings are silently skipped. A white-bg logo on a dark slide (or vice versa) will ship without warning. |
| **Slide deck visual QA** (`15_Skills/tools/slides/check_deck_visual.mjs`) | `node` ≥ 18, `playwright` ≥ 1.40 with the Chromium browser | `brew install node` then `cd .maxos/visual-check && npm install playwright && npx playwright install chromium` | The visual QA cannot run. Without it, the agent has no way to verify the rendered slides before reporting completion. **This is a hard requirement for the slide-deck skill**, not an optional extra. |
| **Memo pack build** (`04_Projects/DMG Media Lead/.../build_pack.py`) | `pandoc`, `weasyprint` | `brew install pandoc weasyprint` | Pack HTML and PDF cannot be regenerated. The previously generated `99_full_pack.pdf` remains on disk but stale. |
| **Interview-guide PDF rendering** (the ad-hoc `pandoc \| weasyprint` chain used in `04_Projects/DMG Media Lead/interviews/interview pdf/`) | `pandoc`, `weasyprint` | `brew install pandoc weasyprint` | Cannot rebuild interview-prep PDFs. |
| **Word document export** (`Skill - Export Markdown to Word Document`, `15_Skills/tools/md_to_docx.py`) | Python standard library only — writes the DOCX OOXML directly. No `python-docx` install needed. | — | None. Self-contained. |
| **Vault validator** (`15_Skills/tools/check_vault.py`) | Python standard library only | — | None. |
| **Knowledge lint and quality gate** (`15_Skills/tools/maxos_quality_gate.py`, `knowledge_lint.py`) | Python standard library only | — | None. Hook fails commit if quality gate detects issues. |

---

## What the workspace assumes installed where

The skills assume tools live at the following paths. If your install is different, update the matrix above for your machine.

| Tool | Expected path on macOS (Homebrew) |
| --- | --- |
| `python3` | `/opt/homebrew/bin/python3` |
| `pandoc` | `/opt/homebrew/bin/pandoc` |
| `weasyprint` | `/opt/homebrew/bin/weasyprint` |
| `node` | `/opt/homebrew/bin/node` |
| `npm` | `/opt/homebrew/bin/npm` |
| Playwright (workspace-local) | `<repo>/.maxos/visual-check/node_modules/playwright/` |
| Chromium for Playwright | `~/Library/Caches/ms-playwright/chromium_headless_shell-*` (downloaded by `npx playwright install chromium`) |

---

## Per-skill quick guide for agents

When an agent picks up a skill to run, it should also verify the dependencies that skill needs.

### Slide Deck Generation

Before building or modifying any deck:

1. Verify `pandoc` is on `$PATH`. If not, the inline fallback parser kicks in silently.
2. Verify `pillow` imports. If not, run `python3 -c "from PIL import Image"`; install via `pip3 install --user --break-system-packages pillow` if missing.
3. Verify Playwright is installed at `.maxos/visual-check/node_modules/playwright/`. If not, install per TL;DR.
4. Verify Chromium is installed for Playwright: `node -e "import('playwright').then(p => console.log('OK'))"` should print `OK` without errors.

After building a deck, **always** run `node 15_Skills/tools/slides/check_deck_visual.mjs <deck.html>` and **read every screenshot as image bytes**, not just the report JSON. See `Skill - Slide Deck Generation.md` for the mandatory visual QA flow.

### Memo Pack Build (DMG project)

The memo pack builder lives inside the DMG project and is non-portable today. It needs `pandoc` and `weasyprint`. The pack builds end-to-end with `python3 04_Projects/DMG Media Lead/interim_cdo_mandate_refactor/v4_clause_3_1_ordered_pack/build_pack.py`.

### Interview-Guide PDF Render

Used ad-hoc when interview prep needs a PDF for sharing or printing. The pipeline:

```bash
pandoc <guide.md> -f markdown+pipe_tables+smart -t html5 --standalone --css /tmp/interview_guide.css -o /tmp/guide.html
weasyprint /tmp/guide.html "<output>.pdf"
```

Stylesheet pattern in `04_Projects/DMG Media Lead/interviews/` (the `interview pdf/` folder).

### Word Document Export

Self-contained — Python stdlib only. Run via `python3 15_Skills/tools/md_to_docx.py <source.md> [--output <dest.docx>]` per the skill card.

---

## Verification script

`15_Skills/tools/check_dependencies.py` prints a one-shot report on which dependencies are available and which are missing, with the install command for each gap.

```bash
python3 15_Skills/tools/check_dependencies.py
```

Run this on every new machine and any time a tool stops working unexpectedly.

---

## Updating this guide

When you add a new skill or tool that introduces a new system dependency:

1. Add a row to the **Skill / tool dependency matrix** above.
2. Add a per-skill section under **Per-skill quick guide for agents** if the dependency has setup nuance.
3. Add the dependency check to `15_Skills/tools/check_dependencies.py`.
4. Mention the dependency in the skill's own `Skill - <Name>.md` card under a `## Dependencies` section.

The guide is the single source of truth. Per-skill cards should reference it, not duplicate it.
