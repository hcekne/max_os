---
type: workflow
status: active
owner:
review_cycle: monthly
tags: [workflow, html, artifact, safety]
---

# Workflow - HTML Artifact Review

## Goal
Review an HTML artifact or worklet for usefulness, provenance, and safety before approving, sharing, or using it in a harness.

## Inputs
- HTML artifact or worklet file
- Companion manifest, if present
- Listed canonical source files
- Intended use case and audience

## Related Policies
- [[00_System/Document Model]]
- [[00_System/Rendering Policy]]
- [[00_System/Artifact Safety Policy]]
- [[Skill - Review HTML Artifact Safety]]

## Steps
1. Confirm the file is an artifact or worklet, not canonical memory.
2. Read the companion manifest or create one from the appropriate template.
3. Check top-of-file metadata for source files, generated date, generator, and approval status.
4. Verify the artifact accurately reflects listed Markdown sources.
5. Review for secrets, hidden instructions, external dependencies, scripts, forms, storage, and network calls.
6. Decide whether the file can be approved, needs revision, or should be archived.
7. If the artifact reveals needed source changes, record them as a Markdown proposal.
8. Update the manifest review fields with reviewer, date, decision, and constraints.

## Outputs
- Reviewed artifact or worklet
- Updated manifest
- Safety review notes
- Optional Markdown proposal for canonical source updates

## Quality checklist
- [ ] Markdown source remains canonical.
- [ ] Metadata and manifest are complete.
- [ ] Safety review is complete.
- [ ] Approval status is accurate.
- [ ] Any source updates are explicit proposals or approved edits.
- [ ] File can be removed without losing canonical truth.

## Automation opportunities
- Run [[Skill - Review HTML Artifact Safety]] before human approval.
- Generate missing manifests from templates.
- Produce a Markdown proposal from reviewed artifact findings.
