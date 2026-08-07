---
type: policy
status: active
---

# Policy

How information is handled in this workspace. This file changes rarely and
deliberately. Where behavior is enforced by code — `knowledge_lint.py`
validates the metadata vocabularies below; the MaxOS app implements the
Rubbish Bin behavior — this file matches the code, not the other way around.

## Document types

- **Note** — canonical Markdown memory: people, organizations, clients,
  projects, plans, interactions, content, decisions, commitments, open
  loops. YAML frontmatter carries metadata; the Markdown body remains the
  human-readable source of truth. Link notes with `[[Note Name]]`.
- **Executable workflow recipe** — Markdown with `type: maxos-workflow`
  frontmatter in `AUTOMATE/Workflows/Automations/`. The frontmatter is the
  recipe contract; the body is the human description. Run outputs live only
  under `AUTOMATE/Workflows/Automations/artifacts/`.
- **Artifact** — generated or hand-authored human-facing output, usually
  HTML, in `KNOWLEDGE/Content/Artifacts/`. Artifacts may render canonical
  Markdown; they never replace it.
- **Proposal** — a suggested change awaiting approval, in
  `SYSTEM/Proposals/`. Not truth until applied to the canonical note.
- **State** — JSON for strict machine data, YAML frontmatter for note
  metadata. Never move canonical note bodies into YAML or HTML.
- **Scoped code repository** — an engineering resource attached to a hosted
  run; not Markdown memory. Summarize durable lessons into a note and link
  the repository or commit.

Precedence when sources disagree: canonical Markdown notes → approved
proposals applied to them → generated JSON state → rendered HTML output.
Generated output is never, by itself, authority for changing canonical
Markdown.

## Lifecycle and metadata

Add lifecycle frontmatter when it improves future cleanup judgment — drafts,
event-bound prep, version families, generated exports — not to every file.

Vocabulary (enforced at commit time by `knowledge_lint.py`):

- `lifecycle`: `evergreen`, `active`, `temporary`, `expired`, `superseded`,
  `archive`, `delete_candidate`
- `status`: `draft`, `active`, `canonical`, `superseded`, `expired`,
  `archived`, `final` — plus task statuses `backlog`, `todo`, `open`,
  `closed`, `pending`, `in_progress`, `blocked`, `done`, `complete`,
  `completed`
- `retention_policy`: `keep`, `review`, `archive`, `delete_after_review`,
  `preserve_final_only`, `preserve_canonical_only`
- `confidentiality`: `private`, `client_confidential`, `internal`,
  `public_template_safe`

Optional helper fields: `canonical`, `version_family`, `supersedes`,
`superseded_by`, `valid_until`, `review_after`, `archive_after`,
`delete_after`.

High-retention by default: final deliverables, client-provided source
material, contracts, invoices, submitted documents, legal and commercial
files. When classification is unclear, do not move the file — keep it active
or propose `NEEDS_HUMAN_REVIEW` in `SYSTEM/Proposals/`.

## Archive and Rubbish Bin

- `SYSTEM/Cleaning/Archive/` holds historically useful material that has
  left the active surface: superseded drafts that explain a final version,
  past-phase project artifacts, event material whose event has passed.
  Mirror the source path beneath the root
  (`SYSTEM/Cleaning/Archive/KNOWLEDGE/Notes/...`), prefer `git mv`, and
  record significant moves in `SYSTEM/Cleaning/Archive/Index.md`. Do not
  create distributed `Archive/` folders inside active project folders.
- `SYSTEM/Cleaning/Rubbish Bin/` holds clearly stale, superseded, low-value
  material queued for deletion. Working standalone, mirror the source path
  and set `superseded_by` / `delete_after` when useful. **The MaxOS app's
  Move-to-Rubbish-Bin places files flat at the bin root, its Empty action
  deletes bin contents immediately, and bin contents are excluded from the
  automatic git backup** — treat the bin as short-lived, never rely on a
  hold window, and never bin anything high-retention.
- Deletion anywhere outside the Rubbish Bin requires explicit owner approval
  and a recorded reason.
- Prefer archiving over deletion when in doubt; keep one canonical active
  note per topic and retire redundant variants.

## Git preservation

Git history is the preservation layer; active folders stay clean.

- Check `git status` before bulk moves, deletes, or metadata sweeps; commit
  before large cleanups; prefer `git mv` so history stays legible.
- Never rewrite Git history unless the owner explicitly requests it.
- Push rules live in `AGENTS.md`: never push a remote named `upstream`;
  outside the MaxOS harness any push requires owner approval.

## Generated output

- Never put secrets, API keys, tokens, credentials, private URLs, or hidden
  operational instructions in generated files.
- Generated files never become the only home of a decision, commitment,
  fact, or plan. If a rendered view reveals a needed update, apply it to the
  canonical Markdown note.
- Prefer self-contained HTML: no external scripts, fonts, images, or
  analytics; semantic structure and readable contrast. Review scripts,
  forms, iframes, storage, and network calls before approving an artifact
  that needs them.
- Exception on record: the slide-deck toolkit
  (`AUTOMATE/Skills/tools/slides/`) currently loads Chart.js from a CDN.
  Treat generated decks as trusted-viewer output until the chart assets are
  inlined; do not extend the exception to new artifact kinds.
- Name artifacts descriptively (`Artifact - Topic - YYYY-MM-DD.html`) and
  identify source files, generator, and date in a comment at the top.

## Root files and ownership

- Root markdown allowlist: `README.md`, `AGENTS.md`, `CLAUDE.md`,
  `SKILLS.md` (enforced by `check_vault.py`). No domain mirror files at the
  root.
- **Template-owned** (updated from the upstream template): `AGENTS.md`,
  `SYSTEM/Policy.md`, `SYSTEM/Standalone.md`, `SYSTEM/.instructions.md`,
  `SYSTEM/Templates/`, every folder `.instructions.md`,
  `.github/copilot-instructions.md`.
- **User-owned** (shipped once, never modified by the upstream template
  again): `CLAUDE.md`, `SYSTEM/Actor.md`, `SYSTEM/State.md`,
  `SYSTEM/Memory.md`, `SYSTEM/Log.md`, `SYSTEM/Proposals/`, and everything
  in `KNOWLEDGE/` and `PLAN/`. Template updates must never conflict with
  edits to these files.
