# Artifact Safety Policy

HTML artifacts and worklets are useful, but they are not trusted memory.

Treat generated HTML as untrusted unless it has been reviewed for safety and approved for a specific use.

## Core Rules

- Do not include secrets in HTML.
- Do not include API keys, tokens, credentials, private URLs, or hidden operational instructions.
- Do not silently overwrite canonical Markdown based on generated HTML.
- Do not treat rendered output as more authoritative than the source files.
- Prefer self-contained HTML with no external network calls.
- Use sandboxed rendering when viewed in a harness.
- Keep edits minimal, factual, linked, and reversible.

## Untrusted Behaviors

Review carefully before approving HTML that contains:
- `<script>` tags
- event handlers such as `onclick`
- forms
- iframes
- external images, fonts, scripts, stylesheets, or analytics
- storage APIs such as `localStorage`, `sessionStorage`, or IndexedDB
- network APIs such as `fetch`, WebSockets, or beacon requests
- file upload controls

These features are not banned, but they require a clear purpose, visible disclosure, and a manifest entry.

## Safe Defaults

For static artifacts:
- no JavaScript by default
- no remote dependencies by default
- no hidden tracking
- no secrets or unnecessary sensitive personal data
- source metadata visible in comments and manifest

For worklets:
- JavaScript may be used for local interaction
- state should be local JSON or harness-provided runtime state
- output should be a proposal unless a human explicitly approves applying changes
- any harness access should be optional and documented

## Harness Rendering

When a harness renders HTML, prefer:
- sandboxed iframe rendering
- no same-origin privilege unless required
- no network access unless explicitly approved
- explicit import/export boundaries
- visible source and approval metadata

Suggested iframe baseline:

```html
<iframe sandbox="allow-scripts" title="Max OS artifact preview"></iframe>
```

Only add more sandbox permissions when the worklet manifest explains why.

## Safety Review Checklist

- [ ] Source files are identified.
- [ ] Generated date and generator are identified.
- [ ] Approval status is present.
- [ ] No secrets are present.
- [ ] External dependencies are absent or justified.
- [ ] Scripts are absent or reviewed.
- [ ] Forms and network calls are absent or justified.
- [ ] Any proposed canonical changes are represented as Markdown proposals.
- [ ] The file can be deleted without losing canonical truth.
