---
type: maxos-workflow
name: Point of View Generator
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: industry_or_sector
    type: string
    label: Industry or sector
  - name: focal_topic
    type: string
    label: Topic or lens, optional
  - name: geography
    type: string
    label: Geography, optional
  - name: audience
    type: string
    label: Target audience, optional
  - name: known_thesis
    type: string
    label: Known thesis or concern, optional
  - name: context_doc_path
    type: document
    label: Context document, optional
steps:
- id: pov_intake
  name: POV Intake and Framing Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the POV request.

    Inputs:
    - industry_or_sector: {industry_or_sector}
    - focal_topic: {focal_topic}
    - geography: {geography}
    - audience: {audience}
    - known_thesis: {known_thesis}
    - context_doc_path: {context_doc_path}

    If context_doc_path is provided, read it and extract only the context relevant to the POV.

    Produce:
    1. Clear scope definition
    2. Target reader or audience
    3. Known thesis or concern
    4. Initial questions the POV must answer
    5. Boundary conditions and exclusions
    6. Early hypotheses
    7. What evidence is needed

    If focal_topic is blank, infer 2-4 plausible disruption lenses for the sector, but do not choose only one yet.
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: sector_signal_research
  name: Sector Signal Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research the sector outside-in for {industry_or_sector}, using {focal_topic} as the main lens if provided.

    Focus on signals that can support strong points of view:
    - market growth, profit pools, and margin pressure
    - customer behavior shifts
    - technology shifts
    - regulatory or policy pressure
    - workforce and operating-model changes
    - new entrants and business model attacks
    - capital markets or investor pressure
    - examples of incumbents adapting or struggling

    Produce a concise source-backed signal map.
    Separate sourced facts, examples, inferences, and open evidence gaps.
  inputs:
  - pov_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: sector_economics_analyst
  name: Sector Economics and Workflow Analyst
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Analyze how the sector actually works today.

    Produce:
    - Value chain and profit pool map
    - Incumbent business model
    - Customer buying logic
    - Core workflows, jobs-to-be-done, and cost drivers
    - Where the current model is brittle
    - Which tasks, workflows, or revenue pools could be disaggregated
    - Which parts of the sector may become more valuable

    If the topic is AI, be specific about which tasks AI can substitute, augment, compress, or reprice.
  inputs:
  - pov_intake
  - sector_signal_research
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: five_pov_generator
  name: Five Distinct POV Generator
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Generate exactly five distinct point-of-view territories for {industry_or_sector}.

    Do not converge on one favorite. Carry all five forward.

    Each POV must have a different angle. Useful angle types include:
    - economics and profit pool shift
    - customer or buyer behavior shift
    - operating model or workflow disaggregation
    - technology or AI substitution
    - workforce, talent, and organization
    - regulation, trust, or risk
    - new entrant or ecosystem disruption

    For each of the five POVs, provide:
    1. Working title
    2. Sharp claim
    3. Why now
    4. Mechanism of change
    5. Evidence and signals
    6. Who wins and who loses
    7. Strongest counterargument
    8. What leaders should do if this POV is right
    9. Confidence level and evidence gaps

    The five POVs must be meaningfully different from each other.
  inputs:
  - sector_signal_research
  - sector_economics_analyst
  output:
    as: text
  position:
    x: 1420
    y: -40
- id: first_plain_english_explainer
  name: First 12-Year-Old Explanation Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Explain each of the five POV territories as if speaking to a smart 12-year-old.

    For each POV, answer:
    - What is changing?
    - Why is it changing?
    - Why should someone care?
    - What would happen if this POV is right?

    Do not dumb it down. Make it clear.
    Flag any POV that cannot be explained simply, because that means the logic is probably weak.
  inputs:
  - five_pov_generator
  output:
    as: text
  position:
    x: 1750
    y: -40
- id: pov_sharpening_plan
  name: POV Sharpening Plan
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Create a sharpening plan for all five POVs.

    Do not eliminate any POV.

    For each POV, specify:
    - How to make the claim sharper
    - What evidence would make it credible
    - What wording is too generic
    - What counterargument must be addressed
    - What would make it more surprising or useful
    - What practical leadership implication should be included

    Output a concise refinement brief that the drafting loop can use.
  inputs:
  - five_pov_generator
  - first_plain_english_explainer
  output:
    as: text
  position:
    x: 2080
    y: 80
- id: pov_draft_pack
  name: Five POV Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft a five-POV pack from the loop context.

    Requirements:
    - Keep exactly five POVs.
    - Preserve distinctness across the five.
    - Make each POV a real argument, not a theme.
    - Include evidence, mechanism, counterargument, and implications.
    - Make the writing concrete and executive-readable.
    - For consulting/professional services examples, analyze the economics of leverage, junior work, trust, client outcomes, implementation accountability, and workflow disaggregation.
  inputs: []
  output:
    as: text
  position:
    x: 2430
    y: -40
- id: second_plain_english_explainer
  name: Second 12-Year-Old Explanation Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the five drafted POVs into plain English a smart 12-year-old could explain.

    Do this as a clarity test:
    - Keep exactly five POVs.
    - For each POV, state the simple version of the claim.
    - Identify unclear logic, hidden assumptions, or vague words.
    - Suggest one concrete example that would make the POV easier to understand.
  inputs:
  - pov_draft_pack
  output:
    as: text
  position:
    x: 2760
    y: -40
- id: anti_ai_style_editor
  name: Anti-AI Style Editor
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Read and apply the POV writing style guide.

    Rewrite the five POV draft pack to remove generic AI writing patterns.

    Preserve the five-POV structure and the substance of the argument, but improve:
    - specificity
    - sentence rhythm
    - evidence discipline
    - concrete examples
    - human executive voice
    - clarity

    Avoid generic language such as "rapidly evolving landscape", "unlock value", "leverage synergies", "not just X but Y", and vague transformation claims.
  inputs:
  - pov_draft_pack
  - second_plain_english_explainer
  - doc_pov_style_guide
  output:
    as: text
  position:
    x: 3090
    y: -40
- id: pov_red_team
  name: POV Red-Team Reviewer
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the five POVs hard.

    Check:
    - Are there exactly five POVs?
    - Are they genuinely distinct?
    - Are the claims sharp enough to be debated?
    - Is the mechanism of change clear?
    - Is evidence separated from inference?
    - Are counterarguments serious?
    - Are any POVs generic AI content?
    - Would a client executive find this useful?
    - Would a smart 12-year-old understand the core idea?

    Score each POV from 1-10 and give concrete fixes.
  inputs:
  - anti_ai_style_editor
  output:
    as: text
  position:
    x: 3420
    y: -40
- id: final_pov_pack
  name: Final Five-POV Markdown Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown file.

    Title:
    # Point of View Generator: {industry_or_sector}

    Include exactly five POVs.

    Required structure:
    1. Executive Summary
    2. Sector and Topic Scope
    3. The Five POVs at a Glance
    4. POV 1
    5. POV 2
    6. POV 3
    7. POV 4
    8. POV 5
    9. Plain-English Version for a Smart 12-Year-Old
    10. Cross-POV Comparison
    11. Evidence, Assumptions, and Confidence
    12. Strongest Counterarguments
    13. Suggested Next Research and Validation Questions

    For each POV include:
    - Working title
    - Sharp claim
    - Why now
    - Mechanism of change
    - Evidence and signals
    - Who wins and who loses
    - Counterargument
    - Implications for leaders
    - Confidence level

    Keep the language human, specific, and free of generic AI-writing patterns.
  inputs:
  - pov_quality_loop
  output:
    as: file
    format: md
    filename: '{industry_or_sector} - Point of View Generator - {date}'
  position:
    x: 4080
    y: 95
loops:
- id: pov_quality_loop
  name: Five-POV Sharpening Loop
  inputs:
  - pov_sharpening_plan
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Five distinct, sharp, evidence-aware, plain-English, non-generic POVs.
  judge_every: 1
  cycle_targets:
  - pov_draft_pack
  feedback_sources:
  - second_plain_english_explainer
  - anti_ai_style_editor
  - pov_red_team
  exit_targets:
  - pov_quality_judge
  position:
    x: 2410
    y: 210
judges:
- id: pov_quality_judge
  name: Five-POV Quality Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the pack is ready.

    Pass only if:
    - There are exactly five POVs.
    - The five POVs are distinct.
    - Each POV has a sharp claim, mechanism, evidence, counterargument, and implication.
    - The writing avoids generic AI patterns.
    - The plain-English explanation is clear enough for a smart 12-year-old.
    - The output is useful for an executive or consultant developing thought leadership.

    Return:
    - Decision: PASS or RETRY
    - Score: N/10
    - Reasons
    - Required fixes
  pass_condition: score >= 8.5
  inputs: []
  pass_targets:
  - final_pov_pack
  retry_targets:
  - pov_quality_loop
  position:
    x: 3750
    y: 210
documents:
- id: doc_pov_style_guide
  path: 11_Notes/Point of View Writing Style Guide.md
  label: POV writing style guide
  optional: false
  position:
    x: 3060
    y: 260
lanes:
- id: lane_research
  label: Research and framing
  color: cyan
  opacity: 0.08
- id: lane_povs
  label: Five POV generation and sharpening
  color: violet
  opacity: 0.08
- id: lane_quality
  label: Clarity, style, and quality control
  color: amber
  opacity: 0.08
edges:
- from: trigger
  to: pov_intake
- from: pov_intake
  to: sector_signal_research
- from: pov_intake
  to: sector_economics_analyst
- from: sector_signal_research
  to: sector_economics_analyst
- from: sector_signal_research
  to: five_pov_generator
- from: sector_economics_analyst
  to: five_pov_generator
- from: five_pov_generator
  to: first_plain_english_explainer
- from: five_pov_generator
  to: pov_sharpening_plan
- from: first_plain_english_explainer
  to: pov_sharpening_plan
- from: pov_sharpening_plan
  to: pov_quality_loop
- from: pov_quality_loop
  to: pov_draft_pack
- from: pov_draft_pack
  to: second_plain_english_explainer
- from: pov_draft_pack
  to: anti_ai_style_editor
- from: doc_pov_style_guide
  to: anti_ai_style_editor
- from: second_plain_english_explainer
  to: anti_ai_style_editor
- from: anti_ai_style_editor
  to: pov_red_team
- from: second_plain_english_explainer
  to: pov_quality_loop
- from: anti_ai_style_editor
  to: pov_quality_loop
- from: pov_red_team
  to: pov_quality_loop
- from: pov_quality_loop
  to: pov_quality_judge
- from: pov_quality_judge
  to: final_pov_pack
---

# Point of View Generator

Generates five distinct, evidence-aware points of view about an industry or sector, optionally through a topic lens such as AI. The flow keeps all five POVs alive, sharpens them through a refinement loop, forces plain-English explanation, applies an anti-generic-AI writing style guide, and outputs a final Markdown pack.
