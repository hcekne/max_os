# Worklet Conventions

Worklets are optional interactive HTML tools inside Max OS.

They support richer task interfaces while preserving the Markdown-first system.

## Placement

Store worklets in `20_Modules/Worklets/`.

Recommended structure:

```text
20_Modules/Worklets/
  Worklet - Topic.html
  Worklet Manifest - Topic.md
  Worklet - Topic.state.example.json
```

Use a folder per worklet only when the worklet has multiple files.

## Worklet Manifest

Each meaningful worklet should have a manifest that records:
- purpose
- source files
- input contract
- output contract
- state files, if any
- generator or maintainer
- approval status
- safety notes
- optional harness permissions

Start from `99_Templates/TPL - Worklet Manifest.md`.

## Runtime Boundary

A worklet may run in two modes:

1. Standalone mode: opens as self-contained HTML.
2. Harness mode: receives optional data from a rendering harness.

Harness mode must be optional unless the manifest says otherwise. A worklet should not require Max OS to become an application repo.

## State

Use JSON for worklet state.

State files should:
- be explicit and inspectable
- point back to canonical Markdown sources when relevant
- avoid secrets
- be safe to regenerate when derived
- not replace notes, plans, goals, workflows, or system state

Use YAML frontmatter only for Markdown manifests and notes.

## Outputs

Worklets can produce:
- visual views
- filtered summaries
- local calculations
- Markdown proposals
- JSON state updates

Worklets must not silently rewrite canonical Markdown. If a worklet suggests edits, export them as a proposal that a human or approved agent applies separately.

## HTML Conventions

- Keep worklets self-contained when practical.
- Use semantic HTML and accessible labels.
- Include metadata comments at the top.
- Avoid remote dependencies by default.
- Keep JavaScript narrowly scoped to local interaction.
- Name buttons and controls by their action.
- Provide visible fallback content if JavaScript fails.

## Optional Harness Contract

If a harness is available, a worklet may read optional runtime data from `window.MaxOSRuntime`.

The manifest must document:
- expected inputs
- produced outputs
- requested permissions
- whether network access is needed
- whether persistent state is used

No worklet should assume that harness runtime exists unless it is explicitly designed only for harness use.
