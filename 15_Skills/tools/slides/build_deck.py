"""Build a slide deck from a folder of numbered markdown slide files.

Usage:
    python3 build_deck.py <deck_folder> [--with-notes]

Each slide file is a markdown file with YAML-subset frontmatter. See
`Skill - Slide Deck Generation.md` for the full format spec.

Outputs:
    <deck_folder>/deck.html        # default
    <deck_folder>/deck-notes.html  # when --with-notes is passed
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
CSS_FILE = SCRIPT_DIR / "deck.css"

CHART_JS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def detect_logo_background(asset_path: Path) -> tuple[int, int, int, int] | None:
    """Return the dominant corner pixel RGBA of an image, or None if Pillow isn't available."""
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return None
    try:
        img = Image.open(asset_path).convert("RGBA")
    except Exception:
        return None
    w, h = img.size
    return img.getpixel((1, 1))


def classify_background(rgba: tuple[int, int, int, int]) -> str:
    """Tag a background colour as 'transparent', 'white', 'dark', or 'colour' (other)."""
    r, g, b, a = rgba
    if a < 16:
        return "transparent"
    lightness = (r + g + b) / 3
    if r > 240 and g > 240 and b > 240:
        return "white"
    if lightness < 64:
        return "dark"
    return "colour"


def check_logo_safety(specs: list[tuple[str, str]], deck_dir: Path, slide_bg: str) -> list[str]:
    """Inspect each logo against the slide background it will sit on.

    `specs` is a list of (csv-paths, role) pairs, e.g. [("assets/dmg.png", "cover_logo")].
    `slide_bg` is the slide background type the role lands on: 'dark' or 'white'.
    Returns a list of human-readable warning strings (empty list = all logos compatible).
    """
    warnings: list[str] = []
    for csv_paths, role in specs:
        if not csv_paths:
            continue
        for path in (p.strip() for p in csv_paths.split(",") if p.strip()):
            asset_path = deck_dir / path
            if not asset_path.exists():
                warnings.append(f"{role}: file not found: {path}")
                continue
            pixel = detect_logo_background(asset_path)
            if pixel is None:
                continue  # Pillow not available; skip silently
            kind = classify_background(pixel)
            if kind == "transparent":
                continue  # Transparent backgrounds work anywhere.
            if slide_bg == "dark" and kind == "white":
                warnings.append(
                    f"{role}: {path} has a WHITE background but the target slide is DARK. "
                    "The logo will render as a white rectangle on the dark cover. "
                    "Use a transparent or dark-background version, or change the slide background."
                )
            elif slide_bg == "white" and kind == "dark":
                warnings.append(
                    f"{role}: {path} has a DARK background but the target slide is WHITE. "
                    "The logo will render as a dark rectangle on the white slide. "
                    "Use a transparent or white-background version, or change the slide background."
                )
            elif slide_bg == "dark" and kind == "dark":
                # Compatible: both dark. No warning, but worth noting in verbose mode.
                pass
            elif slide_bg == "white" and kind == "white":
                pass
            else:
                warnings.append(
                    f"{role}: {path} has a {kind} background; verify it suits the {slide_bg} slide."
                )
    return warnings


def render_logo_block(spec: str, deck_dir: Path, css_class: str) -> str:
    """Render one or more logo image tags from a frontmatter logo spec.

    `spec` is either a single path (e.g. "assets/dmg.png") or a comma-separated
    list. Each path is rendered as an <img> with the given css class.
    `deck_dir` is used only to verify the file exists; the path used in the
    rendered HTML is the relative path as written (so it works for both the
    on-disk HTML and the in-folder asset).
    """
    if not spec:
        return ""
    paths = [p.strip() for p in spec.split(",") if p.strip()]
    if not paths:
        return ""
    images = []
    for path in paths:
        asset_path = deck_dir / path
        alt = asset_path.stem.replace("_", " ").replace("-", " ")
        images.append(f'<img src="{escape(path)}" class="{css_class}" alt="{escape(alt)}">')
    return "".join(images)


def embed_assets(html: str, deck_dir: Path) -> str:
    """Replace <img src="local/path"> with base64 data URIs so the HTML is self-contained."""
    pattern = re.compile(r'<img\b([^>]*?)\bsrc="([^"]+)"([^>]*)>', re.IGNORECASE)

    def replace(match: re.Match[str]) -> str:
        before, src, after = match.group(1), match.group(2), match.group(3)
        if src.startswith(("data:", "http://", "https://", "//")):
            return match.group(0)
        asset_path = (deck_dir / src).resolve()
        try:
            data = asset_path.read_bytes()
        except (FileNotFoundError, IsADirectoryError):
            return match.group(0)
        mime, _ = mimetypes.guess_type(str(asset_path))
        if not mime:
            mime = "application/octet-stream"
        encoded = base64.b64encode(data).decode("ascii")
        return f'<img{before} src="data:{mime};base64,{encoded}"{after}>'

    return pattern.sub(replace, html)


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        sys.exit(f"ERROR: required command not found: {name}")
    return path


def inline_md(text: str) -> str:
    """Render the small inline Markdown subset used by slide bodies."""
    placeholders: list[str] = []

    def protect(match: re.Match[str]) -> str:
        placeholders.append(match.group(0))
        return f"\x00RAW{len(placeholders) - 1}\x00"

    protected = re.sub(r"<[^>]+>", protect, text)
    protected = escape(protected)
    protected = re.sub(r"`([^`]+)`", r"<code>\1</code>", protected)
    protected = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", protected)
    protected = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", protected)

    for index, raw in enumerate(placeholders):
        protected = protected.replace(f"\x00RAW{index}\x00", raw)
    return protected


def render_table(lines: list[str]) -> str:
    def split_row(row: str) -> list[str]:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    header = split_row(lines[0])
    body_rows = [split_row(row) for row in lines[2:]]
    out = ["<table>", "<thead>", "<tr>"]
    out.extend(f"<th>{inline_md(cell)}</th>" for cell in header)
    out.extend(["</tr>", "</thead>", "<tbody>"])
    for row in body_rows:
        out.append("<tr>")
        out.extend(f"<td>{inline_md(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.extend(["</tbody>", "</table>"])
    return "\n".join(out)


def fallback_md_to_html(markdown_text: str) -> str:
    """Render the limited Markdown subset used by Max OS slide decks.

    Pandoc remains preferred when installed. This fallback keeps the slide
    builder usable in lightweight agent environments where pandoc is absent.
    It supports headings, paragraphs, ordered/unordered lists, pipe tables,
    basic inline emphasis/code, and raw HTML blocks.
    """
    lines = markdown_text.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("<script"):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if "</script>" in lines[i]:
                    i += 1
                    break
                i += 1
            out.append("\n".join(block))
            continue

        if stripped.startswith("<") and stripped.endswith(">"):
            out.append(line)
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1]):
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline_md(heading.group(2))}</h{level}>")
            i += 1
            continue

        unordered = re.match(r"^\s*[-*]\s+(.+)$", line)
        if unordered:
            out.append("<ul>")
            while i < len(lines):
                item = re.match(r"^\s*[-*]\s+(.+)$", lines[i])
                if not item:
                    break
                out.append(f"<li>{inline_md(item.group(1))}</li>")
                i += 1
            out.append("</ul>")
            continue

        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered:
            out.append("<ol>")
            while i < len(lines):
                item = re.match(r"^\s*\d+[.)]\s+(.+)$", lines[i])
                if not item:
                    break
                out.append(f"<li>{inline_md(item.group(1))}</li>")
                i += 1
            out.append("</ol>")
            continue

        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("<")
                or nxt.startswith("|")
                or re.match(r"^(#{1,3})\s+", nxt)
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+[.)]\s+", nxt)
            ):
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{inline_md(' '.join(para))}</p>")

    return "\n".join(out).strip()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse a YAML-subset frontmatter block.

    Supports:
    - `key: value` (string scalar; may be quoted with single or double quotes)
    - `key: |` (literal block scalar; content is the indented block that follows)
    - blank lines and # comments
    """
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.group(1), match.group(2)
    result: dict[str, str] = {}

    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "|":
            # Block scalar: consume indented following lines.
            block_lines: list[str] = []
            i += 1
            base_indent: int | None = None
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    block_lines.append("")
                    i += 1
                    continue
                indent = len(nxt) - len(nxt.lstrip(" "))
                if base_indent is None:
                    base_indent = indent if indent > 0 else 1
                if indent < base_indent:
                    break
                block_lines.append(nxt[base_indent:])
                i += 1
            # Trim trailing blank lines
            while block_lines and block_lines[-1] == "":
                block_lines.pop()
            result[key] = "\n".join(block_lines)
            continue

        # Strip matching quotes
        if len(value) >= 2 and ((value[0] == value[-1]) and value[0] in ('"', "'")):
            value = value[1:-1]

        result[key] = value
        i += 1

    return result, body


def md_to_html(markdown_text: str) -> str:
    """Render markdown body to HTML using pandoc."""
    if not markdown_text.strip():
        return ""
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return fallback_md_to_html(markdown_text)
    proc = subprocess.run(
        [pandoc, "--from=markdown+pipe_tables+smart+raw_html", "--to=html5", "--wrap=none"],
        input=markdown_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def load_template(template_name: str) -> str:
    path = TEMPLATES_DIR / f"{template_name}.html"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def substitute(template: str, mapping: dict) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        return str(mapping.get(key, ""))
    return re.sub(r"\{\{([^}]+)\}\}", replace, template)


def discover_slides(deck_dir: Path) -> list[Path]:
    files = sorted(
        p for p in deck_dir.iterdir()
        if p.is_file()
        and p.suffix == ".md"
        and not p.name.startswith(".")
        and p.name not in {"README.md", "deck.yaml"}
    )
    if not files:
        sys.exit(f"No slide markdown files found in {deck_dir}")
    return files


def read_deck_meta(deck_dir: Path) -> dict:
    """Read optional deck.yaml as a flat key:value frontmatter-style block."""
    meta_file = deck_dir / "deck.yaml"
    if not meta_file.exists():
        return {}
    text = meta_file.read_text(encoding="utf-8").strip()
    if not text.startswith("---"):
        text = "---\n" + text + "\n---\n"
    fm, _ = parse_frontmatter(text + ("\n" if not text.endswith("\n") else ""))
    return fm


def render_slide(file_path: Path, slide_number: int, slide_count: int, deck_meta: dict, deck_dir: Path) -> str:
    text = file_path.read_text(encoding="utf-8")
    fm, body_md = parse_frontmatter(text)

    template_name = fm.get("template")
    if not template_name:
        sys.exit(f"{file_path.name}: missing 'template' in frontmatter")

    template = load_template(template_name)
    body_html = md_to_html(body_md)

    subtitle = fm.get("subtitle", "")
    subtitle_block = f'<div class="slide__subtitle">{escape(subtitle)}</div>' if subtitle else ""

    # Optional "kicker" callout: a one-line meta-message rendered as a band at
    # the bottom of the body area. Templates that opt into the kicker pattern
    # include {{kicker_block}}; the placeholder renders nothing when the slide
    # author didn't define a kicker.
    kicker = fm.get("kicker", "")
    kicker_block = f'<div class="callout slide__kicker">{md_to_html(kicker).strip()}</div>' if kicker else ""

    notes = fm.get("notes", "")
    notes_html = md_to_html(notes) if notes else ""

    # Logo blocks: cover logo on title/closing slides, footer brand strip on content slides.
    cover_logo_spec = fm.get("cover_logo", deck_meta.get("cover_logo", ""))
    cover_logo_imgs = render_logo_block(cover_logo_spec, deck_dir, "cover-logo")
    cover_logo_block = f'<div class="cover-logo-block">{cover_logo_imgs}</div>' if cover_logo_imgs else ""

    brand_footer_spec = fm.get("brand_footer", deck_meta.get("brand_footer", ""))
    brand_footer_imgs = render_logo_block(brand_footer_spec, deck_dir, "brand-footer-logo")

    # Convention: brand logos render in the RIGHT footer slot; text (e.g. the
    # "Confidential draft — DATE" line) sits in the LEFT slot. When brand_footer
    # is set, footer_right shows the logos; otherwise it falls back to whatever
    # text is in the footer_right frontmatter / deck.yaml field.
    footer_right_text = fm.get("footer_right", deck_meta.get("footer_right", ""))
    if brand_footer_imgs:
        footer_right_rendered = f'<div class="footer-brand-strip">{brand_footer_imgs}</div>'
    else:
        footer_right_rendered = escape(footer_right_text)

    mapping = {
        "slide_number": str(slide_number),
        "slide_count": str(slide_count),
        "title": escape(fm.get("title", "")),
        "subtitle": escape(subtitle),
        "subtitle_block": subtitle_block,
        "eyebrow": escape(fm.get("eyebrow", "")),
        "body": body_html,
        "notes": notes_html,
        "footer_left": escape(fm.get("footer_left", deck_meta.get("footer_left", ""))),
        "footer_right": footer_right_rendered,
        "prepared_for": escape(fm.get("prepared_for", "")),
        "prepared_by": escape(fm.get("prepared_by", "")),
        "date": escape(fm.get("date", "")),
        "status": escape(fm.get("status", "")),
        "cover_logo_block": cover_logo_block,
        "kicker_block": kicker_block,
        # Legacy slot retained as a no-op for backward compatibility.
        "brand_footer_block": "",
    }

    # Pass-through for any extra frontmatter key the slide author defines.
    # This lets new templates declare named regions (e.g. q1_title, q1_body,
    # phase_1_title, x_axis) without needing per-template Python wiring.
    # For each extra key we expose two placeholders:
    #   {{key}}    -> HTML-escaped scalar (safe for inline text and attrs)
    #   {{key_md}} -> markdown-rendered HTML block (use this for body-like fields
    #                 that may contain lists, bold, links, etc.)
    # Keys already in `mapping` are NOT overwritten (the fixed semantics win).
    for key, value in fm.items():
        if key in mapping or key in {"template", "cover_logo", "brand_footer", "subtitle"}:
            continue
        text_value = value if isinstance(value, str) else str(value)
        if key not in mapping:
            mapping[key] = escape(text_value)
        md_key = f"{key}_md"
        if md_key not in mapping:
            mapping[md_key] = md_to_html(text_value) if text_value.strip() else ""

    # Any placeholder a template references but the slide didn't define should
    # render as empty rather than leaving the literal "{{key}}" in the output.
    template_keys = set(re.findall(r"\{\{([^}]+)\}\}", template))
    for tk in template_keys:
        mapping.setdefault(tk, "")

    return substitute(template, mapping)


def build_html(deck_dir: Path, with_notes: bool, embed: bool = False) -> Path:
    slide_files = discover_slides(deck_dir)
    deck_meta = read_deck_meta(deck_dir)

    css_text = CSS_FILE.read_text(encoding="utf-8")
    # Per-deck theme.css override (loaded after deck.css so it wins on conflicts).
    theme_file = deck_dir / "theme.css"
    if theme_file.exists():
        theme_text = theme_file.read_text(encoding="utf-8")
        css_text = css_text + "\n\n/* === Per-deck theme.css === */\n" + theme_text

    deck_title = deck_meta.get("title", deck_dir.name)

    # Pre-build logo safety pass: scan every slide for cover_logo and brand_footer
    # references and warn loudly if the logo background does not match the slide
    # background. This catches the "white logo on dark slide" / "dark logo on white
    # slide" failure modes before render.
    logo_warnings: list[str] = []
    for slide_file in slide_files:
        fm, _ = parse_frontmatter(slide_file.read_text(encoding="utf-8"))
        template_name = fm.get("template", "")
        cover_logo_spec = fm.get("cover_logo", deck_meta.get("cover_logo", ""))
        brand_footer_spec = fm.get("brand_footer", deck_meta.get("brand_footer", ""))
        # Title / section / closing templates render on a dark cover; content / agenda on white.
        if template_name in {"title", "section_divider", "closing"}:
            specs = [(cover_logo_spec, f"{slide_file.name} cover_logo")]
            slide_bg = "dark"
            logo_warnings.extend(check_logo_safety(specs, deck_dir, slide_bg))
            # Content-style footer logos do not normally appear on cover slides; skip.
        else:
            specs = [(brand_footer_spec, f"{slide_file.name} brand_footer")]
            slide_bg = "white"
            logo_warnings.extend(check_logo_safety(specs, deck_dir, slide_bg))
    if logo_warnings:
        print("\n[LOGO SAFETY] One or more logos look incompatible with their target slide:")
        for warning in logo_warnings:
            print(f"  - {warning}")
        print("[LOGO SAFETY] Build proceeds, but inspect the rendered slides carefully.\n", file=sys.stderr)

    rendered_slides = []
    for index, slide_file in enumerate(slide_files, start=1):
        rendered_slides.append(render_slide(slide_file, index, len(slide_files), deck_meta, deck_dir))

    body_class = "deck with-notes" if with_notes else "deck"
    slides_html = "\n".join(rendered_slides)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(deck_title)}</title>
  <style>
{css_text}
  </style>
  <script src="{CHART_JS_CDN}"></script>
</head>
<body>
  <div class="{body_class}">
{slides_html}
  </div>
</body>
</html>
"""

    if embed:
        html = embed_assets(html, deck_dir)

    # Strip trailing whitespace on each line so the file passes a strict pre-commit hook.
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"

    out_name = "deck-notes.html" if with_notes else "deck.html"
    out_path = deck_dir / out_name
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_folder", help="Path to the deck folder containing slide markdown files")
    parser.add_argument("--with-notes", action="store_true", help="Also build deck-notes.html showing speaker notes")
    parser.add_argument("--embed-assets", action="store_true", help="Inline local <img> assets as base64 so the HTML is self-contained")
    args = parser.parse_args()

    deck_dir = Path(args.deck_folder).resolve()
    if not deck_dir.is_dir():
        sys.exit(f"Not a directory: {deck_dir}")

    clean_path = build_html(deck_dir, with_notes=False, embed=args.embed_assets)
    print(f"Built: {clean_path}")

    if args.with_notes:
        notes_path = build_html(deck_dir, with_notes=True, embed=args.embed_assets)
        print(f"Built: {notes_path}")

    print()
    print("View: open the HTML file in a browser (Chrome / Safari / Firefox).")
    print("Export PDF: in the browser, File -> Print -> 'Save as PDF', orientation landscape, no margins, scale 100%, Background Graphics on.")


if __name__ == "__main__":
    main()
