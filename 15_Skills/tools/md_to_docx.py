#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError as exc:
    print(
        "Missing dependency: python-docx.\n"
        "Create a virtual environment and install it with:\n"
        "  python3 -m venv /tmp/maxos-docx-venv\n"
        "  source /tmp/maxos-docx-venv/bin/activate\n"
        "  pip install python-docx\n",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


TITLE_COLOR = RGBColor(19, 52, 89)
ACCENT_COLOR = RGBColor(28, 96, 168)
TEXT_COLOR = RGBColor(41, 41, 41)
MUTED_COLOR = RGBColor(102, 102, 102)
TABLE_HEADER_FILL = "D9E7F5"


@dataclass
class Heading:
    level: int
    text: str


@dataclass
class Paragraph:
    text: str


@dataclass
class ListItem:
    ordered: bool
    level: int
    text: str


@dataclass
class Table:
    rows: list[list[str]]


@dataclass
class Formula:
    text: str


TOKEN_MIXED = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
UL_RE = re.compile(r"^(\s*)-\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
TABLE_SEPARATOR_RE = re.compile(r"^\|?(?:\s*:?-+:?\s*\|)+\s*$")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
LATEX_TEXT_RE = re.compile(r"\\text\{([^}]*)\}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a Markdown note to a styled .docx file.")
    parser.add_argument("input", help="Path to the Markdown file.")
    parser.add_argument("output", nargs="?", help="Output .docx path. Defaults to input stem + .docx")
    parser.add_argument("--doc-title", help="Optional document title override.")
    parser.add_argument(
        "--orientation",
        choices=("portrait", "landscape"),
        default="portrait",
        help="Page orientation for the exported Word document.",
    )
    return parser.parse_args()


def read_markdown(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1].lstrip("\n")
    return text


def strip_markup(text: str) -> str:
    def replace_md_link(match: re.Match[str]) -> str:
        return match.group(1)

    def replace_wiki_link(match: re.Match[str]) -> str:
        target = match.group(1)
        if "|" in target:
            _, label = target.split("|", 1)
            return label
        label = target.split("/")[-1]
        return label.removesuffix(".md")

    text = MD_LINK_RE.sub(replace_md_link, text)
    text = WIKI_LINK_RE.sub(replace_wiki_link, text)
    return text


def clean_text(text: str) -> str:
    return strip_markup(text).replace("\u00a0", " ").strip()


def clean_formula(text: str) -> str:
    text = LATEX_TEXT_RE.sub(r"\1", text)
    text = text.replace("\\text{-}", "-")
    text = text.replace("\\ ", " ")
    text = text.replace("\\", "")
    return text.strip()


def split_cover_block(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    cover_data: dict[str, str] = {}
    filtered: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if line.startswith("## Cover"):
            index += 1
            while index < len(lines):
                current = lines[index]
                if current.startswith("## "):
                    break
                stripped = current.strip()
                if stripped.startswith("- ") and ":" in stripped[2:]:
                    key, value = stripped[2:].split(":", 1)
                    cover_data[key.strip()] = clean_text(value.strip())
                index += 1
            continue
        filtered.append(line)
        index += 1

    return cover_data, filtered


def parse_elements(lines: list[str]) -> list[object]:
    elements: list[object] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped == "$$":
            math_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index].strip() != "$$":
                math_lines.append(lines[index].rstrip())
                index += 1
            if index < len(lines) and lines[index].strip() == "$$":
                index += 1
            elements.append(Formula(clean_formula(" ".join(math_lines))))
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            text = clean_text(heading_match.group(2))
            elements.append(Heading(level, text))
            index += 1
            continue

        if "|" in stripped and index + 1 < len(lines) and TABLE_SEPARATOR_RE.match(lines[index + 1].strip()):
            rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index]:
                row = [clean_text(cell) for cell in lines[index].strip().strip("|").split("|")]
                rows.append(row)
                index += 1
            if len(rows) > 1:
                rows.pop(1)
            elements.append(Table(rows))
            continue

        ul_match = UL_RE.match(line)
        if ul_match:
            indent = len(ul_match.group(1).replace("\t", "    "))
            level = min(indent // 2, 2)
            elements.append(ListItem(False, level, clean_text(ul_match.group(2))))
            index += 1
            continue

        ol_match = OL_RE.match(line)
        if ol_match:
            indent = len(ol_match.group(1).replace("\t", "    "))
            level = min(indent // 2, 2)
            elements.append(ListItem(True, level, clean_text(ol_match.group(3))))
            index += 1
            continue

        paragraph_lines = [line.rstrip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if candidate_stripped == "$$":
                break
            if HEADING_RE.match(candidate):
                break
            if UL_RE.match(candidate) or OL_RE.match(candidate):
                break
            if "|" in candidate_stripped and index + 1 < len(lines) and TABLE_SEPARATOR_RE.match(lines[index + 1].strip()):
                break
            paragraph_lines.append(candidate.rstrip())
            index += 1
        elements.append(Paragraph(clean_text(" ".join(paragraph_lines))))

    return elements


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def add_page_number(paragraph) -> None:
    run = paragraph.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char_begin)
    run._r.append(instr_text)
    run._r.append(fld_char_end)


def apply_document_defaults(document: Document, doc_title: str, orientation: str) -> None:
    section = document.sections[0]
    if orientation == "landscape":
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Cm(29.7)
        section.page_height = Cm(21)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
    section.top_margin = Cm(2.1)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

    styles = document.styles

    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = TEXT_COLOR
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    title = styles["Title"]
    title.font.name = "Aptos Display"
    title.font.size = Pt(26)
    title.font.bold = True
    title.font.color.rgb = TITLE_COLOR
    title.paragraph_format.space_after = Pt(10)

    subtitle = styles.add_style("Memo Subtitle", WD_STYLE_TYPE.PARAGRAPH)
    subtitle.base_style = styles["Normal"]
    subtitle.font.name = "Aptos"
    subtitle.font.size = Pt(12.5)
    subtitle.font.color.rgb = MUTED_COLOR
    subtitle.paragraph_format.space_after = Pt(6)

    heading_1 = styles["Heading 1"]
    heading_1.font.name = "Aptos Display"
    heading_1.font.size = Pt(16)
    heading_1.font.bold = True
    heading_1.font.color.rgb = TITLE_COLOR
    heading_1.paragraph_format.space_before = Pt(18)
    heading_1.paragraph_format.space_after = Pt(8)

    heading_2 = styles["Heading 2"]
    heading_2.font.name = "Aptos"
    heading_2.font.size = Pt(12.5)
    heading_2.font.bold = True
    heading_2.font.color.rgb = ACCENT_COLOR
    heading_2.paragraph_format.space_before = Pt(12)
    heading_2.paragraph_format.space_after = Pt(4)

    heading_3 = styles["Heading 3"]
    heading_3.font.name = "Aptos"
    heading_3.font.size = Pt(11)
    heading_3.font.bold = True
    heading_3.font.color.rgb = TEXT_COLOR
    heading_3.paragraph_format.space_before = Pt(8)
    heading_3.paragraph_format.space_after = Pt(2)

    formula = styles.add_style("Formula", WD_STYLE_TYPE.PARAGRAPH)
    formula.base_style = styles["Normal"]
    formula.font.name = "Aptos Mono"
    formula.font.size = Pt(10)
    formula.font.color.rgb = TITLE_COLOR
    formula.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    formula.paragraph_format.space_before = Pt(6)
    formula.paragraph_format.space_after = Pt(8)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.style = styles["Normal"]
    footer_run = footer.add_run(f"{doc_title}  |  ")
    footer_run.font.size = Pt(8.5)
    footer_run.font.color.rgb = MUTED_COLOR
    add_page_number(footer)


def add_cover_page(document: Document, title: str, cover_data: dict[str, str]) -> None:
    paragraph = document.add_paragraph(style="Title")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.add_run(title)

    prepared_for = cover_data.get("Prepared for")
    if prepared_for:
        p = document.add_paragraph(style="Memo Subtitle")
        p.add_run("Prepared for: ").bold = True
        p.add_run(prepared_for)

    prepared_by = cover_data.get("Prepared by")
    if prepared_by:
        p = document.add_paragraph(style="Memo Subtitle")
        p.add_run("Prepared by: ").bold = True
        p.add_run(prepared_by)

    date = cover_data.get("Date")
    if date:
        p = document.add_paragraph(style="Memo Subtitle")
        p.add_run("Date: ").bold = True
        p.add_run(date)

    status = cover_data.get("Status")
    if status:
        p = document.add_paragraph(style="Memo Subtitle")
        p.add_run("Status: ").bold = True
        p.add_run(status)

    spacer = document.add_paragraph()
    spacer.paragraph_format.space_after = Pt(12)

    divider = document.add_paragraph()
    divider.paragraph_format.space_after = Pt(18)
    run = divider.add_run(" ")
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1C60A8")
    border.append(bottom)
    divider._p.get_or_add_pPr().append(border)
    run.add_break(WD_BREAK.PAGE)


def add_inline_runs(paragraph, text: str) -> None:
    text = strip_markup(text)
    parts = TOKEN_MIXED.split(text)
    if not parts:
        paragraph.add_run(text)
        return

    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
            continue
        if part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Aptos Mono"
            run.font.size = Pt(9.5)
            continue
        if part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
            continue
        paragraph.add_run(part)


def export_markdown(
    input_path: Path,
    output_path: Path,
    doc_title_override: str | None,
    orientation: str,
) -> None:
    markdown = read_markdown(input_path)
    lines = markdown.splitlines()

    title = input_path.stem
    if lines and lines[0].startswith("# "):
        title = clean_text(lines[0][2:])
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)

    doc_title = doc_title_override or title
    cover_data, filtered_lines = split_cover_block(lines)
    elements = parse_elements(filtered_lines)

    document = Document()
    apply_document_defaults(document, doc_title, orientation)
    add_cover_page(document, doc_title, cover_data)

    for element in elements:
        if isinstance(element, Heading):
            if element.level == 1:
                level = 1
            elif element.level == 2:
                level = 1
            elif element.level == 3:
                level = 2
            else:
                level = 3
            paragraph = document.add_paragraph(style=f"Heading {level}")
            add_inline_runs(paragraph, element.text)
            continue

        if isinstance(element, Paragraph):
            paragraph = document.add_paragraph(style="Normal")
            add_inline_runs(paragraph, element.text)
            continue

        if isinstance(element, ListItem):
            if element.ordered:
                style_name = "List Number" if element.level == 0 else f"List Number {element.level + 1}"
            else:
                style_name = "List Bullet" if element.level == 0 else f"List Bullet {element.level + 1}"
            paragraph = document.add_paragraph(style=style_name)
            add_inline_runs(paragraph, element.text)
            continue

        if isinstance(element, Formula):
            paragraph = document.add_paragraph(style="Formula")
            paragraph.add_run(element.text)
            continue

        if isinstance(element, Table):
            table = document.add_table(rows=len(element.rows), cols=len(element.rows[0]))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.style = "Table Grid"
            for row_index, row in enumerate(element.rows):
                for col_index, cell_text in enumerate(row):
                    cell = table.cell(row_index, col_index)
                    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    cell.text = ""
                    paragraph = cell.paragraphs[0]
                    paragraph.style = document.styles["Normal"]
                    add_inline_runs(paragraph, cell_text)
                    if row_index == 0:
                        set_cell_shading(cell, TABLE_HEADER_FILL)
                        for run in paragraph.runs:
                            run.bold = True
            document.add_paragraph()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else input_path.with_suffix(".docx")
    export_markdown(input_path, output_path, args.doc_title, args.orientation)
    print(output_path)


if __name__ == "__main__":
    main()
