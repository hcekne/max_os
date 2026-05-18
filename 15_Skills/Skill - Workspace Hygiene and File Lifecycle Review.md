---
type: skill
status: active
trigger_phrase: run workspace hygiene review
tags: [skill, workspace-hygiene, lifecycle, archive, git, cleanup]
---

# Skill - Workspace Hygiene and File Lifecycle Review

## Purpose
Review a Max OS workspace for file bloat, stale material, duplicate drafts, expired prep, unclear canonical files, and lifecycle metadata gaps, then produce or apply a safe cleanup plan.

## When to Use
Use this skill when:
- a project folder has too many drafts, prep notes, research files, or generated artifacts;
- a major meeting, sprint, deliverable, or project phase has ended;
- content folders contain many versions of the same draft;
- monthly review calls for note hygiene;
- the user asks to clean up, archive, deduplicate, or identify canonical files.

## Trigger Phrases
- "run workspace hygiene review"
- "review this project folder for bloat"
- "find stale files and archive candidates"
- "identify canonical files"
- "clean old drafts without deleting anything"
- "prepare a lifecycle cleanup proposal"

## Inputs
- Workspace root path
- Optional target folder or project
- Optional mode: `PLAN_ONLY`, `APPLY_SAFE`, or `APPLY_APPROVED`
- Optional date window or milestone date
- Optional approved proposal for apply mode

## Outputs
- Workspace hygiene proposal in `00_System/Proposals/`
- File classification table
- Canonical file recommendations
- Archive/delete/merge candidates
- Lifecycle metadata recommendations
- Optional safe archive moves or metadata updates, depending on mode
- Public Max OS improvement proposal when reusable patterns are found

## Operating Modes

### PLAN_ONLY
Inspect the workspace and create a cleanup proposal. Do not move, delete, rename, or rewrite existing files.

### APPLY_SAFE
Apply only safe, reversible, non-destructive changes:
- create archive folders;
- create proposal files;
- create archive indexes;
- add lifecycle metadata where obvious;
- move clearly expired/superseded files into archive using `git mv`.

Do not delete files.

### APPLY_APPROVED
Only after explicit human approval, apply agreed archive moves, metadata updates, canonical renames, and deletions.

Default to `PLAN_ONLY` unless the user explicitly requests another mode.

## File Classification Taxonomy

Use one or more classifications per reviewed file:

- `KEEP_ACTIVE` - remains relevant to current work and should stay in active workspace.
- `KEEP_CANONICAL` - is, or should become, the source of truth for a topic, deliverable, project state, plan, or reference note.
- `EVERGREEN_REFERENCE` - contains lasting knowledge that should remain available.
- `FINAL_DELIVERABLE` - submitted, shared, or otherwise important final artifact.
- `ARCHIVE` - historical value but should move out of active workspace.
- `EXPIRED` - tied to a date, event, or phase that has passed.
- `SUPERSEDED` - replaced by a newer, better, final, or canonical file.
- `MERGE_CANDIDATE` - useful material should be merged into a canonical file before archiving or deletion.
- `DELETE_CANDIDATE` - redundant, generated, temporary, or superseded; deletion requires explicit approval.
- `METADATA_UPDATE` - should receive lifecycle metadata but otherwise remain where it is.
- `NEEDS_HUMAN_REVIEW` - may matter, but cannot be safely classified automatically.

For each reviewed file, record:
- relative path;
- classification;
- reason;
- confidence: high / medium / low;
- suggested action;
- related canonical file, if any;
- suggested archive destination, if any;
- suggested metadata, if any;
- whether human approval is required.

## Lifecycle Metadata Schema

Use YAML frontmatter where useful:

```yaml
---
title:
type:
status:
project:
created:
last_reviewed:
valid_until:
review_after:
archive_after:
delete_after:
lifecycle:
canonical:
supersedes:
superseded_by:
retention_policy:
confidentiality:
---
```

Allowed `lifecycle` values:
- `evergreen`
- `active`
- `temporary`
- `expired`
- `superseded`
- `archive`
- `delete_candidate`

Allowed `status` values:
- `draft`
- `active`
- `canonical`
- `superseded`
- `expired`
- `archived`
- `final`

Allowed `retention_policy` values:
- `keep`
- `review`
- `archive`
- `delete_after_review`
- `preserve_final_only`
- `preserve_canonical_only`

Allowed `confidentiality` values:
- `private`
- `client_confidential`
- `internal`
- `public_template_safe`

Do not add lifecycle metadata to every file blindly. Add it where it improves future review decisions.

## Git Safety Process
1. Run `git status --short --branch`.
2. Record current branch and remote.
3. If there are uncommitted changes, warn the user and recommend committing before cleanup.
4. Never rewrite Git history.
5. Prefer `git mv` for file moves.
6. Do not delete without explicit approval.
7. Do not push without explicit approval.
8. Treat final deliverables, contracts, submitted documents, invoices, legal/commercial documents, and client-provided materials as high-retention by default.

## Review Process
1. Inspect top-level folder counts.
2. Identify large project/content folders.
3. Identify archive folders and proposal folders.
4. Find recently modified files.
5. Find old files.
6. Search filename bloat patterns:
   - `v1`, `v2`, `v14`
   - `draft`
   - `final`
   - `latest`
   - `current`
   - `old`
   - `backup`
   - `copy`
   - `revised`
   - `split`
   - `temp`
   - `scratch`
   - `prep`
   - `interview`
   - `memo`
   - `proposal`
   - `notes`
   - `research`
7. For project folders, distinguish:
   - current active work;
   - canonical project state;
   - research;
   - meetings/interview prep;
   - working drafts;
   - final deliverables;
   - decisions;
   - archive;
   - scratch/generated material.
8. Review versioned deliverable packs:
   - numbered drafts;
   - final/stakeholder/submitted exports;
   - generated PDF/DOCX/HTML variants;
   - split section packs and build scripts.
9. Review interview/event packs:
   - upcoming prep;
   - expired prep;
   - completed summaries;
   - raw transcripts;
   - generated Word/PDF prep packs.
10. Review generated artifacts and runtime byproducts:
   - generated HTML/PDF/DOCX outputs;
   - generated pack folders;
   - build scripts and CSS;
   - `__pycache__` and `*.pyc` files.
11. Create a proposal before applying changes.

## Archive Process
1. Identify high-confidence archive candidates.
2. Confirm they are not final deliverables, legal/commercial documents, invoices, contracts, or client-provided source materials.
3. Identify archive destination.
4. If applying, create archive folder and archive index first.
5. Use `git mv` for moves.
6. Add metadata such as `status: archived`, `lifecycle: archive`, `superseded_by`, and `retention_policy` where useful.
7. Update canonical indexes and project state links.

## Deletion Approval Process
1. Record delete candidates in proposal only.
2. Explain why Git history is sufficient preservation.
3. Confirm no final/canonical/legal/source value remains.
4. Wait for explicit approval.
5. Apply deletion only in `APPLY_APPROVED`.
6. Show Git diff after deletion.

## Version Bloat Handling
For multiple versions of the same artifact:
1. Identify likely canonical/latest/current/final file.
2. Preserve final/submitted versions separately.
3. Recommend one clean canonical filename.
4. Move old versions to archive, or mark as delete candidates after approval.
5. Merge useful content into canonical file before retiring old files.
6. Add `canonical: true` to the current file when useful.
7. Add `superseded_by` to old versions when useful.

## Deliverable-Pack Handling
When a project contains a deliverable pack with many Markdown sections, generated PDF/DOCX/HTML files, build scripts, and old numbered versions:
1. Identify the final/submitted deliverable, if any.
2. Identify the canonical source format used to generate it.
3. Keep the final/submitted file and canonical source visible or clearly linked.
4. Archive old numbered versions and generated variants when superseded.
5. Preserve build scripts only if they are needed to regenerate a useful final artifact.
6. Treat generated artifacts as non-canonical unless explicitly marked final/submitted.

## Interview-Pack Handling
When a project contains interview prep, completed interview notes, raw transcripts, and generated prep packs:
1. Keep upcoming interview prep active until the event date.
2. Archive expired prep after the event date.
3. Keep completed interview summaries active while synthesis is underway.
4. Move raw transcripts out of inbox root after processing.
5. Archive generated Word/PDF interview packs after the interview phase closes.
6. Link completed summaries from the project state or current synthesis file.

## Runtime Byproduct Handling
- `__pycache__/` and `*.pyc` should not be committed.
- If tracked runtime byproducts are found, propose removal from Git and add ignore rules.
- Do not delete source scripts just because their generated bytecode is deleted.

## Project-Folder Hygiene Logic
Use existing project patterns where they work. If a folder is bloated or ambiguous, recommend a structure such as:

```text
04_Projects/<Project Name>/
  00_Project State.md
  01_Current/
  02_Working/
  03_Research/
  04_Deliverables/
  05_Meetings/
  06_Decisions/
  90_Archive/
  99_Scratch/
```

Do not impose this globally if a lighter structure is enough.

## Public-Template Extraction Logic
When a hygiene run reveals reusable Max OS improvements:
1. Extract the generic pattern only.
2. Remove private names, client details, confidential numbers, and internal-only facts.
3. Prefer policies, templates, skill improvements, and workflow rules.
4. Create a privacy-safe proposal under `00_System/Proposals/`.
5. If the public repo is available locally, prepare additive changes on a branch.
6. Do not commit or push public changes without explicit approval.

## Anti-Patterns
- Creating endless new drafts instead of updating the canonical file.
- Keeping every old version active because it may someday be useful.
- Moving final deliverables without review.
- Treating archive as a garbage pile with no index.
- Adding lifecycle metadata mechanically to every file.
- Deleting files just because they look stale.
- Copying private project context into public templates.

## Example Commands

```bash
git status --short --branch
find . -type f -not -path './.git/*' | awk -F/ '{print $2}' | sort | uniq -c | sort -nr
find 04_Projects -type f | rg -i '(v[0-9]+|draft|final|latest|old|copy|prep|interview|memo|research)'
find 04_Projects/<Project Name> -type f -printf '%s %p\n' | sort -nr
find . -type f | rg '(__pycache__|\.pyc$)'
python3 15_Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
git mv "old/path.md" "04_Projects/<Project Name>/90_Archive/old/path.md"
```

## Example Proposal Output

```md
| File | Classification | Reason | Confidence | Suggested action | Approval |
|---|---|---|---|---|---|
| Project/Prep - 2026-04-01.md | EXPIRED, ARCHIVE | Meeting date has passed | high | Move to project archive | required before move |
| Project/Memo v03.md | SUPERSEDED, DELETE_CANDIDATE | Replaced by canonical final memo | medium | Delete after approval | required |
| Project/Final Readout.pdf | FINAL_DELIVERABLE | Shared externally | high | Keep | required for any move |
```

## Quality Checks
- [ ] Git status checked before proposing or applying changes
- [ ] Mode stated explicitly
- [ ] No deletion in `PLAN_ONLY` or `APPLY_SAFE`
- [ ] Final/client/legal/commercial files protected
- [ ] Classifications include reason and confidence
- [ ] Canonical files identified where possible
- [ ] Archive destinations proposed
- [ ] Metadata updates are targeted, not blanket-applied
- [ ] Versioned deliverable packs are reviewed for canonical/final outputs
- [ ] Interview prep, completed summaries, and raw transcripts are separated
- [ ] Generated artifacts are not treated as canonical unless marked final/submitted
- [ ] Runtime byproducts are not committed
- [ ] Knowledge lint run on changed Markdown files when proposals, policies, skills, workflows, templates, or canonical notes are changed
- [ ] Public repo extraction is privacy-safe
- [ ] Final report lists unresolved questions

## Final Reporting Format
End every run with:
1. Mode used
2. What was inspected
3. Bloat patterns found
4. Proposal file created or updated
5. Files modified or moved, if any
6. Delete candidates awaiting approval
7. Human-review items
8. Public Max OS improvements identified
9. Recommended next action
