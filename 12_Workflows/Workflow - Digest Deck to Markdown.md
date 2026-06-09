---
type: workflow
status: draft
owner:
review_cycle: monthly
tags: [workflow, ai, slides, markdown]
---

# Workflow - Digest Deck to Markdown

## Goal
- Convert a source slide deck into a structured markdown digest that can be reused as high-quality AI context.

## Inputs
- One source deck (`.pdf` for MVP)
- Destination file name for digest in `05_Content/`
- Chosen output schema (slide sections + summary fields)

## Steps
1. Place source deck in a known processing location.
2. Run the deck-digester process for the file.
3. For each slide, capture:
   - title
   - subtitle (or blank)
   - text blocks
   - visual description (images/charts/diagrams)
   - slide summary (1–3 sentences)
4. Compile all slides in original order into one markdown document.
5. Run quality review and fix obvious extraction issues.
6. Save final digest to `05_Content/` and link it to the project note.

## Outputs
- One markdown file per deck, ordered slide-by-slide.
- Reusable context asset for future deck writing and optimization.

## Quality checklist
- [ ] Slide count in output matches source deck.
- [ ] No missing slides.
- [ ] Text extraction is legible and mostly accurate.
- [ ] Visual descriptions are specific, not generic.
- [ ] Each slide has a concise summary.
- [ ] File naming follows a consistent pattern.

## Automation opportunities
- Auto-generate digest filename from source deck name and date.
- Auto-link digest to `[[Project - Slide Deck Digester]]`.
- Batch mode for multiple decks once MVP quality is stable.
