# LLM Operating Manual

This file is the primary instruction set for any AI working inside Max OS.

## Audience
- LLMs only.
- Human users should start in `README.md`.

## Mandatory Read Set (in order)
0. Run `sh 15_Skills/tools/ensure_local_setup.sh`
1. [[00_System/System State]]
2. [[00_System/Planning Cadence]]
3. [[00_System/Planning Memory]]
4. [[00_System/Indexes]]
5. Active goals in `13_Goals/` (if any)

## Session Start Algorithm
1. Run `sh 15_Skills/tools/ensure_local_setup.sh`.
2. If local setup fails, report the blocker before editing files.
3. Read `System State`.
4. Resolve today's local date.
5. If `last_interaction_date` is not today, update it and append a session log line.
6. Compute due reviews from canonical last-review dates:
   - Weekly due if 7+ days since `last_weekly_review_date`
   - Monthly due if month changed since `last_monthly_review_date`
   - Quarterly due if quarter changed since `last_quarterly_review_date`
   - Yearly due if year changed since `last_yearly_review_date`
7. Run due items in order: yearly -> quarterly -> monthly -> weekly.
8. If `10_Inbox/` has pending captures, process them.
9. Align today's daily plan with active goals in `13_Goals/`.
10. Surface workspace hygiene review when weekly/monthly cadence or visible file bloat signals call for it.
11. Propose next 1-3 concrete actions.

## Local Setup Protocol
Purpose: ensure each clone has the local Git hook and quality-gate tooling active before agents work in it.

Tracked setup requirements live in `00_System/local_setup_requirements.yaml`.
Ignored local setup state lives in `.maxos/local_setup_status.yaml`.

At the start of work:
1. Run `sh 15_Skills/tools/ensure_local_setup.sh`.
2. Confirm `.maxos/local_setup_status.yaml` exists and says `ready: true`.
3. If it says `ready: false` or the command fails, stop and report the blocker.

The script is safe to run repeatedly. It checks `python3`, verifies required files, installs or repairs `core.hooksPath=.githooks`, ensures `.githooks/pre-commit` is executable, and writes the ignored local status file.

## Inbox Processing Algorithm
1. Scan `10_Inbox/` newest-to-oldest, using direct directory listings before relying on globbed search.
2. Route each item to one destination: people, organization, client, project, interaction, content, or todo.
3. Create missing notes from templates in `99_Templates/`.
4. Merge factual updates into canonical notes.
5. Extract explicit tasks into `08_Todos/` or today's daily note.
6. Add cross-links between touched notes.
7. Move processed raw captures out of active inbox roots.
8. Use `16_Cleaning/Rubbish Bin/10_Inbox/` as the default destination for low-retention processed captures; use `16_Cleaning/Archive/10_Inbox/` when the raw source has historical value.
9. Do not leave already-routed article drafts, transcripts, or processed captures beside active inbox items.

## Interaction Update Algorithm
When given an interaction note:
1. Ensure every mentioned person has a note in `01_People/`.
2. Ensure referenced organization/client/project notes exist.
3. Update relevant person notes with latest interaction date, key facts, open loops, and links.
4. Update referenced organization/client/project note with key updates and commitments.
5. Return a short factual changelog.

## Note Lifecycle and Archive Protocol
Purpose: keep `11_Notes/` high-signal and reduce redundancy for both humans and AI.

When to run:
- During monthly review cycles, or when multiple notes cover the same topic.

Archive trigger conditions (any):
- A newer canonical note supersedes older notes.
- A note is mostly duplicated by another active note.
- A draft/synthesis is no longer needed as an active working note.

Archive process:
1. Pick one canonical active note to keep in `11_Notes/` root.
2. Move historically useful superseded notes to `16_Cleaning/Archive/11_Notes/`.
3. Move clearly stale or low-value superseded notes to `16_Cleaning/Rubbish Bin/11_Notes/`.
4. Set frontmatter `status: archived` in archived notes or `lifecycle: delete_candidate` in rubbish-bin notes where useful.
5. Add a short "Archive status" pointer to the canonical note.
6. Remove archived notes from active index lists (for example in `11_Notes/README.md`).
7. Update major goals/projects to reference the canonical note only.

Guardrails:
- Preserve history, but keep active strategy surfaces minimal.
- Prefer archiving over deletion unless explicitly requested.
- Avoid creating extra system files for each cleanup; update existing indexes/manuals instead.
- For workspace-wide hygiene, use [[Skill - Workspace Hygiene and File Lifecycle Review]] and [[Workflow - Weekly Workspace Hygiene Review]].
- Use `16_Cleaning/Archive/` for historically useful material.
- Use `16_Cleaning/Rubbish Bin/` for clearly stale, superseded, or low-value material that should be purged quickly.
- Deletion outside the rubbish-bin purge path requires explicit approval.

## Workspace Hygiene and File Lifecycle Protocol
Purpose: keep the active workspace focused while using Git history and archives for preservation.

When to run:
- Weekly in `PLAN_ONLY` if recent work created many drafts, exports, generated artifacts, or inbox captures.
- Monthly as a deeper review of high-bloat folders.
- At project closeout, after major deliverables, or after event/interview phases.

Operating modes:
- `PLAN_ONLY`: inspect and propose only.
- `APPLY_SAFE`: create folders, proposals, indexes, and reversible archive moves only.
- `APPLY_APPROVED`: apply explicitly approved archive moves, metadata updates, renames, or deletions.

Rules:
1. Check `git status --short --branch` before cleanup.
2. Do not delete files without explicit approval.
3. Do not push public repo updates without explicit approval.
4. Prefer updating canonical files over creating uncontrolled new variants.
5. Use lifecycle metadata for temporary, event-specific, draft, superseded, and generated files when it helps future review.
6. Treat final deliverables, legal/commercial files, invoices, contracts, and source materials as high-retention.
7. Treat generated HTML/PDF/DOCX exports as non-canonical unless explicitly final/submitted.
8. Do not track runtime byproducts such as `__pycache__/` or `*.pyc`.
9. Extract privacy-safe reusable patterns into public Max OS proposals when appropriate.

## Knowledge System Lint Protocol
Purpose: catch broken Markdown structure before files enter the knowledge system.

When to run:
- Before committing substantial changes to Markdown files.
- After inbox processing creates or updates many canonical notes.
- After adding or changing system files, skills, workflows, templates, policies, or project state files.
- During monthly workspace hygiene.

Default command:

```bash
python3 15_Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
```

Checks:
- Frontmatter opens and closes correctly.
- Known lifecycle metadata values are within policy sets.
- Markdown heading structure is navigable.
- `[[wiki-links]]` resolve to note files.
- Local Markdown links resolve to existing files and anchors where practical.

Fix lint errors before commit unless the user explicitly accepts a documented exception.

## Commit Quality Gate Protocol
Purpose: make commit readiness deterministic for Max OS changes.

Before committing substantial changes:
1. Run `git status --short --branch`.
2. Run `sh 15_Skills/tools/ensure_local_setup.sh`.
3. Confirm `.maxos/local_setup_status.yaml` says `ready: true`.
4. Run `python3 15_Skills/tools/maxos_quality_gate.py --root .` when preparing a review.
5. For public-template changes, run `python3 15_Skills/tools/maxos_quality_gate.py --root . --full --public-template`.
6. Review untracked files explicitly.
7. Fix failures or document accepted exceptions.
8. Do not push without explicit human approval.

The quality gate checks:
- `git diff --check`;
- knowledge lint;
- tracked and untracked runtime byproducts;
- optional public-template privacy and secret patterns.

The local hook is stored in `.githooks/pre-commit` because `.git/hooks/` is not versioned. `core.hooksPath=.githooks` tells Git to run the versioned hook before every local commit in that clone.

## Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, commitments, or outcomes.
- Ask one focused clarification question only when required context is missing.
- Treat `last_*_review_date` fields as canonical truth.
- Keep `20_Modules/` optional unless explicitly activated in `System State`.
- Keep one canonical active note per strategy topic when possible; archive redundant variants.
- Use Git as the preservation layer; do not keep every intermediate draft active merely as history.
- Run knowledge lint on changed Markdown files before committing structural knowledge-system changes.
- Run the Max OS quality gate before committing public-template or system changes.
- Never delete, push, or rewrite history without explicit human approval.

## Required Session Output
1. Due reviews summary and reason.
2. Ordered checklist for this session.
3. Inbox processing summary (if inbox had pending captures).
4. Updated links to active plan/review notes.
5. `System State` updates after completed review steps.
