---
type: maxos-workflow
name: Interview and Voice of Customer Synthesis Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: research_question
    type: string
    label: Research question
  - name: client_or_market
    type: string
    label: Client or market
  - name: transcript_doc_path
    type: document
    label: Transcript or notes
  - name: interviewee_context
    type: string
    label: Interviewee context
  - name: output_goal
    type: string
    label: Output goal
steps:
- id: interview_intake
  name: Interview Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Read interview material if transcript_doc_path is provided: {transcript_doc_path}

    Inputs:
    - research_question: {research_question}
    - client_or_market: {client_or_market}
    - interviewee_context: {interviewee_context}
    - output_goal: {output_goal}

    Produce a factual extraction:
    - Key quotes or paraphrased statements
    - Jobs, pains, gains, buying criteria
    - Emotions and intensity
    - Contradictions
    - Evidence tags
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: theme_coder
  name: Theme Coding Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Code the interview into themes.

    Produce:
    - Theme map
    - Frequency or strength signals
    - Representative evidence
    - Surprises
    - Open questions for more interviews
  inputs:
  - interview_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: implication_synthesizer
  name: Customer Implication Synthesizer
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Turn the coded interview themes into client implications.

    Produce:
    - What customers really care about
    - Where current offering/process may fail
    - Commercial, product, pricing, or service implications
    - Hypotheses to test next
  inputs:
  - theme_coder
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: voc_draft
  name: VOC Synthesis Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the voice-of-customer synthesis from the loop context. Keep it grounded in what was actually said.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: voc_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the synthesis so a smart 12-year-old could understand what customers said, what it means, and what should be done next.
  inputs:
  - voc_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: voc_critique
  name: VOC Evidence Reviewer
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the synthesis. Look for overclaiming from too little evidence, missing nuance, ungrounded quotes, and unclear implications.
  inputs:
  - voc_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_voc_synthesis
  name: Final VOC Synthesis
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown output:
    # Interview and Voice-of-Customer Synthesis: {research_question}
    1. Executive Summary
    2. Interview Context
    3. Key Customer Themes
    4. Evidence and Representative Statements
    5. Customer Jobs, Pains, and Gains
    6. Commercial/Product/Process Implications
    7. Hypotheses to Validate
    8. Recommended Next Interviews
    9. Evidence Limits and Confidence
  inputs:
  - voc_loop
  output:
    as: file
    format: md
    filename: '{research_question} - VOC Synthesis - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: voc_loop
  name: VOC Quality Loop
  inputs:
  - implication_synthesizer
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Grounded, useful, non-overstated voice-of-customer synthesis.
  judge_every: 1
  cycle_targets:
  - voc_draft
  feedback_sources:
  - voc_plain_english
  - voc_critique
  exit_targets:
  - voc_judge
  position:
    x: 1320
    y: 205
judges:
- id: voc_judge
  name: VOC Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the VOC synthesis is evidence-grounded, nuanced, useful, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_voc_synthesis
  retry_targets:
  - voc_loop
  position:
    x: 2430
    y: 205
---

# Interview and Voice of Customer Synthesis Flow

Extracts interview evidence, codes themes, translates them into implications, and uses a critique loop to avoid overclaiming.
