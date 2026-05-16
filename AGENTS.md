# Agents

This workspace is **Max OS** — a personal operating system for knowledge workers built on plain Markdown. AI agents operating here should follow the instructions below.

## Quick Start
1. Read `00_System/LLM Operating Manual.md` for full algorithms and rules.
2. Read `00_System/System State.md` for current dates and active plans.
3. Read `SKILLS.md` for a manifest of executable capabilities.

## Vault Structure

| Folder | Purpose | Key Pattern |
|--------|---------|-------------|
| `00_System/` | AI operating rules and system state | Read first every session |
| `01_People/` | One note per person | `First Last.md` |
| `02_Organizations/` | Company and org notes | `Org Name.md` |
| `03_Clients/` | Client folders | `Client - Name.md` in each folder |
| `04_Projects/` | Active projects | `Project - Name.md` |
| `05_Content/` | Written content | Pillar + derivative model |
| `05_Content/Artifacts/` | Generated HTML artifacts | Source-linked, non-canonical |
| `06_Interactions/` | Meeting/call/event notes | Date-first filenames |
| `07_Daily/` | Daily notes | `YYYY-MM-DD.md` |
| `08_Todos/` | Task backlog | Markdown tasks with due dates |
| `09_Planning/` | Plans by cadence | `Weekly/`, `Monthly/`, `Quarterly/`, `Two-Year/` |
| `10_Inbox/` | Raw captures | Process daily, route to canonical locations |
| `11_Notes/` | General notes | Archive superseded to `11_Notes/Archive/` |
| `12_Workflows/` | Human-led repeatable processes | Step-by-step with quality checks |
| `13_Goals/` | Major goals | One note per goal |
| `14_Guides/` | Setup and usage guides | For human onboarding |
| `15_Skills/` | Agent-executable capabilities | Structured skill cards |
| `20_Modules/` | Optional capability packs | Disabled by default |
| `20_Modules/Worklets/` | Optional HTML worklets | Interactive, non-canonical |
| `99_Templates/` | Templates for new notes | Used by Inbox Processing and skills |

## Operational Loops

### Session Start
Follow the Session Start Algorithm in `00_System/LLM Operating Manual.md`:
1. Read System State → resolve date → check recurring triggers
2. Compute due reviews → run them in order (yearly > quarterly > monthly > weekly)
3. Process inbox if items pending
4. Align daily plan with active goals
5. Propose next 1–3 concrete actions

### Inbox Processing
Route items from `10_Inbox/` to canonical note locations. Create missing notes from templates in `99_Templates/`. Extract tasks to `08_Todos/` or today's daily note. Cross-link everything.

### Interaction Processing
When given an interaction note: ensure all mentioned people/orgs/clients have notes, update them with key facts and dates, return a changelog.

### Review Cadence
Reviews are driven by `last_*_review_date` fields in System State. Cadence rules are in `00_System/Planning Cadence.md`. Never skip ahead — run each due review in order.

## Access Patterns for External Agents

If you are an external agent (e.g., OpenClaw, custom bot) with partial access:

- **Read first:** `00_System/`, `SKILLS.md`, `AGENTS.md`
- **Task sources:** `08_Todos/` and `10_Inbox/` for pending work
- **Reference data:** `01_People/`, `02_Organizations/`, `03_Clients/`, `04_Projects/`
- **Output locations:** `07_Daily/`, `06_Interactions/`, `05_Content/`
- **Modify with care:** `00_System/System State.md`, `13_Goals/` — only update after completing the corresponding review or action

## HTML Artifacts and Worklets

Max OS follows the principle: Markdown memory. HTML worklets. JSON state. Git history. Harness runtime.

- Markdown remains canonical truth for memory, notes, people, projects, goals, plans, daily notes, interactions, workflows, skills, and system state.
- HTML can be generated for rich visual artifacts and optional interactive worklets.
- Store static HTML artifacts in `05_Content/Artifacts/`.
- Store interactive HTML worklets in `20_Modules/Worklets/`.
- Do not silently overwrite canonical Markdown based on generated HTML.
- HTML artifacts should include metadata identifying source files, generated date, generator, and approval status.
- Treat generated HTML as untrusted until reviewed.
- Do not include secrets, tokens, credentials, hidden prompts, or private operational data in HTML.
- Prefer self-contained HTML for portable artifacts.
- Use sandboxed rendering when HTML is viewed in a harness.
- Use JSON for structured runtime state; do not use HTML as the state source of truth.
- Keep edits minimal, factual, linked, and reversible.

## Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, commitments, or outcomes.
- Use `[[Note Name]]` wiki-links.
- Treat `last_*_review_date` fields as canonical truth.
- One canonical note per strategy topic; archive redundant variants.
