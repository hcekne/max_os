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

# Lifecycle Metadata Template

Use this template as a frontmatter reference for files that need explicit lifecycle management.

## Field Notes
- `status`: draft, active, canonical, superseded, expired, archived, final
- `lifecycle`: evergreen, active, temporary, expired, superseded, archive, delete_candidate
- `canonical`: true/false
- `supersedes`: file(s) this replaces
- `superseded_by`: file that replaces this one
- `retention_policy`: keep, review, archive, delete_after_review, preserve_final_only, preserve_canonical_only
- `confidentiality`: private, client_confidential, internal, public_template_safe
