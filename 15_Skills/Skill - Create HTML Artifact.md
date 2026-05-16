---
type: skill
status: active
tags: [skill, html, artifact, rendering]
---

# Skill - Create HTML Artifact

## Purpose
Create a static, self-contained HTML artifact from canonical Markdown or approved source material without replacing the Markdown source of truth.

## Trigger
Use this skill when the user asks for a rich visual artifact, briefing, dashboard, preview, or shareable HTML view based on Max OS content.

## Inputs
- Canonical source Markdown files or explicitly provided source material
- Desired artifact purpose and audience
- Optional output filename under `05_Content/Artifacts/`
- Optional approval status

## Steps
1. Read [[00_System/Document Model]], [[00_System/Rendering Policy]], and [[00_System/Artifact Safety Policy]].
2. Identify the canonical source files and preserve their wiki-links in the artifact metadata.
3. Confirm the output belongs in `05_Content/Artifacts/` and does not replace a Markdown note.
4. Start from `99_Templates/TPL - HTML Artifact.html` unless a better existing artifact is provided.
5. Create a self-contained HTML file with semantic structure, accessible headings, readable contrast, and no remote dependencies by default.
6. Add metadata at the top of the HTML file: source files, generated date, generator, approval status, and manifest path if any.
7. Create or update an artifact manifest from `99_Templates/TPL - Artifact Manifest.md` when the artifact is meaningful enough to track.
8. If the artifact suggests canonical changes, write them as a Markdown proposal instead of changing source notes silently.

## Outputs
- HTML artifact in `05_Content/Artifacts/`
- Optional artifact manifest next to the HTML file
- Optional Markdown proposal for canonical updates

## Quality Checks
- [ ] Markdown source files remain canonical.
- [ ] HTML metadata identifies source files, generated date, generator, and approval status.
- [ ] Artifact is self-contained or dependencies are justified in the manifest.
- [ ] No secrets are present.
- [ ] Artifact can be deleted without losing canonical truth.
- [ ] Any source-note changes are proposed or explicitly approved.

## Safety Notes
- Treat generated HTML as untrusted until reviewed.
- Do not include credentials, private tokens, hidden prompts, or unnecessary sensitive data.
- Prefer no JavaScript for static artifacts.
- Use sandboxed rendering when a harness displays the artifact.
