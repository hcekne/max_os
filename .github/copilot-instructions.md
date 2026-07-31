# Max OS — Copilot Instructions

This workspace is **Max OS**, a personal operating system for knowledge workers built on plain Markdown.

## Bootstrap (read in order)
1. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` — verify clone-local setup and hooks
2. `SYSTEM/LLM Operating Manual.md` — full instruction set and algorithms
3. `SYSTEM/System State.md` — current dates, active plans, and review checkpoints
4. `SYSTEM/Indexes.md` — where each type of note belongs
5. `SKILLS.md` — agent-executable capabilities

## Key Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, or commitments.
- Treat `last_*_review_date` fields in System State as canonical truth.
- Use `[[Note Name]]` wiki-links when referencing other notes.
- Process `ACTION CENTER/Agent Inbox/` when asked or when items are pending.
- Prefer updating canonical files over creating endless new versions.
- Use lifecycle metadata for temporary, event-specific, draft, superseded, and generated files when useful.
- Archive superseded drafts after review; do not delete without explicit approval.
- Run `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` before committing structural knowledge-system changes.
- Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` at session start; missing or false `.maxos/local_setup_status.yaml` means setup is incomplete.
- Use `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root . --full --public-template` before public-template commits or pull requests.
- Do not commit runtime byproducts such as `__pycache__/` or `*.pyc`.
- Do not push public repo changes without explicit approval.

## Generated Artifacts
- Markdown remains canonical truth for memory, notes, projects, goals, plans, workflows, skills, and system state.
- Store generated HTML artifacts in `KNOWLEDGE/Content/Artifacts/`.
- Store optional interactive worklets in `AUTOMATE/Modules/Worklets/`.
- Do not silently overwrite canonical Markdown based on generated HTML.
- Do not include secrets, tokens, credentials, hidden prompts, or private operational data in generated artifacts.

## Folder Overview
| Folder | Purpose |
|--------|---------|
| `SYSTEM/` | AI operating rules and system state (read first) |
| `KNOWLEDGE/People/` | One note per person (`First Last.md`) |
| `KNOWLEDGE/Organizations/` | Company and org notes |
| `KNOWLEDGE/Clients/` | Client folders with `Client - Name.md` |
| `KNOWLEDGE/Projects/` | `Project - Name.md` |
| `KNOWLEDGE/Content/` | Written content (pillar + derivatives) |
| `KNOWLEDGE/Content/Artifacts/` | Generated HTML artifacts |
| `KNOWLEDGE/Interactions/` | Date-first interaction notes |
| `PLAN/Daily/` | Daily notes |
| `PLAN/Todos/` | Task backlog |
| `PLAN/` | Weekly, Monthly, Quarterly, Two-Year plans |
| `ACTION CENTER/` | My Inbox, Agent Inbox, and externally ready Outbox |
| `KNOWLEDGE/Notes/` | General notes; archive superseded to `KNOWLEDGE/Notes/Archive/` |
| `AUTOMATE/Workflows/` | Repeatable human-led processes |
| `PLAN/Goals/` | One note per major goal |
| `SYSTEM/Guides/` | Setup and usage guides |
| `AUTOMATE/Skills/` | Agent-executable capabilities |
| `AUTOMATE/Modules/` | Optional capability packs (disabled by default) |
| `AUTOMATE/Modules/Worklets/` | Optional HTML worklets |
| `SYSTEM/Templates/` | Templates for new notes |
