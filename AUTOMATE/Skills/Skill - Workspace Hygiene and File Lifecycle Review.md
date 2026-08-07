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
- Workspace hygiene proposal in `SYSTEM/Proposals/`
- File classification table
- Canonical file recommendations
- Archive/rubbish-bin/delete/merge candidates
- Lifecycle metadata recommendations
- Optional safe archive moves or metadata updates, depending on mode
- Public Max OS improvement proposal when reusable patterns are found

## Operating Modes

### PLAN_ONLY
Inspect the workspace and create a cleanup proposal. Do not move, delete, rename, or rewrite existing files.

### APPLY_SAFE
Apply only safe, reversible, non-destructive changes:
- create central archive or rubbish-bin folders;
- create proposal files;
- create archive or rubbish-bin indexes;
- add lifecycle metadata where obvious;
- move clearly expired files into the central archive using `git mv`;
- move clearly superseded low-value versions into the central rubbish bin using `git mv`.

Do not delete files.

### APPLY_APPROVED
Only after explicit human approval, apply agreed archive moves, metadata updates, canonical renames, and deletions.

Rubbish-bin purge is the only exception: files already in the central rubbish bin may be deleted once they satisfy the Rubbish Bin rules in [[SYSTEM/Policy]].

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
version_family:
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
1. Inspect the vault root for stray markdown files outside the allowed control-file set, especially empty files and domain mirror files.
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
8. Create a proposal before applying changes.

Root-level empty markdown placeholders and domain mirror files should default to `DELETE_CANDIDATE` unless they contain meaningful content that clearly belongs elsewhere.

## Archive Process
1. Identify high-confidence archive candidates.
2. Confirm they are not final deliverables, legal/commercial documents, invoices, contracts, or client-provided source materials.
3. Identify archive destination.
4. If applying, create archive folder and archive index first.
5. Use `git mv` for moves into `SYSTEM/Cleaning/Archive/`.
6. Add metadata such as `status: archived`, `lifecycle: archive`, `superseded_by`, and `retention_policy` where useful.
7. Update canonical indexes and project state links.

## Rubbish-Bin Process
1. Identify clearly superseded, low-value, or stale version files.
2. Confirm a current canonical replacement exists.
3. Confirm the file is not final, submitted, client-provided, legal, or commercial.
4. Move it into `SYSTEM/Cleaning/Rubbish Bin/` using a mirrored source path.
5. Add `delete_after` and `superseded_by` where useful.
6. Update any active links that should now point to the current canonical version.

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
3. Recommend one clean canonical family stem.
4. Move old versions to the rubbish bin by default, or to the archive if they have explicit historical value.
5. Merge useful content into canonical file before retiring old files.
6. Add `canonical: true` and `version_family` to the current file when useful.
7. Add `superseded_by` to old versions when useful.

## Project-Folder Hygiene Logic
Use existing project patterns where they work. If a folder is bloated or ambiguous, recommend a structure such as:

```text
KNOWLEDGE/Projects/<Project Name>/
  00_Project State.md
  01_Current/
  02_Working/
  03_Research/
  04_Deliverables/
  05_Meetings/
  06_Decisions/
```

Do not impose this globally if a lighter structure is enough.

## Public-Template Extraction Logic
When a hygiene run reveals reusable Max OS improvements:
1. Extract the generic pattern only.
2. Remove private names, client details, confidential numbers, and internal-only facts.
3. Prefer policies, templates, skill improvements, and workflow rules.
4. Create a privacy-safe proposal under `SYSTEM/Proposals/`.
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
find KNOWLEDGE/Projects -type f | rg -i '(v[0-9]+|draft|final|latest|old|copy|prep|interview|memo|research)'
find KNOWLEDGE/Projects/<Project Name> -type f -printf '%s %p\n' | sort -nr
git mv "old/path.md" "SYSTEM/Cleaning/Archive/KNOWLEDGE/Projects/<Project Name>/old/path.md"
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
- [ ] Archive or rubbish-bin destinations proposed
- [ ] Metadata updates are targeted, not blanket-applied
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
