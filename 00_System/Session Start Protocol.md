# Session Start Protocol

Use this at the beginning of any session (especially after long gaps).

## Goal
Determine what review cadence is due and guide the user into the right next actions.

## Mandatory First Action
1. Read [[00_System/System State]] first.
2. Resolve today's local date.
3. If `last_interaction_date` is not today's date, update it immediately before continuing.

## Required Inputs
- [[00_System/System State]]
- [[00_System/Planning Cadence]]
- [[00_System/Planning Memory]]
- Latest notes in `07_Daily/` and `09_Planning/`

## Trigger Rules (date-based)
- Weekly review due if 7+ days since `last_weekly_review_date`.
- Monthly review due if month has changed since `last_monthly_review_date`.
- Quarterly review due if quarter has changed since `last_quarterly_review_date`.
- Yearly review due if year has changed since `last_yearly_review_date`.

## Canonical Date Rule
- `last_*_review_date` fields are authoritative.
- "Next review" dates are optional convenience only and must never be used as the source of truth.
- Always compute due status from today's date vs last review dates.

## Execution Order (when multiple are due)
1. Yearly
2. Quarterly
3. Monthly
4. Weekly
5. Daily plan for today

## Session Output (must produce)
1. **Due Reviews Summary** (what is due right now and why).
2. **Review Run Plan** (ordered checklist for this session).
3. **Updated Links** (what active plan/review notes to open next).
4. **System State update** (new last_* dates after completion).

## Standard Prompt for Any AI
Use this prompt in chat:

"Run the Session Start Protocol. Read `00_System/System State.md`, `00_System/Planning Cadence.md`, and `00_System/Planning Memory.md`. Determine which reviews are due (weekly/monthly/quarterly/yearly) based on today's date, then propose an ordered review checklist. After I confirm completion, update `System State` with new review dates and draft the next weekly plan aligned with current quarterly and two-year direction."
