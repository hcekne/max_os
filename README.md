# Max OS

Max OS is the system I use to run my work.

It plans across years, quarters, weeks, and days.
It remembers people, projects, and decisions.
It executes work as jobs.
It never changes truth without your approval.

Max OS is not just an assistant.
It is an operating system.

And it is yours to edit.
You can change the folders, templates, prompts, and rules at any time.
This repo is a starting point, not a cage.

If you can write text, you can run Max OS.

---

## Start in 60 seconds
1. Open this folder in your editor.
2. In a terminal, run:

```bash
sh 15_Skills/tools/ensure_local_setup.sh
```

3. Start chat with your AI tool.
4. Paste this prompt:

"Use this workspace as Max OS. Read `00_System/LLM Operating Manual.md`. Check `00_System/System State.md` and tell me what I should do today. Then process anything in `10_Inbox/` and give me my top 3 actions."

## Use with AI tools

Most AI tools auto-discover this workspace with zero setup:
- **VS Code Copilot** reads `.github/copilot-instructions.md` automatically.
- **Claude Code** reads `CLAUDE.md` automatically.
- **OpenAI Codex** reads `AGENTS.md` automatically.

Or choose a setup guide for manual configuration:
- `14_Guides/Guide - VS Code Chat.md`
- `14_Guides/Guide - Codex CLI.md`
- `14_Guides/Guide - Claude Code.md`

## Make it yours
- Edit any Markdown file to fit how you think and work.
- Keep what helps, remove what doesn't.
- Start simple, then evolve the system as your work grows.

## Daily loop
1. Capture notes during the day.
2. Drop rough notes in `10_Inbox/` when needed.
3. Ask AI to process inbox and propose priorities.
4. Ask AI to update `00_System/System State.md` at the end of the session.

## Workspace hygiene
Max OS treats the active workspace as the current operating surface, archives as historical context, and Git as the full preservation layer.

- Run `12_Workflows/Workflow - Weekly Workspace Hygiene Review.md` weekly or after heavy project work.
- Use `15_Skills/Skill - Workspace Hygiene and File Lifecycle Review.md` to classify drafts, generated files, expired prep, superseded versions, canonical notes, archive candidates, and delete candidates.
- Default to `PLAN_ONLY`; archive moves and deletions require explicit approval.
- Keep final deliverables and canonical Markdown easy to find, while moving stale working files out of active folders.
- Use lifecycle metadata from `99_Templates/TPL - Lifecycle Metadata.md` for temporary, event-specific, superseded, and generated material when useful.

## Knowledge linting
Before committing substantial Markdown changes, run the knowledge-system lint skill to check frontmatter, headings, wiki-links, and local Markdown links:

```bash
python3 15_Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
```

For a full pre-commit quality gate:

```bash
python3 15_Skills/tools/maxos_quality_gate.py --root .
```

To make that gate run automatically before every local commit, install the versioned Git hook once per clone:

```bash
sh 15_Skills/tools/ensure_local_setup.sh
```

The setup script writes ignored local state to `.maxos/local_setup_status.yaml`. If that file is missing or says `ready: false`, the clone is not fully initialized. The hook uses `git config core.hooksPath .githooks`, so Git runs `.githooks/pre-commit` before creating a commit. A failing hook aborts the commit until the issue is fixed.

For private-to-public template work, create an ignored local denylist:

```bash
cp 00_System/public_template_denylist.example.txt .maxos/public_template_denylist.txt
```

Add private names, clients, projects, and terms to that local file. The public-template quality gate uses it automatically.

## Structure at a glance

| Folder | Purpose |
|--------|--------|
| `00_System/` | AI operating rules and system state (read first) |
| `01_People/` | One note per person (`First Last.md`) |
| `02_Organizations/` | Company and org notes |
| `03_Clients/` | Client folders with `Client - Name.md` |
| `04_Projects/` | `Project - Name.md` |
| `05_Content/` | Written content (pillar + derivatives) |
| `06_Interactions/` | Date-first interaction notes |
| `07_Daily/` | Daily notes |
| `08_Todos/` | Task backlog |
| `09_Planning/` | Weekly, Monthly, Quarterly, Two-Year plans |
| `10_Inbox/` | Raw captures — process daily |
| `11_Notes/` | General notes; archive superseded to `11_Notes/Archive/` |
| `12_Workflows/` | Repeatable human-led processes |
| `13_Goals/` | One note per major goal |
| `14_Guides/` | Setup and usage guides |
| `15_Skills/` | Agent-executable capabilities |
| `20_Modules/` | Optional capability packs (disabled by default) |
| `99_Templates/` | Templates for new notes |

Full folder map: `00_System/Indexes.md`.
Agent capability manifest: `SKILLS.md`.

## Notes and linking
- Max OS is plain Markdown files.
- Link notes with `[[Note Name]]`.
- It works especially well in Obsidian (backlinks and graph view).

## Markdown-first, multi-format aware
- Markdown is the source of truth for memory, plans, people, projects, goals, workflows, skills, and system state.
- HTML artifacts and worklets are supported for rich human-facing views, but they do not replace canonical Markdown.
- JSON can be used for structured worklet state when needed.
- Future harnesses can render artifacts and worklets in a middle-pane interface while keeping Max OS usable as plain files.

## Private personal copy (recommended)
Use this repo as a public starter and keep your real notes in a private repo.
Setup + sync instructions are in the guides:
- `14_Guides/README.md`
