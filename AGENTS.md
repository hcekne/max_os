# Agents

This workspace is **Max OS** — a plain-Markdown operating system for work. This file is the canonical entry-point for any AI agent (tool-neutral).

Max OS is **owner-neutral**: you may be operating **on behalf of** a human owner or **as** a pure-AI owner. Read `00_System/Actor Profile.md` first to learn which — in `human` mode the system is a cooperation between a human mind and an LLM (the human decides); in `ai` mode you are the principal and the vault is your persistent memory.

## Bootstrap (read in order)
1. Run `sh 15_Skills/tools/ensure_local_setup.sh` — verify clone-local setup and hooks.
2. `00_System/Actor Profile.md` — owner type and operating mode.
3. `00_System/LLM Operating Manual.md` — primary instruction set and algorithms.
4. `00_System/AI Actor & Memory Model.md` — how the vault works as your persistent memory.
5. `00_System/System State.md` — canonical review dates and active surfaces.
6. `00_System/Indexes.md` — folder and placement map.
7. `00_System/Session Log.md` — append a dated bullet at the end of the session.
8. `SKILLS.md` — manifest of agent-executable capabilities (read when the task needs one).
9. `14_Guides/Guide - MaxOS Online Scope and Shared Resources.md` — read when
   the session includes organization projects, shared skills, code repositories,
   or Workflow Builder automations.

Per-folder rules live in each numbered folder's `.instructions.md`.

## Core Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, commitments, or outcomes.
- Use `[[Note Name]]` wiki-links when referencing other notes.
- Treat `last_*_review_date` fields in `00_System/System State.md` as canonical truth.
- Route `10_Action_Center/Agent_Inbox/` items into canonical notes; keep active folders focused on current work.
- Move stale or superseded material into `16_Cleaning/` rather than deleting it.

## Validation
- Run `sh 15_Skills/tools/ensure_local_setup.sh` at session start. Missing or false `.maxos/local_setup_status.yaml` means setup is incomplete.
- Run `python3 15_Skills/tools/check_vault.py` to surface frontmatter, wiki-link, naming, hygiene, and system-state drift. Warn-only; exits 0.
- Run `python3 15_Skills/tools/maxos_quality_gate.py --root .` before commits or structural changes.
- The local Git hook in `.githooks/pre-commit` runs the quality gate before every commit once setup is installed.
- Do not commit runtime byproducts such as `__pycache__/` or `*.pyc`.

## System dependencies
Several skills need external software beyond Python's standard library (pandoc, WeasyPrint, Node + Playwright + Chromium, Pillow). Before running any skill from `SKILLS.md` on a new machine, read `14_Guides/Guide - System Dependencies.md` and run `python3 15_Skills/tools/check_dependencies.py` to verify the toolchain is in place. Do not silently degrade to a fallback path; install the missing dependency and re-run.

## External Agent Access Pattern
- Task sources: `10_Action_Center/Agent_Inbox/`, `08_Todos/`
- Reference data: `01_People/`, `02_Organizations/`, `03_Clients/`, `04_Projects/`
- Typical outputs: `07_Daily/`, `06_Interactions/`, `05_Content/`
- Owner-review delivery: `10_Action_Center/My_Inbox/`
- Externally ready delivery: `10_Action_Center/Outbox/`
- Only modify `00_System/System State.md` and `13_Goals/` when the corresponding review or action has actually been completed.

## MaxOS Online Scope Pattern
When running through MaxOS Online, the visible working context may include more
than this private workspace:

- the owner's personal Max OS workspace;
- organization projects shared with the owner;
- organization-level skills or instructions;
- code repositories explicitly added to chat/workflow scope.

Treat scope as an allowlist. If a folder or repository is not in scope, do not
assume it exists or try to reach it. Treat organization projects and code
repositories as shared/runtime resources, not as private workspace folders to
silently copy. For details, read
`14_Guides/Guide - MaxOS Online Scope and Shared Resources.md`.
