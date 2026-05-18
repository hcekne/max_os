---
type: policy
status: active
created: 2026-05-16
review_cycle: quarterly
tags: [policy, lifecycle, hygiene, files, metadata]
---

# Document Lifecycle Policy

## Purpose
Keep the active Max OS workspace focused on current operating material while preserving historical context through archive folders and Git history.

## Core Principle
Active workspace = current operating surface.
Archive = historically useful but not actively needed.
Git history = full preservation layer.
Lifecycle metadata = structured expiry and review logic.
Agent hygiene skill = recurring cleanup intelligence.

## Lifecycle Metadata
Use YAML frontmatter for files where lifecycle state matters. Do not add metadata blindly to every note.

Recommended schema:

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

## Allowed Lifecycle Values
- `evergreen` - lasting reference material that remains useful beyond the original project or event.
- `active` - currently relevant working material.
- `temporary` - working, scratch, generated, or task-specific material with expected expiry.
- `expired` - tied to a date, meeting, phase, or event that has passed.
- `superseded` - replaced by a newer, final, or canonical file.
- `archive` - historically useful but no longer part of the active operating surface.
- `delete_candidate` - likely removable after explicit approval because Git preserves history and no active/final value remains.

## Allowed Status Values
- `draft`
- `active`
- `canonical`
- `superseded`
- `expired`
- `archived`
- `final`

## Allowed Retention Policies
- `keep` - retain indefinitely in active or archive location.
- `review` - review on or after a specified date.
- `archive` - move out of active surface when no longer current.
- `delete_after_review` - eligible for deletion only after explicit approval.
- `preserve_final_only` - retain final/submitted file and retire intermediates.
- `preserve_canonical_only` - retain canonical file and retire duplicates or old working versions.

## Allowed Confidentiality Values
- `private`
- `client_confidential`
- `internal`
- `public_template_safe`

## When to Add Metadata
Add lifecycle metadata when it improves future agent judgment, especially for:
- event prep
- meeting prep
- draft deliverables
- versioned deliverable packs
- generated HTML, PDF, and DOCX exports
- build scripts and support files for generated packs
- interview prep and completed interview summaries
- temporary research
- project-specific scratch files
- files with obvious expiry dates
- files with many versions
- files likely to be superseded

## Classification Rules
- Canonical files should be marked `status: canonical`, `lifecycle: active`, and `canonical: true` where useful.
- Final deliverables should be marked `status: final`, `retention_policy: keep`, and should not be moved or deleted without explicit approval.
- Event prep should have `valid_until` or `archive_after` based on the event date.
- Draft series should identify the current/canonical version and mark older drafts as `superseded` before archiving.
- Client-provided files, contracts, invoices, submitted documents, legal/commercial files, and final deliverables are high-retention by default.
- If classification is uncertain, use `NEEDS_HUMAN_REVIEW` in proposals rather than changing the file.

## Versioned Deliverables
Versioned deliverables should not all remain active indefinitely.

Recommended handling:
- mark the current/final version as canonical or final;
- preserve final/submitted files with `retention_policy: keep`;
- archive older numbered versions once the canonical/final version is confirmed;
- mark older drafts with `superseded_by` where useful;
- treat generated exports (`.docx`, `.pdf`, `.html`) as outputs from canonical Markdown unless explicitly submitted as final deliverables.

## Interview and Event Materials
Interview and event files should be lifecycle-aware:
- upcoming prep can stay active until the event date;
- expired prep should be archived after the meeting;
- completed interview summaries can stay active while synthesis is underway;
- raw transcripts should move out of inbox root after processing;
- generated interview packs should be archived or kept with the relevant project phase, not left as loose root files.

## Generated Artifact Lifecycle
Generated files are useful, but they should not obscure canonical Markdown.

Use these defaults:
- Markdown source and project state remain canonical.
- HTML/PDF/DOCX exports are generated unless marked final/submitted.
- Build scripts and CSS used for generated packs should live with the pack or in a tooling folder.
- Python bytecode and runtime cache files should never be committed.
- Generated scratch experiments should be delete candidates after review.

## Agent Responsibilities
Agents should:
1. Prefer updating canonical files over creating uncontrolled new versions.
2. Mark temporary and event-specific files with expiry or review metadata when useful.
3. Propose archive/delete actions before applying them.
4. Use Git as the preservation layer, not as an excuse for uncontrolled active-folder bloat.
5. Never delete files without explicit approval.
