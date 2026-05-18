---
type: policy
status: active
created: 2026-05-16
review_cycle: quarterly
tags: [policy, archive, hygiene, files]
---

# Archive Policy

## Purpose
Define when and how Max OS moves material out of active folders without losing useful historical context.

## Archive Instead of Delete When
- The file has historical value but is no longer actively used.
- The file records reasoning, decisions, prep, or context that may help future review.
- The file is a previous phase artifact for an active project.
- The file is a superseded draft that may still explain how the final version was created.
- The file is an event-specific artifact whose event has passed.

## Delete Only After Approval When
- The file is generated scratch material.
- The file is an obsolete duplicate of a canonical or final file.
- The file is a broken extraction, temporary export, or stale intermediate.
- The file is non-canonical, non-final, and preserved in Git history.

Deletion always requires explicit human approval unless a future policy says otherwise for a narrow automated path.

## Archive Locations
Use the smallest archive scope that preserves context:

- Project-specific files: `04_Projects/<Project Name>/90_Archive/` or existing project `Archive/`.
- Versioned deliverables: `04_Projects/<Project Name>/90_Archive/Draft Versions/` or an existing project archive.
- Expired interview prep: `04_Projects/<Project Name>/90_Archive/Interview Prep/`.
- Generated packs: `04_Projects/<Project Name>/90_Archive/Generated Packs/` when no longer active.
- General notes: `11_Notes/Archive/`.
- Todos: `08_Todos/Completed/` for completed todos, or archive folder if obsolete.
- Content drafts: archive under the relevant content folder when a canonical/final version exists.
- System proposals: `00_System/Proposals/`.

Existing project archive folders may be kept. New projects should prefer numbered folders if adopting a structured project layout.

## Archive Indexes
Each significant archive folder should eventually have an `Archive Index.md` that records:
- archive period
- project or domain
- files archived
- why archived
- canonical replacement, if any
- retrieval notes
- related commits

## Avoid Unusable Archives
Do not dump every stale file into one flat archive forever.

Archive structure should preserve enough context to retrieve material:
- by project
- by phase
- by month/quarter
- by deliverable
- by event type where useful

## Archive Process
1. Check `git status`.
2. Confirm there are no unrelated uncommitted changes, or recommend committing first.
3. Classify candidate files.
4. Create/update cleanup proposal.
5. Get approval for non-trivial moves.
6. Use `git mv` for moves.
7. Add lifecycle metadata where useful.
8. Update archive index and canonical project links.
9. Review `git diff`.
10. Commit with a clear cleanup message when approved.

## Special Archive Cases

### Versioned Deliverables
- Keep the final/submitted file visible or clearly linked.
- Archive intermediate numbered versions once the final version is confirmed.
- Preserve enough context to reconstruct the draft path through Git and archive index notes.

### Interview Packs
- Keep current/upcoming interview prep active.
- Move expired prep to archive after the interview date.
- Keep completed interview summaries where the active project can find them during synthesis.
- Move raw transcripts out of inbox root after processing.

### Generated Packs
- Archive generated HTML/PDF/DOCX packs when they are no longer the current output.
- Do not treat generated HTML as canonical source.
- Keep build scripts only when they are needed to regenerate a final or useful artifact.
