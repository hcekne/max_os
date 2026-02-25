# AI Assistant Guide

This file defines the minimum reliable behavior for any AI in this vault.

## Read Order
1. [[00_System/User Quickstart]]
2. [[00_System/System State]]
3. [[00_System/Session Start Protocol]]
4. [[00_System/Planning Memory]]

## Non-Negotiable Start
Before any planning advice:
1. Read [[00_System/System State]].
2. Resolve today's local date.
3. If `last_interaction_date` is not today, update it and append a Session Log line.
4. Compute due reviews using last review dates.

If this is not done, stop and do it first.

## Core Loop (Tier 0 and Tier 1)
1. Tell the user what is due now.
2. Run due items in order: yearly -> quarterly -> monthly -> weekly -> daily plan.
3. After each completed review, update `System State`.
4. Propose next 1-3 concrete actions.

## Rules
- Keep guidance short, concrete, and linked.
- Do not invent facts.
- Ask one focused question if required info is missing.
- Treat `last_*_review_date` as canonical truth.
- Save planning improvements in [[00_System/Planning Memory]].
