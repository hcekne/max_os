---
type: maxos-workflow
name: Commercial Due Diligence and Investment Memo Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: target_company
    type: string
    label: Target company
  - name: investment_thesis
    type: string
    label: Investment thesis
  - name: geography
    type: string
    label: Geography
  - name: data_room_doc_path
    type: document
    label: Data room summary
  - name: key_questions
    type: string
    label: Key questions
steps:
- id: cdd_intake
  name: CDD Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the CDD input for {target_company}. If data_room_doc_path is provided, read it: {data_room_doc_path}

    Produce:
    - Investment thesis
    - Key diligence questions
    - Known facts
    - Data-room-derived claims
    - Unknowns and evidence gaps
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: market_diligence
  name: Market Diligence Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research the target's market. Cover market size, growth, segments, customer demand, competitors, pricing/margins, regulation, and disruption risks.
  inputs:
  - cdd_intake
  output:
    as: text
  position:
    x: 760
    y: -40
- id: company_diligence
  name: Company Diligence Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research {target_company}. Cover business model, products, customers, financial profile, growth, margin drivers, sales model, pricing model, and operational risks.
  inputs:
  - cdd_intake
  output:
    as: text
  position:
    x: 760
    y: 190
- id: diligence_synthesis
  name: Diligence Synthesis Agent
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Synthesize market and company diligence into an investor-oriented view.

    Produce:
    - Investment thesis assessment
    - Key value creation levers
    - Commercial risks
    - Diligence questions that remain
    - Initial recommendation: attractive, mixed, or concerning
  inputs:
  - market_diligence
  - company_diligence
  output:
    as: text
  position:
    x: 1100
    y: 80
- id: investment_memo_draft
  name: Investment Memo Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the commercial due diligence memo from the loop context. Make it decision-useful for an investment committee.
  inputs: []
  output:
    as: text
  position:
    x: 1450
    y: -40
- id: investment_memo_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the memo so a smart 12-year-old could understand what the company does, why it might be a good investment, and what could go wrong.
  inputs:
  - investment_memo_draft
  output:
    as: text
  position:
    x: 1780
    y: -40
- id: investment_memo_critique
  name: Investment Memo Red Team
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Red-team the investment memo. Look for unsupported claims, one-sided optimism, missing downside, weak evidence, and unclear recommendation logic.
  inputs:
  - investment_memo_plain_english
  output:
    as: text
  position:
    x: 2110
    y: -40
- id: final_cdd_memo
  name: Final CDD Investment Memo
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown memo:
    # Commercial Due Diligence Memo: {target_company}
    1. Executive Summary
    2. Investment Thesis
    3. Company Overview
    4. Market Attractiveness
    5. Competitive Position
    6. Growth and Margin Levers
    7. Commercial Risks
    8. Diligence Questions
    9. Recommendation
    10. Evidence, Assumptions, and Confidence
  inputs:
  - cdd_loop
  output:
    as: file
    format: md
    filename: '{target_company} - Commercial Due Diligence Memo - {date}'
  position:
    x: 2770
    y: 95
loops:
- id: cdd_loop
  name: CDD Memo Quality Loop
  inputs:
  - diligence_synthesis
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Balanced, evidence-backed, investor-useful CDD memo.
  judge_every: 1
  cycle_targets:
  - investment_memo_draft
  feedback_sources:
  - investment_memo_plain_english
  - investment_memo_critique
  exit_targets:
  - cdd_judge
  position:
    x: 1330
    y: 205
judges:
- id: cdd_judge
  name: CDD Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the investment memo is balanced, evidence-backed, decision-useful, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_cdd_memo
  retry_targets:
  - cdd_loop
  position:
    x: 2440
    y: 205
---

# Commercial Due Diligence and Investment Memo Flow

Creates an outside-in CDD memo with market diligence, company diligence, a red-team loop, and a final investment-committee-ready output.
