# Agents

This workspace is **Max OS** — a plain-Markdown operating system for work. This file is the canonical entry-point for any AI agent (tool-neutral).

Max OS is **owner-neutral**: you may be operating **on behalf of** a human owner or **as** a pure-AI owner. Read `SYSTEM/Actor Profile.md` first to learn which — in `human` mode the system is a cooperation between a human mind and an LLM (the human decides); in `ai` mode you are the principal and the vault is your persistent memory.

## Bootstrap (read in order)
1. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` — verify clone-local setup and hooks.
2. `SYSTEM/Actor Profile.md` — owner type and operating mode.
3. `SYSTEM/LLM Operating Manual.md` — primary instruction set and algorithms.
4. `SYSTEM/AI Actor & Memory Model.md` — how the vault works as your persistent memory.
5. `SYSTEM/System State.md` — canonical review dates and active surfaces.
6. `SYSTEM/Indexes.md` — folder and placement map.
7. `SYSTEM/Session Log.md` — append a dated bullet at the end of the session.
8. `SKILLS.md` — manifest of agent-executable capabilities (read when the task needs one).
9. `SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources.md` — read when
   the session includes organization projects, shared skills, code repositories,
   or Workflow Builder automations.

Per-folder rules live in each workspace folder's `.instructions.md`.

## Core Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, commitments, or outcomes.
- Use `[[Note Name]]` wiki-links when referencing other notes.
- Treat `last_*_review_date` fields in `SYSTEM/System State.md` as canonical truth.
- Route `ACTION CENTER/Agent Inbox/` items into canonical notes; keep active folders focused on current work.
- Move stale or superseded material into `SYSTEM/Cleaning/` rather than deleting it.

## Validation
- Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` at session start. Missing or false `.maxos/local_setup_status.yaml` means setup is incomplete.
- Run `python3 AUTOMATE/Skills/tools/check_vault.py` to surface frontmatter, wiki-link, naming, hygiene, and system-state drift. Warn-only; exits 0.
- Run `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` before commits or structural changes.
- The local Git hook in `.githooks/pre-commit` runs the quality gate before every commit once setup is installed.
- Do not commit runtime byproducts such as `__pycache__/` or `*.pyc`.

## System dependencies
Several skills need external software beyond Python's standard library (pandoc, WeasyPrint, Node + Playwright + Chromium, Pillow). Before running any skill from `SKILLS.md` on a new machine, read `SYSTEM/Guides/Guide - System Dependencies.md` and run `python3 AUTOMATE/Skills/tools/check_dependencies.py` to verify the toolchain is in place. Do not silently degrade to a fallback path; install the missing dependency and re-run.

## External Agent Access Pattern
- Task sources: `ACTION CENTER/Agent Inbox/`, `PLAN/Todos/`
- Reference data: `KNOWLEDGE/People/`, `KNOWLEDGE/Organizations/`, `KNOWLEDGE/Clients/`, `KNOWLEDGE/Projects/`
- Typical outputs: `PLAN/Daily/`, `KNOWLEDGE/Interactions/`, `KNOWLEDGE/Content/`
- Owner-review delivery: `ACTION CENTER/My Inbox/`
- Externally ready delivery: `ACTION CENTER/Outbox/`
- Only modify `SYSTEM/System State.md` and `PLAN/Goals/` when the corresponding review or action has actually been completed.

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
`SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources.md`.

<!-- maxos-workspace-v2:start -->
## MaxOS workspace layout

Use the physical folder names exactly as written below when reading, writing,
linking, or telling the user where a file lives:

- `ACTION CENTER/My Inbox`: results and updates for the user to review.
- `ACTION CENTER/Agent Inbox`: new files and requests for MaxOS to process.
- `ACTION CENTER/Outbox`: finished items ready to download, share, or send.
- `KNOWLEDGE`: long-lived knowledge, including People, Organizations, Clients,
  Projects, Content, Interactions, Notes, and custom user folders.
- `PLAN`: Daily notes, Todos, Goals, Weekly, Quarterly, Reviews, and Two-Year plans.
- `AUTOMATE`: Workflows, Skills, and Modules.
- `SYSTEM`: operating instructions, Guides, Cleaning, Templates, and Storage References.

Do not invent or display retired numbered folder names. Root technical folders,
Git metadata, provider configuration, and `code/` remain at the workspace root.
<!-- maxos-workspace-v2:end -->
