---
type: workflow
status: active
owner:
review_cycle: monthly
tags: [workflow, prompting, website, ui, antigravity, gemini]
---

# Workflow - Generate Website UI Prompts (Antigravity + Gemini)

## Goal
- Systematically create high-quality website-generation prompts with consistent structure, then iterate fast across visual styles and conversion goals.

## Inputs
- Project/context name
- Target audience and business objective
- Visual style direction (brand mood, references)
- Design system details (palette, typography, spacing, radius, texture)
- Required sections/components
- Interaction/animation complexity level
- Tech stack constraints
- CTA model (single vs dual CTA)
- Domain + launch channel constraints (Cloudflare Pages, registrar, etc.)

## Steps
1. Copy `[[TPL - Prompt Website UI Generation]]` and create a new prompt note in `11_Notes/`.
2. Fill the Design System block first (colors, typography, texture, spacing/radius).
3. Define component architecture section-by-section (navbar, hero, features, pricing, footer, etc.).
4. Add explicit technical constraints (framework, animation lifecycle, libraries, code quality).
5. Add a hard execution directive to avoid generic outputs.
6. Run prompt in Antigravity with Gemini 3.1 Pro.
7. Evaluate output using the quality checklist below.
8. Create v2/v3 prompt variants by changing one variable cluster at a time (style, interaction depth, content density).
9. Save final prompt + generated output links in the note.
10. Add a deployment handoff block with exact build/deploy assumptions (`npm run build`, `dist`, env vars needed).

## Prompt Strategy
- Keep structure stable; vary style and component mechanics deliberately.
- Be explicit about transitions and behavior logic (timings, easing curves, trigger conditions).
- Use real image/style references where possible.
- Set “negative constraints” (what to avoid) to reduce generic AI patterns.

## Outputs
- Prompt note with versioned variants (v01, v02, v03)
- Generated website output(s)
- Short retrospective on what produced best quality
- Launch handoff metadata for deployment (framework preset, build command, output dir, env vars)

## Quality checklist
- [ ] Visual identity is distinctive and consistent end-to-end.
- [ ] Components behave like functional UI artifacts, not static blocks.
- [ ] Motion has intent (timing/easing/trigger logic is coherent).
- [ ] Code stack and implementation constraints are followed.
- [ ] Output avoids generic AI-web patterns.
- [ ] CTA logic is explicit and conversion-ready.
- [ ] Deployment assumptions match Cloudflare Pages static setup.
- [ ] Waitlist and analytics hooks are included if required.

## Automation opportunities
- Build a mini “prompt generator” note that outputs first draft from a small input form.
- Add scoring rubric fields (visual quality, interaction quality, implementation realism) per prompt version.
