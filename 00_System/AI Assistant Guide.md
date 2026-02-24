# AI Assistant Guide

This file helps any AI assistant quickly understand how to operate this vault.

## Read Order (always)
1. [[00_System/Start Here]]
2. [[00_System/Session Start Protocol]]
3. [[00_System/System State]]
4. [[00_System/Planning Cadence]]
5. [[00_System/Planning Memory]]
6. [[00_System/Indexes]]

## Core Operating Expectations
- Do not invent facts.
- Keep edits minimal, explicit, and linked.
- Preserve planning continuity by updating `System State` when reviews complete.
- When in doubt, ask for missing context in one concise question.

## Planning Behavior
- Detect due horizons from dates in `System State`.
- If multiple reviews are overdue, run in order: yearly -> quarterly -> monthly -> weekly.
- After reviews, propose next week plan and align with higher horizons.

## Interaction Behavior
- If user shares a conversation or event update, suggest updating:
  - daily note
  - relevant project/client/person note
  - weekly plan (if priorities changed)

## Definition of Helpful
- Turn vague requests into structured next actions.
- Keep user moving with small, high-leverage steps.
- Save improvements into [[00_System/Planning Memory]].
