# Max OS

Max OS is a plain-Markdown operating system for work.

It keeps plans, people, projects, notes, and inbox capture in one editable workspace.
The rules are simple: keep canonical notes clear, keep raw capture temporary, and keep the system easy to change.

**The owner can be a human or an AI.** Max OS is owner-neutral:
- A **human working with an LLM** — the system is a cooperation between a human mind and an LLM (human directs and decides; LLM recalls, drafts, and executes).
- A **pure-AI actor** — e.g. a chief-of-staff agent booted from the public template, which uses the vault as its own persistent memory.

The owner type is declared in `SYSTEM/Actor Profile.md`, and `SYSTEM/AI Actor & Memory Model.md` explains how the vault serves as memory across sessions.

---

## Start in 60 seconds
1. Open this folder in your editor.
2. In a terminal, run:

```bash
sh AUTOMATE/Skills/tools/ensure_local_setup.sh
```

3. Start chat with your AI tool.
4. Paste this prompt:

"Use this workspace as Max OS. Read `SYSTEM/LLM Operating Manual.md`. Check `SYSTEM/System State.md` and tell me what I should do today. Then process anything in `ACTION CENTER/Agent Inbox/` and give me my top 3 actions."

## Workspace Map
- `ACTION CENTER/` — short-lived work moving between you and Max OS: My Inbox,
  Agent Inbox, and Outbox.
- `KNOWLEDGE/` — long-lived people, organizations, clients, projects, content,
  interactions, notes, and your own custom folders.
- `PLAN/` — daily work, todos, goals, weekly and quarterly plans, reviews, and
  longer-range direction.
- `AUTOMATE/` — reusable workflows, agent skills, and optional modules.
- `SYSTEM/` — operating instructions, memory, guides, templates, cleaning, and
  storage references.

Start with `SYSTEM/Actor Profile.md`, `SYSTEM/LLM Operating Manual.md`, and
`SYSTEM/System State.md`. The full placement map is `SYSTEM/Indexes.md`.

## Use with AI tools
The canonical agent entry-point is `AGENTS.md`. Tool-specific files exist as thin wrappers so each tool finds something at its expected filename:
- VS Code Copilot reads `.github/copilot-instructions.md`.
- Claude Code reads `CLAUDE.md` (one-line pointer to `AGENTS.md`).
- OpenAI Codex and other agents read `AGENTS.md` directly.
- Setup guides live in `SYSTEM/Guides/`.

## Use with MaxOS Online
Most users will interact with this template through MaxOS Online. In that mode,
an agent may be given a scoped view that includes this private workspace plus
organization projects, shared skills, or code repositories selected by the
owner.

- Personal Markdown memory remains the canonical private workspace.
- Organization projects are shared scoped resources, not folders to silently
  copy into the private workspace.
- Code repositories can be added to scope for engineering work; summarize
  durable learnings back into Markdown when useful.
- Executable Workflow Builder recipes live in `AUTOMATE/Workflows/Automations/`.

## Working Style
- Keep everything editable as plain Markdown.
- Link notes with `[[Note Name]]`.
- Keep one canonical active note per topic when practical.
- Move stale or superseded material into `SYSTEM/Cleaning/` instead of leaving it in active folders.

## Quality Gates
- Local setup status is written to `.maxos/local_setup_status.yaml` and ignored by Git.
- The pre-commit hook runs `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` before each commit after setup is installed.
- Use `python3 AUTOMATE/Skills/tools/check_vault.py` for broader warn-only vault drift checks.
- Use `.maxos/public_template_denylist.txt` for private terms that must not appear in public-template work.

## System Dependencies
Some skills and tools rely on software beyond Python's standard library (pandoc, WeasyPrint, Pillow, Node + Playwright). The canonical reference is `SYSTEM/Guides/Guide - System Dependencies.md`, which lists every external dependency, what it is used for, the install command, and the failure mode if missing.

To check what is installed and what is missing on your machine:

```bash
python3 AUTOMATE/Skills/tools/check_dependencies.py
```

Read `SYSTEM/Guides/Guide - System Dependencies.md` before running any skill for the first time on a new machine.

## More Help
- Full folder map: `SYSTEM/Indexes.md`
- Skills manifest: `SKILLS.md`
- Setup guides: `SYSTEM/Guides/README.md`
- System dependencies (mandatory pre-read on a fresh clone): `SYSTEM/Guides/Guide - System Dependencies.md`
