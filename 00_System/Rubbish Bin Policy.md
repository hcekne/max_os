---
type: policy
status: active
created: 2026-05-18
review_cycle: quarterly
tags: [policy, rubbish-bin, hygiene, deletion, versions]
---

# Rubbish Bin Policy

## Purpose
Define the short-retention path for files that are clearly stale, superseded, and likely safe to delete soon.

Use [[00_System/Document Lifecycle Policy]] for classification. This file defines what the rubbish-bin path means and when purge is allowed.

## Use Rubbish Bin For
- older draft versions in a clear version family;
- stale intermediate exports;
- superseded scratch or generated material;
- redundant copies that are preserved in Git and replaced by a current canonical version;
- processed raw captures that no longer belong in active inbox folders.

## Do Not Use Rubbish Bin For
- final deliverables;
- client-provided source materials;
- contracts, invoices, legal/commercial documents;
- evergreen reference material;
- files whose status is still materially unclear.

## Structure
- Root: `16_Cleaning/Rubbish Bin/`
- Mirror the source path beneath that root so origin context stays obvious.

Example:

```text
05_Content/Article - Topic - v02.md
-> 16_Cleaning/Rubbish Bin/05_Content/Article - Topic - v02.md
```

## Metadata
When useful, add or update:

```yaml
status: superseded
lifecycle: delete_candidate
superseded_by:
delete_after:
retention_policy: delete_after_review
```

Use `delete_after` as the purge date. Default window: 30 days from the move into the rubbish bin unless a different window is explicitly justified.

## Purge Rule
Files already in `16_Cleaning/Rubbish Bin/` may be deleted when all of the following are true:
- `delete_after` is on or before today, or the file has sat in the rubbish bin for more than 30 days;
- the file is not canonical, final, client-provided, legal, commercial, evergreen reference, or otherwise high-retention;
- Git history already preserves it when it was previously tracked;
- no active note still depends on that exact file path.

This is the only allowed auto-delete path, and future harnesses must keep it narrow.

## Review Cadence
- Weekly hygiene: identify new rubbish-bin candidates.
- Monthly review: purge rubbish-bin items whose retention window has expired.
- Project closeout: move obvious stale drafts straight to the rubbish bin instead of keeping them in active folders.

## Human Review Boundary
If a file is ambiguous, keep it out of the rubbish bin and classify it as `NEEDS_HUMAN_REVIEW` or archive it instead.
