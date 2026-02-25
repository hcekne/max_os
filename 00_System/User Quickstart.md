# User Quickstart

Use Max Vault in chat-first mode. No scripts required.

## What this is
A simple operating system for your work and life built from Markdown notes plus an AI assistant.

## Daily flow (Tier 0)
1. Start chat and ask: "Run Session Start Protocol and tell me what is due today."
2. Review the due checklist the assistant gives you.
3. Complete the most important items.
4. Let the assistant update notes and `System State` after each completed review.

## Daily flow (Tier 1)
Use the same flow as Tier 0, but enforce this strict routine:
- Always read `00_System/System State.md` first.
- Always update `last_interaction_date` when a new day starts.
- Always compute due reviews from last review dates.

## If you skipped days or weeks
- Start as normal.
- The assistant checks what reviews are overdue.
- Run overdue reviews in order: yearly -> quarterly -> monthly -> weekly.

## Minimal prompts you can use
- "Start my day. Check System State and tell me what is due."
- "Run weekly review from last week plan and daily notes."
- "Update System State now based on what we completed."

## Keep it simple
- Capture quickly in notes.
- Link notes with `[[...]]` when relevant.
- Use a few workflow tags only when needed.
- Prefer consistency over perfect structure.
