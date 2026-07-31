# Skills

Manifest of agent-executable capabilities in Max OS. Each entry is a pointer to a canonical card; read the linked file for trigger, inputs, steps, outputs, and quality checks.

- **Skills** (agent-autonomous): defined in `15_Skills/`. Differ from workflows in that agents can run them end-to-end without human steering.
- **Workflows** (human-led, step-by-step with checkpoints): defined in `12_Workflows/`.
- **Core algorithms** (Session Start, My Inbox Review, Agent Inbox Processing,
  Interaction Processing, Note Lifecycle): defined inline in
  `00_System/LLM Operating Manual.md`.

When adding or removing a skill or workflow, update the relevant list below.

## Skills (`15_Skills/`)
- [[Skill - Digest Deck to Markdown]]
- [[Skill - Evidence Finding and Narrative Integration with Validation Loops]]
- [[Skill - Executive Thought Leadership Rewriter with Review Loops]]
- [[Skill - Export Markdown to Word Document]]
- [[Skill - Knowledge System Lint and Link Check]]
- [[Skill - Pre-Commit Knowledge Quality Gate]]
- [[Skill - Process PDF Profiles to People Notes]]
- [[Skill - Slide Deck Generation]]
- [[Skill - Workspace Hygiene and File Lifecycle Review]]

## Workflows (`12_Workflows/`)
- [[Workflow - Backport Private Learnings to Public Repo via Pull Request]]
- [[Workflow - Build AI GTM Deck from Ideas or Articles]]
- [[Workflow - Content Waterfall from Pillar Article]]
- [[Workflow - Create LinkedIn Carousel from Thought Leadership Article]]
- [[Workflow - Create a Video]]
- [[Workflow - Digest Deck to Markdown]]
- [[Workflow - Draft LinkedIn Newsletter from Thesis]]
- [[Workflow - Generate Website UI Prompts (Antigravity + Gemini)]]
- [[Workflow - Launch Max OS Website in 90 Minutes]]
- [[Workflow - Meeting Prep Assistant]]
- [[Workflow - Process PDF Profiles to People Notes]]
- [[Workflow - Ship Idea to Live Website (Factory Sprint)]]
- [[Workflow - Thought Leadership Article Lifecycle]]
- [[Workflow - Weekly Todo Hygiene and Archive]]
- [[Workflow - Weekly Workspace Hygiene Review]]
- [[Workflow - Write LinkedIn Posts for One Specific Reader]]
- [[Workflow - Write an Article]]

## Tools (`15_Skills/tools/`)
- `15_Skills/tools/check_dependencies.py` — one-shot system-dependency report (pandoc, WeasyPrint, Node, Playwright + Chromium, Pillow, git hooks). Pairs with `14_Guides/Guide - System Dependencies.md`.
- `15_Skills/tools/check_vault.py` — warn-only vault validator (frontmatter, wiki-links, naming, hygiene, System State sanity).
- `15_Skills/tools/ensure_local_setup.sh` — idempotent local clone setup and hook installer.
- `15_Skills/tools/knowledge_lint.py` — strict changed-file/frontmatter/link validator used by the quality gate.
- `15_Skills/tools/maxos_quality_gate.py` — pre-commit quality gate for whitespace, lint, byproducts, and public-template privacy scan.
- `15_Skills/tools/md_to_docx.py` — Markdown → Word document export (used by `Skill - Export Markdown to Word Document`).
- `15_Skills/tools/slides/build_deck.py` — Markdown slide folder → self-contained HTML deck. Needs `pandoc`, optional `pillow` for logo safety check.
- `15_Skills/tools/slides/check_deck_visual.mjs` — headless browser screenshot and overflow QA for generated HTML decks. Needs `node`, Playwright + Chromium installed under `.maxos/visual-check/`.

## System Dependencies
External software some skills and tools require (pandoc, WeasyPrint, Node + Playwright, Pillow) is documented in `14_Guides/Guide - System Dependencies.md`. Run `python3 15_Skills/tools/check_dependencies.py` to verify everything is installed on a new machine.
