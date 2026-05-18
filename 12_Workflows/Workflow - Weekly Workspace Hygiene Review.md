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
- Identify expired or superseded material.
- Propose archive actions.
- Recommend targeted lifecycle metadata updates.

### Monthly Deep Cleanup
- Review large project and content folders.
- Clean version bloat.
- Archive old phases into `16_Cleaning/Archive/`.
- Move clear low-retention delete candidates into `16_Cleaning/Rubbish Bin/`.
- Identify canonical files.
- Prepare cleanup commit plan.

### Project Closeout Review
- Preserve final deliverables.
- Archive working drafts.
- Update project state.
- Move low-value generated scratch to the rubbish bin when policy allows.
- Extract reusable lessons.
- Propose public Max OS improvements.

### Deliverable-Pack Review
- Identify the final/submitted deliverable.
- Move older numbered drafts and generated exports out of active root.
- Preserve build scripts, source sections, and final outputs with clear index notes.
- Confirm generated HTML/PDF/DOCX files do not become canonical truth.

### Interview-Pack Review
- Separate upcoming interview prep, completed interview notes, raw transcripts, and generated Word/PDF packs.
- Archive expired prep after the interview date.
- Keep completed interview summaries linked from the project state.
- Route raw transcripts out of inbox root after processing.

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
- Hygiene proposal in `00_System/Proposals/`
- File classification table
- Suggested archive/delete/merge actions
- Lifecycle metadata recommendations
- Updated project state recommendations
- Public-template improvement proposal when relevant

## Steps
1. Check Git status and branch.
2. If there are uncommitted changes, warn the user and recommend committing before any cleanup.
3. Run a lightweight bloat scan:
   - file counts by top-level folder;
   - largest project folders;
   - filename bloat patterns;
   - recent files;
   - old files;
   - archive/proposal folder presence.
4. Pick one or two high-bloat folders for detailed review.
5. Classify files using the taxonomy in [[Skill - Workspace Hygiene and File Lifecycle Review]].
6. Identify canonical files and final deliverables.
7. Identify high-confidence archive candidates.
8. Identify merge candidates and delete candidates.
9. Create or update a proposal in `00_System/Proposals/`.
10. Run [[Skill - Knowledge System Lint and Link Check]] on changed Markdown files if the review created or modified system, project, skill, workflow, template, or proposal files.
11. Do not apply moves or deletions unless the user explicitly requests `APPLY_SAFE` or `APPLY_APPROVED`.

## Human Approval Points
- Moving final deliverables
- Moving contracts, invoices, legal/commercial files, or client-provided source materials
- Deleting any file outside the `16_Cleaning/Rubbish Bin/` purge policy
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
- Number of versioned deliverable files by artifact family
- Number of generated HTML/PDF/DOCX files in active roots
- Number of raw inbox captures still sitting in active inbox folders instead of `16_Cleaning/`
- Number of lint errors and warnings on changed Markdown files

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
  - propose rubbish-bin moves for clear delete candidates
  - identify canonical files
  - prepare cleanup commit

project_closeout:
  - preserve final deliverables
  - archive working drafts
  - update project state
  - extract reusable lessons
  - propose public Max OS improvements
```

The harness should never automatically delete files unless explicit future policy allows it.
The only narrow exception is files already in `16_Cleaning/Rubbish Bin/` that satisfy `00_System/Rubbish Bin Policy.md`.
