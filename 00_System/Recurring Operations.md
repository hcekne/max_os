---
type: control-register
status: active
created: 2026-05-16
review_cycle: monthly
tags: [operations, recurring, control-surface, hygiene]
---

# Recurring Operations

This note is the canonical register for standing operational reminders. Global control files should reference this note instead of hardcoding client or project names.

## How to use
- Keep only currently live obligations in the active table.
- Use `valid_from` and `valid_until` so agents can quickly decide what is in force today.
- If an obligation is tied to a client or project, link the relevant canonical note directly in the row.
- During monthly review or project closeout, retire rows whose engagement or date window has ended.

## Active Recurring Obligations

| Obligation | Trigger | Status | Valid from | Valid until | Linked note |
| --- | --- | --- | --- | --- | --- |
| Complete timesheets before starting deep work. | Every Friday morning | active | 2026-03-01 |  |  |

## Client / Project Obligation Pattern
Add a named row only when the obligation is currently live and genuinely recurring.

| Obligation | Trigger | Status | Valid from | Valid until | Linked note |
| --- | --- | --- | --- | --- | --- |
| Complete monthly invoicing for `[[Client or Project]]`. | First day of each month | active | YYYY-MM-DD | YYYY-MM-DD or blank | `[[Client - Name]]` or `[[Project - Name]]` |

## Retire Rules
- Remove ended obligations from the active table as soon as the engagement ends.
- If historical trace is useful, move the row into a short retired section with `valid_until` filled in.
- Do not leave ended client or project names hardcoded in [[00_System/LLM Operating Manual]] or [[00_System/Planning Cadence]].