---
type: workflow
status: active
owner: 
review_cycle: monthly
tags: [workflow, content, article, thought-leadership]
---

# Workflow - Thought Leadership Article Lifecycle

## Goal
Create high-quality thought leadership articles faster, with structured review rounds and clean AI-human collaboration.

## Inputs
- topic or thesis
- target audience
- desired outcome
- references, examples, data points

## Steps
1. Create article note from `TPL - Content Pillar Article`.
2. Define thesis, audience, and one-line promise.
3. Build outline with AI (sections + key arguments).
4. Draft v1 (human + AI collaboration).
5. Start review round notes from `TPL - Content Review Round`.
6. Have AI read full article + all review notes and propose integration plan.
7. Apply changes for v2 and log what changed.
8. Repeat round-based review until final.
9. Publish and capture final URL + reuse summary.

## AI context rule (critical)
Before each revision pass, AI must read:
- current article note
- all review round notes
- previous change log in article note

Then AI should output:
1. proposed integration plan
2. unresolved conflicts between reviewers
3. exact sections to revise

## Outputs
- final article (publish-ready)
- decision log of major edits
- repurposing brief for downstream content

## Quality checklist
- [ ] Thesis is clear in first section
- [ ] Argument structure is coherent end-to-end
- [ ] Reviewer feedback is either integrated or explicitly rejected with reason
- [ ] Final article has clear close and next step

## Automation opportunities
- AI-generated revision plan from multi-reviewer comments
- AI-generated "accepted vs rejected" feedback table
- AI-generated repurposing brief after final draft
