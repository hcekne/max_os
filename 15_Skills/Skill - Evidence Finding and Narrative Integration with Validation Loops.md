---
type: skill
status: active
trigger_phrase: strengthen my article with evidence
tags: [skill, content, evidence, research, thought-leadership, validation]
---

# Skill - Evidence Finding and Narrative Integration with Validation Loops

## Purpose
Strengthen a thought-leadership article with only the highest-value supporting evidence, integrated naturally into the prose and validated against original sources before finalization.

## Trigger
Use this skill when the user wants to strengthen an article with credible data points, supporting evidence, or statistics without turning the piece into a research memo and can provide the full article draft.

This skill complements [[Skill - Executive Thought Leadership Rewriter with Review Loops]] when the article structure is already strong and the missing layer is evidence, credibility, or urgency.

## Inputs

### Required
- full article draft

### Optional
- stakeholder or editor feedback
- intended publisher, sponsor, client, or firm context
- preferred geographies, sectors, or source types
- excluded organizations, competitors, or source categories
- publication style benchmark
- preferred limit on number of inserted data points (default: two to three)

## Start Gate
- Do not begin evidence selection until the article draft is provided.
- If optional inputs are missing, proceed without them.
- Before research begins, ask whether the piece is being written for a specific firm, client, or publication and whether any organizations or source categories should be excluded.
- Treat the named "operating lenses" below as perspectives for the same agent unless the user explicitly asks for delegated agents.
- Default to two to three inserted proof points unless the user explicitly requests a different limit.

## Output Package
1. argument map
2. candidate insertion points
3. evidence bank
4. selected proof points and why they were chosen
5. rejected candidates and why they were not selected
6. integration plan
7. rewritten article with integrated evidence
8. source validation log
9. sources list in order of first appearance
10. short editor's note explaining how the evidence improved the article

## Operating Lenses
- Argument Mapper: identify the thesis, core claims, and strongest insertion opportunities.
- Research Miner: gather a broad bank of high-credibility evidence candidates.
- Evidence Evaluator: rank candidates and select only the strongest few.
- Narrative Integrator: rewrite the article so evidence feels native to the prose.
- Source Validator: corroborate every chosen point directly in the original source.
- Executive Reader: ensure the final piece still reads like premium thought leadership.

## Strict Rules
- Do not overload the article with statistics.
- Do not insert evidence just because it is interesting.
- Every inserted data point must strengthen a core claim already present in the article.
- Prefer evidence that is credible, recent enough to feel current, easy to explain in one sentence, commercially meaningful, and relevant to the article's target audience.
- Avoid evidence that is too niche, hard to interpret, loosely related, or impressive but strategically irrelevant.
- Rewrite surrounding sentences so the data feels embedded in the narrative, not bolted on.
- Never rely heavily on weak, noisy, or low-credibility sources.
- Respect explicit exclusion rules for organizations, competitor firms, publishers, or source categories.
- Never finalize a chosen proof point unless it is corroborated in the original source used to support it.

## Source Hierarchy
- regulators, official statistics offices, central banks, and industry regulators
- company filings and investor documents
- top-tier consulting and industry research firms
- reputable trade associations
- major trusted publishers and data-rich research institutions

Prefer primary sources when available. If a secondary source reports a number, trace it back to the original source before finalizing the article.

## Steps

### Phase 1 - Argument Mapping
1. Read the article carefully and identify:
   - the core thesis
   - the main supporting arguments
   - the most important commercial implications
   - where evidence would materially strengthen credibility
2. Output a short argument map and a ranked list of the five to eight strongest candidate insertion points.

### Phase 2 - Research Expansion
1. Search broadly for evidence that could support the article.
2. For each strong insertion point, gather multiple possible data points rather than stopping at the first usable number.
3. Record source, date, exact metric, geography, and why it matters for each candidate.
4. Build an evidence bank with at least ten possible data points where possible.
5. Tag each candidate by relevance, credibility, recency, ease of integration, and strategic value.

### Phase 3 - Evidence Selection
1. Rank the evidence bank against the article's core claims.
2. Select only the best two to three data points by default.
3. Use these criteria:
   - directly supports a core claim
   - highly credible source
   - easy to explain
   - meaningful to executive readers
   - improves the article more than alternative candidates
   - can be integrated without disrupting flow
4. Explain why rejected candidates were not selected.

### Phase 4 - Integration Planning
1. For each chosen data point, identify the best paragraph or sentence for insertion.
2. Decide whether it should prove a claim, sharpen a commercial implication, make a sector example concrete, or increase urgency.
3. Decide whether surrounding text needs a light or moderate rewrite.

### Phase 5 - Narrative Integration
1. Rewrite the article to integrate the chosen data points naturally.
2. Preserve the article's voice, pacing, and readability.
3. Adjust nearby wording so the numbers feel organic.
4. Cut a sentence elsewhere if needed to preserve flow and concision.

### Phase 6 - Validation Loop and Final Review
1. Re-open every chosen source and corroborate the exact metric, date, geography, and context directly in the original source.
2. If any chosen data point cannot be corroborated exactly as used in the article, discard it, replace it, and repeat validation.
3. Continue the reselection and revalidation loop until every chosen proof point is source-verified.
4. Review the evidence-enhanced article and confirm that:
   - inserted data points feel natural
   - the article is more credible
   - the narrative still flows
   - no paragraph feels overloaded
   - the article remains executive and readable

## Tone Rules
- Keep the article commercial, crisp, and executive.
- Use numbers to strengthen arguments, not replace them.
- Prefer elegant integration such as:
  - "The economics are already visible in..."
  - "The pattern is clear in..."
  - "Recent data from X shows..."
- Avoid weak or clunky framing such as:
  - "According to a study"
  - "Research suggests"
  - "One interesting statistic is"

## Quality Checks
- [ ] Article draft was provided before evidence work started
- [ ] Argument map was completed
- [ ] Five to eight insertion opportunities were ranked
- [ ] Evidence bank contains ten or more candidates where possible
- [ ] Only two to three proof points were selected unless the user requested otherwise
- [ ] Every chosen proof point was corroborated in the original source
- [ ] Any unverified point was rejected and replaced before finalization
- [ ] Rejected candidates were explained
- [ ] Final article still reads smoothly and does not feel overloaded
- [ ] Sources list is ordered by first appearance
