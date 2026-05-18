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
1. Open previous weekly plan in `09_Planning/Weekly`.
2. Review linked daily notes in `07_Daily` for the same week.
3. Compare plan vs actual (what was done, what slipped, why).
4. Capture lessons in [[00_System/Planning Memory]].
5. Draft next weekly plan aligned to current quarterly plan.
6. Run lightweight workspace hygiene in `PLAN_ONLY` when recent work created many drafts, exports, inbox captures, or generated files.
7. Run changed-file knowledge lint if the week included substantial note creation, system changes, or inbox processing.
8. Confirm workload buffer for incoming/unplanned work.

## Monthly Session (45-60 min)
1. Review the month across weekly plans/reviews and daily highlights.
2. Identify execution patterns (what repeated and why).
3. Capture process improvements in [[00_System/Planning Memory]].
4. Update operating rules for next month.
5. Run note hygiene in `11_Notes`: consolidate duplicates, archive historically useful superseded notes to `16_Cleaning/Archive/11_Notes`, move clear delete candidates to `16_Cleaning/Rubbish Bin/11_Notes`, and keep active index lists clean.
6. Run monthly workspace hygiene using `12_Workflows/Workflow - Weekly Workspace Hygiene Review.md` as the operating loop and `15_Skills/Skill - Workspace Hygiene and File Lifecycle Review.md` as the executable review skill.
7. Run full or high-bloat-folder knowledge lint and capture unresolved issues in a report if warnings are too noisy to fix immediately.

## Quarterly Session (60-90 min)
1. Review the quarter plan in `09_Planning/Quarterly`.
2. Summarize weekly performance trends and lessons.
3. Update priorities, constraints, and active projects.
4. Refresh next 12 weeks of direction.
5. Update assumptions in [[00_System/Planning Memory]].

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
- Workspace hygiene lightweight review runs weekly in `PLAN_ONLY` when file bloat signals are present.
- Workspace hygiene deep review runs monthly, at project closeout, and after major deliverables.
- Knowledge lint runs before commits that change canonical Markdown and during monthly hygiene.

## Copilot Review Prompt (use in session)
- "Read this weekly plan, the linked daily notes for that week, and `00_System/Planning Memory.md`. Compare planned vs actual, propose 3 process improvements, append improvements to Planning Memory, then draft next week plan aligned to the active quarterly plan."
- "Run `15_Skills/Skill - Workspace Hygiene and File Lifecycle Review.md` in `PLAN_ONLY` for recent files and high-bloat folders. Create or update a hygiene proposal in `00_System/Proposals/` without moving or deleting anything."
- "Run `15_Skills/Skill - Knowledge System Lint and Link Check.md` on changed Markdown files. Fix errors and summarize warnings that should be handled later."
