---
type: policy
status: active
created: 2026-05-16
review_cycle: quarterly
tags: [policy, git, preservation, hygiene]
---

# Git Preservation Policy

## Purpose
Clarify how Max OS uses Git to preserve history while keeping the active Markdown workspace clean.

## Principle
Git is the full-history layer. Active folders should not preserve every old draft, intermediate export, or generated scratch file.

## Core Rules
- Commit before large cleanup operations whenever possible.
- Check `git status` before moving, deleting, or bulk-editing files.
- Prefer `git mv` for moves so history remains clear.
- Do not rewrite Git history unless the human explicitly requests it.
- Do not delete files outside the narrow rubbish-bin purge path.
- Do not push cleanup commits without explicit approval.
- Treat final deliverables, contracts, invoices, submitted documents, legal/commercial files, and client-provided source materials as high-retention by default.

## Cleanup Stance
- Use Git history as preservation, not as an excuse for active-folder bloat.
- Prefer keeping the current canonical or final version visible and retiring old working versions.
- Default old low-value versions into `SYSTEM/Cleaning/Rubbish Bin/` unless the archive path is clearly better.

## Deletion Standard
- Outside the rubbish-bin purge path, deletion requires explicit human approval and a recorded reason.
- Files already in `SYSTEM/Cleaning/Rubbish Bin/` may be deleted without separate case-by-case approval if they satisfy [[SYSTEM/Rubbish Bin Policy]].

## Recommended Commit Pattern
Use focused commit messages:
- `Archive expired project prep files`
- `Add lifecycle metadata to draft deliverables`
- `Clean content draft version bloat`
- `Add workspace hygiene and lifecycle management`

## Agent Reporting
Every hygiene run should report branch/status before changes, moved files, modified files, deletion proposals, human-review items, and a commit recommendation.
