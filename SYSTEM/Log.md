---
type: log
status: active
tags: [system, log, append-only]
---

# Log

Append-only episodic record of what happened in this workspace.

- Append one dated bullet (`- YYYY-MM-DD: ...`) after meaningful work, with
  `[[wiki-links]]` to the notes touched. Batch small related runs into one
  bullet; skip trivial read-only sessions.
- Never rewrite or compact past entries. Git is the history layer; this file
  is the recall layer an agent can search.
- The nightly consolidation routine (when enabled) reads new entries here and
  curates durable lessons into `SYSTEM/Memory.md`.

## Entries

- YYYY-MM-DD: Workspace initialised from the Max OS template.
