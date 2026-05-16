# Rendering Policy

Rendering is the process of turning canonical Markdown or structured state into a human-facing view.

Max OS supports rendering, but rendering must not change what is canonical.

## Rendering Targets

### Markdown render
Use normal Markdown rendering for notes, plans, workflows, skills, and daily work.

### HTML artifact
Use an HTML artifact when a static, portable, polished view helps a human review or share information.

Examples:
- executive summary view
- visual briefing
- review dashboard
- content preview
- read-only planning board

Store these in `05_Content/Artifacts/`.

### HTML worklet
Use an HTML worklet when interaction is needed.

Examples:
- guided weekly review panel
- task triage interface
- scenario calculator
- planning board with filters

Store these in `20_Modules/Worklets/`.

## Source Metadata

Every generated HTML file should include metadata identifying:
- source files
- generated date
- generator
- approval status
- related manifest, if any

Use an HTML comment at the top of the file and matching `<meta>` tags when practical.

## Approval Status

Use one of these values:
- `draft`: incomplete or manually edited
- `generated`: produced from source files but not reviewed
- `proposed`: suggests changes to canonical notes
- `approved`: reviewed and accepted for its stated purpose
- `archived`: retained for history only

Approval status describes the artifact or worklet, not the truth of its content.

## Generated vs Canonical

Generated files may quote, summarize, or visualize canonical Markdown. They must not become the only place where a decision, commitment, person fact, project status, goal, or plan is recorded.

If a generated view reveals a needed update, create or apply a Markdown proposal to the canonical note.

## Rendering Requirements

- Prefer self-contained HTML for portability.
- Keep HTML accessible: semantic structure, readable contrast, labels, keyboard-friendly controls, and useful titles.
- Do not require a database.
- Do not require a harness to use Max OS.
- Use sandboxed rendering when a harness displays HTML.
- Keep any harness API optional and documented in the worklet manifest.

## File Placement

- Static HTML artifacts: `05_Content/Artifacts/`
- Interactive HTML worklets: `20_Modules/Worklets/`
- Companion manifests: next to the artifact or worklet, using the relevant manifest template from `99_Templates/`
- Canonical source notes: remain in their normal Markdown folders

## Naming

Use descriptive names that preserve the document type:
- `Artifact - Topic - YYYY-MM-DD.html`
- `Artifact Manifest - Topic - YYYY-MM-DD.md`
- `Worklet - Topic.html`
- `Worklet Manifest - Topic.md`

Avoid replacing existing Markdown names with HTML names.
