---
type: maxos-workflow
name: Market Landscape and Competitor Battlecard Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: market_or_industry
    type: string
    label: Market or industry
  - name: geography
    type: string
    label: Geography
  - name: focal_company
    type: string
    label: Focal company
  - name: research_question
    type: string
    label: Research question
  - name: source_pack_doc_path
    type: document
    label: Source pack
steps:
- id: market_scope
  name: Market Scope Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Define the market scope for {market_or_industry} in {geography}. If source_pack_doc_path is provided, read it: {source_pack_doc_path}

    Produce:
    - Market definition
    - Included/excluded segments
    - Focal company context
    - Key research questions
    - Evidence gaps
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: market_research
  name: Market Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research the market. Cover size, growth, segments, customer needs, value chain, regulation, technology shifts, pricing/margin dynamics, and key risks.
    Cite source names and dates where possible.
  inputs:
  - market_scope
  output:
    as: text
  position:
    x: 760
    y: -30
- id: competitor_research
  name: Competitor Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research the competitor landscape for the market and focal company.

    Produce:
    - Competitor table
    - Positioning and differentiation
    - Relative strengths and weaknesses
    - Pricing/commercial model differences
    - Likely moves and vulnerabilities
  inputs:
  - market_scope
  output:
    as: text
  position:
    x: 760
    y: 190
- id: landscape_synthesis
  name: Landscape Synthesis Agent
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Synthesize the market and competitor research into a practical consultant view.

    Produce:
    - Market map
    - Competitive positioning
    - Strategic implications for {focal_company}
    - Commercial/pricing implications
    - 5-8 battlecard messages
  inputs:
  - market_research
  - competitor_research
  output:
    as: text
  position:
    x: 1100
    y: 80
- id: battlecard_draft
  name: Battlecard Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the market landscape and competitor battlecard from the loop context. Make it useful in client conversations.
  inputs: []
  output:
    as: text
  position:
    x: 1450
    y: -40
- id: battlecard_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the battlecard so a smart 12-year-old can understand who competes with whom, why customers choose one option, and what the focal company should do.
  inputs:
  - battlecard_draft
  output:
    as: text
  position:
    x: 1780
    y: -40
- id: battlecard_critique
  name: Battlecard Critique Agent
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the battlecard for unsupported claims, missing competitors, generic strategy, weak commercial insight, and confusing language.
  inputs:
  - battlecard_plain_english
  output:
    as: text
  position:
    x: 2110
    y: -40
- id: final_battlecard
  name: Final Market Landscape and Battlecard
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown report:
    # Market Landscape and Competitor Battlecard: {market_or_industry}
    1. Executive Summary
    2. Market Definition and Scope
    3. Market Size, Growth, and Segments
    4. Value Chain and Buying Dynamics
    5. Competitor Landscape
    6. Battlecards by Competitor
    7. Pricing and Commercial Implications
    8. Strategic Moves for {focal_company}
    9. Evidence, Assumptions, and Confidence
  inputs:
  - battlecard_loop
  output:
    as: file
    format: md
    filename: '{market_or_industry} - Market Landscape Battlecard - {date}'
  position:
    x: 2770
    y: 95
loops:
- id: battlecard_loop
  name: Battlecard Quality Loop
  inputs:
  - landscape_synthesis
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Clear, evidence-backed, commercially useful battlecard.
  judge_every: 1
  cycle_targets:
  - battlecard_draft
  feedback_sources:
  - battlecard_plain_english
  - battlecard_critique
  exit_targets:
  - battlecard_judge
  position:
    x: 1330
    y: 205
judges:
- id: battlecard_judge
  name: Battlecard Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the battlecard is specific, evidence-backed, commercially useful, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_battlecard
  retry_targets:
  - battlecard_loop
  position:
    x: 2440
    y: 205
---

# Market Landscape and Competitor Battlecard Flow

Builds a source-backed market landscape and competitor battlecard with a looped plain-English quality review.
