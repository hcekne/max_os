# Max OS

Max OS is a plain-Markdown operating system for work.

It keeps plans, people, projects, notes, and inbox capture in one editable workspace.
The rules are simple: keep canonical notes clear, keep raw capture temporary, and keep the system easy to change.

**The owner can be a human or an AI.** Max OS is owner-neutral:
- A **human working with an LLM** — the system is a cooperation between a human mind and an LLM (human directs and decides; LLM recalls, drafts, and executes).
- A **pure-AI actor** — e.g. a chief-of-staff agent booted from the public template, which uses the vault as its own persistent memory.

The owner type is declared in `00_System/Actor Profile.md`, and `00_System/AI Actor & Memory Model.md` explains how the vault serves as memory across sessions.

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

## Core Surfaces
- `00_System/Actor Profile.md` — who owns this workspace (human or AI) and how it operates.
- `00_System/AI Actor & Memory Model.md` — how the vault works as the owner's persistent memory.
- `00_System/LLM Operating Manual.md` — the canonical AI operating rules.
- `00_System/System State.md` — current dates, active plans, and review checkpoints.
- `00_System/Indexes.md` — where each kind of note belongs.
- `10_Inbox/` — raw capture waiting to be processed.
- `07_Daily/`, `08_Todos/`, `09_Planning/` — day-to-day execution and planning.

## Use with AI tools
The canonical agent entry-point is `AGENTS.md`. Tool-specific files exist as thin wrappers so each tool finds something at its expected filename:
- VS Code Copilot reads `.github/copilot-instructions.md`.
- Claude Code reads `CLAUDE.md` (one-line pointer to `AGENTS.md`).
- OpenAI Codex and other agents read `AGENTS.md` directly.
- Setup guides live in `14_Guides/`.

## Working Style
- Keep everything editable as plain Markdown.
- Link notes with `[[Note Name]]`.
- Keep one canonical active note per topic when practical.
- Move stale or superseded material into `16_Cleaning/` instead of leaving it in active folders.

## Quality Gates
- Local setup status is written to `.maxos/local_setup_status.yaml` and ignored by Git.
- The pre-commit hook runs `python3 15_Skills/tools/maxos_quality_gate.py --root .` before each commit after setup is installed.
- Use `python3 15_Skills/tools/check_vault.py` for broader warn-only vault drift checks.
- Use `.maxos/public_template_denylist.txt` for private terms that must not appear in public-template work.

## System Dependencies
Some skills and tools rely on software beyond Python's standard library (pandoc, WeasyPrint, Pillow, Node + Playwright). The canonical reference is `14_Guides/Guide - System Dependencies.md`, which lists every external dependency, what it is used for, the install command, and the failure mode if missing.

To check what is installed and what is missing on your machine:

```bash
python3 15_Skills/tools/check_dependencies.py
```

Read `14_Guides/Guide - System Dependencies.md` before running any skill for the first time on a new machine.

## More Help
- Full folder map: `00_System/Indexes.md`
- Skills manifest: `SKILLS.md`
- Setup guides: `14_Guides/README.md`
- System dependencies (mandatory pre-read on a fresh clone): `14_Guides/Guide - System Dependencies.md`
