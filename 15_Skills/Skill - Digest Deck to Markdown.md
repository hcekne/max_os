---
type: skill
status: active
trigger_phrase: digest this deck to markdown
tags: [skill, slides, presentation, deck, markdown, extraction]
---

# Skill - Digest Deck to Markdown

## Purpose
Convert one or more presentation deck PDFs into high-fidelity Markdown digests, with one section per slide/page that preserves visible text, slide structure, and useful visual context.

## Trigger
Use this skill when the user asks to read, digest, transcribe, extract, convert, or summarize a slide deck, presentation, or PDF into one Markdown file.

Typical trigger phrases:
- "digest this deck"
- "convert this presentation to markdown"
- "read this slide deck"
- "extract this PDF deck slide by slide"
- "turn this presentation into a markdown digest"

## Scope
- Input format: PDF only
- Output format: one `.md` file per source PDF
- Output location: default `05_Content/`, or an explicitly requested destination such as a project folder under `04_Projects/`
- Priority: accuracy and completeness over speed

## Inputs
- One or more source presentation decks as PDF
- Optional output filename
- Optional destination path under `05_Content/` or a project folder such as `04_Projects/<Project Name>/`

## Output Contract
Produce exactly one Markdown file per deck.

Default filename pattern:
- `Deck Digest - <Source Deck Name> (YYYY-MM-DD).md`

The output file should contain:
1. Deck title and source metadata
2. Optional deck-level summary
3. One section per slide, in original order
4. For each slide:
   - title
   - subtitle if present
   - detected slide type
   - layout notes
   - all visible text, organized by block
   - visual description of charts, images, diagrams, and tables
   - speaker notes if available
   - one-slide summary

## End-State Definition
After a successful run:
- The Markdown file exists in the requested destination.
- The number of slide sections matches the number of slides/pages in the source PDF.
- No slide is skipped, including title, agenda, divider, closing, or appendix slides.
- Text is captured as faithfully as possible.
- Unclear or unreadable content is flagged rather than invented.

## Slide-Type Rules
Classify each slide into one of these types:
- `title`
- `agenda`
- `divider`
- `content`
- `chart`
- `table`
- `appendix`
- `closing`
- `unknown`

Use the best-fit type based on the slide's visible function. If a slide mixes types, choose the dominant one and explain the mixed structure in layout notes.

## Extraction Rules
1. Process slides in original order.
2. Capture all visible text on every slide.
3. Preserve wording as closely as possible.
4. Do not rewrite slide text unless minor cleanup is needed for legibility.
5. If text is unreadable or extraction is uncertain, mark it clearly as `[unclear]` or `[partially unreadable]`.
6. Never invent missing words, figures, or claims.
7. Preserve bullet order and obvious hierarchy.
8. Keep repeated slide furniture only if it is actually meaningful content.

## Text-Block Organization Rules
Organize visible slide text by block rather than dumping it as one paragraph.

Reading-order rules:
- Top to bottom
- Left to right within the same row
- Preserve grouped boxes or panels where visible
- Preserve headers separately from their body text

Block-format rules:
- Use one numbered item per major text block.
- If a block has a header, label it explicitly.
- Keep bullets under the correct block.
- If a slide has columns, reflect that in the block descriptions or layout notes.

## Visual Description Rules
For charts, diagrams, images, tables, icons, and other visuals:
- Describe what is visibly present and relevant.
- Mention labels, axes, legends, or callouts if readable.
- Do not infer non-visible numbers or conclusions.
- If the visual mainly reinforces a text point, say so briefly.
- If there is no meaningful visual beyond text layout, say `No separate visual beyond text layout.`

## Speaker Notes Rules
- Include speaker notes only if they are actually available from the source.
- Do not infer speaker notes from slide text.
- If no notes are available, say `None available`.

## Required Markdown Schema

Use this structure:

```md
---
type: content
status: active
source_file: <source filename>
source_format: pdf
deck_title: <deck title>
slide_count: <N>
created: YYYY-MM-DD
tags: [content, deck-digest, slides]
---

# Deck Digest - <Deck Title>

## Source
- Source file: <filename>
- Source format: PDF
- Slide count: <N>

## Deck Summary
- Topic:
- Major sections:
- Overall takeaway:

## Slide 01 - <Title or Untitled>
- Slide type: <type>
- Subtitle: <subtitle or blank>
- Layout: <brief structural description>

### Text Blocks
1. <Block name or position>
   - Header: <header text if present>
   - Content:
     - <bullet / sentence>
     - <bullet / sentence>

### Visuals
- <factual visual description>

### Speaker Notes
- <notes or None available>

### Slide Summary
- <1-3 sentence summary>
```

## Steps

### Phase 1 - Intake
1. Confirm the source file is a PDF.
2. Confirm the output location, defaulting to `05_Content/` unless the user requested a project-scoped destination.
3. Derive or confirm the output filename.
4. Determine the total slide/page count.

### Phase 2 - Slide-by-Slide Capture
1. Process every slide sequentially.
2. Detect the slide type.
3. Capture title and subtitle if present.
4. Note the layout structure briefly.
5. Extract all visible text and organize it by block.
6. Describe meaningful visuals factually.
7. Include speaker notes if available.
8. Write a short slide summary.

### Phase 3 - Assemble the Digest
1. Compile all slide sections into one Markdown file.
2. Add deck-level source metadata.
3. Add a short deck summary only after all slides have been reviewed.
4. Save the final digest to the requested destination.

### Phase 3b - Batch Runs
1. If multiple PDFs were requested, repeat Phases 1-3 for each source file.
2. Keep one output Markdown per source PDF.
3. If the destination is project-scoped, add or update project links after all files are written.

### Phase 4 - Quality Review
1. Check that slide count matches.
2. Check that no slide types were accidentally skipped.
3. Check that text blocks are organized cleanly.
4. Check that visuals are described factually, not generically.
5. Check that unclear text is flagged rather than guessed.

## Outputs
- One Markdown digest file per source PDF in the requested destination
- One ordered section per slide
- A deck-level summary suitable for later AI use

## Quality Checks
- [ ] Slide count in the Markdown file matches the PDF slide/page count
- [ ] Every slide has its own section
- [ ] Title, subtitle, and text blocks are captured where present
- [ ] Visuals are described without hallucinated content
- [ ] Speaker notes are only included when actually available
- [ ] Agenda, divider, appendix, and closing slides are not skipped
- [ ] Unclear text is marked explicitly instead of silently rewritten
- [ ] Output is saved as one `.md` file per source PDF in the requested destination

## Ambiguity Handling
- If a slide title is missing, use `Untitled` and rely on slide number.
- If text extraction is incomplete, flag the missing parts.
- If a layout is unusual, describe the structure plainly rather than forcing a rigid template.
- If a slide is mostly visual, keep the text section minimal and make the visual description more explicit.

## Operating Principle
High-fidelity slide reading, not generic summarization. The Markdown digest should let a later agent or human reconstruct what was actually on each slide without needing to reopen the deck.
