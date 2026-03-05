# LLM Operating Manual

This file is the primary instruction set for any AI working inside Max OS.

## Audience
- LLMs only.
- Human users should start in `README.md`.

## Mandatory Read Set (in order)
1. [[00_System/System State]]
2. [[00_System/Planning Cadence]]
3. [[00_System/Planning Memory]]
4. [[00_System/Indexes]]
5. Active goals in `13_Goals/` (if any)

## Session Start Algorithm
1. Read `System State` first.
2. Resolve today's local date.
3. If `last_interaction_date` is not today, update it and append a session log line.
4. Compute due reviews from canonical last-review dates:
   - Weekly due if 7+ days since `last_weekly_review_date`
   - Monthly due if month changed since `last_monthly_review_date`
   - Quarterly due if quarter changed since `last_quarterly_review_date`
   - Yearly due if year changed since `last_yearly_review_date`
5. Run due items in order: yearly -> quarterly -> monthly -> weekly.
6. If `10_Inbox/` has pending captures, process them.
7. Align today's daily plan with active goals in `13_Goals/`.
8. Propose next 1-3 concrete actions.

## Inbox Processing Algorithm
1. Scan `10_Inbox/` newest-to-oldest.
2. Route each item to one destination: people, organization, client, project, interaction, content, or todo.
3. Create missing notes from templates in `99_Templates/`.
4. Merge factual updates into canonical notes.
5. Extract explicit tasks into `08_Todos/` or today's daily note.
6. Add cross-links between touched notes.
7. Mark inbox item processed (move, archive, or processed marker).

## Interaction Update Algorithm
When given an interaction note:
1. Ensure every mentioned person has a note in `01_People/`.
2. Ensure referenced organization/client/project notes exist.
3. Update relevant person notes with latest interaction date, key facts, open loops, and links.
4. Update referenced organization/client/project note with key updates and commitments.
5. Return a short factual changelog.

## Note Lifecycle and Archive Protocol
Purpose: keep `11_Notes/` high-signal and reduce redundancy for both humans and AI.

When to run:
- During monthly review cycles, or when multiple notes cover the same topic.

Archive trigger conditions (any):
- A newer canonical note supersedes older notes.
- A note is mostly duplicated by another active note.
- A draft/synthesis is no longer needed as an active working note.

Archive process:
1. Pick one canonical active note to keep in `11_Notes/` root.
2. Move superseded notes to `11_Notes/Archive/` (do not delete by default).
3. Set frontmatter `status: archived` in moved notes.
4. Add a short "Archive status" pointer to the canonical note.
5. Remove archived notes from active index lists (for example in `11_Notes/README.md`).
6. Update major goals/projects to reference the canonical note only.

Guardrails:
- Preserve history, but keep active strategy surfaces minimal.
- Prefer archiving over deletion unless explicitly requested.
- Avoid creating extra system files for each cleanup; update existing indexes/manuals instead.

## Rules
- Keep edits minimal, factual, and linked.
- Do not invent names, dates, commitments, or outcomes.
- Ask one focused clarification question only when required context is missing.
- Treat `last_*_review_date` fields as canonical truth.
- Keep `20_Modules/` optional unless explicitly activated in `System State`.
- Keep one canonical active note per strategy topic when possible; archive redundant variants.

## Required Session Output
1. Due reviews summary and reason.
2. Ordered checklist for this session.
3. Inbox processing summary (if inbox had pending captures).
4. Updated links to active plan/review notes.
5. `System State` updates after completed review steps.
