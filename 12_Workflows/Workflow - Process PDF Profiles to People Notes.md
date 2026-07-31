---
type: workflow
status: superseded
superseded_by: "[[15_Skills/Skill - Process PDF Profiles to People Notes]]"
owner:
trigger_phrase: process my PDF profiles
tags: [workflow, profiles, linkedin, extraction, people-notes]
---

# Workflow - Process PDF Profiles to People Notes

> **Superseded.** This workflow has been promoted to a skill. Use `15_Skills/Skill - Process PDF Profiles to People Notes.md` instead.
>
> Profile PDFs now go directly into Agent Inbox; no dedicated staging subtree
> is required. See `14_Guides/Guide - Export LinkedIn Profiles as PDF.md` for
> export instructions.

## Status
This workflow is retained only as a historical pointer.

- Use `15_Skills/Skill - Process PDF Profiles to People Notes.md` for all live behavior.
- Pass selected PDF paths from `10_Action_Center/Agent_Inbox/` to the skill.
- Do not recreate retired profile-staging or extraction folders.
- The skill keeps extraction in runtime scratch space and moves successfully
  processed source PDFs to the matching Agent Inbox path below
  `16_Cleaning/Rubbish Bin/`.
