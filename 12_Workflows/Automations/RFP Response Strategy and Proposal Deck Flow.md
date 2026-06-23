---
type: maxos-workflow
name: RFP Response Strategy and Proposal Deck Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: client_or_company
    type: string
    label: Client or company
  - name: rfp_doc_path
    type: document
    label: RFP document
  - name: proposal_deadline
    type: string
    label: Proposal deadline
  - name: offering_context
    type: string
    label: Offering context
  - name: team_context
    type: string
    label: Team context
steps:
- id: rfp_intake
  name: RFP Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Read and extract the RFP if rfp_doc_path is provided: {rfp_doc_path}

    Inputs:
    - client_or_company: {client_or_company}
    - proposal_deadline: {proposal_deadline}
    - offering_context: {offering_context}
    - team_context: {team_context}

    Produce a structured RFP extraction:
    - Stated objectives
    - Explicit requirements
    - Implied requirements
    - Evaluation criteria
    - Deliverables and deadlines
    - Constraints, procurement rules, and risks
    - Questions for clarification
    Mark each point as RFP-derived, user-provided, or inferred.
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: client_research
  name: Client Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research {client_or_company} outside-in. Focus on strategy, commercial pressure, financial performance, operating model, competitors, and why this RFP may exist now.

    Produce a concise evidence-backed client context pack with source notes and confidence levels.
  inputs:
  - rfp_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: response_strategy
  name: Response Strategy Agent
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Build the proposal response strategy.

    Include:
    - Win themes
    - No-regret answer structure
    - Differentiators
    - Risks and red flags
    - Evidence/proof points needed
    - Pricing/commercial stance if relevant
    - Partner/subcontractor or capability gaps
    - Clarification questions
  inputs:
  - rfp_intake
  - client_research
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: proposal_outline
  name: Proposal and Deck Outline Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Turn the response strategy into a proposal and presentation outline.

    This is not a visual design task. Produce:
    - Executive narrative
    - Recommended proposal sections
    - Recommended presentation slides
    - Proof points per section
    - Case examples to include
    - Gaps the team must fill manually
  inputs:
  - response_strategy
  output:
    as: text
  position:
    x: 1420
    y: 80
- id: proposal_draft
  name: Proposal Pack Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the proposal strategy pack from the loop context. Include a board-level story, proposal answer plan, and Markdown slide-by-slide deck skeleton.
  inputs: []
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: proposal_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the proposal pack so a smart 12-year-old could understand the client's ask, our answer, and why it should win.
    Keep the professional structure. Remove jargon and make the logic concrete.
  inputs:
  - proposal_draft
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: proposal_critique
  name: Red-Team Proposal Reviewer
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Red-team the proposal pack.

    Look for:
    - Missed RFP requirements
    - Weak win themes
    - Unsupported claims
    - Procurement risks
    - Overly technical or vague language
    - Missing proof points
    Give concrete fixes for the next loop.
  inputs:
  - proposal_plain_english
  output:
    as: text
  position:
    x: 2430
    y: -40
- id: final_rfp_strategy_pack
  name: Final RFP Response Strategy Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown output.

    Structure:
    # RFP Response Strategy: {client_or_company}
    1. Executive Summary
    2. What the Client Is Asking For
    3. Win Themes
    4. Recommended Proposal Answer
    5. Proposal Structure
    6. Presentation Deck Skeleton
    7. Proof Points and Case Examples Needed
    8. Risks, Gaps, and Clarification Questions
    9. Team Workplan to Submission
    10. Evidence and Assumptions

    Keep this as a strategy and deck-content pack, not a technical implementation plan.
  inputs:
  - rfp_quality_loop
  output:
    as: file
    format: md
    filename: '{client_or_company} - RFP Response Strategy Pack - {date}'
  position:
    x: 3090
    y: 95
loops:
- id: rfp_quality_loop
  name: Proposal Quality Loop
  inputs:
  - proposal_outline
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Proposal strategy is complete, compliant, persuasive, and plain-English clear.
  judge_every: 1
  cycle_targets:
  - proposal_draft
  feedback_sources:
  - proposal_plain_english
  - proposal_critique
  exit_targets:
  - proposal_quality_judge
  position:
    x: 1650
    y: 205
judges:
- id: proposal_quality_judge
  name: Proposal Quality Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the RFP response strategy is compliant, persuasive, specific, and understandable.
    Return:
    Decision: PASS or RETRY
    Score: N/10
    Reasons:
    Required fixes:
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_rfp_strategy_pack
  retry_targets:
  - rfp_quality_loop
  position:
    x: 2760
    y: 205
---

# RFP Response Strategy and Proposal Deck Flow

Turns an RFP into a response strategy, proposal structure, and Markdown deck skeleton, with a red-team review loop before the final inbox output.
