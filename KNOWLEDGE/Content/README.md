# Content

Store your content work: articles, videos, scripts, and publishing plans.

## What to keep here
- article ideas and drafts
- video concepts and production notes
- outlines, hooks, and key messages
- publishing checklist and post-publication notes
- presentation storylines and slide drafts

## Tip
If content belongs to a client or project, link both notes together.

## Recommended operating model
- Start with one pillar article (thought leadership / point of view).
- Use that pillar as source material for derivative assets.
- Track review rounds explicitly before publish.

## Where to save files
- Keep all content-related files in `KNOWLEDGE/Content/`.
- Save the main article as one file in `KNOWLEDGE/Content/`.
- Save each review round as its own file in `KNOWLEDGE/Content/`.
- Save each derivative asset as its own file in `KNOWLEDGE/Content/`.

This keeps everything in one place so AI can scan titles/headings quickly.

## Core templates
- `SYSTEM/Templates/TPL - Content Pillar Article.md`
- `SYSTEM/Templates/TPL - Content Review Round.md`
- `SYSTEM/Templates/TPL - Content Derivative Asset.md`
- `SYSTEM/Templates/TPL - Presentation AI GTM.md`

## Related workflows
- `AUTOMATE/Workflows/Workflow - Thought Leadership Article Lifecycle.md`
- `AUTOMATE/Workflows/Workflow - Content Waterfall from Pillar Article.md`
- `AUTOMATE/Workflows/Workflow - Build AI GTM Deck from Ideas or Articles.md`

## Simple naming pattern
- Pillar article: `Article - Topic - v01.md`
- Review rounds: `Review - Topic - Round 1 - Reviewer Name.md`
- Derivative assets: `Asset - Channel - Topic - Variant A.md`

## How article + reviews connect
1. Create article note from `TPL - Content Pillar Article`.
2. Add writing directly in the article note.
3. For each reviewer, create a review note from `TPL - Content Review Round`.
4. In each review note, link back to the article using `[[Article - ...]]`.
5. In the article note, list and link all review round notes.
6. Ask AI to read article + all linked review notes before proposing edits.

## Example file set
- `Article - AI Pricing POV - v01.md`
- `Review - AI Pricing POV - Round 1 - Partner A.md`
- `Review - AI Pricing POV - Round 2 - Partner B.md`
- `Asset - LinkedIn - AI Pricing POV - Variant A.md`
- `Asset - Video Script - AI Pricing POV - 90s.md`
- `Presentation - AI GTM - AI Pricing POV - v01.md`

## Optional later optimization
If `KNOWLEDGE/Content/` becomes very large, create subfolders:
- `KNOWLEDGE/Content/Articles/`
- `KNOWLEDGE/Content/Reviews/`
- `KNOWLEDGE/Content/Assets/`

Start flat first. Split into subfolders only when volume gets high.
