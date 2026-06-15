# Slide Deck Patterns

Reusable layout patterns, the template catalog, and pandoc gotchas for the Max OS slide-deck skill.
Pair this with [deck.css](deck.css) (CSS), [Skill - Slide Deck Generation.md](../../Skill%20-%20Slide%20Deck%20Generation.md) (workflow), and the live [template gallery](_gallery/) (one example slide per template, themeable).

When you build a deck, **start from the templates and patterns here**. To preview a template under your brand palette before writing your slide, rebuild the gallery with the matching `theme-*.css`:

```bash
cd 15_Skills/tools/slides/_gallery
./switch_theme.sh dmg          # or: default, or any theme-*.css you add
python3 ../build_deck.py .
open deck.html
```

Do not re-derive layouts inline in a deck's `theme.css` — promote anything reusable back into [deck.css](deck.css) and document the pattern here.

---

## Typography defaults (don't override unless you have a reason)

The defaults in [deck.css](deck.css) reflect preferences validated across exec read-out decks:

- `.slide__title` — **38px**, line-height **1.1**.
- `.slide__subtitle` — **19px**, margin-bottom **36px**, line-height **1.4**. The big margin matters: exec audiences read subtitles slower than designers expect, and crowding the body against the subtitle reads as a wall of text.
- `.slide__body h3` — margin-bottom **12px** (not 2px). In-body section heads need room between the head and the bullet list that follows.

If a brand has its own type stack (e.g. dmg media's Nunito Sans + Barlow), override `--font-sans` and the `.slide__title, .title-headline, ...` font-family rule in the per-deck `theme.css`. Keep sizes inherited from `deck.css`.

---

## Layout patterns

### 1. Capacity cards — row of titled cards with eyebrow + bullets

For named, parallel capacities or pillars where each card carries substantive content. **Not** for out-of-context value pulls (those are `.metric-card`).

```html
<div class="capacity-row">
  <div class="capacity-card">
    <h3>Heading</h3>
    <ul>
      <li><strong>Lead</strong>. Outcome / proof.</li>
      <li>...</li>
    </ul>
  </div>
  <div class="capacity-card">
    <h3>Heading</h3>
    <ul>...</ul>
  </div>
</div>
```

Default is 2 columns. Use `.capacity-row--3col` or `.capacity-row--4col` modifiers for denser layouts. Above 4 columns the type gets crushed — use a 2×2 grid instead (still `.capacity-row` with `repeat(2, 1fr)` plus more cards).

**Anti-pattern:** writing three or four cards where each card is a different framing of the *same* projects. Reads as padding. If you find yourself doing this, collapse to two cards plus a kicker callout below (see next pattern).

### 2. Kicker callout — meta-message below a row of cards

When you have two strong cards plus a meta-theme that wants to say "and here's *why* these work", put the meta-theme in a `.callout.capacity-kicker` band below the row. Cleaner than reshuffling the same projects into a redundant third card.

```html
<div class="capacity-row">...</div>

<div class="callout capacity-kicker">
  <strong>Why these projects actually land.</strong> POCs picked for real commercial upside, not science projects. Leadership aligned from RFP through to production handover. Operating-model change as the actual deliverable — not the model in isolation.
</div>
```

### 3. Two-column body — left/right grid

```html
<div class="two-col">
  <div class="col">
    ### Left heading
    - Bullet
    - Bullet
  </div>
  <div class="col">
    ### Right heading
    - Bullet
    - Bullet
  </div>
</div>
```

**Critical:** the inner divs need `class="col"` (or any class). Bare `<div>` wrappers get stripped by pandoc — see Pandoc Gotchas below.

### 4. Fixed-width table columns — write the table as raw HTML

Pandoc's pipe-table renderer emits a `<colgroup>` with equal-percentage `<col>` widths that override any CSS you put on `td:nth-child(N)`. To get real per-column widths, **write the table as raw HTML inside the markdown** so the `<col>` widths YOU pick are the ones that ship.

```html
<table class="quick-wins">
<colgroup>
<col style="width: 8%">
<col style="width: 34%">
<col style="width: 28%">
<col style="width: 30%">
</colgroup>
<thead>
<tr><th>#</th><th>Quick win</th><th>Sponsor</th><th>Outcome</th></tr>
</thead>
<tbody>
<tr>
<td><strong>QW1</strong></td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</tbody>
</table>
```

This bypasses pandoc's pipe-table renderer entirely. Pair with CSS:

```css
.slide[data-slide="N"] table.quick-wins {
  width: 95%;
  margin-left: auto;
  margin-right: auto;
  table-layout: fixed;
}
```

`table-layout: fixed` is mandatory — without it the `<col>` widths are advisory and the browser still auto-sizes based on content.

### 5. Metric cards — small punchy value pulls

Built into [deck.css](deck.css) as `.metric-row` + `.metric-card`. Use sparingly and only when the metric reads in context to the audience. **A bare "+0.05 AUC uplift" is meaningless to an ExCo** — they need either a € outcome or a sentence of framing. If you can't frame it in a card-sized space, use a capacity-card instead.

---

## Pandoc gotchas

Pandoc renders the markdown — these are the patterns where it does something surprising and silently breaks the layout. Always inspect the rendered `deck.html` if a CSS rule isn't visibly applying.

### Pipe tables → `<colgroup>` with equal widths

Pandoc emits `<col style="width: 25%">` for each column of a pipe table, regardless of what you wrote. These inline styles outrank `td:nth-child(N)` CSS. **Fix:** write tables as raw HTML (see pattern 4 above).

### Bare `<div>` wrappers get stripped

`<div>` with no class/id is treated as semantically empty and gets stripped. The contents survive but the wrapper is gone — which collapses any grid/flex layout that depended on it.

**Fix:** always put a class on `<div>` wrappers. Example: `class="col"` for `.two-col` children, `class="capacity-card"` for capacity-card children. The class doesn't have to *do* anything CSS-wise; it just keeps the wrapper alive through the pandoc pass.

### Indented raw HTML inside markdown → fenced code block

If a `<div>` block is indented (4+ spaces of leading whitespace), pandoc treats it as a fenced code block and renders the HTML as literal source on the slide.

**Fix:** de-indent raw HTML blocks in markdown. Keep them flush left even when they sit inside list items or blockquotes.

### Subtle: pandoc removes whitespace from `<th>`/`<td>` content

If you write `<td> content </td>` (with leading/trailing space), pandoc preserves the space inside the cell, which can offset alignment. Write `<td>content</td>` without padding-whitespace.

---

## Promoting back to global

If you find yourself writing the same per-deck CSS more than once, **promote it back into [deck.css](deck.css)** and document the pattern here.

The signal: a `theme.css` should only contain palette/font/brand-specific overrides plus narrowly-scoped fixes for a particular slide (e.g. `.slide[data-slide="5"]` table sizing for THAT slide's content). General-purpose layouts (capacity cards, kicker callouts, two-col) belong in the global stylesheet.

---

## Exporting to PDF

Use `node 15_Skills/tools/slides/build_deck_pdf.mjs <deck_folder>/deck.html` to produce a PDF that matches the HTML preview exactly.

**Do NOT use Chromium's `page.pdf()` directly.** It runs a different rasteriser from `page.screenshot()` (the one that renders the HTML preview and the visual QA screenshots), and on slides with subtle card box-shadows the PDF output picks up visible grey halos around every card that aren't in the preview. It also silently activates `@media print` CSS rules, which can shift slide padding from the screen values.

The `build_deck_pdf.mjs` workflow captures each slide as a 2× DPI screenshot via the screen pipeline, then stitches the screenshots into a PDF one-per-page. Because each PDF page is a flat raster, the PDF pipeline can't differ from the screenshot — PDF == HTML preview, pixel-for-pixel.

**Trade-off:** the resulting PDF is a raster (~500 KB – 2 MB for a 12-slide deck) and the text inside slides isn't selectable. If you need selectable text or a smaller file, fall back to browser-native File → Save as PDF (and accept the rendering drift).

If you ever add a custom card pattern that uses box-shadows, drop-shadows, or other subtle visual effects, **inspect the PDF, not just the HTML preview** before reporting the deck done. The two can drift silently.

---

## Template catalog (by slide purpose)

Templates live at [`templates/`](templates/). Each template is referenced from a slide's frontmatter via `template: <name>`. Every template inherits the global [`deck.css`](deck.css) and any per-deck [`theme.css`](../../../04_Projects/) overrides; new templates use only `--color-*` CSS variables (never hardcoded brand colours), so they re-skin automatically under any theme.

Authoring conventions:

- **Named regions → frontmatter fields.** A 2x2 quadrant has `q1_title`, `q1_body`, etc.; a split title has `brand_mark`, `strapline`. Each field maps to `{{q1_title}}` in the template (escaped) or `{{q1_title_md}}` (markdown-rendered HTML block — for fields that contain lists, bold, links).
- **Repeated identical items → markdown list in body.** Agenda items, bullet rows, and any uniform set of items go into the body as a `1. **Lead-in.** Description.` ordered list. The CSS reshapes the list into cards / a timeline / etc. **Use a period after the bold lead-in, not an em-dash separator** — pandoc renders ` — ` as a literal character that hangs awkwardly when `<strong>` is styled `display: block`.

The catalog below is grouped by what the slide does in a consulting deck, not by its shape. Within each group, templates are ordered roughly by frequency of use.

### Opening

#### `title` — classic centred cover
The workhorse opener. Eyebrow / headline / subtitle / four-row metadata grid, all centred on the cover background. Use when you want a calm, formal opener that puts the audience and the brief front-and-centre. See [`_gallery/01_title.md`](_gallery/01_title.md).

Frontmatter: `eyebrow`, `title`, `subtitle`, `prepared_for`, `prepared_by`, `date`, `status`, optional `cover_logo`.

#### `title_hero` — full-bleed cover with image overlay
A photographic or full-bleed visual fills the slide. The eyebrow / headline / subtitle / metadata sit in a darkened lower-left zone (a gradient tint preserves text legibility on any photo). Use when you want a magazine-cover feel and the topic deserves a strong visual anchor (industry photography, hero product shot). When `hero_image` is empty, the cover background colour shines through — useful as a "moody dark cover" variant. See [`_gallery/02_title_hero.md`](_gallery/02_title_hero.md).

Frontmatter: `eyebrow`, `title`, `subtitle`, `prepared_for`, `prepared_by`, `date`, optional `hero_image` (path under the deck folder), optional `cover_logo`.

#### `title_split` — split cover with content + brand block
60/40 split. Left: full cover content on the cover background. Right: an accent-coloured panel with a large brand mark (single letter or word) and an uppercase strapline. Use when the engagement has a clear brand combination to feature ("Client × Helios"), or when you want a graphic identity moment on the cover. See [`_gallery/03_title_split.md`](_gallery/03_title_split.md).

Frontmatter: `eyebrow`, `title`, `subtitle`, `prepared_for`, `prepared_by`, `date`, `brand_mark` (single character or short word), `strapline` (short line, uppercase styling applied by CSS).

#### `title_image_card` — title + offset image card
60/40 split. Left: cover content on the cover background. Right: an inset image card with a thin caption strip at the bottom. The image is a supporting visual rather than the dominant background (cf. `title_hero`). Use when you want to feature a specific photograph (operating site, product) without it overwhelming the title text. Falls back to a brand-coloured card with caption when `hero_image` is empty. See [`_gallery/04_title_image_card.md`](_gallery/04_title_image_card.md).

Frontmatter: `eyebrow`, `title`, `subtitle`, `prepared_for`, `prepared_by`, `date`, optional `hero_image`, optional `caption`.

### Agenda

#### `agenda` — numbered two-column list
The default agenda. 6-8 items split across two columns; numbers in accent colour. Use when items are short, equal weight, and the audience wants to see the whole arc at a glance. See [`_gallery/05_agenda.md`](_gallery/05_agenda.md).

Frontmatter: `eyebrow`, `title`. Body: a markdown ordered list.

#### `agenda_grid` — equal-weight cards in a 3-column grid
Each item gets its own card with the number on the left and a `**Lead-in.** description` body on the right. Use when items deserve a one-line elaboration (not just a label) and you want them to read as parallel sections rather than a sequence. Best for 4-6 items. See [`_gallery/06_agenda_grid.md`](_gallery/06_agenda_grid.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`. Body: a markdown ordered list, each item in `**Lead-in.** Description.` form.

#### `agenda_timeline` — horizontal phase row
A horizontal row of numbered phase nodes joined by a connecting line. Each phase shows a number circle, a short bold title, and a one-line description below. Use when the agenda IS the timeline (i.e. items are sequential phases of work) — not for a list of unrelated topics. Best for 3-6 phases. See [`_gallery/07_agenda_timeline.md`](_gallery/07_agenda_timeline.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`. Body: a markdown ordered list, each item in `**Phase.** Description.` form. Keep titles short (one word or short phrase) — the timeline columns are narrow and long titles will wrap awkwardly.

### Executive Summary

#### `exec_summary_recommendation` — answer-first, with three supporting points
Top: a filled accent-coloured hero card with `WE RECOMMEND` label and the recommendation sentence. Bottom: 3 supporting cards in a row, each carrying a numbered lead-in and a one-sentence justification. Use this as the front-of-deck answer when the audience is busy and the read-out runs short — they get the answer in 10 seconds and the rationale in 60. See [`_gallery/08_exec_summary_recommendation.md`](_gallery/08_exec_summary_recommendation.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `recommendation_label` (e.g. `"WE RECOMMEND"`), `recommendation` (the headline statement). Body: a markdown ordered list of **exactly 3** items in `**Lead.** Description.` form. The 3-column grid is fixed; more items would crowd the cards and fewer would leave gaps.

#### `exec_summary_pyramid` — Minto pyramid as a slide
Top: a wide hero card with `GOVERNING THOUGHT` label and the governing answer; a small downward-pointing triangle hints the pyramid metaphor. Bottom: 3 argument columns, each with a title and a bulleted body of supporting evidence. Use when you want to show that the recommendation rests on *three independent arguments*, each backed by 2-3 facts — typical Minto SCQA structure. Visually distinct from `exec_summary_recommendation` because each supporting column carries its own sub-list. See [`_gallery/09_exec_summary_pyramid.md`](_gallery/09_exec_summary_pyramid.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `governing_label`, `governing_thought`, then for each of the 3 arguments: `arg_N_title` and `arg_N_body` (multi-line block scalar containing a markdown bullet list — rendered via `{{arg_N_body_md}}`). Three argument columns are fixed; deeper structures belong in a follow-on slide.

### Diagnosis

#### `diagnosis_situation_complication` — SCR (Situation / Complication / Resolution)
Three cards in a row joined by arrow connectors. Situation and Complication render in neutral soft-accent; Resolution is filled in the accent colour with white text — emphasising the recommendation at ~60-70% visual weight, matching the conventional SCR proportion. Use when you want to walk the audience through *why now* before stating what to do. See [`_gallery/10_diagnosis_situation_complication.md`](_gallery/10_diagnosis_situation_complication.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, and for each of the three cards: `<role>_label` (e.g. `"SITUATION"`) and `<role>_body` (block scalar with markdown content — rendered via `{{<role>_body_md}}`). Roles: `situation`, `complication`, `resolution`. All three are required.

#### `diagnosis_root_cause` — visible symptom branching to root causes
Top: a dark hero card stating the visible symptom or observed problem. A vertical connector drops to a horizontal cross-bar, which fans out to 2-4 root-cause cards. Use when the audience needs to see that one visible problem has several distinct underlying drivers — i.e. when the diagnosis is genuinely multi-causal and the fix is not one thing. See [`_gallery/11_diagnosis_root_cause.md`](_gallery/11_diagnosis_root_cause.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `symptom_label`, `symptom_body`. Body: a markdown ordered list of 2-4 root-cause items in `**Cause.** Description.` form. The grid auto-fits the number of items.

#### `diagnosis_findings_table` — N findings × evidence × implication
A table-led slide. Three columns: Finding (bold), Evidence (the data), Implication (the so-what). Optional kicker callout band below the table for the meta-message. Use when you have 4-6 discrete findings each needing evidence and a one-line implication — denser than a card layout, more scannable than narrative paragraphs. See [`_gallery/12_diagnosis_findings_table.md`](_gallery/12_diagnosis_findings_table.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker` (renders as a band at the foot of the body — see the Kicker section below). Body: a raw-HTML table with `class="findings-table"` and a `<colgroup>` setting column widths (see the fixed-width table pattern above). Use `<strong>` inline within the Implication column to highlight the key number or phrase.

---

### Framework

#### `framework_2x2_quadrant` — classic two-axis matrix
Four cells with X and Y axis labels. Top-left and top-right cells get an accent left-border emphasising the "high-impact" row; bottom-right uses a neutral grey to signal de-prioritisation. Use this whenever you'd reach for a 2x2 framework — Effort × Impact, Risk × Return, Familiarity × Strategic Value. See [`_gallery/13_framework_2x2_quadrant.md`](_gallery/13_framework_2x2_quadrant.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `x_axis`, `y_axis`, then for each cell `q_tl_*`, `q_tr_*`, `q_bl_*`, `q_br_*` with `_title` and `_body` (markdown). Optional `kicker`.

#### `framework_2x2_centered` — four forces around a central anchor
2x2 layout where the four cells sit around a central circular anchor card. Use when the four cells are *forces or pressures on a central subject* (the client, the product, the asset) rather than independent dimensions on two axes. Inspired by USPS 2010 page 3. See [`_gallery/14_framework_2x2_centered.md`](_gallery/14_framework_2x2_centered.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `top_label`, `bottom_label`, four cells (`tl_title`/`tl_body`, etc.), and `center_label` / `center_body` for the central anchor. Optional `kicker`.

#### `framework_3_pillars` and `framework_4_pillars` — N parallel pillars with depth
A row of 3 or 4 named pillar cards, each with an optional icon/number, a bold title, an italic lead line, and a body of bullets. Use when you have N strategic capacities and each one deserves its own evidence list. The 3-pillar form is the canonical "Three Things" McKinsey layout; the 4-pillar form trades per-pillar density for breadth. See [`_gallery/15_framework_3_pillars.md`](_gallery/15_framework_3_pillars.md) and [`_gallery/16_framework_4_pillars.md`](_gallery/16_framework_4_pillars.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, and for each pillar: `pN_icon` (short text/glyph/number — empty hides the icon block), `pN_title`, `pN_lead` (one-line summary), `pN_body` (multi-line markdown bullets). Optional `kicker`.

#### `framework_6_pillars` — six pillars in a 2×3 grid
Same pillar card visual language as `framework_3_pillars`, but the grid wraps to 2 rows of 3. Use when six parallel capacities, tracks, or workstreams each need a card. Best for resourcing slides, capability portfolios, and similar "six things in parallel" content. Above 6 the type gets crushed — split into two slides instead.

Frontmatter: `eyebrow`, `title`, optional `subtitle`, and for each pillar (1..6): `pN_icon`, `pN_title`, `pN_lead`, `pN_body` (multi-line markdown bullets). Optional `kicker`.

#### `framework_5_plus_foundation` — 3-2-1 tapered pillars with foundation strip
Five pillar cards laid out 3-on-top / 2-centred-below, plus a sixth full-width "foundation" card rendered in the dark cover background with light text — reads as a substrate the five pillars sit on. Use when five parallel items rest on a load-bearing cross-cutting layer (e.g. five strategic priorities backed by a shared platform, four product tracks plus a regulatory backbone, five workstreams with a common ops chassis). The foundation card uses a horizontal layout (title + body inline) to suggest "layer" rather than "additional item".

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each pillar (1..5): `pN_icon`, `pN_title`, `pN_lead`, `pN_body`; plus `foundation_icon`, `foundation_title`, optional `foundation_lead`, `foundation_body_md` (kept short — single sentence or two-bullet list). Optional `kicker`.

#### `framework_inputs_to_output` — multi-source synthesis
Multiple input cards on the left flow via a large accent arrow into a single filled output card on the right. Use when you want to show that the deliverable on the right *reconciles* or *integrates* multiple parallel work-streams. Inspired by USPS 2010 page 2 (BCG + Accenture work synthesised by McKinsey). See [`_gallery/17_framework_inputs_to_output.md`](_gallery/17_framework_inputs_to_output.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `inputs_label`, `i1_title`/`i1_body`, `i2_title`/`i2_body`, optional `i3_title`/`i3_body` (third input card auto-hides if `i3_title` is empty), `output_label`, `output_title`, `output_body` (markdown). Optional `kicker`.

#### `framework_architecture_flow` — system architecture diagram
A three-zone flow diagram: source boxes on the left, two arrow-shaped "pipe" boxes in the middle (the processing zone), output boxes on the right. Each box has a numbered circle. Inspired by IoT 2013 page 10 (the "Internet of Things" high-level architecture). Use for showing how a system, platform or data plane works end-to-end at one level of abstraction. See [`_gallery/18_framework_architecture_flow.md`](_gallery/18_framework_architecture_flow.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `left_zone_label`, `middle_zone_label`, `right_zone_label`, and `box_1_title` through `box_6_title` (six numbered components). Optional `kicker`.

#### `framework_lettered_categories` — A/B/C grouped taxonomy
A sidebar of group labels on the left, with A/B/C... lettered rows on the right. Each row has a bold title and a one-line description. Inspired by IoT 2013 pages 11-13 (six IoT use cases grouped into Information & Automation). Use for taxonomies where each item sits within a higher-level group and you want both layers visible at once. See [`_gallery/19_framework_lettered_categories.md`](_gallery/19_framework_lettered_categories.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `group_a_label`, `group_b_label`. Body: a markdown ordered list using `**Title.** Description.` form. The first half of the list visually maps to group A, the second half to group B (CSS positions them vertically aligned with the sidebar groups).

#### `framework_multiplier` — A × B = C
Two factor cards joined by an "×", then "=" leading to a result card filled in the accent colour. Use when the recommendation rests on a *multiplicative* business case — e.g. cost-per-unit × unit base = annualised impact. Inspired by USPS 2010 page 4 (volume decline × price increase = flat revenue forecast). See [`_gallery/20_framework_multiplier.md`](_gallery/20_framework_multiplier.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, then for each factor and the result: `factor_a_label`/`factor_a_value`/`factor_a_note`, `factor_b_label`/`factor_b_value`/`factor_b_note`, `result_label`/`result_value`/`result_note`. The `_value` field renders as the big number; the `_note` is a small explanatory line below. Optional `kicker`.

#### `framework_capacity_2x2` — DMG-style 2x2 of titled capacity cards
Four titled cards in a 2x2, each with an h3 title and a bulleted body using bold lead-ins. Accent border-left on every card; optional kicker callout below. This is the DMG-deck `capacity-row` pattern (slide 11) extended to four cards — use it for "capabilities" / "tracks" / "domains" slides where each card carries substantive evidence rather than abstract framework labels. Visually distinct from `framework_2x2_quadrant` (which has axis labels and quadrant logic) — use `framework_capacity_2x2` when the four cards are *parallel substantive categories*, not positions on a 2-axis framework. See [`_gallery/49_framework_capacity_2x2.md`](_gallery/49_framework_capacity_2x2.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, then for each card (1..4): `cN_title` and `cN_body` (multi-line markdown bullet list — rendered via `{{cN_body_md}}`). Optional `kicker`. Use `**bold lead-in.**` form for each bullet to anchor the evidence.

### Next steps

#### `next_steps_owners_dates` — action table with owner + target columns
A four-column action table: row number, action description (bold lead-in + supporting line), owner name, target date in accent. Use as the canonical "next-steps" slide of an exec read-out — five rows fits comfortably; six is tight. See [`_gallery/50_next_steps_owners_dates.md`](_gallery/50_next_steps_owners_dates.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a raw HTML `<table class="next-owners-table">` with `<colgroup>` widths (44px / auto / 200px / 140px) and `<thead>` + `<tbody>` rows. Each `<td>` in column 2 should lead with `<strong>...</strong>` for the bold action lead-in. **Don't try to write this as a markdown ordered list with inline `<span>` columns** — pandoc renders the spans as inline siblings, not grid columns, and the layout collapses.

#### `next_steps_two_lanes` — Immediate vs. Follow-on triage
Two side-by-side lane cards. Default labels: "Immediate / This week" (accent-filled, white text) and "Follow-on / Within 14 days" (soft accent). Each lane has a bulleted body with checkbox-style markers. Use when next steps split naturally into immediate vs. follow-on; helps the sponsor team triage what needs them this week vs. what they'll see again. See [`_gallery/51_next_steps_two_lanes.md`](_gallery/51_next_steps_two_lanes.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `lane_1_label` / `lane_1_timeframe` / `lane_1_body` (markdown bullets), `lane_2_label` / `lane_2_timeframe` / `lane_2_body`. Optional `kicker`.

#### `next_steps_horizontal_track` — five horizontal step cards on a connecting line
Five horizontal step cards in a row, joined by a connecting accent line through the numbered nodes on top of each card. Each card carries an action title, a when-by date in accent, and an owner italicized. Use for visual sequencing of immediate next steps — best when the sequence (and the critical path) matters more than the per-step detail. Five steps is the natural fit; the layout is fixed at five. See [`_gallery/52_next_steps_horizontal_track.md`](_gallery/52_next_steps_horizontal_track.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each step (1..5): `sN_action`, `sN_when`, `sN_owner`. Optional `kicker`.

---

### Quantitative

The `data_*` templates are *layout shells*. The author writes the chart (Chart.js inline `<canvas>` + `<script>`) or table (raw HTML) inside the slide body; the template provides the title / subtitle / commentary / callout / kicker scaffold around it. The header, axis-label band, table header tint, heatmap shading and callout chrome all use `--color-*` CSS variables so they re-skin automatically under any theme. **Chart paint (the dataset's `backgroundColor` / `borderColor`) is author-controlled** — if you want DMG-purple bars, write `#9A4E9E` in your Chart.js dataset. The templates can't override what Chart.js renders into a canvas.

#### `data_chart_with_commentary` — chart-left, commentary-right
A two-column layout: chart on the left (~60%), commentary panel on the right (~40%) with an eyebrow label and bulleted body. Use as the workhorse data slide — the chart shows, the commentary tells. Inspired by Transportation 2020 page 3. See [`_gallery/21_data_chart_with_commentary.md`](_gallery/21_data_chart_with_commentary.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `commentary_label` (eyebrow above the right column), `commentary` (markdown block). Body: the chart's `<canvas>` + `<script>`. Optional `kicker`.

#### `data_chart_full_width` — single big chart
The chart takes the full body. Use when the chart needs the full slide width to read — long time-series, multi-line trend with 5+ series, or anything where the commentary would crowd the data. The title doubles as the takeaway. See [`_gallery/22_data_chart_full_width.md`](_gallery/22_data_chart_full_width.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: the chart's `<canvas>` + `<script>`.

#### `data_paired_charts_compare` — two charts side-by-side
Two equally-sized chart panes with their own labels and a thin divider between. Use for "Then vs Now", "A vs B", or "Before vs After" comparisons where each side deserves its own chart. Inspired by Transportation 2020 page 14. See [`_gallery/23_data_paired_charts_compare.md`](_gallery/23_data_paired_charts_compare.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `left_label`, `right_label`, `left_body` and `right_body` (each containing the chart's `<canvas>` + `<script>`; rendered via `{{left_body_md}}` / `{{right_body_md}}`). Optional `kicker`.

#### `data_metric_cards_row` — up to 4 KPI cards
A row of 3 or 4 metric cards, each with a big value, a label, and a small note. The fourth card auto-hides when `m4_value` is empty. Use for the headline KPIs slide at the top of a results / dashboard section. See [`_gallery/24_data_metric_cards_row.md`](_gallery/24_data_metric_cards_row.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each metric `mN_value` / `mN_label` / `mN_note` (N = 1..4; m4 optional), optional `context` (markdown line below the cards), optional `kicker`.

#### `data_heatmap_table` — value-shaded comparison table
A wide table whose numeric cells are shaded by value using `color-mix` (so the shading re-tints under any theme). Use for sector benchmarks or KPI cohorts where the colour pattern reveals the story. Inspired by Transportation 2020 page 4. See [`_gallery/25_data_heatmap_table.md`](_gallery/25_data_heatmap_table.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a raw HTML `<table class="heatmap-table">` with `<colgroup>` widths. Apply `class="h0"` (lightest) through `class="h4"` (strongest accent fill) to each numeric `<td>`. Use `class="num"` on numeric cells for tabular-num alignment. Highlight a focal row with `<tr class="focus-row">`.

#### `exhibit_relevance_matrix` — scored portfolio matrix (rows × grouped columns)
The signature consulting "relevance" exhibit: rows (industries, business units, segments) scored against columns (trends, capabilities, options) as a grid of **qualitative colour blocks** on a *sequential* shade scale, with the columns optionally bucketed under group super-headers and a gradient legend (low → high). Differs from `data_heatmap_table`, which shades *numeric* cells that each carry a value; here the cells are empty colour blocks and the pattern itself is the message. All shades derive from `--color-accent` via `color-mix`, so the matrix and its legend re-tint under any theme. Inspired by McKinsey Tech Trends Outlook 2022, Exhibit 2. See [`_gallery/68_exhibit_relevance_matrix.md`](_gallery/68_exhibit_relevance_matrix.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle` (use it for the full-sentence takeaway), optional `legend_low` / `legend_high` (the gradient legend labels), optional `source` (a footnote line; renders nothing when empty). Body: a raw HTML `<table class="relevance-matrix">` with a `<colgroup>` (first col ~20% for the row labels, the rest split evenly). Structure:
- Optional group super-header row: `<tr class="group-row">` with a leading empty `<th class="rowhead-col">` then one `<th class="colgroup" colspan="N">` per group.
- Column-header row: a leading empty `<th class="rowhead-col">` then one `<th class="colhead">` per column (labels wrap onto 2–3 lines).
- Body rows: `<th class="rowhead">Row label</th>` then one `<td class="cell rN">` per column, where `r0` is the faintest tint and `r4` the full accent. Cells are normally empty; put a number/label inside if you want a value shown (white text auto-applies on `r2`–`r4`).

#### `data_ranked_table_highlight` — ranked comparison with focus row
Cleaner table than the heatmap — no per-cell shading, but with a coral-highlighted focus row drawing the eye to the subject. Use for league-table-style comparisons. Inspired by Transportation 2020 page 11. See [`_gallery/26_data_ranked_table_highlight.md`](_gallery/26_data_ranked_table_highlight.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a raw HTML `<table class="ranked-table">` with `<tr class="focus-row">` for the highlight.

#### `data_chart_with_milestones` — trend with event markers
A trend chart with an optional legend strip below that decodes labelled milestone markers (A, B, C, etc.) drawn on the chart. Use when the chart's story is about *what happened at specific points* — interventions, releases, regime changes. Inspired by Transportation 2020 page 9. See [`_gallery/27_data_chart_with_milestones.md`](_gallery/27_data_chart_with_milestones.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `legend` (markdown one-liner labelling the markers), optional `kicker`. Body: the chart's `<canvas>` + `<script>`.

#### `data_small_multiples_2x2` — 2x2 grid of mini charts
Four small chart panes in a 2x2 grid, each with its own label. Use for "same metric across N regions / segments / periods" — *small multiples* in Tufte's sense. Inspired by Transportation 2020 page 12. See [`_gallery/28_data_small_multiples_2x2.md`](_gallery/28_data_small_multiples_2x2.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each pane `smN_label` and `smN_body` (each body contains a `<canvas>` + `<script>`; rendered via `{{smN_body_md}}`), optional `kicker`. Charts inside this template should be sized small (canvas height ≈ 110px) — the visual checker will fail if they push the kicker into the footer.

#### `data_waterfall_with_callout` — waterfall + side callout
Filled accent callout on the left (arrow-pointing-right shape via `clip-path`), waterfall chart on the right. Use when the bridge from start to end has 4-6 contributing levers worth naming. Inspired by USPS 2010 page 4. See [`_gallery/29_data_waterfall_with_callout.md`](_gallery/29_data_waterfall_with_callout.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `callout_label`, `callout_body` (multi-line markdown), optional `kicker`. Body: the waterfall chart's `<canvas>` + `<script>`.

#### `data_table_with_segments` — table with stacked-bar composition cells
A table whose rows contain a stacked-bar cell visualising a composition (e.g. demographic mix, share-of-X). Use when each row's *breakdown* matters as much as its scalar value. Inspired by Transportation 2020 page 6. See [`_gallery/30_data_table_with_segments.md`](_gallery/30_data_table_with_segments.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a raw HTML `<table class="segments-table">` with composition cells written as `<div class="seg-bar"><span class="seg-1" style="width: X%">N</span>...</div>` (use `.seg-1` through `.seg-4` for the four shade tiers).

---

### Comparison

#### `compare_before_after` — two panes with an arrow between
Left pane (Today / Before, muted), arrow, right pane (Target / After, accent-filled). Use as the transformation-narrative slide: same subject, two states. See [`_gallery/31_compare_before_after.md`](_gallery/31_compare_before_after.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `before_label`, `before_headline`, `before_body` (markdown), `after_label`, `after_headline`, `after_body` (markdown). Optional `kicker`.

#### `compare_options_table` — N options × M criteria with preferred column
A table comparing 2-4 options against a list of criteria, with the recommended option's column highlighted via `class="pref"` on its `<th>` and `<td>` cells. Use ahead of a recommendation slide to show the trade-offs the recommendation rests on. See [`_gallery/32_compare_options_table.md`](_gallery/32_compare_options_table.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a raw HTML `<table class="options-table">` with `<th class="pref">` on the recommended option's header and `<td class="pref">` on each cell in that column. Add `class="verdict"` for the final "Verdict" row's recommended cell.

#### `compare_mirror_bars` — A vs B horizontal bar mirror
Two columns of horizontal bars mirroring around a centre axis (Chart.js mirrored bar chart). Use for direct A-vs-B comparisons across a category list. Mirror legend below labels the two sides. Inspired by Transportation 2020 page 10. See [`_gallery/33_compare_mirror_bars.md`](_gallery/33_compare_mirror_bars.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `left_label`, `right_label`, optional `kicker`. Body: a mirrored horizontal bar chart with one side using negative values and a `ticks.callback` that strips the sign.

#### `compare_two_paths` — Path A vs Path B with pros and cons
Two side-by-side option cards labelled A and B, each with a name, one-liner, pros section and cons section. Use as a decision frame ahead of a recommendation. See [`_gallery/34_compare_two_paths.md`](_gallery/34_compare_two_paths.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `pros_label`, `cons_label`, for each path: `path_N_name`, `path_N_one_liner`, `path_N_pros` (markdown), `path_N_cons` (markdown). Optional `kicker`.

### Timeline / Roadmap

#### `roadmap_swimlane` — workstreams × phases grid
3 workstream lanes × 4 time phases. Top row is phase labels (`phase_N_label`), left column is lane labels (`lane_N_label`), inner cells contain the per-lane-per-phase deliverable. Use when you need to show how multiple workstreams sequence across time. See [`_gallery/35_roadmap_swimlane.md`](_gallery/35_roadmap_swimlane.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `phase_1_label` through `phase_4_label`, `lane_N_label` and `lane_N_pM` (lane N, phase M; both 1..3 lanes × 1..4 phases). Empty cells auto-render as a dashed-outline placeholder. Optional `kicker`.

#### `timeline_milestones` — vertical timeline with numbered nodes
A vertical timeline. Body is a markdown ordered list using `**Date — Milestone name.** Description.` form. CSS renders each item as a numbered milestone row connected by a vertical line. Use for board-level checkpoint timelines. See [`_gallery/36_timeline_milestones.md`](_gallery/36_timeline_milestones.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a markdown ordered list where each item is `**YYYY-MM — Milestone name.** One-line description.`.

#### `timeline_two_horizons` — Now / Next / Later columns
Three labelled horizon cards (Now / Next / Later). The Now card is accent-filled to emphasise the current commitment; Next and Later are softer. Use for roadmaps that need to honour rolling-horizon planning. See [`_gallery/37_timeline_two_horizons.md`](_gallery/37_timeline_two_horizons.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each horizon: `now_label` / `now_timeframe` / `now_body`, `next_*`, `later_*` (body fields are markdown). Optional `kicker`.

### Decision / Ask

#### `decisions_sought` — numbered decisions with named defaults
A list of decisions framed as questions, each with the ask in bold and the implication (default if not approved) named explicitly after. Use as the second-to-last slide of an exec read-out. See [`_gallery/38_decisions_sought.md`](_gallery/38_decisions_sought.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, optional `kicker`. Body: a markdown ordered list where each item is `**Question?** Default if not approved: ...`.

#### `asks_from_sponsor` — intro card + numbered asks list
Intro card on the left framing what's being asked of the sponsor, plus a numbered list of specific asks on the right. Use for "what we need from you in the first 14 days" slides. See [`_gallery/39_asks_from_sponsor.md`](_gallery/39_asks_from_sponsor.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `intro_label`, `intro_body` (markdown). Body: a markdown ordered list, each item in `**Ask.** Detail.` form. Optional `kicker`.

#### `risk_matrix` — 3x3 likelihood × impact grid
A 3x3 grid with risk items written into the cells (`cell_ll` = low/low through `cell_hh` = high/high). Shading gradient from soft to strong toward the top-right (high-impact × high-likelihood) alarm cell. Mitigation panel on the right. Use as the risks slide in any read-out. See [`_gallery/40_risk_matrix.md`](_gallery/40_risk_matrix.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `x_axis`, `y_axis`, nine cells (`cell_ll` through `cell_hh` — leave empty for cells with no risks), `legend_label`, `legend_body` (markdown). Optional `kicker`.

---

### Quote / Photo / Section / Closing

#### `quote_with_portrait` — centred quote, portrait, attribution
A centred big quote with a large opening quotation mark, italicised text, a circular portrait below, attribution and role under that. Inspired by IoT 2013 page 2. Use for setting up a section with a sharp framing quote (no slide title — the quote IS the slide). See [`_gallery/41_quote_with_portrait.md`](_gallery/41_quote_with_portrait.md).

Frontmatter: `eyebrow`, `quote`, `portrait_image` (path; falls back to a soft accent disc when empty), `attribution`, `attribution_role`. No `title` / `subtitle`.

#### `quote_extended` — portrait left, multi-paragraph quote right
A vertical portrait on the left, a multi-paragraph quote on the right with an optional source mark, attribution and role. Inspired by IoT 2013 page 6. Use when the quote is a substantive passage worth two or three paragraphs. See [`_gallery/42_quote_extended.md`](_gallery/42_quote_extended.md).

Frontmatter: `eyebrow`, `portrait_image`, `source_mark` (optional uppercase eyebrow above the quote), `quote_body` (multi-line markdown — paragraphs render as `<p>`), `attribution`, `attribution_role`.

#### `photo_kpi_callouts` — anchor photo + KPI column
A photo on the left (with optional bottom caption strip) and a vertical column of three big-number KPI callouts on the right. Inspired by USPS 2010 page 8. Use for an "anchor visual + headline numbers" slide. See [`_gallery/43_photo_kpi_callouts.md`](_gallery/43_photo_kpi_callouts.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `photo_image`, `photo_caption`, then three KPIs: `kpi_N_value` and `kpi_N_label`. Optional `kicker`.

#### `section_table_of_contents` — full-bleed section divider
Full-bleed accent-coloured section divider with a list of contents items; the current section is visibly outlined. Inspired by Transportation 2020 pages 2 and 7. Use as a recurring divider between major sections of a long deck. See [`_gallery/44_section_table_of_contents.md`](_gallery/44_section_table_of_contents.md).

Frontmatter: `eyebrow`, `contents_label` (small eyebrow above the list). Body: a markdown ordered list where the current section is marked with a trailing italic token, e.g. `2. Challenges and trends *(current)*` — the CSS hides the literal `(current)` and outlines the item.

#### `section_watermark` — commentary + chart + big watermark band
Commentary card on the left, chart(s) on the right, with a HUGE accent-coloured watermark band running across the bottom of the body carrying the section statement. Inspired by IoT 2013 pages 7-9. Use as a section-level statement slide that doubles as data evidence. See [`_gallery/45_section_watermark.md`](_gallery/45_section_watermark.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `commentary_label`, `commentary` (markdown bullets), `watermark_text` (the big band statement). Body: the chart's `<canvas>` + `<script>`. Optional `kicker`.

#### `numbered_actions_kpi_stack` — actions + KPI value column
A stack of numbered, accent-filled action rows with a KPI value column on the right and a total line at the bottom. Inspired by USPS 2010 page 13. Use when you have 3-5 named actions and want each one paired with its quantified impact. See [`_gallery/46_numbered_actions_kpi_stack.md`](_gallery/46_numbered_actions_kpi_stack.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `actions_header`, `kpi_header`, `total_label`, `total_value`. Body: a markdown ordered list where each item is `Action text <span class="kpi">~£XM</span>`. Optional `kicker`.

#### `arrow_infographic_stack` — value-arrow timeline rows
A vertical stack of arrow-shaped period rows: each row has a period label, an arrow, a big value, and a small explanatory note. Inspired by USPS 2010 page 11 (RHB funding infographic). Use for three (or optionally four) periods of a quantitative trajectory. See [`_gallery/47_arrow_infographic_stack.md`](_gallery/47_arrow_infographic_stack.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each row (1..3, optionally 4): `aN_period`, `aN_value`, `aN_note`. The fourth row auto-hides when `a4_period` is empty. Optional `kicker`.

#### `closing_thanks_team` — closing with team credits
A closing slide variant with a centred "Thank you" headline at the top, a row of team-credit cards at the bottom (name + role per person), and a contact line. Use as the final slide of a multi-deliverable engagement read-out. See [`_gallery/48_closing_thanks_team.md`](_gallery/48_closing_thanks_team.md).

Frontmatter: `title`, optional `subtitle`, `credits_label`, four people: `pN_name` / `pN_role` (fourth auto-hides if `p4_name` empty), `contact` (a single line — firm, email, phone).

### Creative (typography, visual metaphors, editorial)

The "creative" group is for moments in a deck that should land emotionally rather than analytically — section turning points, big stats, story setups. Shapes are inline SVG or CSS so they re-skin under any `--color-*` theme.

#### `big_number_hero` — one massive stat fills the slide
A 260px stat centred on the slide with a small uppercase label above and a single-sentence caption below. Stripe / Linear pitch-deck style. Use when the number is the whole argument — let it breathe. See [`_gallery/53_big_number_hero.md`](_gallery/53_big_number_hero.md).

Frontmatter: `eyebrow`, `number_label`, `number` (e.g. `"26%"`, `"£71M"`, `"1 in 4"`), `subtext` (one sentence of context). Optional `kicker`.

#### `pull_quote_full_bleed` — huge typographic quote, no chrome
A 44px serif-aware quote dominating the whole slide, with a big accent quote-mark and attribution + role at the bottom-left. Apple keynote style. No header, no title — the quote IS the slide. See [`_gallery/54_pull_quote_full_bleed.md`](_gallery/54_pull_quote_full_bleed.md).

Frontmatter: `quote`, `attribution`, `attribution_role`. (No `title`, `subtitle`, or `eyebrow`.)

#### `manifesto_principles` — outlined big numbers + statements
Numbered principles where each number is rendered HUGE and OUTLINED (`-webkit-text-stroke`) in the accent colour, behind a bold statement and a one-line description. Use for working principles, values, design rules. **Note:** the `<li>` uses absolute-positioned numbers, not CSS Grid, because pandoc's `<li><strong>X</strong> trailing text</li>` doesn't compose with grid columns. See [`_gallery/55_manifesto_principles.md`](_gallery/55_manifesto_principles.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`. Body: a markdown ordered list using `**Principle name.** Short statement.` form.

#### `big_question_turning_point` — italic serif question
A 56px italic-serif question fills the slide, with a small accent eyebrow above and a muted hint below. Use as a turning-point slide between sections of a long deck — gives the room a question to hold. See [`_gallery/56_big_question_turning_point.md`](_gallery/56_big_question_turning_point.md).

Frontmatter: `eyebrow` (e.g. `"PART TWO — A QUESTION FOR THE ROOM"`), `question` (one sentence ending in `?`), `hint` (one or two sentences of framing).

#### `iceberg_visible_hidden` — above/below the waterline metaphor
Inline SVG iceberg with a peak above the dashed waterline (accent fill) and a larger mass below (lighter accent shade). Two content bands on the right: WHAT THE BOARD SEES (visible) vs. WHAT'S ACTUALLY DRIVING IT (hidden). Use for "the visible KPI is just the tip" diagnoses. See [`_gallery/57_iceberg_visible_hidden.md`](_gallery/57_iceberg_visible_hidden.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `visible_label` / `visible_headline` / `visible_body` (markdown), `hidden_label` / `hidden_headline` / `hidden_body` (markdown). Optional `kicker`.

#### `mountain_summit_path` — SVG mountain with milestone nodes
Inline SVG mountain with a winding dashed path from base to summit, 4 numbered milestone nodes on the path, a summit flag with the goal labelled, and faint distant mountains in the background. Right column: a markdown ordered list of the milestones with bold lead-ins. See [`_gallery/58_mountain_summit_path.md`](_gallery/58_mountain_summit_path.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `summit_label` (the goal at the peak — e.g. `"5% MLR / FY28"`). Body: a markdown ordered list of milestones (1..4), each `**Milestone name.** Description.`. Optional `kicker`.

#### `bridge_now_to_future` — bridge spans two states
NOW state card on the left (soft accent), FUTURE state card on the right (filled accent, white text), a suspension-bridge SVG with arched cable + vertical cables + direction arrow in the middle. Use as the "transformation narrative" slide that's NOT a swimlane. See [`_gallery/59_bridge_now_to_future.md`](_gallery/59_bridge_now_to_future.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `now_label` / `now_headline` / `now_body` (markdown), `future_label` / `future_headline` / `future_body` (markdown), `bridge_label` (small caption under the SVG). Optional `kicker`.

#### `two_circle_venn` — two circles + sweet-spot card
Two overlapping accent-tinted circles with their own titles + bodies, plus a navy "sweet spot" card sitting on top of the intersection. Use when the recommendation lives at the *intersection* of two capabilities or markets. See [`_gallery/60_two_circle_venn.md`](_gallery/60_two_circle_venn.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `left_title` / `left_body` (markdown), `right_title` / `right_body` (markdown), `sweet_spot_title` / `sweet_spot_body` (markdown). Optional `kicker`.

#### `concentric_rings_breakdown` — nested radial layers
Four nested circles from outer ("aspirational") to inner ("core") with progressively darker accent shades, the innermost a filled accent circle carrying a `core_label`. Right column: a legend with matching swatches, titles, descriptions. Use for tier breakdowns (customer segments, investment layers, capability rings). See [`_gallery/61_concentric_rings_breakdown.md`](_gallery/61_concentric_rings_breakdown.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `core_label`, then for each ring (1..4): `rN_title` / `rN_body`. Optional `kicker`. Ring 1 = innermost (most concentrated), ring 4 = outermost (most aspirational).

#### `magazine_cover` — editorial cover for a major section opener
A full magazine-cover layout: serif masthead at top, big serif headline + standfirst + byline on the left, hero image strip on the right, "inside this issue" sidebar with a numbered list of contents. No standard slide header / title — the whole slide IS the cover. Use as a section-opener for big multi-part decks. See [`_gallery/62_magazine_cover.md`](_gallery/62_magazine_cover.md).

Frontmatter: `masthead_title` (publication name), `masthead_issue` (issue/date label), `hero_image` (path; falls back to accent block), `cover_kicker`, `headline`, `standfirst`, `byline`, `inside_label`. Body: a markdown ordered list of inside-this-issue items.

#### `storyboard_panels` — 5 horizontal story panels
Five horizontal storyboard panels in a row, each with a numbered frame (background image with a numbered chip overlay) and a caption below. Use for sequential narratives — "a day in the life", "how the journey unfolds", "what changes step by step". See [`_gallery/63_storyboard_panels.md`](_gallery/63_storyboard_panels.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, for each panel (1..5): `pN_image` (path; falls back to soft accent block) and `pN_caption` (markdown — bold lead-in + description). Optional `kicker`. **Note:** captions use `{{pN_caption_md}}` in the template so `**bold**` markdown renders correctly.

#### `headline_with_subtext_stack` — NYT visual-essay shape
A 60px serif headline taking 1-2 lines, then a deck (subhead) below it, then 3 numbered notes side-by-side with accent top-borders and small numbered chips. Use as a story-led variant of `exec_summary_recommendation` — same content, more editorial polish. See [`_gallery/64_headline_with_subtext_stack.md`](_gallery/64_headline_with_subtext_stack.md).

Frontmatter: `eyebrow`, `headline` (the big serif title), `deck` (one-paragraph subhead). Body: a markdown ordered list of **exactly 3** notes in `**Note title.** Description.` form. Optional `kicker`.

#### `stat_with_dot_proof` — big stat + 100-dot grid
A big stat (140px) on the left with a label and caption, a 10×10 dot grid on the right where N of 100 dots are highlighted in accent. Use to make abstract percentages tangible — "26 of every 100 people walked away". The grid is populated by an inline script reading `data-highlighted` and `data-total`. See [`_gallery/65_stat_with_dot_proof.md`](_gallery/65_stat_with_dot_proof.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `stat_number` (e.g. `"26"`), `stat_label`, `stat_caption`, `highlighted_count` (integer), `total_count` (integer; defaults to 100). Optional `kicker`.

#### `comparison_split_screen` — full-bleed 50/50 dramatic compare
Full-bleed two-column split with a centre seam carrying a VS pill. Left side dark cover-bg, right side accent. Each side has a label / headline / one-line body positioned at the bottom. No slide header — the split IS the slide. Use as a dramatic before/after or A vs B turning point. See [`_gallery/66_comparison_split_screen.md`](_gallery/66_comparison_split_screen.md).

Frontmatter: `vs_label` (e.g. `"VS"`), `left_image` / `left_label` / `left_headline` / `left_body`, `right_image` / `right_label` / `right_headline` / `right_body`. (No `title`, `eyebrow`, etc. — the slide is the visual.)

#### `annotated_diagram` — central SVG with numbered callouts
A central hexagonal SVG with 6 numbered nodes around its perimeter and a centre label, flanked by two columns of numbered callout cards (3 left, 3 right). Use when the slide needs to show *what touches what* — the centre is the hub, the 6 callouts are the surfaces. See [`_gallery/67_annotated_diagram.md`](_gallery/67_annotated_diagram.md).

Frontmatter: `eyebrow`, `title`, optional `subtitle`, `centre_label_top` / `centre_label_bottom` (two lines inside the hex), then for each callout (1..6): `aN_title` / `aN_body`. Optional `kicker`.

---

### McKinsey pack (Tech Trends Outlook archetypes, gallery 68-98)

Layout archetypes ported from the McKinsey Tech Trends Outlook deck. All theme-agnostic (`--color-*` + `color-mix`), so they re-skin under any brand. Three shared "exhibit chrome" classes are available to ANY template: `.exhibit-label` (uppercase accent kicker, e.g. "EXHIBIT 3"), `.takeaway` (the full-sentence so-what under the title), `.source-note` (a footnote line that hides when empty). The chrome order in the exhibit_* templates is: header, `.exhibit-label` (`{{exhibit_label}}`), title (a question), `.takeaway` (`{{subtitle}}`), body, `.source-note` (`{{source}}`), footer.

**Important authoring note (raw-HTML bodies):** most of these templates expect the body written as raw HTML. Pandoc parses a `<div>` as a native div and then treats any **4-space-indented** child lines as a code block, so they render as literal monospace text. Write raw-HTML body markup flush-left (no leading indentation), exactly like the `relevance_matrix` example.

Openers / index:
- `title_report_cover` — white report cover: lower-left title + `kind`/`date`, right-side hero panel (`hero_image`, or a decorative accent panel when unset). FM: `title`, `kind`, `date`, opt `cover_logo`, `hero_image`. See [`_gallery/69_title_report_cover.md`](_gallery/69_title_report_cover.md).
- `section_divider_hero` — dark section break, headline + `accent_label` + `date`, right CSS arc motif (or `hero_image`). FM: `title`, `accent_label`, `date`, opt `cover_logo`, `hero_image`. See `_gallery/70_*`.
- `trends_overview_grid` — white icon-tile grid; body is raw HTML `.trend-grid > .trend-tile` (icon + name + note). FM: `title`, `subtitle`. See `_gallery/71_*`.
- `grouped_index_two_buckets` — dark two-bucket themed contents; body raw HTML `.bucket-cols > .bucket`. FM: `title`. See `_gallery/72_*`.

Exhibit shells:
- `exhibit_takeaway` — the base exhibit shell (label + question title + takeaway + source + body bullets). FM: `exhibit_label`, `title`, `subtitle`, `source`. See `_gallery/73_*`.
- `exhibit_two_column` / `exhibit_three_column` — same chrome over 2 / 3 labelled bullet columns. FM as above. See `_gallery/74_*`, `_gallery/75_*`.
- `exhibit_bignum_impact_rows` — left big stat + right `.impact-row` list (icon + label + desc) + a `.callout` band (`band`). FM: `exhibit_label`, `title`, `subtitle`, `bignum`, `bignum_label`, `band`, `source`. See `_gallery/76_*`.
- `exhibit_icon_row_table` — 2-col `table.icon-row-table` (icon + category | implication). FM: `exhibit_label`, `title`, `subtitle`, `source`. See `_gallery/77_*`.
- `takeaway_three_kpis` — exhibit chrome over 3 large KPI cards. FM: `exhibit_label`, `title`, `subtitle`, `source`. See `_gallery/98_*`.

Comparison / definition:
- `comparison_attribute_grid` — `table.attr-grid`: optional grouped super-headers, icon+name column heads, attribute rows with a left label column. FM: `title`, `subtitle`, `source`. See `_gallery/78_*`.
- `comparison_by_generation` — `table.gen-table`: row label + 3 descriptive columns (Summary / Previous / Next). FM: `title`, `subtitle`, `source`. See `_gallery/79_*`.
- `definition_two_lists` (dark) / `definition_split_light` (white) — narrow title rail + `lead` paragraph + two labelled lists. FM: `title`, `lead`, (`subtitle`,`source` on the light one). See `_gallery/81_*`, `_gallery/82_*`.

Quantitative:
- `feature_columns_with_stats` — grouped feature columns (`.feat-cols`) + bottom big-stat strip (`.stat-strip`). FM: `title`, `subtitle`, `source`. See `_gallery/80_*`.
- `chart_with_stat_callouts` — Chart.js chart left + `.stat-callout` column right. FM: `title`, `subtitle`, `source`. See `_gallery/83_*`.
- `bubble_value_breakdown` — proportional Chart.js bubble chart + side legend. FM: `title`, `subtitle`, `source`. See `_gallery/84_*`.
- `kpi_stat_callouts_band` — a band of icon + big-number + caption cells (`.kpi-band > .kpi-cell`). FM: `title`, `subtitle`, `source`. See `_gallery/85_*`.
- `adoption_scoreboard` — `table.scoreboard`: items x rating dimensions, each cell a CSS bar gauge (`.gauge > .gauge__fill` width % inline) + score. FM: `title`, `subtitle`, `source`. See `_gallery/86_*`.
- `scorecard_dimensions` — single `subject` scored across dimensions (label + gauge + verdict) + overall callout. FM: `title`, `subtitle`, `subject`, `source`. See `_gallery/87_*`.
- `stat_hero_band` — one giant `bignum` + `bignum_label` beside a context paragraph + callout. FM: `title`, `subtitle`, `bignum`, `bignum_label`, `source`. See `_gallery/97_*`.

Narrative / proof:
- `proof_points_by_segment` — `.proof-row` list: icon + segment label | prose example(s). FM: `title`, `subtitle`, `source`. See `_gallery/88_*`.
- `open_questions_numbered` — `.oq-row` list: number + topic | bold question + bullets. FM: `title`, `subtitle`, `source`. See `_gallery/89_*`.
- `benefits_and_risks` — two columns, Benefits vs Risks and uncertainties; the risks column body is the `risks_body` field. FM: `title`, `subtitle`, `source`, `risks_body`. See `_gallery/90_*`.
- `topics_of_debate_table` — `table.debate-table` with a coloured category-tag pill per row + a tag legend. FM: `title`, `subtitle`, `source`. See `_gallery/91_*`.
- `resources_links` — knowledge-center / related-reading link lists (markdown links in body). FM: `title`, `eyebrow`. See `_gallery/92_*`.

Diagrams:
- `value_chain_flow` — flex row of numbered stage boxes joined by chevrons (`.chain > .chain-step`); optional outcome via `kicker`. FM: `title`, `subtitle`, `source`. See `_gallery/93_*`.
- `matrix_2x2_bubble` — 2x2 plot with axis labels and `.plot-bubble` items positioned by inline `left/top:%` and sized by inline `--size`. FM: `title`, `subtitle`, `x_low`, `x_high`, `y_low`, `y_high`, `source`. The bubble element IS the circle (sized by `--size`, centred via translate); keep bubble centres roughly 20-80% on each axis so circles + labels stay inside the frame. See `_gallery/94_*`.
- `ecosystem_orbit` — central `center_label` node with 6 satellites on a fixed 528x370 stage; SVG connector lines share the stage coordinate system, so if you move a satellite update BOTH the CSS `left/top` and the matching SVG `<line>` endpoint in the template. FM: `title`, `subtitle`, `center_label`, `source`. See `_gallery/95_*`.
- `maturity_curve_band` — 3 maturity-stage columns (Emerging / Maturing / Mature) with chips (`.maturity-track > .stage > .maturity-chip`). FM: `title`, `subtitle`, `source`. See `_gallery/96_*`.

---

## Kicker callout (cross-template feature)

Any template can opt into a "kicker" — a one-line meta-message rendered as a callout band at the foot of the body area. Author simply adds `kicker:` to the slide's frontmatter; if the template includes `{{kicker_block}}` in its HTML, the band renders only when the kicker is set.

```yaml
---
template: diagnosis_findings_table
title: "..."
kicker: "**The pattern.** Each of these is known at director level, but none has an owner with the authority to act."
---
```

Use kickers sparingly — one per slide, when there's a meta-theme that wants to say "and here's why all of this matters together." Templates that currently support `{{kicker_block}}`: `diagnosis_findings_table`. Other content templates can opt in by adding `{{kicker_block}}` to their HTML (it renders as empty when no kicker is set, so the slide is unaffected for authors who don't use it).

---

*More template groups (Framework, Quantitative, Comparison, Timeline/Roadmap, Decision/Ask, Closing) coming in subsequent batches.*
