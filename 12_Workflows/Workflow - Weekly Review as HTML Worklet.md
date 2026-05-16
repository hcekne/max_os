---
type: workflow
status: draft
owner:
review_cycle: monthly
tags: [workflow, weekly-review, html, worklet]
---

# Workflow - Weekly Review as HTML Worklet

## Goal
Use an optional HTML worklet to support weekly review while keeping the weekly plan, review notes, and system state in Markdown.

## Inputs
- Active weekly plan from `09_Planning/Weekly/`
- Relevant daily notes from `07_Daily/`
- [[00_System/Planning Memory]]
- [[00_System/System State]]
- Optional worklet in `20_Modules/Worklets/`

## Related Policies
- [[00_System/Document Model]]
- [[00_System/Rendering Policy]]
- [[00_System/Worklet Conventions]]
- [[Skill - Create HTML Worklet]]

## Steps
1. Read the current weekly plan, linked daily notes, Planning Memory, and System State.
2. Generate or open a weekly review worklet in `20_Modules/Worklets/`.
3. Load only the review inputs needed for the session.
4. Use the worklet to compare planned work, completed work, slipped work, and lessons.
5. Export findings as a Markdown proposal.
6. Human reviews the proposal and applies approved updates to the weekly review note and Planning Memory.
7. Update System State only after the weekly review is actually completed.
8. Keep the worklet optional; the same review must remain possible directly in Markdown.

## Outputs
- Optional HTML weekly review worklet
- Markdown proposal for weekly review findings
- Approved weekly review note in `09_Planning/Reviews/`
- Approved Planning Memory updates, if any
- System State update only after review completion

## Quality checklist
- [ ] Weekly review can still be completed without the worklet.
- [ ] Worklet does not silently edit Markdown.
- [ ] Proposal links source plan and daily notes.
- [ ] Approved findings are backported to canonical Markdown.
- [ ] System State is updated only after completed review steps.
- [ ] Worklet state is JSON if structured runtime state is needed.

## Automation opportunities
- Pre-fill a worklet from weekly plan and daily notes.
- Generate a Markdown proposal from worklet output.
- Run artifact safety review before using the worklet in a harness.
