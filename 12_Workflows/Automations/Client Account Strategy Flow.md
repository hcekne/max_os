---
type: maxos-workflow
name: Client Account Strategy Flow
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
  - name: account_goal
    type: string
    label: Account goal
  - name: known_relationships
    type: string
    label: Known relationships
  - name: account_notes_doc_path
    type: document
    label: Account notes
  - name: current_opportunities
    type: string
    label: Current opportunities
steps:
- id: account_context_intake
  name: Account Context Intake
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the account strategy input. If account_notes_doc_path is provided, read it: {account_notes_doc_path}

    Produce:
    - Known client facts and relationships
    - Current opportunities
    - Account goal
    - Missing information
    - Evidence tags
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: client_business_research
  name: Client Business Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research {client_or_company}. Focus on business model, financial performance, strategic priorities, leadership, pain points, competitors, and likely transformation agenda.

    Produce an evidence-backed client business profile with source notes.
  inputs:
  - account_context_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: white_space_mapper
  name: White-Space Mapper
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Identify practical commercial white space for this account.

    Produce:
    - Likely business problems
    - Buying centers and likely sponsors
    - Relationship gaps
    - Potential offerings or use cases
    - Priority opportunity hypotheses
    - First meetings or proof points needed
  inputs:
  - account_context_intake
  - client_business_research
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: account_plan_draft
  name: Account Plan Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the account strategy from the loop context.

    Include account thesis, stakeholder strategy, opportunity map, 30/60/90 day plan, next-best actions, risks, and validation questions.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: account_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the account plan so a smart 12-year-old could understand who we want to help, what problems they have, and what we should do next.
  inputs:
  - account_plan_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: account_critique
  name: Account Strategy Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Challenge the account plan. Look for wishful thinking, vague opportunities, missing decision makers, weak next steps, and unsupported assumptions.
  inputs:
  - account_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_account_strategy
  name: Final Account Strategy
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown account strategy.

    Structure:
    # Client Account Strategy: {client_or_company}
    1. Executive Summary
    2. Account Thesis
    3. Client Business Context
    4. Stakeholder and Relationship Map
    5. White-Space Opportunities
    6. Priority Plays
    7. 30/60/90 Day Action Plan
    8. Meeting Plan and Talk Tracks
    9. Risks and Assumptions
    10. Validation Questions
  inputs:
  - account_strategy_loop
  output:
    as: file
    format: md
    filename: '{client_or_company} - Account Strategy - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: account_strategy_loop
  name: Account Strategy Quality Loop
  inputs:
  - white_space_mapper
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Practical, specific, testable account strategy with clear next actions.
  judge_every: 1
  cycle_targets:
  - account_plan_draft
  feedback_sources:
  - account_plain_english
  - account_critique
  exit_targets:
  - account_strategy_judge
  position:
    x: 1320
    y: 205
judges:
- id: account_strategy_judge
  name: Account Strategy Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the account plan is actionable, specific, believable, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_account_strategy
  retry_targets:
  - account_strategy_loop
  position:
    x: 2430
    y: 205
---

# Client Account Strategy Flow

Builds a practical account plan with stakeholder mapping, white-space hypotheses, next-best actions, and a looped quality gate.
