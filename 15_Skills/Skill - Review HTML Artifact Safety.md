---
type: skill
status: active
tags: [skill, html, artifact, worklet, safety, review]
---

# Skill - Review HTML Artifact Safety

## Purpose
Review an HTML artifact or worklet for safety, provenance, and canonical-source integrity before it is approved or shared.

## Trigger
Use this skill when the user asks to review, approve, publish, share, or run an HTML artifact or worklet.

## Inputs
- HTML artifact or worklet file
- Companion manifest, if present
- Canonical source files listed in metadata or manifest
- Intended viewing context, including any harness permissions

## Steps
1. Read [[00_System/Artifact Safety Policy]] and [[00_System/Rendering Policy]].
2. Inspect the top-of-file HTML metadata and any companion manifest.
3. Verify source files, generated date, generator, and approval status are present.
4. Check that the HTML does not contain secrets, tokens, credentials, or unnecessary sensitive data.
5. Review scripts, event handlers, forms, storage usage, iframes, network calls, and remote dependencies.
6. Confirm any risky behavior is necessary, visible, and documented in the manifest.
7. Confirm the file does not silently overwrite canonical Markdown or claim to be canonical truth.
8. If the artifact proposes note changes, ensure they are represented as Markdown proposals.
9. Return a safety finding with approval recommendation and required fixes.

## Outputs
- Safety review summary
- Required fixes, if any
- Approval recommendation: approve, approve with constraints, revise, or reject
- Optional updated manifest review fields

## Quality Checks
- [ ] Metadata is present and consistent with the manifest.
- [ ] No secrets are present.
- [ ] External dependencies are absent or justified.
- [ ] Scripts and event handlers are reviewed.
- [ ] Forms, storage, and network calls are absent or justified.
- [ ] Canonical Markdown remains the source of truth.
- [ ] Harness sandboxing requirements are stated.

## Safety Notes
- Treat the HTML as untrusted during review.
- Do not execute unknown scripts when static inspection is enough.
- Do not copy secrets from source Markdown into generated HTML.
- Prefer sandboxed preview with minimal permissions.
