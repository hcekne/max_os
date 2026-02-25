# Optional Modules

This folder contains optional capability packs that extend Max OS beyond the core work operating system.

## Design principle
- Keep the core (`00_System` to `10_Inbox`) lightweight and work-first.
- Add modules only when needed.
- Modules should not break daily core workflows if unused.

## Current modules
- `Finance-Subscriptions/` - recurring payments, utilities, billing reminders.
- `Lifestyle-Training/` - health/training planning and readiness-aware scheduling.

## Enablement rule
A module is considered active only when:
1. Its `STATUS.md` says `active`, and
2. `00_System/System State.md` references it in notes or fields.
