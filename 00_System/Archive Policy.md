---
type: policy
status: active
created: 2026-05-16
review_cycle: quarterly
tags: [policy, archive, hygiene, files]
---

# Archive Policy

## Purpose
Define the archive-specific path for material that should leave the active workspace but still be kept for history or retrieval.

Use [[00_System/Document Lifecycle Policy]] for classification. This file defines what the archive path means and how to use it.

## Use Archive When
- The file has historical value but is no longer actively used.
- The file records reasoning, decisions, prep, or context that may help future review.
- The file is a previous phase artifact for an active project.
- The file is a superseded draft that may still explain how the final version was created.
- The file is an event-specific artifact whose event has passed.

## Do Not Use Archive When
- The file is clearly stale, superseded, and low-value enough for the rubbish bin.
- The file is still current and belongs in the active workspace.
- The file is ambiguous enough that it still needs human review.

## Archive Structure
- Archive root: `16_Cleaning/Archive/`
- Mirror the source path beneath that root so origin context stays obvious.
- Do not create new distributed `Archive/` folders inside active project or content folders.
- Existing distributed archives are legacy surfaces and should be migrated incrementally during later hygiene passes.

Typical structure:

```text
16_Cleaning/Archive/
	04_Projects/<Project Name>/...
	05_Content/<Content Family>/...
	11_Notes/...
```

## Archive Indexing
- `16_Cleaning/Archive/Index.md` should record significant moves and archive conventions.
- Add family- or source-specific indexes only when the folder becomes large enough to need them.

## Archive Move Checklist
1. Check `git status`.
2. Confirm the file belongs in archive rather than the rubbish bin.
3. Use `git mv` into `16_Cleaning/Archive/...`.
4. Add lifecycle metadata when useful.
5. Update important links and archive indexes.
