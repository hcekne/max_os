---
type: skill
status: active
trigger_phrase: export this markdown to word
tags: [skill, markdown, word, docx, export, formatting]
---

# Skill - Export Markdown to Word Document

## Purpose
Convert a Markdown note into a clean, presentation-ready `.docx` file and, when requested, a companion `.pdf` file suitable for sharing externally.

## Trigger
Use this skill when the user asks to:
- export a note to Word
- turn Markdown into a `.docx`
- prepare a formatted Word version of a memo
- create a client-ready Word document from a Markdown draft

Typical trigger phrases:
- "turn this memo into a Word document"
- "export this markdown to docx"
- "make this note into a nicely formatted Word file"
- "create a shareable Word version"

## Scope (Version 1)
- Input format: Markdown only
- Output format: one `.docx` file and optionally one `.pdf` file
- Priority: strong formatting, readability, and clean business presentation
- Best suited for memo-style notes, plans, briefings, and structured project documents

## Inputs
- One source Markdown file
- Optional output filename
- Optional destination path
- Optional title override if the source heading should not become the Word title
- Optional page orientation: `portrait` or `landscape`
- Optional PDF export

The source note may also declare export defaults in frontmatter:
- `export_orientation: landscape`
- `export_pdf: true`

## Output Contract
Produce one `.docx` file and optionally one `.pdf` file.

Default filename pattern:
- same path and stem as the source markdown file, with `.docx` extension
- same path and stem as the source markdown file, with `.pdf` extension when PDF export is enabled

The document should:
1. Use a clean cover page when the note contains a `## Cover` section
2. Preserve the document hierarchy through headings
3. Render bullet and numbered lists cleanly
4. Render tables as real Word tables
5. Preserve formulas as readable centered text blocks
6. Strip wiki-link syntax and markdown-link syntax into human-readable text
7. Apply a polished memo-style layout with consistent fonts, spacing, and page numbering
8. Respect the user's requested page orientation
9. Generate a companion PDF when requested explicitly or when the source note sets `export_pdf: true`

## Tooling
Use:
- `15_Skills/tools/md_to_docx.py`

Dependency:
- `python-docx`
- `reportlab`

Recommended isolated setup:
```bash
python3 -m venv /tmp/maxos-docx-venv
source /tmp/maxos-docx-venv/bin/activate
pip install python-docx
pip install reportlab
```

## Command Pattern
```bash
python3 15_Skills/tools/md_to_docx.py \
  "path/to/input.md" \
  "path/to/output.docx"
```

Optional title override:
```bash
python3 15_Skills/tools/md_to_docx.py \
  "path/to/input.md" \
  "path/to/output.docx" \
  --doc-title "Client Memo Title"
```

Optional landscape export:
```bash
python3 15_Skills/tools/md_to_docx.py \
  "path/to/input.md" \
  "path/to/output.docx" \
  --orientation landscape
```

Optional PDF companion export:
```bash
python3 15_Skills/tools/md_to_docx.py \
  "path/to/input.md" \
  "path/to/output.docx" \
  --orientation landscape \
  --pdf
```

## Steps

### Phase 1 - Intake
1. Confirm the source file is Markdown.
2. Confirm or derive the output path.
3. Confirm the desired page orientation.
4. If the user did not specify orientation, ask explicitly: `portrait` or `landscape`.
5. Check whether the source note already sets `export_orientation` or `export_pdf` in frontmatter.
6. Check whether `python-docx` is available.
7. If PDF export is needed, check whether `reportlab` is available.
8. If missing, create an isolated virtualenv and install the dependency.

### Phase 2 - Export
1. Run `15_Skills/tools/md_to_docx.py` on the source note.
2. Use the same folder as the source unless the user asked for a different destination.
3. If the note contains a `## Cover` section, let the exporter turn that into the Word cover page.
4. Pass `--orientation landscape` when requested, or let the source frontmatter drive the default orientation.
5. Pass `--pdf` when the user requested a PDF, or let the source frontmatter drive the default PDF export.

### Phase 3 - Review
1. Confirm the `.docx` file exists.
2. Confirm the filename and location are correct.
3. If PDF export was requested, confirm the `.pdf` file exists at the expected path.
4. If the note includes tables or formulas, make sure they were exported into readable structures.
5. If the note is especially important, offer a second pass for tone or layout refinement before final sharing.

## Quality Checks
- [ ] Output file exists at the expected path
- [ ] Document title is clean and human-readable
- [ ] Headings, bullets, and numbered lists are preserved
- [ ] Tables are rendered as Word tables
- [ ] Wiki-links are converted into readable text
- [ ] Orientation matches the user's request
- [ ] PDF exists when requested
- [ ] The memo looks presentation-ready, not like a raw text dump

## Operating Principle
Do not produce a bare conversion if the note is meant for external reading. The point of the export is not only compatibility with Word; it is to produce a document that already feels like a finished memo.