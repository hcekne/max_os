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

## Rules
- Commit before large cleanup operations whenever possible.
- Check `git status` before moving, deleting, or bulk-editing files.
- Prefer `git mv` for moves so history remains clear.
- Do not rewrite Git history unless the human explicitly requests it.
- Do not delete files without explicit approval.
- Do not push cleanup commits without explicit approval.
- Treat final deliverables, contracts, invoices, submitted documents, legal/commercial files, and client-provided source materials as high-retention by default.
- Do not commit Python bytecode, runtime cache folders, or generated intermediate files that can be recreated.

## Draft and Version Cleanup
When many draft versions exist:
1. Identify the current canonical or final version.
2. Preserve final/submitted deliverables separately.
3. Archive or delete old generated/intermediate versions after approval.
4. Add `superseded_by` metadata to old versions when useful.
5. Add `canonical: true` metadata to the current version when useful.

## Deletion Standard
Deletion may be appropriate after approval if all of the following are true:
- the file is not canonical;
- the file is not final/submitted;
- the file is not a contract, invoice, source material, or legal/commercial document;
- useful content has been merged or is duplicated elsewhere;
- Git history preserves the old file;
- the cleanup proposal records the reason.

## Recommended Commit Pattern
Use focused commit messages:
- `Archive expired project prep files`
- `Add lifecycle metadata to draft deliverables`
- `Clean content draft version bloat`
- `Add workspace hygiene and lifecycle management`

## Ignore Defaults
Repos should ignore local runtime byproducts:

```gitignore
__pycache__/
*.py[cod]
```

Do not globally ignore `.pdf`, `.docx`, or `.html` because those may be final deliverables or supported artifacts in Max OS. Classify them through lifecycle policy instead.

## Agent Reporting
Every hygiene run should report:
- branch and status before changes;
- files moved;
- files modified;
- files proposed for deletion;
- files requiring human review;
- commit recommendation;
- public-template improvements discovered.
