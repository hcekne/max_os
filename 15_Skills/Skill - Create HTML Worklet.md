---
type: skill
status: active
tags: [skill, html, worklet, module, json-state]
---

# Skill - Create HTML Worklet

## Purpose
Create a small interactive HTML worklet that supports a specific task while keeping canonical Max OS memory in Markdown.

## Trigger
Use this skill when the user asks for an interactive panel, local tool, guided form, calculator, review surface, or harness-rendered worklet.

## Inputs
- Worklet purpose and target workflow
- Canonical source Markdown files, if any
- Input and output contract
- Optional JSON state shape
- Optional output filename under `20_Modules/Worklets/`

## Steps
1. Read [[00_System/Document Model]], [[00_System/Rendering Policy]], [[00_System/Artifact Safety Policy]], and [[00_System/Worklet Conventions]].
2. Confirm the worklet belongs in `20_Modules/Worklets/` and remains optional.
3. Define the input contract, output contract, and whether JSON state is needed.
4. Start from `99_Templates/TPL - HTML Worklet.html` unless a more specific existing worklet is provided.
5. Keep the HTML self-contained unless the manifest justifies external dependencies.
6. Add top-of-file metadata: source files, generated date, generator, approval status, state files, and manifest path.
7. Create a worklet manifest from `99_Templates/TPL - Worklet Manifest.md`.
8. Make any canonical-note edits a proposal output unless the user explicitly approves applying them.
9. If a harness runtime is used, document optional APIs and requested permissions in the manifest.

## Outputs
- HTML worklet in `20_Modules/Worklets/`
- Worklet manifest next to the HTML file
- Optional JSON state example or schema
- Optional Markdown proposal for canonical updates

## Quality Checks
- [ ] Worklet does not require Max OS to become an application repo.
- [ ] Markdown source files remain canonical.
- [ ] Inputs, outputs, and state are documented.
- [ ] JSON is used for structured runtime state when needed.
- [ ] No secrets are present.
- [ ] Harness permissions are optional or explicitly documented.
- [ ] Proposed canonical changes are exported for review.

## Safety Notes
- Treat worklet HTML as untrusted until reviewed.
- Keep JavaScript narrowly scoped to local interaction.
- Avoid network calls and remote dependencies by default.
- Use sandboxed rendering in a harness.
