---
type: session-log
status: active
tags: [system, log, append-only]
---

# Session Log

Append-only log of agent / human sessions against the vault. Maintained separately from [[System State]] so the state file stays a small, scannable checkpoint header. See [[00_System/AI Actor & Memory Model]] for how this serves as episodic memory.

## How to use
- Append one bullet per session at the bottom, dated `YYYY-MM-DD:`.
- Never rewrite or compact past entries — Git is the history layer.
- Canonical review dates live in [[System State]]; this log is the narrative trail.
- For monthly / quarterly / yearly summaries, link from the relevant planning note in `09_Planning/`.

## Log
- YYYY-MM-DD: Workspace initialised from the public Max OS template.
