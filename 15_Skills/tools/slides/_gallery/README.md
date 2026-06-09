# Slide Template Gallery

A live, themeable showcase of every slide template in the Max OS slide-deck skill. Each slide demonstrates one template filled with plausible (but fictional) consulting content so authors can preview the layout, the frontmatter contract, and the type/colour treatment under a given brand.

## Build

```bash
python3 ../build_deck.py .
open deck.html
```

## Swap theme

The gallery ships with two themes:

- `theme-default.css` — neutral executive (navy accent on white; the bare `deck.css` defaults)
- `theme-dmg.css` — DMG media (mid-purple accent, deep-purple cover, Nunito Sans + Barlow)

Switch:

```bash
./switch_theme.sh default     # neutral
./switch_theme.sh dmg         # DMG media
python3 ../build_deck.py .    # rebuild
```

The script copies the chosen file to `theme.css`, which the build script picks up automatically. Add a new theme by dropping `theme-<name>.css` alongside the others.

## Adding a new template to the gallery

1. Write the template at `../templates/<name>.html`.
2. Add CSS for it to `../deck.css` (use `--color-*` variables, never hardcoded brand colours).
3. Add a gallery slide `NN_<name>.md` here with fake but realistic content.
4. Rebuild and run visual QA: `node ../check_deck_visual.mjs deck.html`.
5. Document the template's frontmatter contract in `../PATTERNS.md` under the right purpose group.

## Fake client roster (use these names when writing example slides)

So readers can tell at a glance that a slide is illustrative, not real client work:

- **NorthBank** — retail bank, UK
- **Halcyon Retail** — apparel retailer, EU
- **Brightline Media** — newspaper / digital publisher
- **Vanta Logistics** — last-mile delivery
- **Orenda Health** — health insurer
- **Lumera Energy** — utilities
