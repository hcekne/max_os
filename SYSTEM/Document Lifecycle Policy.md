---
type: policy
status: active
created: 2026-05-16
review_cycle: quarterly
tags: [policy, lifecycle, hygiene, files, metadata]
---

# Document Lifecycle Policy

## Purpose
Define the lifecycle decision model for files in Max OS.

## Lifecycle Model
- `active` = current operating surface.
- `archive` = no longer active, but still useful for history or retrieval.
- `rubbish bin` = no longer active, low-value, and likely deleteable after a short hold.
- `git history` = the preservation layer behind all of the above.
- If classification is unclear, do not move the file. Mark it as `NEEDS_HUMAN_REVIEW` in a proposal.

## Lifecycle Metadata
Use YAML frontmatter when it improves later cleanup judgment. Do not add lifecycle metadata blindly to every file.

Recommended lifecycle fields:

```yaml
status:
lifecycle:
canonical:
version_family:
supersedes:
superseded_by:
valid_until:
review_after:
archive_after:
delete_after:
retention_policy:
confidentiality:
```

Add normal note metadata separately as needed.

## Allowed Lifecycle Values
- `evergreen` - lasting reference material.
- `active` - currently relevant working material.
- `temporary` - working, scratch, generated, or task-specific material.
- `expired` - tied to a date, meeting, phase, or event that has passed.
- `superseded` - replaced by a newer, final, or canonical file.
- `archive` - historically useful but no longer active.
- `delete_candidate` - likely removable after the rubbish-bin hold period.

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
- `delete_after_review` - eligible for deletion through the rubbish-bin purge path.
- `preserve_final_only` - retain final/submitted file and retire intermediates.
- `preserve_canonical_only` - retain canonical file and retire duplicates or old working versions.

## Allowed Confidentiality Values
- `private`
- `client_confidential`
- `internal`
- `public_template_safe`

## When to Add Metadata
Add lifecycle metadata when it improves future agent judgment, especially for event prep, draft deliverables, temporary research, project-specific scratch files, files with obvious expiry dates, and files with many versions.

For version families, add `version_family` when the relationship may stop being obvious after later restructuring from a single file into a folder or bundle.

## Classification Rules
- Keep a file active when it is current, canonical, final, or still needed for execution.
- Archive a file when it is no longer active but still useful for history, reasoning, retrieval, or later review.
- Use the rubbish bin when a file is clearly superseded, stale, low-value, and likely safe to purge after a short hold.
- Final deliverables, client-provided source material, contracts, invoices, submitted documents, and legal or commercial files are high-retention by default.
- If a file is ambiguous, do not force classification. Keep it active or propose `NEEDS_HUMAN_REVIEW`.

## Common Metadata Patterns
- Mark canonical files with `status: canonical`, `lifecycle: active`, and `canonical: true` when useful.
- Mark final deliverables with `status: final` and `retention_policy: keep`.
- Use `valid_until` or `archive_after` for date-bound prep.
- Use `superseded_by` and `delete_after` when retiring old versions into the rubbish bin.
- Use `retention_policy: preserve_canonical_only` or `preserve_final_only` for obvious version families.

## Policy Boundaries
- Use [[SYSTEM/Archive Policy]] for archive structure and archive moves.
- Use [[SYSTEM/Rubbish Bin Policy]] for bin guardrails and purge rules.
- Use [[SYSTEM/Git Preservation Policy]] for Git-specific cleanup behavior.
