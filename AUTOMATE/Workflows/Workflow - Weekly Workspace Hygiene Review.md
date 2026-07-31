---
type: workflow
status: active
owner:
review_cycle: weekly
tags: [workflow, workspace-hygiene, lifecycle, archive, git]
---

# Workflow - Weekly Workspace Hygiene Review

## Purpose
Make workspace hygiene a recurring Max OS operating loop so active folders stay focused and Git preserves full history.

## Related Skill
- [[Skill - Workspace Hygiene and File Lifecycle Review]]

## Recommended Cadence

### Hourly / Daily Agent Scans
- Detect possible bloat signals.
- Summarize new files.
- Flag missing lifecycle metadata on obvious temporary/event-specific files.
- Do not move or delete files.

### Weekly Hygiene Review
- Run [[Skill - Workspace Hygiene and File Lifecycle Review]] in `PLAN_ONLY`.
- Classify recent files.
- Scan `SYSTEM/` control files for client- or project-specific instructions that should live in project notes, historical logs, or [[SYSTEM/Recurring Operations]] instead.
- Identify expired or superseded material.
- Propose archive and rubbish-bin actions.
- Recommend targeted lifecycle metadata updates.

### Monthly Deep Cleanup
- Review large project and content folders.
- Clean version bloat.
- Archive old phases.
- Purge rubbish-bin items past their retention window.
- Identify canonical files.
- Prepare cleanup commit plan.

### Project Closeout Review
- Preserve final deliverables.
- Archive working drafts.
- Update project state.
- Extract reusable lessons.
- Propose public Max OS improvements.

### Pre-Deliverable Review
- Confirm canonical draft.
- Move scratch/generated variants out of the active surface.
- Ensure final export path is clear.
- Protect source materials and final deliverables.

### Post-Major-Milestone Review
- Archive expired meeting prep and phase-specific plans.
- Update project state with final decisions and next phase.
- Identify merge candidates and delete candidates.

## Inputs
- Current date
- `git status --short --branch`
- Recent commits
- Target project or workspace scope
- Existing proposal files, if any
- Current active project state files

## Outputs
- Hygiene proposal in `SYSTEM/Proposals/`
- File classification table
- Suggested archive/rubbish/delete/merge actions
- Lifecycle metadata recommendations
- Updated project state recommendations
- Public-template improvement proposal when relevant

## Steps
1. Check Git status and branch.
2. If there are uncommitted changes, warn the user and recommend committing before any cleanup.
3. Run a lightweight bloat scan:
  - vault-root markdown files outside the allowed control-file set;
   - file counts by top-level folder;
   - largest project folders;
   - filename bloat patterns;
   - recent files;
   - old files;
   - archive/proposal folder presence.
4. Scan `SYSTEM/` control files for stale client- or project-specific references in global instructions.
5. Pick one or two high-bloat folders for detailed review.
6. Classify files using the taxonomy in [[Skill - Workspace Hygiene and File Lifecycle Review]].
7. Identify canonical files and final deliverables.
8. Identify high-confidence archive candidates.
9. Identify high-confidence rubbish-bin candidates.
10. Identify merge candidates and delete candidates.
11. Create or update a proposal in `SYSTEM/Proposals/`.
12. Do not apply moves or deletions unless the user explicitly requests `APPLY_SAFE` or `APPLY_APPROVED`, except for the narrow rubbish-bin purge path.

## Human Approval Points
- Moving final deliverables
- Moving contracts, invoices, legal/commercial files, or client-provided source materials
- Deleting any file
- Modifying canonical project state
- Public repo changes
- Remote pushes

## Git Commit Pattern
Recommended private workspace commit message:

```text
Add workspace hygiene and lifecycle management
```

For later cleanup operations, use focused messages:
- `Archive expired project prep files`
- `Add lifecycle metadata to draft deliverables`
- `Clean content draft version bloat`

## Metrics to Track
- Total files by major folder
- Number of files in high-bloat project folders
- Number of active draft/version files
- Number of archive candidates
- Number of delete candidates awaiting approval
- Number of canonical files identified
- Number of files needing human review
- Number of public-template improvements identified

## Project State Updates
When a project is reviewed:
- Update the project note with current canonical deliverables.
- Move stale links into an archive section.
- Add a "Current Operating Surface" section if the project folder is complex.
- Record unresolved questions and next review date.

## Public Max OS Improvements
During each monthly or project-closeout review, ask:
- Is this a reusable Max OS pattern?
- Can it become a skill, workflow, template, policy, or AGENTS.md rule?
- Can it be generalized without private context?
- Should it be proposed for the public Max OS repo?

## Future Harness Integration

```text
hourly:
  - scan recent changes
  - detect bloat signals
  - flag potential expiry/review candidates

daily:
  - summarise new files
  - identify files missing lifecycle metadata
  - update lightweight hygiene observations

weekly:
  - run Workspace Hygiene and File Lifecycle Review in PLAN_ONLY mode
  - create or update a hygiene proposal
  - notify the principal of archive/delete candidates

monthly:
  - run deeper review of high-bloat folders
  - propose archive moves
  - identify canonical files
  - prepare cleanup commit

project_closeout:
  - preserve final deliverables
  - archive working drafts
  - update project state
  - extract reusable lessons
  - propose public Max OS improvements
```

The harness may only auto-delete files already in `SYSTEM/Cleaning/Rubbish Bin/` when [[SYSTEM/Rubbish Bin Policy]] allows it.
