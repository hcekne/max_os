---
type: skill
status: active
trigger_phrase: export this markdown to word
tags: [skill, markdown, word, docx, export, formatting]
---

# Skill - Export Markdown to Word Document

## Purpose
Convert a Markdown note into a clean `.docx` file with business-ready Word formatting.

## Trigger
Use this skill when the user asks to:
- export a note to Word
- turn Markdown into a `.docx`
- prepare a formatted Word version of a memo
- create a shareable Word version of a Markdown draft

Typical trigger phrases:
- "turn this memo into a Word document"
- "export this markdown to docx"
- "make this note into a nicely formatted Word file"
- "create a shareable Word version"

## Scope
- Input format: Markdown only
- Output format: one `.docx` file
- Priority: clear formatting, readability, and clean business presentation
- Best suited for memo-style notes, plans, briefings, and structured project documents

## Inputs
- One source Markdown file
- Optional output filename
- Optional destination path
- Optional title override if the source heading should not become the Word title
- Optional page orientation: `portrait` or `landscape`

## Output Contract
Produce exactly one `.docx` file.

Default filename pattern:
- same path and stem as the source Markdown file, with `.docx` extension

The document should:
1. Use a clean cover page when the note contains a `## Cover` section.
2. Preserve the document hierarchy through headings.
3. Render bullet and numbered lists cleanly.
4. Render tables as real Word tables.
5. Preserve formulas as readable centered text blocks.
6. Strip wiki-link syntax and Markdown-link syntax into human-readable text.
7. Apply a polished memo-style layout with consistent fonts, spacing, and page numbering.
8. Respect the user's requested page orientation.

## Tooling
Use:
- `15_Skills/tools/md_to_docx.py`

Dependency:
- `python-docx`

Recommended isolated setup:

```bash
python3 -m venv /tmp/maxos-docx-venv
source /tmp/maxos-docx-venv/bin/activate
pip install python-docx
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

## Steps

### Phase 1 - Intake
1. Confirm the source file is Markdown.
2. Confirm or derive the output path.
3. Confirm the desired page orientation.
4. If the user did not specify orientation, use `portrait` unless the document contains wide tables.
5. Check whether `python-docx` is available.
6. If missing, create an isolated virtual environment and install the dependency.

### Phase 2 - Export
1. Run `15_Skills/tools/md_to_docx.py` on the source note.
2. Use the same folder as the source unless the user asked for a different destination.
3. If the note contains a `## Cover` section, let the exporter turn that into the Word cover page.
4. Pass `--orientation landscape` when requested; otherwise export in portrait mode.

### Phase 3 - Review
1. Confirm the `.docx` file exists.
2. Confirm the filename and location are correct.
3. If the note includes tables or formulas, make sure they were exported into readable Word structures.
4. If the note is especially important, offer a second pass for tone or layout refinement before final sharing.

## Quality Checks
- [ ] Output file exists at the expected path
- [ ] Document title is clean and human-readable
- [ ] Headings, bullets, and numbered lists are preserved
- [ ] Tables are rendered as Word tables
- [ ] Wiki-links are converted into readable text
- [ ] Orientation matches the user's request
- [ ] The memo looks presentation-ready, not like a raw text dump

## Operating Principle
Do not produce a bare conversion if the note is meant for external reading. The point of the export is not only compatibility with Word; it is to produce a document that already feels like a finished memo.
