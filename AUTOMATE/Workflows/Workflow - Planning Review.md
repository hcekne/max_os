---
type: workflow
status: active
tags: [planning, review, routine]
---

# Workflow - Planning Review

Run the owner's planning loop on request. To schedule it, create an executable
Workflow Builder recipe from this card; this Markdown card is guidance, not a
schedulable recipe. Reviews happen when invoked, not before every piece of
work.

## Trigger

- The owner asks for a daily plan, a weekly/quarterly review, or "what
  should I do today".
- Or: an executable Workflow Builder recipe created from this card.

## Steps

1. Read `SYSTEM/State.md`, `SYSTEM/Memory.md` (preferences, standing
   obligations), active goals in `PLAN/Goals/`, and the current horizon
   plans linked from State.
2. Surface standing obligations from `SYSTEM/Memory.md` whose window
   includes today.
3. If `ACTION CENTER/My Inbox/` has pending results, summarize the review
   queue. If `ACTION CENTER/Agent Inbox/` has pending captures, process them
   per that folder's instructions.
4. For a **daily plan**: pull due items from `PLAN/Todos/`, align with
   active goals, write today's note in `PLAN/Daily/`, propose the top 1–3
   actions.
5. For a **weekly / quarterly / two-year review**: follow the method in
   `PLAN/.instructions.md`; capture reusable lessons in `SYSTEM/Memory.md`.
6. Update the `active_*` links and `last_interaction_date` in
   `SYSTEM/State.md`, and append one dated bullet to `SYSTEM/Log.md`.

## Outputs

- Today's daily note and/or the horizon plan and review notes.
- Updated `SYSTEM/State.md` links; a dated `SYSTEM/Log.md` entry.
- A short ordered checklist of proposed next actions.

## Quality checks

- [ ] No invented commitments, dates, or outcomes.
- [ ] Plans reference real todos, goals, and notes by `[[wiki-link]]`.
- [ ] Lessons written to `SYSTEM/Memory.md` replace superseded entries
      rather than duplicating them.
