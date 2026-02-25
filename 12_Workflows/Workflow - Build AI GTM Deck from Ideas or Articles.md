---
type: workflow
status: active
owner: 
review_cycle: monthly
tags: [workflow, content, presentation, gtm, ai]
---

# Workflow - Build AI GTM Deck from Ideas or Articles

## Goal
Create a high-quality AI go-to-market presentation quickly from raw ideas, articles, or previous decks.

## Inputs
- one or more of:
  - rough ideas in notes
  - pillar article
  - existing PPT/deck notes
- target client and context
- meeting objective

## Steps
1. Create a new deck note from `TPL - Presentation AI GTM`.
2. Gather all source materials and link them in the deck note.
3. Ask AI to extract key arguments, evidence, and recommendations from sources.
4. Fill slides in sequence (1 to 9) with one clear message each.
5. Ask AI to stress-test narrative flow:
   - Is the logic coherent from market -> choice -> capabilities -> use cases -> proof -> next steps?
6. Tighten wording for executive audience.
7. Add speaker notes and finalize.

## AI prompt pattern
"Read this deck note and all linked source materials. Propose improvements slide by slide, preserving the 9-slide structure. Flag weak claims, missing proof points, and unclear transitions. Then provide a revised version for each slide with concise executive wording."

## Outputs
- final deck storyline in Markdown
- slide-by-slide content ready for PowerPoint/Google Slides
- optional speaker notes

## Quality checklist
- [ ] Every slide has one core message
- [ ] Strategic map leads to clear capability choices
- [ ] AI use cases are tied to capabilities and business value
- [ ] Proof points demonstrate credibility
- [ ] Next steps are concrete and commercially clear

## Optional conversion step
- Export slide content into your preferred deck tool (PowerPoint, Google Slides, Keynote).
