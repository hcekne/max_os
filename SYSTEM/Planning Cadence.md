# Planning Cadence

## Goal
Run planning and review loops across horizons so daily execution stays aligned with longer-term direction.

## Horizons
- Weekly: execution focus and next actions.
- Monthly: pattern review and process improvement.
- Quarterly: outcomes and major priorities.
- Yearly: strategic reset and long-horizon alignment.
- Two-Year: direction and target state.

## Weekly Session (30-45 min)
1. Open previous weekly plan in `PLAN/Weekly`.
2. Review linked daily notes in `PLAN/Daily` for the same week.
3. Compare plan vs actual (what was done, what slipped, why).
4. Capture lessons in [[SYSTEM/Planning Memory]].
5. Draft next weekly plan aligned to current quarterly plan.
6. Confirm workload buffer for incoming/unplanned work.
7. Run [[Workflow - Weekly Workspace Hygiene Review]] in `PLAN_ONLY` for recent files and high-bloat active project folders.

## Monthly Session (45-60 min)
1. Review the month across weekly plans/reviews and daily highlights.
2. Identify execution patterns (what repeated and why).
3. Capture process improvements in [[SYSTEM/Planning Memory]].
4. Update operating rules for next month.
5. Run note hygiene in `KNOWLEDGE/Notes` using the Note Lifecycle and Archive Protocol in [[SYSTEM/LLM Operating Manual]] plus the lifecycle policies in `SYSTEM/`.
6. Run a deeper workspace hygiene review for large project/content folders and prepare archive/delete proposals.
7. Review [[SYSTEM/Recurring Operations]] and retire ended rows or stale control-surface references.

## Quarterly Session (60-90 min)
1. Review the quarter plan in `PLAN/Quarterly`.
2. Summarize weekly performance trends and lessons.
3. Update priorities, constraints, and active projects.
4. Refresh next 12 weeks of direction.
5. Update assumptions in [[SYSTEM/Planning Memory]].

## Yearly Session (90-120 min)
1. Review all quarterly outcomes and major misses.
2. Reassess strategic constraints and opportunities.
3. Refresh direction for the next 12 months.
4. Ensure yearly direction supports the two-year goal state.

## Two-Year Session (90 min, quarterly cadence)
1. Re-read latest two-year goal state.
2. Check whether quarterly plans still point to that direction.
3. Adjust trajectory for new constraints/opportunities.

## Trigger Rules
- Weekly due every 7 days.
- Monthly due when calendar month changes.
- Quarterly due when calendar quarter changes.
- Yearly due when calendar year changes.
- When multiple reviews are due, run them in order: yearly -> quarterly -> monthly -> weekly.

## Operational Recurrence (Non-negotiable)
- The canonical source for standing operational reminders is [[SYSTEM/Recurring Operations]].
- On session start, surface only obligations marked `active` whose valid window includes today.
- During monthly review and project closeout, retire ended obligations and remove stale hardcoded references from global control files.

## Copilot Review Prompt (use in session)
- "Read this weekly plan, the linked daily notes for that week, and `SYSTEM/Planning Memory.md`. Compare planned vs actual, propose 3 process improvements, append improvements to Planning Memory, then draft next week plan aligned to the active quarterly plan."
- "Run `AUTOMATE/Skills/Skill - Workspace Hygiene and File Lifecycle Review.md` in `PLAN_ONLY` for recent files and high-bloat folders. Create or update a hygiene proposal in `SYSTEM/Proposals/` without moving or deleting anything."
- "Run `AUTOMATE/Skills/Skill - Knowledge System Lint and Link Check.md` on changed Markdown files. Fix errors and summarize warnings that should be handled later."
