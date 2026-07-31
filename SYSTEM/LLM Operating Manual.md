# LLM Operating Manual

This file is the primary instruction set for any AI working inside Max OS — whether operating **on behalf of** a human owner or **as** a pure-AI owner.

## Audience & Owner Mode
- Written for the AI operating in this vault. Humans can read it too; for orientation start in `README.md`.
- Max OS is owner-neutral. Check `actor_type` in [[SYSTEM/Actor Profile]] before acting:
  - **`human`** — the workspace is a cooperation between a human mind and an LLM. The human is principal and holds final authority; you recall, draft, structure, and execute against these notes. Surface options and defer decisions that are the human's to make.
  - **`ai`** — you (or the agent you serve) are the principal owner. Act within the autonomy level and escalation rules recorded in the Actor Profile, and use the vault as your persistent memory.

## Identity & Memory
The control surfaces in `SYSTEM/` are this actor's persistent memory across sessions — see [[SYSTEM/AI Actor & Memory Model]] for the full model. In short: `Actor Profile` is identity, `System State` is working memory, `Session Log` is episodic memory, `Planning Memory` is learned memory. Read them at session start to recover state; write them to persist it.

## Scoped Resources In MaxOS Online
When this workspace is opened through MaxOS Online, the harness may attach
additional scoped resources to the agent run:

- personal workspace folders;
- organization projects shared with the owner;
- organization skills or instructions;
- code repositories explicitly selected for the chat or workflow.

Scope is an allowlist, not a search target. Work only with the resources the
owner has made available. Do not infer access to other organizations, projects,
repositories, or private notes. Treat shared organization projects and code
repositories as runtime resources; only write to them when the user has clearly
asked and the scope allows it.

When useful, summarize durable findings from shared projects or code repos back
into canonical Markdown in this workspace, but do not bulk-copy shared or client
material into personal notes.

For the full model, read
[[SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources]].

## Mandatory Read Set (in order)
0. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`
1. [[SYSTEM/Actor Profile]] — confirm owner type and operating mode
2. [[SYSTEM/System State]]
3. [[SYSTEM/Planning Cadence]]
4. [[SYSTEM/Planning Memory]]
5. [[SYSTEM/Indexes]]
6. Active goals in `PLAN/Goals/` (if any)

## Session Start Algorithm
1. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`.
2. If local setup fails, report the blocker before editing files.
3. Read `System State`.
4. Resolve today's local date.
5. Check recurring obligations using [[SYSTEM/Recurring Operations]]. Surface only active rows whose valid window includes today.
6. If `last_interaction_date` is not today, update it in [[SYSTEM/System State]] and append a dated bullet to [[SYSTEM/Session Log]].
7. Compute due reviews using the trigger rules in [[SYSTEM/Planning Cadence]].
8. Run due reviews in the order defined in [[SYSTEM/Planning Cadence]].
9. If `ACTION CENTER/My Inbox/` has pending results, surface the review queue
   to the owner.
10. If `ACTION CENTER/Agent Inbox/` has pending captures, process them.
11. Align today's daily plan with active goals in `PLAN/Goals/`.
12. Pull due items from `PLAN/Todos/` and place today's must-do subset in the daily note.
13. Propose next 1-3 concrete actions.

## Local Setup Protocol
Purpose: ensure each clone has the local Git hook and quality-gate tooling active before agents work in it.

Tracked setup requirements live in `SYSTEM/local_setup_requirements.yaml`.
Ignored local setup state lives in `.maxos/local_setup_status.yaml`.

At the start of work:
1. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`.
2. Confirm `.maxos/local_setup_status.yaml` exists and says `ready: true`.
3. If it says `ready: false` or the command fails, stop and report the blocker.

The script is safe to run repeatedly. It checks `python3`, verifies required files, installs or repairs `core.hooksPath=.githooks`, ensures `.githooks/pre-commit` is executable, and writes the ignored local status file.

## Note Lifecycle and Archive Protocol
Purpose: keep `KNOWLEDGE/Notes/` high-signal and reduce redundancy for both humans and AI.

When to run:
- During monthly review cycles, or when multiple notes cover the same topic.

Archive trigger conditions (any):
- A newer canonical note supersedes older notes.
- A note is mostly duplicated by another active note.
- A draft/synthesis is no longer needed as an active working note.

Archive process:
1. Pick one canonical active note to keep in `KNOWLEDGE/Notes/` root.
2. Move historically useful superseded notes to `SYSTEM/Cleaning/Archive/KNOWLEDGE/Notes/`.
3. Move clearly stale or low-value superseded notes to `SYSTEM/Cleaning/Rubbish Bin/KNOWLEDGE/Notes/`.
4. Set lifecycle metadata in moved notes.
5. Add a short "Archive status" pointer to the canonical note when useful.
6. Remove moved notes from active index lists.
7. Update major goals/projects to reference the canonical note only.

Guardrails:
- Preserve history, but keep active strategy surfaces minimal.
- Prefer archiving over deletion unless explicitly requested.
- Avoid creating extra system files for each cleanup; update existing indexes/manuals instead.

## Workspace Hygiene and File Lifecycle Protocol
Purpose: keep the full Max OS workspace clean, not only `KNOWLEDGE/Notes/`.

When to run:
- Weekly in `PLAN_ONLY` mode for recent files and high-bloat folders.
- Monthly for deeper project/content cleanup proposals.
- At project closeout, before major deliverables, and after major milestones.

Primary instructions:
- [[Skill - Workspace Hygiene and File Lifecycle Review]]
- [[Workflow - Weekly Workspace Hygiene Review]]
- [[SYSTEM/Document Lifecycle Policy]]
- [[SYSTEM/Archive Policy]]
- [[SYSTEM/Rubbish Bin Policy]]
- [[SYSTEM/Git Preservation Policy]]

Guardrails:
- Do not delete files outside the narrow rubbish-bin purge path.
- Check Git status before moves, deletes, or bulk metadata changes.
- Prefer updating canonical files over creating uncontrolled versions.
- Flag root-level markdown files outside the allowed control-file set as hygiene candidates, especially empty files and workspace folder-mirror files.
- Use `SYSTEM/Cleaning/Archive/` for historically useful material.
- Use `SYSTEM/Cleaning/Rubbish Bin/` for clearly stale, superseded, or low-value material that should be purged quickly.
- Use Git history as the full preservation layer.
- Classify uncertain files as `NEEDS_HUMAN_REVIEW`.
- Treat final deliverables, contracts, submitted documents, invoices, legal/commercial documents, and client-provided materials as high-retention.

## My Inbox Review Algorithm
1. List `ACTION CENTER/My Inbox/` directly.
2. Summarize what each item is, where it came from, and what decision or action
   the owner needs to take.
3. Do not treat delivery to My Inbox as approval.
4. After the owner reviews an item, route durable material to its canonical
   folder and move the transient copy to Archive or Rubbish Bin according to
   retention value.

## Agent Inbox Processing Algorithm
1. Scan `ACTION CENTER/Agent Inbox/` newest-to-oldest, using direct directory listings before relying on globbed search.
2. Route each item to one destination: people, organization, client, project, interaction, content, or todo.
3. Create missing notes from templates in `SYSTEM/Templates/`.
4. Merge factual updates into canonical notes.
5. Extract explicit tasks into `PLAN/Todos/` or today's daily note.
6. Add cross-links between touched notes.
7. Move each processed inbox item out of the active root of `ACTION CENTER/Agent Inbox/` and into `SYSTEM/Cleaning/Rubbish Bin/ACTION CENTER/Agent Inbox/...`, mirroring the original source path after `ACTION CENTER/Agent Inbox/`. Do not recreate retired processed-staging folders inside the inbox.

## Knowledge System Lint Protocol
Purpose: catch broken Markdown structure before files enter the knowledge system.

Default strict command:

```bash
python3 AUTOMATE/Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
```

Use `python3 AUTOMATE/Skills/tools/check_vault.py` for broader warn-only private-vault drift checks.

Checks:
- Frontmatter opens and closes correctly.
- Known lifecycle metadata values are within policy sets.
- Markdown heading structure is navigable.
- `[[wiki-links]]` resolve to note files.
- Local Markdown links resolve to existing files and anchors where practical.

## Commit Quality Gate Protocol
Purpose: make commit readiness deterministic for Max OS changes.

Before committing substantial changes:
1. Run `git status --short --branch`.
2. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`.
3. Confirm `.maxos/local_setup_status.yaml` says `ready: true`.
4. Run `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` when preparing a review.
5. Run `python3 AUTOMATE/Skills/tools/check_vault.py` for warn-only private-vault drift review.
6. Review untracked files explicitly.
7. Fix failures or document accepted exceptions.
8. Do not push without explicit human approval.

## Interaction Update Algorithm
When given an interaction note:
1. Ensure every mentioned person has a note in `KNOWLEDGE/People/`.
2. Ensure referenced organization/client/project notes exist.
3. Update relevant person notes with latest interaction date, key facts, open loops, and links.
4. Update referenced organization/client/project note with key updates and commitments.
5. Return a short factual changelog.

## Note Lifecycle and Archive Protocol
Purpose: keep `KNOWLEDGE/Notes/` high-signal and reduce redundancy for both humans and AI.

When to run:
- During monthly review cycles, or when multiple notes cover the same topic.

Archive trigger conditions (any):
- A newer canonical note supersedes older notes.
- A note is mostly duplicated by another active note.
- A draft/synthesis is no longer needed as an active working note.

Archive process:
1. Pick one canonical active note to keep in `KNOWLEDGE/Notes/` root.
2. Move historically useful superseded notes to `SYSTEM/Cleaning/Archive/KNOWLEDGE/Notes/`.
3. Move clearly stale or low-value superseded notes to `SYSTEM/Cleaning/Rubbish Bin/KNOWLEDGE/Notes/`.
4. Set frontmatter `status: archived` in archived notes or `lifecycle: delete_candidate` in rubbish-bin notes where useful.
5. Add a short "Archive status" pointer to the canonical note.
6. Remove archived notes from active index lists (for example in `KNOWLEDGE/Notes/README.md`).
7. Update major goals/projects to reference the canonical note only.

Guardrails:
- Preserve history, but keep active strategy surfaces minimal.
- Prefer archiving over deletion unless explicitly requested.
- Avoid creating extra system files for each cleanup; update existing indexes/manuals instead.
- For workspace-wide hygiene, use [[Skill - Workspace Hygiene and File Lifecycle Review]] and [[Workflow - Weekly Workspace Hygiene Review]].
- Use `SYSTEM/Cleaning/Archive/` for historically useful material.
- Use `SYSTEM/Cleaning/Rubbish Bin/` for clearly stale, superseded, or low-value material that should be purged quickly.
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
python3 AUTOMATE/Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
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
2. Run `sh AUTOMATE/Skills/tools/ensure_local_setup.sh`.
3. Confirm `.maxos/local_setup_status.yaml` says `ready: true`.
4. Run `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` when preparing a review.
5. For public-template changes, run `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root . --full --public-template`.
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
- Keep `AUTOMATE/Modules/` optional unless explicitly activated in `System State`.
- Keep one canonical active note per strategy topic when possible; archive redundant variants.

## Required Session Output
1. Due reviews summary and reason.
2. Ordered checklist for this session.
3. My Inbox review summary and Agent Inbox processing summary (when either had
   pending items).
4. Updated links to active plan/review notes.
5. `System State` updates after completed review steps.
6. Operational reminders due today from [[SYSTEM/Recurring Operations]] (if any).
