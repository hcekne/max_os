# Max OS

Max OS is an AI workflow operating system for knowledge work. Your plans,
people, projects, notes, and inbox live in one plain-Markdown workspace that
both you and AI agents can read, search, link, and edit.

Most users run Max OS through **MaxOS Online**: the hosted app adds chat with
agents that work directly in this workspace, scheduled and event-triggered
workflows via the Workflow Builder, connected organization sources, code
repositories, large-file storage, and run history. The workspace itself stays
a portable git repository you own — it also works entirely standalone with a
local AI tool, and that portability is a design guarantee, not an accident.

**The owner can be a human or an AI.** In `human` mode the system is a
cooperation between a human mind and an LLM; in `ai` mode an agent owns the
workspace as its persistent memory. `SYSTEM/Actor.md` declares which.

## Workspace map

- `ACTION CENTER/` — short-lived work moving between you and Max OS: My
  Inbox (for you to review), Agent Inbox (for Max OS to process), Outbox
  (ready to send).
- `KNOWLEDGE/` — long-lived people, organizations, clients, projects,
  content, interactions, and notes.
- `PLAN/` — daily notes, todos, goals, weekly and quarterly plans, reviews,
  and longer-range direction.
- `AUTOMATE/` — reusable workflows, agent skills, and optional modules.
- `SYSTEM/` — the kernel: who this workspace belongs to (`Actor.md`), what
  is true now (`State.md`), what to remember (`Memory.md`), what happened
  (`Log.md`), how information is handled (`Policy.md`), plus templates,
  proposals, and cleaning surfaces.

Every folder carries its own `.instructions.md` with local rules. The agent
entry point is `AGENTS.md`; `CLAUDE.md` and
`.github/copilot-instructions.md` are thin pointers so each tool finds
something at its expected filename. `CLAUDE.md` is yours to extend — template
updates never touch it.

## Using Max OS

**Hosted (recommended):** sign in to MaxOS Online, open your workspace, and
talk to it — agents read `AGENTS.md` and your folder instructions
automatically. Build automations in the Workflow Builder; they run on
schedules or events without a browser open.

**Standalone:** clone the repo, then follow `SYSTEM/Standalone.md` (one setup
script, one dependency check, start your AI tool in the folder).

## Working style

- Everything is plain Markdown; link notes with `[[Note Name]]`.
- One canonical active note per topic; stale material moves to
  `SYSTEM/Cleaning/` per `SYSTEM/Policy.md`.
- Quality gates guard commits: the pre-commit hook runs the knowledge lint
  and workspace checks (`AGENTS.md` → Validation).
