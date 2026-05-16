---
type: skill
status: active
tags: [skill, markdown, html, artifact, conversion]
---

# Skill - Convert Markdown to HTML Artifact

## Purpose
Convert a canonical Markdown note or set of notes into a read-only HTML artifact while preserving Markdown as the source of truth.

## Trigger
Use this skill when the user asks to render, convert, preview, package, or share Markdown content as HTML.

## Inputs
- Source Markdown note or notes
- Optional target audience and rendering purpose
- Optional artifact filename under `05_Content/Artifacts/`
- Optional companion manifest request

## Steps
1. Read [[00_System/Document Model]], [[00_System/Rendering Policy]], and [[00_System/Artifact Safety Policy]].
2. Read the source Markdown and preserve factual content without inventing details.
3. Decide whether the output is a static artifact or an interactive worklet. Use a worklet only when interaction is required.
4. Create the HTML artifact in `05_Content/Artifacts/` using `99_Templates/TPL - HTML Artifact.html`.
5. Include source files, generated date, generator, and approval status in top-of-file metadata.
6. Preserve important wiki-link references as visible text or source metadata.
7. Keep the artifact self-contained and accessible.
8. Create an artifact manifest when the artifact will be reused, reviewed, or shared.
9. Leave canonical Markdown unchanged unless the user explicitly asks for a source-note edit.

## Outputs
- Read-only HTML artifact in `05_Content/Artifacts/`
- Optional artifact manifest
- Optional Markdown proposal for source-note improvements discovered during conversion

## Quality Checks
- [ ] Source Markdown remains unchanged unless explicitly approved.
- [ ] Artifact content matches the source and does not invent facts.
- [ ] Metadata identifies source files, generated date, generator, and approval status.
- [ ] Important wiki-links remain visible or traceable.
- [ ] HTML is self-contained or dependencies are justified.
- [ ] No secrets are present.

## Safety Notes
- Generated HTML is untrusted until reviewed.
- Do not embed private data beyond what is necessary for the stated artifact purpose.
- Do not use generated HTML as the basis for silent Markdown updates.
- Use sandboxed rendering in any harness preview.
