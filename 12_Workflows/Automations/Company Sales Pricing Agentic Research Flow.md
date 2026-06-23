---
type: maxos-workflow
name: Company Sales Pricing Agentic Research Flow
version: 1
status: draft
trigger:
  position:
    x: -612
    y: 145
  type: manual
  params:
  - name: company_name
    type: string
  - name: company_website
    type: string
  - name: ticker
    type: string
  - name: country_or_region
    type: string
  - name: industry
    type: string
  - name: known_business_context
    type: string
steps:
- id: input_normalization
  name: Input Normalization Agent
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Input Normalization Agent for a company sales, pricing, and
    agentic pricing architecture research workflow.


    Target company input:

    - company_name: {company_name}

    - company_website: {company_website}

    - ticker: {ticker}

    - country_or_region: {country_or_region}

    - industry: {industry}

    - known_business_context: {known_business_context}


    Work even if only company_name is provided. Use live web research where needed.


    Produce a concise Markdown company profile seed with:

    1. Normalized company identity: official name, likely website, headquarters, country
    or region, exchange/ticker if public, ownership status, and industry.

    2. Disambiguation notes: any similarly named companies and why you selected this
    one.

    3. Input completeness: which optional inputs were provided and which were absent.

    4. RFP flag: say whether an RFP Markdown path was provided. Do not read or analyze
    the RFP in this step.

    5. Early hypotheses: likely business model, likely primary customer type, likely
    sales motions, and likely pricing complexity.

    6. Research plan: the source types the next step should prioritize.


    Clearly mark each item as one of:

    - Sourced fact

    - User-provided input

    - Inferred hypothesis

    - Unknown


    Output only the Markdown profile seed.

    '
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 406
    y: 260
- id: source_discovery
  name: Source Discovery Agent
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Source Discovery Agent. Build the evidence base for outside-in
    research on {company_name}.


    Use the normalized company profile seed below. Find high-quality, current, attributable
    sources. Prioritize primary sources and dated documents.


    Required source categories where available:

    - Annual report, 10-K, 20-F, registration document, integrated report, or equivalent

    - Investor presentations, capital markets day material, earnings releases, earnings
    transcripts

    - Company website pages describing products, business units, customers, pricing,
    channels, partners, and geographies

    - Segment reporting and financial data sources

    - Credible industry reports or regulator/statistical sources

    - Reputable third-party references for market structure, competitors, and pricing
    models


    If fewer than 8 useful sources are found, run a second discovery pass using alternative
    search terms:

    - official company name plus annual report

    - official company name plus investor presentation

    - official company name plus pricing

    - official company name plus sales channel

    - official company name plus segment revenue

    - industry plus pricing model


    Produce a Markdown source map with columns or bullets for:

    - Source title

    - URL

    - Publisher

    - Date or fiscal year

    - Source type

    - What it is useful for

    - Reliability tier: Primary, high-quality secondary, or contextual

    - Evidence tags: financials, products, customers, channels, sales process, pricing,
    systems/data, industry, risks


    Also include a short "Evidence Gaps" section listing important questions not covered
    by sources.


    Do not synthesize conclusions yet. Output only the source map.

    '
  inputs:
  - input_normalization
  output:
    as: text
  position:
    x: 752
    y: 4
- id: financial_commercial_research
  name: Financial and Commercial Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Financial and Commercial Research Agent. Analyze {company_name}''s
    financial and commercial profile using the source map and company seed.


    Research and synthesize:

    - Annual revenue or sales, with fiscal year and currency

    - Revenue development over time

    - Margin development over time: gross margin, EBITDA margin, operating margin,
    net margin, or the closest available measures

    - Profitability and business performance

    - Segment reporting and business-unit performance

    - Geographic revenue mix

    - Product or service revenue mix where available

    - Volume signals where available: units or volumes sold, number of customers or
    accounts, order/transaction counts, and average selling price or average deal/contract
    size (state fiscal year and source)

    - Key commercial risks, margin pressures, demand pressures, cost pressures, and
    growth constraints

    - Any signs of pricing power, pricing pressure, discounting pressure, mix effects,
    churn, volume pressure, or contract renegotiation


    Rules:

    - Prefer primary financial sources. Use secondary sources only where primary sources
    are missing.

    - Cite the source title and year or date next to important figures.

    - Do not invent figures. If unavailable, say "not found in available sources."

    - Separate sourced facts from inferred commercial implications.


    Output a Markdown research artifact with:

    1. Financial snapshot

    2. Revenue trend

    3. Margin and profitability trend

    4. Segment and geography view

    5. Product/service revenue view

    6. Commercial pressure points

    7. Pricing implications

    8. Confidence and evidence gaps

    '
  inputs:
  - input_normalization
  - source_discovery
  output:
    as: text
  position:
    x: 1012
    y: 168
- id: product_market_customer_research
  name: Product Market and Customer Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: "You are the Product, Market, and Customer Research Agent for {company_name}.\n\
    \nUsing the company seed and source map, determine what the company sells, to\
    \ whom, and through which channels.\n\nCover:\n- Products and services\n- Core\
    \ business units\n- Customer segments and buyer types\n- End markets\n- Approximate\
    \ customer or account counts, deal/order frequency, and unit or volume sold, where\
    \ stated or reasonably inferable (label sourced vs inferred)\n- Revenue model\
    \ classification: B2B, B2C, B2B2C, channel-driven, marketplace-driven, distributor-driven,\
    \ contract-driven, project-driven, subscription-driven, usage-driven, tender/RFP-driven,\
    \ franchise-driven, partner-led, or other\n- Whether multiple sales models need\
    \ separate analysis\n- Named competitors or alternatives where useful\n- Buying\
    \ triggers and customer needs\n- Customer value proposition\n- Evidence for each\
    \ sales motion classification\n\nProduce:\n1. What the company sells\n2. Who buys\
    \ it\n3. How buying likely happens\n4. Sales motion classification table\n5. Branch\
    \ recommendations for the next workflow step:\n   - B2B branch: relevant / not\
    \ relevant / uncertain\n   - B2C branch: relevant / not relevant / uncertain\n\
    \   - Other motions branch: list relevant special motions such as distributor,\
    \ channel, partner, marketplace, tender, franchise, project, subscription, usage,\
    \ or retail\n6. Confidence and evidence gaps\n\nClearly distinguish sourced facts\
    \ from inferred hypotheses.\n"
  inputs:
  - input_normalization
  - source_discovery
  output:
    as: text
  position:
    x: 1012
    y: 422
- id: core_commercial_brief
  name: Core Commercial Brief Aggregator
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Core Commercial Brief Aggregator for {company_name}.


    Compress the input normalization, source discovery, financial/commercial research,
    and product/market/customer research into one concise common brief that downstream
    agents can rely on instead of rereading every raw artifact.


    The purpose of this step is context compression. Do not make this a long report.
    Keep it practical, evidence-aware, and easy to reuse.


    Produce Markdown with:

    1. Company identity and disambiguation

    2. What the company sells, to whom, and where

    3. Financial and commercial snapshot

    4. Main revenue streams, margin pressures, and commercial risks

    5. Sales motion hypothesis and evidence

    6. Pricing complexity hypothesis

    7. Most important source register: 8-15 key sources with title, URL, date/year,
    and why each matters

    8. Evidence gaps and validation questions

    9. Confidence levels: high, medium, low


    Rules:

    - Separate sourced facts, user-provided inputs, inferred hypotheses, and unknowns.

    - Prefer sharp bullets over long prose.

    - Keep enough detail for downstream branch analysts, but remove duplication.

    - Target 1,500-2,500 words unless evidence is very limited.


    Output only the common commercial brief.'
  inputs:
  - input_normalization
  - source_discovery
  - financial_commercial_research
  - product_market_customer_research
  output:
    as: text
  position:
    x: 1374
    y: 51
- id: core_plain_english_explainer
  name: Plain English Core Explainer
  provider: claude
  model: opus
  thinking: high
  prompt: 'Rewrite the core commercial brief so a bright 12-year-old could understand
    what {company_name} does and why its sales and pricing are complicated.


    This is not a childish rewrite. It is a clarity forcing step. Explain the real-world
    meaning in plain language.


    Rules:

    - Use short, direct sentences.

    - Explain jargon the first time it appears.

    - Use simple examples or analogies when helpful.

    - Preserve the substance, facts, caveats, and confidence levels.

    - Do not add new claims.

    - Make the output useful for a non-expert business stakeholder.


    Output Markdown with:

    1. The company in plain English

    2. What it sells and who buys it

    3. How money probably comes in

    4. Why pricing is likely easy or hard

    5. What we know vs what we are guessing

    6. Five simple questions a client interview should answer


    Output only the plain-English explainer.'
  inputs:
  - core_commercial_brief
  output:
    as: text
  position:
    x: 1680
    y: 361
- id: sales_motion_branching
  name: Sales Motion Branching Agent
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: "You are the Sales Motion Branching Agent. Read the curated Core Commercial\
    \ Brief.\n\nDecide which sales-pricing analysis branches are relevant for {company_name}.\
    \ This workflow engine will run all branch agents, so your job is to give them\
    \ a precise branch plan and relevance rules.\n\nOutput Markdown with:\n1. Sales\
    \ motion classification\n   - Mostly B2B, mostly B2C, mixed, or other\n   - Confidence\
    \ level\n   - Evidence\n2. Branch instructions\n   - B2B branch: run deeply if\
    \ relevant; otherwise output \"Not relevant\" with short reasoning\n   - B2C branch:\
    \ run deeply if relevant; otherwise output \"Not relevant\" with short reasoning\n\
    \   - Other motions branch: which special motions to analyze, such as distributors,\
    \ channels, partners, marketplaces, tenders, franchises, project sales, subscriptions,\
    \ usage pricing, or retail\n3. Branch-specific questions each analyst must answer\n\
    4. What evidence is strong vs weak\n5. What must be validated with the client\n\
    \nDo not perform the branch analysis yourself. Make the routing logic crisp.\n\
    \nYou receive the curated Core Commercial Brief, not all raw research. Use it\
    \ as the common source of truth for branch routing.\n"
  inputs:
  - core_commercial_brief
  output:
    as: text
  position:
    x: 2040
    y: 255
- id: b2b_sales_process_analysis
  name: B2B Sales Process Analyst
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the B2B Sales Process Analyst for {company_name}.


    First decide whether the B2B branch is relevant based on the branch plan and evidence.
    If it is not relevant, output only:

    "# B2B Sales Process Analysis\n\nNot relevant for this company based on the available
    evidence.\n\nReason: ..."


    If relevant or uncertain, perform a deep outside-in B2B sales and pricing process
    analysis.


    Cover:

    - Demand generation and lead sources: inbound, outbound, account-based, partner-led,
    tender/RFP, events, digital, referrals

    - Typical customer journey

    - Typical deal journey

    - Sales roles likely involved: account executive, account manager, solution consultant,
    product specialist, sales engineer, deal desk, pricing manager, finance, legal,
    operations, supply chain, leadership

    - Qualification process and likely CRM stages

    - Product/service configuration or solution design

    - Pricing request and quote/proposal/tender response

    - Negotiation

    - Approval thresholds and escalation logic

    - Contracting and legal review

    - Fulfilment/delivery handoff

    - Renewal, upsell, cross-sell, and account management

    - Documents produced or consumed

    - Handoffs between sales, pricing, finance, legal, operations, supply chain, and
    leadership

    - Pricing touchpoints and likely friction points


    Output Markdown with a process map, role map, document map, likely systems touched,
    pricing handoffs, pain points, and confidence levels.

    Separate sourced facts from inferred hypotheses.


    Use the Core Commercial Brief as your evidence base. Do not ask downstream agents
    to reconstruct raw financial or product research.

    '
  inputs:
  - core_commercial_brief
  - sales_motion_branching
  output:
    as: text
  position:
    x: 2242
    y: -50
- id: b2c_sales_process_analysis
  name: B2C Sales Process Analyst
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the B2C Sales Process Analyst for {company_name}.


    First decide whether the B2C branch is relevant based on the branch plan and evidence.
    If it is not relevant, output only:

    "# B2C Sales Process Analysis\n\nNot relevant for this company based on the available
    evidence.\n\nReason: ..."


    If relevant or uncertain, perform a deep outside-in B2C sales and pricing process
    analysis.


    Cover:

    - Customer acquisition: brand, marketing, performance marketing, retail, ecommerce,
    app, marketplace, partners, stores, distributors

    - Customer journey from awareness to purchase to retention

    - Product selection and bundling

    - Pricing mechanics: list price, dynamic price, promotions, discounts, subscriptions,
    usage, bundles, loyalty, markdowns, regional prices

    - Promotion and campaign governance

    - Channel conflict and price consistency issues

    - Customer segmentation and personalization

    - Forecasting, demand planning, inventory/capacity constraints where relevant

    - Revenue management or yield management where relevant

    - Documents, data, and systems likely used

    - Handoffs between marketing, sales/channel, pricing, finance, product, operations,
    supply chain, and leadership

    - Likely manual or fragmented points


    Output Markdown with a customer journey map, commercial lever map, pricing mechanics,
    systems/data view, pain points, and confidence levels.

    Separate sourced facts from inferred hypotheses.


    Use the Core Commercial Brief as your evidence base. Do not ask downstream agents
    to reconstruct raw financial or product research.

    '
  inputs:
  - core_commercial_brief
  - sales_motion_branching
  output:
    as: text
  position:
    x: 2254
    y: 90
- id: other_sales_motion_analysis
  name: Other Sales Motion Analyst
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Other Sales Motion Analyst for {company_name}.


    Analyze sales motions that are not a simple direct B2B or direct B2C model. Use
    the branch plan to decide what matters.


    Possible motions include:

    - Distributor-led sales

    - Channel partner sales

    - Marketplace sales

    - Franchise or dealer models

    - Tender/RFP-led sales

    - Project-based sales

    - Government/public-sector procurement

    - Enterprise framework agreements

    - Subscription or usage-based sales

    - Retail or wholesale models

    - OEM, reseller, or embedded/B2B2C models


    If none are relevant, output only:

    "# Other Sales Motion Analysis\n\nNo material additional sales motions found beyond
    the B2B/B2C branches.\n\nReason: ..."


    If relevant, for each motion cover:

    - How demand likely enters the company

    - Who owns the relationship

    - Who controls price and commercial terms

    - How quotes, tenders, proposals, or partner offers are created

    - Approval steps and governance

    - Margin leakage risks

    - Documents and data used

    - Systems likely touched

    - Where agentic workflows could help


    Output Markdown with one subsection per relevant special sales motion.

    Separate sourced facts from inferred hypotheses.


    Use the Core Commercial Brief as your evidence base. Do not ask downstream agents
    to reconstruct raw financial or product research.

    '
  inputs:
  - core_commercial_brief
  - sales_motion_branching
  output:
    as: text
  position:
    x: 2248
    y: 522
- id: sales_motion_synthesis
  name: Sales Motion Synthesis Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Sales Motion Synthesis Pack aggregator for {company_name}.


    Read the branch plan and the B2B, B2C, and other-sales-motion analyses. Create
    one curated sales-motion pack for downstream pricing, systems, transformation,
    and final synthesis steps.


    Do not paste all branch outputs. Reduce them to the relevant motions and explain
    how they fit together.


    Produce Markdown with:

    1. Sales motion verdict: mostly B2B, mostly B2C, mixed, or special model

    2. Relevant sales motions only; for non-relevant branches, include one short exclusion
    note

    3. End-to-end sales process map by relevant motion

    4. Role map: who likely does what

    5. Document and handoff map

    6. Pricing touchpoints by stage

    7. Likely bottlenecks, delays, manual work, and margin leakage points

    8. Plain-English example deal or customer journey

    9. Evidence strength and assumptions

    10. Validation questions


    Rules:

    - Keep this as a synthesis pack, not a full report.

    - Separate sourced facts, inferred hypotheses, and speculation.

    - Prefer process clarity over exhaustive detail.

    - Target 1,500-2,500 words.


    Output only the sales motion synthesis pack.'
  inputs:
  - sales_motion_branching
  - b2b_sales_process_analysis
  - b2c_sales_process_analysis
  - other_sales_motion_analysis
  output:
    as: text
  position:
    x: 2476
    y: 205
- id: scale_volume_estimation
  name: Sales and Pricing Scale Estimator
  provider: claude
  model: opus
  thinking: high
  prompt: "You are the Sales and Pricing Scale Estimator for {company_name}.\n\nYour\
    \ job is to estimate the SCALE of the company's sales and pricing operations:\
    \ how big the sales organisation likely is, and how many sales interactions and\
    \ pricing events a supporting system would have to handle. This sizes \"how much\
    \ volume an agentic sales/pricing system must cope with.\"\n\nUse the Core Commercial\
    \ Brief (revenue, customers, products, geographies) and the Sales Motion Synthesis\
    \ Pack (deal types, sales process) as evidence. Reason from the economics:\n-\
    \ Revenue and revenue mix\n- Customer types and likely customer counts\n- Goods/services\
    \ sold and likely unit or order volumes\n- Deal types and typical deal/contract\
    \ size (average selling price or average deal value)\n- Sales motions (transactional\
    \ vs large complex deals; B2B vs B2C vs channel/tender)\n\nProduce Markdown with:\n\
    \n1. Sizing assumptions and method\n   - State the key assumptions and the Fermi\
    \ logic (e.g. annual revenue / average deal size = approximate deals per year).\
    \ Show the arithmetic.\n2. Sales organisation scale\n   - Likely sales headcount\
    \ and role mix (AEs, account managers, sales engineers, deal desk, pricing, channel\
    \ managers), number of sales teams, and regions/segments covered.\n3. Sales interaction\
    \ volume per year\n   - Approximate leads, opportunities, meetings, quotes/proposals,\
    \ tenders/RFPs, orders, and renewals - whichever fit the company's motions.\n\
    4. Pricing event volume per year\n   - Approximate price-setting and price-change\
    \ events: quotes priced, deals needing pricing/approval, list-price changes, promotions,\
    \ contract repricings, tenders priced.\n5. Transaction and data volume\n   - Approximate\
    \ deals/orders per year, active customers, products/SKUs, and the resulting record/throughput\
    \ volume a system would handle (steady-state and peak).\n6. Scale verdict\n  \
    \ - Low / medium / high volume, and what that implies for how much automation,\
    \ decision support, and agentic tooling is justified.\n7. Confidence and validation\
    \ questions\n   - What is sourced vs inferred, and the few questions a client\
    \ interview should answer to firm up the numbers.\n\nRules:\n- Always give low\
    \ / base / high ranges, not single point estimates, and show the assumptions behind\
    \ each number.\n- Prefer order-of-magnitude correctness over false precision.\n\
    - Clearly separate sourced facts, user-provided inputs, inferred estimates, and\
    \ speculation.\n- Do not present estimates as if they were sourced figures.\n\n\
    Output only the scale estimate.\n"
  inputs:
  - core_commercial_brief
  - sales_motion_synthesis
  output:
    as: text
  position:
    x: 2476
    y: 470
- id: pricing_architecture_analysis
  name: Pricing Architecture Analyst
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Pricing Architecture Analyst for {company_name}.


    Infer the company''s likely pricing function and pricing architecture from the
    research and sales motion analyses.


    Analyze:

    - How pricing is likely organized

    - Who likely owns pricing decisions

    - How prices are likely set

    - Pricing methods likely used: list price, negotiated, dynamic, tender-based,
    cost-plus, value-based, market-based, index-linked, contract-based, subscription-based,
    usage-based, promotion-driven, algorithmic, or hybrid

    - Inputs needed for pricing decisions

    - Outputs generated by pricing

    - How pricing differs by product, customer, region, segment, contract type, channel,
    and deal size

    - Approval thresholds and governance

    - Deal desk involvement

    - Discounting, rebates, incentives, promotions, and commercial terms

    - Margin controls and leakage risks

    - Pricing KPIs

    - Best-practice pricing methods for the industry

    - Where the process is likely manual, fragmented, inconsistent, slow, or risky

    - Opportunities for automation, decision support, margin protection, and agentic
    workflows


    Output Markdown with:

    1. Pricing architecture hypothesis

    2. Pricing ownership and governance

    3. Price-setting methods by sales motion

    4. Pricing inputs and outputs

    5. Approval and exception handling model

    6. Margin risk and leakage points

    7. Industry best-practice comparison

    8. Agentic pricing opportunity map

    9. Confidence and validation questions


    Be explicit about what is sourced, inferred, and speculative.


    Use the Sales Motion Synthesis Pack as the process map. Do not reread or restate
    every branch analysis; build the pricing architecture from the synthesized sales
    motions.

    '
  inputs:
  - core_commercial_brief
  - sales_motion_synthesis
  output:
    as: text
  position:
    x: 2860
    y: 30
- id: systems_data_document_flow
  name: Systems Data and Document Flow Analyst
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Systems, Data, and Document Flow Analyst for {company_name}.


    Map the likely sales/pricing process inputs, outputs, systems, documents, and
    handoffs. This is a business-process map, not a technical architecture.


    Include likely:

    - CRM data

    - ERP data

    - Product master data

    - Customer master data

    - Contract data

    - Historical transaction data

    - Margin and cost data

    - Discounts, rebates, incentives, and promotions

    - Sales forecasts

    - Pipeline data

    - Tender/RFP documents

    - Customer requirements

    - Competitive intelligence

    - Pricing guidelines

    - Approval matrices

    - Finance and margin reports

    - Data warehouse or planning system inputs


    Produce:

    1. End-to-end information flow map

    2. System-of-record hypotheses

    3. Documents and artifacts by process stage

    4. Data entities likely needed

    5. Inputs and outputs of pricing decisions

    6. Human handoffs and likely friction

    7. Governance, audit, and control points

    8. Evidence quality and assumptions


    Do not specify frontend/backend architecture, cloud components, database design,
    or implementation details.


    Use the Sales Motion Synthesis Pack and Pricing Architecture Analysis as your
    inputs. Focus on the practical information flow, not raw research repetition.

    '
  inputs:
  - sales_motion_synthesis
  - pricing_architecture_analysis
  output:
    as: text
  position:
    x: 2948
    y: 298
- id: rfp_analysis
  name: Optional RFP Analysis Agent
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Optional RFP Analysis Agent for {company_name}.


    If no RFP Markdown path was provided, or if the provided document content is empty,
    output:

    "# RFP Analysis\n\nNo RFP document was provided or readable. The rest of the workflow
    should rely on outside-in research only."


    If an RFP document is provided in the document input, read it carefully after
    considering the outside-in research. Then produce a dedicated RFP synthesis.


    Extract:

    - RFP summary

    - Stated client objectives

    - Explicit requirements

    - Implied requirements

    - Current-state pain points

    - Data, systems, workflows, pricing, sales, operating model, AI, automation, governance,
    and transformation ambition

    - Constraints, required personas, integrations, controls, or operating-model signals

    - What the RFP says about relevant dashboards, journeys, records, and POC ideas


    Compare the RFP against the outside-in research:

    - What does the RFP confirm?

    - What does it contradict?

    - What does it sharpen?

    - How should the sales/pricing architecture hypothesis change?

    - Which agentic opportunities and POC ideas become more or less relevant?


    Clearly separate:

    - RFP-derived facts

    - Outside-in sourced facts

    - Inferences

    - Speculative hypotheses


    Output Markdown only.


    Use the curated upstream packs as context before reading the RFP. Do not repeat
    their full contents; explain how the RFP confirms, sharpens, or changes them.

    '
  inputs:
  - core_commercial_brief
  - sales_motion_synthesis
  - pricing_architecture_analysis
  - systems_data_document_flow
  - doc_rfp
  output:
    as: text
  position:
    x: 3284
    y: 468
- id: pricing_operating_model_pack
  name: Pricing and Operating Model Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Pricing and Operating Model Pack aggregator for {company_name}.


    Combine the sales motion synthesis, pricing architecture analysis, systems/data/document
    flow, and optional RFP analysis into one curated operating-model pack.


    The purpose is to give downstream transformation and final synthesis agents a
    clean picture of how pricing probably works in the real world.


    Produce Markdown with:

    1. Likely pricing operating model in one page

    2. Pricing ownership and governance

    3. Price-setting methods by sales motion

    4. Inputs, outputs, systems, and documents

    5. Approval and exception flow

    6. Data entities needed for pricing and sales decisions

    7. Manual work, fragmentation, bottlenecks, and margin leakage risks

    8. RFP-confirmed facts and RFP implications, if an RFP was provided

    9. Industry best-practice comparison

    10. Confidence levels and evidence gaps

    11. Client validation questions

    12. Estimated sales and pricing scale: approximate sales team size, sales interactions
    per year, pricing events per year, and deal/transaction volumes a supporting system
    would handle (with assumptions and low/base/high ranges), from the scale estimate
    input.


    Rules:

    - Keep this pack concise and structured.

    - Clearly label RFP-derived facts separately from outside-in facts and inferences.

    - Do not include technical architecture, cloud design, database schema, UI styling,
    frontend/backend design, or implementation details.

    - Target 1,500-2,500 words.


    Output only the pricing and operating model pack.'
  inputs:
  - sales_motion_synthesis
  - pricing_architecture_analysis
  - systems_data_document_flow
  - rfp_analysis
  - scale_volume_estimation
  output:
    as: text
  position:
    x: 3534
    y: 277
- id: agentic_transformation_design
  name: Agentic Transformation Designer
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Agentic Transformation Designer for {company_name}.


    Identify where agents could transform the sales and pricing lifecycle. Use outside-in
    research and, if present, the RFP synthesis. If the RFP exists, explicitly prioritize
    opportunities that match it.


    Consider agent opportunities across:

    - Lead/opportunity qualification

    - Tender/RFP analysis

    - Product/customer matching

    - Price recommendation

    - Discount and margin guardrails

    - Deal desk support

    - Contract/commercial term review

    - Approval routing

    - Competitor and market monitoring

    - Margin leakage detection

    - Sales performance analysis

    - Executive reporting

    - Continuous learning from won/lost deals


    Recommend around 2 to 4 agents most compelling for this company.

    Use the estimated sales and pricing scale to size the value case for each agent:
    roughly how many interactions, quotes, or pricing events it would handle per year,
    and whether that volume justifies automation.


    For each agent include:

    - Agent name

    - Business purpose

    - Trigger or workflow stage

    - Inputs

    - Outputs

    - Actions or recommendations

    - Human oversight point

    - Value case

    - Implementation complexity: Low, Medium, or High

    - Risks and controls

    - RFP relevance if an RFP was provided


    Also include:

    - Operating-model before/after summary

    - Human governance model

    - Highest-value quick wins

    - Highest-risk assumptions to validate


    Do not design the technical architecture or build plan.


    Use the plain-English explainer and curated synthesis packs. Make every agent
    opportunity concrete enough that a non-expert can understand who uses it, what
    it looks at, and what decision it improves.

    '
  inputs:
  - core_plain_english_explainer
  - sales_motion_synthesis
  - pricing_operating_model_pack
  - scale_volume_estimation
  output:
    as: text
  position:
    x: 4302
    y: -16
- id: demo_concept_blueprint
  name: Demo Concept Blueprint Designer
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: "You are the Demo Concept Blueprint Designer for {company_name}.\n\nTranslate\
    \ the research into a business-level demo concept that can feed a separate later\
    \ workflow. Do not design or build the demo. Do not specify technical architecture,\
    \ Azure components, backend/frontend structure, database design, UI styling, look\
    \ and feel, or code.\n\nStay at the business and operating-model level.\n\nInclude:\n\
    1. Suggested personas/logins\n   - Salesperson or account manager\n   - Pricing\
    \ manager\n   - Group pricing or commercial executive\n   - Deal desk analyst\n\
    \   - Finance manager\n   - Product manager\n   - Regional sales leader\n   -\
    \ Any company-specific roles\n2. Relevant business dashboard pages\n   - Only\
    \ business-purpose pages, not visual design\n3. Example user journeys\n   - For\
    \ example salesperson, pricing manager, executive, deal desk, finance\n4. Agents\
    \ to showcase\n   - Around 2 to 4, aligned to the agentic transformation step\n\
    5. Data entities likely needed\n6. Example simulated records\n7. Key sales/pricing\
    \ situations the demo should illustrate\n8. What the demo should make the client\
    \ understand about an agentic sales/pricing operating model\n\nIf an RFP synthesis\
    \ exists, reflect its stated objectives, requirements, personas, workflows, and\
    \ POC priorities.\n\nOutput practical Markdown. Keep it concise enough to brief\
    \ a later demo-design workflow.\n\nUse the pricing operating model pack and agentic\
    \ transformation design as your source material. Keep the demo blueprint business-level\
    \ and real-world relatable.\n"
  inputs:
  - pricing_operating_model_pack
  - agentic_transformation_design
  output:
    as: text
  position:
    x: 4604
    y: 518
- id: transformation_demo_pack
  name: Transformation and Demo Synthesis Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Transformation and Demo Synthesis Pack aggregator for {company_name}.


    Combine the plain-English company explainer, pricing operating model pack, agentic
    transformation design, and demo concept blueprint into one practical pack.


    The purpose is to make the transformation story real-world relatable: what changes
    for a salesperson, pricing manager, deal desk analyst, finance manager, and executive?


    Produce Markdown with:

    1. Human before/after story in plain English

    2. The 2-4 most compelling agents and why they matter

    3. Human oversight model

    4. Personas/logins that matter most

    5. Business dashboard pages that make sense

    6. Example user journeys

    7. Data entities and example simulated records

    8. Key sales/pricing situations the demo should illustrate

    9. Prioritized POC ideas with business value and feasibility

    10. Risks, controls, and validation questions


    Rules:

    - Stay business-level.

    - Do not specify technical architecture, Azure components, backend/frontend design,
    database design, UI styling, look and feel, or code.

    - Use simple language and concrete examples.

    - Target 1,500-2,500 words.


    Output only the transformation and demo synthesis pack.'
  inputs:
  - core_plain_english_explainer
  - pricing_operating_model_pack
  - agentic_transformation_design
  - demo_concept_blueprint
  output:
    as: text
  position:
    x: 5054
    y: 344
- id: final_synthesis
  name: Final Synthesis Agent
  provider: claude
  model: opus
  thinking: high
  prompt: 'You are the Final Synthesis Agent. Aggregate the curated workflow packs
    into one coherent Markdown document for {company_name}.


    The document must help a consultant walk into a client conversation with a strong
    outside-in hypothesis of the company''s sales process, pricing architecture, data
    requirements, relevant agent opportunities, possible personas/logins, dashboard
    concepts, example user journeys, and prioritized POC ideas.


    Required title:

    # Company Sales, Pricing, and Agentic Pricing Architecture Research: {company_name}


    Required structure:

    ## 1. Executive Summary

    - What the company sells

    - How it likely sells

    - How it likely prices

    - Key sales/pricing complexity

    - Best agentic transformation opportunities

    - Most relevant demo concepts

    - Estimated scale of sales and pricing operations (sales team size, interactions,
    pricing events, deal volumes)

    - Whether an RFP was provided and how it shaped the conclusions


    ## 2. Company Overview

    - Company description

    - Business units

    - Products/services

    - Customers

    - Markets

    - Geographic footprint


    ## 3. Financial and Commercial Profile

    - Revenue/sales

    - Revenue trends

    - Margins

    - Segment performance

    - Commercial pressures

    - Growth/margin risks


    ## 4. Sales Motion Classification

    - B2B/B2C/mixed classification

    - Sales channels

    - Customer types

    - Buying processes

    - Deal types

    - Contracting patterns


    ## 5. Likely Sales Process Map

    For each relevant sales motion, cover:

    - Demand generation / lead source

    - Customer request / opportunity creation

    - Qualification

    - Solution/product configuration

    - Pricing request

    - Quote/proposal/tender response

    - Negotiation

    - Approval

    - Contracting

    - Fulfilment / delivery handoff

    - Renewal / upsell / account management


    ## 6. Likely Pricing Function and Pricing Architecture

    - Pricing ownership

    - Pricing governance

    - Price-setting methods

    - Discounting and approval logic

    - Deal desk involvement

    - Margin controls

    - Key pricing inputs

    - Key pricing outputs

    - Pricing KPIs

    - Likely pain points


    ## 7. Systems, Data, and Documents

    - CRM

    - ERP

    - Data warehouse

    - Product/customer master

    - Contract systems

    - Pricing tools

    - Finance/margin data

    - Sales planning data

    - Documents and artifacts used in the process

    - Estimated sales and pricing scale the systems must handle: sales team size,
    sales interactions per year, pricing events per year, and deal/transaction/record
    volumes (low/base/high)


    Include this section only if an RFP was provided and readable:

    ## 8. RFP-Specific Context

    - RFP summary

    - Stated client objectives

    - Explicit requirements

    - Implied requirements

    - Current-state pain points

    - Required or implied workflows

    - Relevant data/systems/process constraints

    - How the RFP changes the outside-in sales/pricing hypothesis

    - Implications for agent opportunities and POC prioritization


    ## 9. Industry Best Practice

    - Best-practice pricing approaches for this industry

    - Best-practice sales/pricing operating model

    - Best-practice analytics and AI opportunities

    - Benchmark comparison to the likely current-state architecture


    ## 10. Agentic Transformation Opportunities

    For each proposed agent:

    - Agent name

    - Business purpose

    - Inputs

    - Outputs

    - Actions/recommendations

    - Human oversight point

    - Value case

    - Implementation complexity

    - Risks/controls

    - RFP relevance, if an RFP was provided


    ## 11. Business-Level Demo Concept Blueprint

    Do not include technical architecture, visual design, Azure implementation details,
    or code-level design.

    Include:

    - Suggested personas/logins

    - Relevant business dashboard pages

    - Example user journeys

    - Agents to showcase

    - Data entities likely needed

    - Example simulated records

    - What the demo should make the client understand


    ## 12. Prioritized POC Ideas

    2 to 4 candidate POCs, with:

    - Why each matters

    - Data needed

    - Business value

    - Demo feasibility

    - Productionization considerations

    - RFP relevance, if applicable


    ## 13. Assumptions, Evidence, and Confidence

    - Sourced facts

    - RFP-derived facts, if applicable

    - Inferred assumptions

    - Speculative hypotheses

    - Confidence levels

    - Evidence gaps

    - Recommended validation questions for client interviews


    ## 14. Appendix

    - Source list

    - Notes from research branches

    - RFP extraction notes, if applicable

    - Additional observations


    Rules:

    - Clearly separate sourced facts, RFP-derived facts, inferred hypotheses, and
    speculative assumptions.

    - Include confidence levels.

    - Do not include technical architecture, cloud architecture, database schema,
    UI styling, frontend/backend design, or implementation details.

    - Keep the output as a polished Markdown document.

    - Do not include meta-commentary about the workflow.


    You are deliberately receiving curated aggregation packs, not all raw artifacts.
    Use those packs as the source of truth. Do not attempt to restate every intermediate
    artifact. Build a coherent report from the compressed evidence.

    '
  inputs:
  - core_commercial_brief
  - core_plain_english_explainer
  - sales_motion_synthesis
  - pricing_operating_model_pack
  - transformation_demo_pack
  - scale_volume_estimation
  output:
    as: text
  position:
    x: 5788
    y: 40
- id: final_plain_english_rewrite
  name: Plain English Final Rewrite
  provider: claude
  model: opus
  thinking: high
  prompt: 'Rewrite the draft final report so it is clear enough for a bright 12-year-old
    to understand, while still being professional enough for a client conversation.


    This is a clarity forcing step. Preserve the report''s structure, facts, caveats,
    confidence levels, source distinctions, RFP distinctions, and recommendations.
    Do not add new evidence or new claims.


    Rules:

    - Keep the exact title and the numbered section structure.

    - Use plain English, short sentences, and active voice.

    - Explain business jargon briefly when needed.

    - Make abstract ideas concrete with simple business examples.

    - Preserve all important nuance: sourced fact vs RFP fact vs inference vs speculation.

    - Keep the demo section business-level only. Do not introduce technical architecture,
    Azure, frontend/backend, database, UI styling, or code.

    - Remove filler, vague consulting language, and unnecessary repetition.


    Output only the rewritten full Markdown report.'
  inputs:
  - final_synthesis
  output:
    as: text
  position:
    x: 6086
    y: 294
- id: quality_review
  name: Quality Review Agent
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: 'You are the Quality Review Agent. Review the draft final Markdown document
    for {company_name} and output the improved final document only.


    Check hard for:

    - Missing required sections

    - Unsupported claims

    - Weak assumptions presented as facts

    - Contradictions between branch analyses

    - Missing confidence levels

    - Missing source list or weak source tracking

    - Failure to separate sourced facts, RFP-derived facts, inferred hypotheses, and
    speculation

    - RFP misuse: if an RFP was provided, the document must use it appropriately and
    clearly; if no RFP was provided, it must not pretend one exists

    - Demo concept drift: the demo section must remain business-level and must not
    specify technical architecture, Azure components, backend/frontend design, database
    design, UI styling, look and feel, or code structure

    - Overly generic agent recommendations

    - POC ideas that are not tied to the company''s sales/pricing architecture

    - Missing validation questions for client interviews


    Improve the document directly:

    - Tighten wording

    - Add caveats where evidence is weak

    - Remove or reframe unsupported statements

    - Ensure the final output follows the required section structure

    - Keep practical sales/pricing/process/agent understanding at the center


    Output only the final polished Markdown document, starting with:

    # Company Sales, Pricing, and Agentic Pricing Architecture Research: {company_name}


    Also check that the final report is plain-English enough for a smart non-expert
    to follow. Prefer concrete examples over jargon, while preserving professional
    tone and evidence discipline.

    '
  inputs:
  - final_plain_english_rewrite
  - core_commercial_brief
  - pricing_operating_model_pack
  - transformation_demo_pack
  output:
    as: file
    format: md
    filename: '{company_name} - Sales Pricing Agentic Architecture Research - {date}'
  position:
    x: 6262
    y: 148
documents:
- id: doc_rfp
  path: ''
  label: RFP document (optional)
  optional: true
  position:
    x: 2826
    y: 584
lanes:
- id: lane_research
  label: Research and core brief
  color: cyan
  opacity: 0.08
  position:
    x: 280
    y: -80
  size:
    width: 1650
    height: 610
- id: lane_branches
  label: Sales motion branches and synthesis
  color: violet
  opacity: 0.08
  position:
    x: 1980
    y: -100
  size:
    width: 708
    height: 740
- id: lane_operating_model
  label: Pricing, systems, and RFP synthesis
  color: amber
  opacity: 0.08
  position:
    x: 2774
    y: -80
  size:
    width: 1054
    height: 760
- id: lane_transformation
  label: Agentic transformation and demo pack
  color: green
  opacity: 0.08
  position:
    x: 4094
    y: -150
  size:
    width: 1418
    height: 896
- id: lane_final
  label: Final report, plain-English rewrite, review
  color: blue
  opacity: 0.08
  position:
    x: 5640
    y: -34
  size:
    width: 880
    height: 500
---

# Company Sales Pricing Agentic Research Flow

Trigger: manual. Steps: Input Normalization Agent → Source Discovery Agent → Financial and Commercial Research Agent → Product Market and Customer Research Agent → Core Commercial Brief Aggregator → Plain English Core Explainer → Sales Motion Branching Agent → B2B Sales Process Analyst → B2C Sales Process Analyst → Other Sales Motion Analyst → Sales Motion Synthesis Pack → Sales and Pricing Scale Estimator → Pricing Architecture Analyst → Systems Data and Document Flow Analyst → Optional RFP Analysis Agent → Pricing and Operating Model Pack → Agentic Transformation Designer → Demo Concept Blueprint Designer → Transformation and Demo Synthesis Pack → Final Synthesis Agent → Plain English Final Rewrite → Quality Review Agent.
