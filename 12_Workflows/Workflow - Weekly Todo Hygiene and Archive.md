---
type: workflow
status: active
owner:
trigger_phrase: run weekly todo hygiene
tags: [workflow, todo, planning, hygiene, archive]
---

# Workflow - Weekly Todo Hygiene and Archive

## Purpose
Keep `08_Todos/` focused on real current priorities by reviewing, cleaning, and archiving tasks weekly.

## Trigger
Use this workflow whenever you say: **"run weekly todo hygiene"**.

## End-State Definition
At the end of a successful run:
- Active and backlog tasks in `08_Todos/` are current and relevant.
- Completed/closed tasks are moved to `08_Todos/Completed/`.
- Duplicate tasks are merged.
- `08_Todos/Index.md` reflects current state.

## Steps
1. **Scan and classify all todos**
   - Read all files in `08_Todos/` root.
   - Classify each as: `active`, `backlog`, `completed`, `stale`, `duplicate`, or `out-of-scope`.

2. **Handle completed and closed items**
   - If `status: completed`, move file to `08_Todos/Completed/`.
   - If task is no longer relevant, set `status: completed`, add closure reason in Notes, then archive.

3. **Handle stale and overdue items**
   - If overdue but still relevant: update target date and add one-line reason in Notes.
   - If stale and low value: close + archive.

4. **Merge duplicates**
   - Keep one canonical todo.
   - Move unique useful checklist items into canonical file.
   - Mark duplicate as completed with note: "Merged into ..." and archive.

5. **Refresh index**
   - Update `08_Todos/Index.md` sections:
     - Active
     - Backlog
     - Completed (Archived)

6. **Weekly summary output**
   - Report:
     - Total todos reviewed
     - Archived completed count
     - Merged duplicates count
     - Rescheduled count
     - Closed as out-of-scope count

## Heuristics
- Prefer fewer, clearer todos over many overlapping todos.
- A todo should have one clear outcome and one owner.
- If no meaningful action can be identified, close + archive.
