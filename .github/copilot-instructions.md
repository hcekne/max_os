# Max OS — Copilot Instructions

This workspace is **Max OS**, a personal operating system for knowledge workers built on plain Markdown.

## Bootstrap (read in order)
1. Run `sh 15_Skills/tools/ensure_local_setup.sh` — verify clone-local setup and hooks
2. `00_System/LLM Operating Manual.md` — full instruction set and algorithms
3. `00_System/System State.md` — current dates, active plans, and review checkpoints
4. `00_System/Indexes.md` — where each type of note belongs
5. `SKILLS.md` — agent-executable capabilities

## Key Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, or commitments.
- Treat `last_*_review_date` fields in System State as canonical truth.
- Use `[[Note Name]]` wiki-links when referencing other notes.
- Process `10_Inbox/` when asked or when items are pending.
- Prefer updating canonical files over creating endless new versions.
- Use lifecycle metadata for temporary, event-specific, draft, superseded, and generated files when useful.
- Archive superseded drafts after review; do not delete without explicit approval.
- Run `python3 15_Skills/tools/maxos_quality_gate.py --root .` before committing structural knowledge-system changes.
- Run `sh 15_Skills/tools/ensure_local_setup.sh` at session start; missing or false `.maxos/local_setup_status.yaml` means setup is incomplete.
- Use `python3 15_Skills/tools/maxos_quality_gate.py --root . --full --public-template` before public-template commits or pull requests.
- Do not commit runtime byproducts such as `__pycache__/` or `*.pyc`.
- Do not push public repo changes without explicit approval.

## Generated Artifacts
- Markdown remains canonical truth for memory, notes, projects, goals, plans, workflows, skills, and system state.
- Store generated HTML artifacts in `05_Content/Artifacts/`.
- Store optional interactive worklets in `20_Modules/Worklets/`.
- Do not silently overwrite canonical Markdown based on generated HTML.
- Do not include secrets, tokens, credentials, hidden prompts, or private operational data in generated artifacts.

## Folder Overview
| Folder | Purpose |
|--------|---------|
| `00_System/` | AI operating rules and system state (read first) |
| `01_People/` | One note per person (`First Last.md`) |
| `02_Organizations/` | Company and org notes |
| `03_Clients/` | Client folders with `Client - Name.md` |
| `04_Projects/` | `Project - Name.md` |
| `05_Content/` | Written content (pillar + derivatives) |
| `05_Content/Artifacts/` | Generated HTML artifacts |
| `06_Interactions/` | Date-first interaction notes |
| `07_Daily/` | Daily notes |
| `08_Todos/` | Task backlog |
| `09_Planning/` | Weekly, Monthly, Quarterly, Two-Year plans |
| `10_Inbox/` | Raw captures, process daily |
| `11_Notes/` | General notes; archive superseded to `11_Notes/Archive/` |
| `12_Workflows/` | Repeatable human-led processes |
| `13_Goals/` | One note per major goal |
| `14_Guides/` | Setup and usage guides |
| `15_Skills/` | Agent-executable capabilities |
| `20_Modules/` | Optional capability packs (disabled by default) |
| `20_Modules/Worklets/` | Optional HTML worklets |
| `99_Templates/` | Templates for new notes |
