---
type: note
status: draft
owner:
created: 2026-03-03
tags: [max-os, learnings, operations]
---

# Note - Patterns Learned from Real Usage

## Why this note exists
- This captures practical patterns from day-to-day Max OS usage that are useful for other users.
- Focus is on transferable operating patterns, not personal/private data.

## Pattern 1: People + interactions become a core operating surface
- In real usage, relationship memory often becomes one of the highest-value parts of the system.
- Practical implication: keep person notes, interaction notes, and follow-up loops tightly linked.

## Pattern 2: Governance files are not optional
- Session-start rules, review cadence, and system-state files provide structure that prevents drift.
- Practical implication: adopt and keep `00_System` files updated early.

## Pattern 3: Project + TODO + planning linkage drives execution
- A reliable execution pattern is:
  - one project note as source of truth,
  - multiple linked TODOs for workstreams,
  - weekly/monthly planning links for prioritization.

## Pattern 4: Workflows and templates should evolve quickly
- New repeatable tasks appear fast.
- Practical implication: add small workflows/templates when repetition appears; avoid waiting for a perfect design.

## Pattern 5: Keep core simple, make advanced capabilities optional
- Core Max OS works best as a human+AI operating system over files.
- Advanced extensions should be optional modules to avoid overloading first-time users.

## Suggested next improvements for public users
- Add a "Relationship Intelligence" quickstart guide.
- Add a short "Project Execution Triad" example (project + TODO + plan links).
- Keep optional modules clearly separated from core onboarding.
