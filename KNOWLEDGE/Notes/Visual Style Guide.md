# MaxOS Visual Style Guide

Purpose:

Keep `maxos.online` and `app.maxos.online` visually consistent so moving from the public site into the product feels like entering the same system.

## Brand Mark

Primary mark:

- A square dark tile containing a gradient `M`.
- Tile background: `#070B12`.
- Tile border: `#1E2A44`.
- `M` gradient: `#00D1FF` to `#8B5CF6`.

Wordmark:

- `Max` uses the brand gradient.
- `OS` is white.
- Use the full `MaxOS` wordmark in footers, empty states, login screens, and product shell moments where brand recall matters.
- Use the compact `M` mark in tight navigation spaces and browser/favicon contexts.

Avoid:

- Writing user-facing product names as `Max OS`.
- Using internal names like `AgentCard` or `Harness`.
- Placing the full wordmark beside the compact mark in the same header unless there is enough visual need.

## Color Tokens

Core surfaces:

- Background: `#070B12`.
- Surface: `#0E1524`.
- Primary text: `#D9E4FF`.
- Border/signal: `#1E2A44`.

Brand gradient:

- Start: `#00D1FF`.
- End: `#8B5CF6`.

Supporting gradient stops:

- Blue: `#4F7FFF`.
- Indigo: `#6A6DFF`.
- Violet: `#8B5CF6`.

Use gradient sparingly:

- Logo wordmark.
- Primary CTA backgrounds.
- One hero or primary emphasis at a time.
- Workflow-builder accents.

Do not apply gradient to every important phrase. If the `MaxOS` wordmark is already using the gradient, keep nearby headlines white.

## Typography

Landing typography:

- Heading font: Sora.
- Body font: Inter.
- Mono/UI font: JetBrains Mono.

Usage:

- Sora for page titles, section titles, card titles, and brand wordmarks.
- Inter for paragraphs and long-form content.
- JetBrains Mono for navigation, labels, counters, system tags, and small technical metadata.

Keep labels slightly larger than tiny utility text:

- Section labels: `text-sm`, uppercase, mono, accent blue.
- Body copy: calm, readable, and not overly compressed.

## Layout Language

MaxOS should feel:

- Professional.
- Technical.
- Calm.
- Powerful.
- Enterprise-ready.

Use:

- Dark full-width sections.
- Thin signal borders.
- Restrained panels.
- Clear grids where comparison is useful.
- Flow diagrams for process/system explanation.
- Row/list layouts where repeated cards would feel monotonous.

Avoid:

- Neon cyberpunk styling.
- Decorative orbs or bokeh backgrounds.
- Too many card grids in sequence.
- Overusing gradients.
- Rounded marketing-style pill overload.

## Components

### Header

Public landing header:

- Compact `M` mark on the left.
- Navigation: Product, Documentation, Pricing, Login.
- Login is visually emphasized as a white button.

Platform header recommendation:

- Use the same compact `M` mark.
- Keep the shell dark.
- Main product navigation should prioritize Knowledge, Agents, Workflows.
- Secondary product/admin areas should be visually quieter.

### Buttons

Primary CTA:

- Gradient background from `#00D1FF` to `#8B5CF6`.
- Dark text: `#070B12`.
- Mono medium label.

Secondary CTA:

- Signal border.
- Surface/background fill.
- Primary text.
- Subtle blue or violet glow on hover.

### Panels

Panel frame:

- Border: `#1E2A44`.
- Background: `#0E1524` or transparent surface variation.
- Optional small blue corner accents are acceptable.

Use cards for:

- Feature summaries.
- Enterprise capability groups.
- Repeated content with similar weight.

Use rows or flows for:

- Narrative selling points.
- Process explanations.
- Long repeated lists.

## Product Areas

Use these three concepts consistently:

- Knowledge: memory, context, source material, user-owned information.
- Agents: reasoning, execution, assistants, collaboration.
- Workflows: repeatable human-agent processes, automation, orchestration.

The product should never feel like a generic chat UI. MaxOS is an operating system for human-agentic work.

## Copy Principles

Primary positioning:

- MaxOS is the operating system for human-agentic work.

Supporting message:

- MaxOS combines knowledge, workflows, and AI agents into a single operating system.
- It helps humans and AI agents think, plan, execute, and learn together.
- Workflows become more powerful as AI models improve.

Knowledge-system framing:

- The MaxOS Knowledge System remains open, portable, markdown-native, and user-owned.
- Knowledge management is a core feature, not the whole product.

Enterprise framing:

- Bring your own models.
- Cloud or self-hosted deployment.
- Sovereign AI through your own model layer or AI infrastructure.
- Enterprise integrations, governance, and data ownership.

## App Integration Notes

For `app.maxos.online`:

- Match the same dark shell colors.
- Use the same compact `M` mark in the app chrome.
- Use the `MaxOS` wordmark on login, onboarding, workspace creation, and empty states.
- Keep Knowledge, Agents, and Workflows as first-class navigation concepts.
- Use the same primary gradient for key actions, but keep routine actions neutral.
- Avoid introducing a separate color system for the app unless the contrast or interaction state requires it.

The user should feel:

"I clicked Login and entered the same product I was just reading about."
