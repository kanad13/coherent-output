# Value-Focused Product Comparison

## Purpose

Use this approach when researching and comparing products to identify best value. Balance price with compatibility, essential features, reliability, and total ownership cost.

## Default User Priorities

Use these priorities by default and apply any explicit user adjustments:

1. Required functionality and compatibility
2. Safety, reliability, and support
3. Strong performance for the price
4. Low total cost of ownership
5. Useful, evidence-backed features

Use the default priorities as the buyer profile. Ask a focused question when an unknown requirement—such as size, platform, region, or compatibility—could reverse the recommendation. In other cases, state the assumption and proceed.

When region, currency, or purchase channel is unknown, ask one focused question if the answer can change availability, price, warranty, or compatibility. In other cases, state the default region and price date.

## Inputs

The user may provide one or more:

- Product names or links
- Store listings
- Quotations or price sheets
- Specifications
- Screenshots or photographs
- Add-ons, bundles, fees, or warranty information

Transcribe images faithfully and mark unreadable or ambiguous text as uncertain.

## Research Workflow

### 1. Normalize the Candidates

- Identify the exact model, variant, region, generation, capacity, and bundle.
- Separate base product, included accessories, optional add-ons, recurring fees, taxes, and delivery costs.
- Detect listings that combine reviews or specifications from different variants.
- Mark unresolved identity or configuration differences.

### 2. Establish Category Requirements

Research current category norms using authoritative sources, standards bodies, manufacturer documentation, specialist testing, and reputable retailers.

Identify:

- Mandatory safety, compatibility, or functional requirements
- Recommended features that materially improve ownership
- Optional conveniences
- Current typical specifications and price ranges
- Common omissions, misleading metrics, and failure modes
- Warranty length and terms, service network, parts or consumables, return policy, and software-support period when applicable

Cite every externally verifiable factual claim and link to the exact supporting page.
Place an inline Markdown link immediately after each researched claim. Use the final Sources section as an index of these claim-level citations.

### 3. Explain the Technical Terms

For every meaningful specification or category term:

- Give a plain-language definition.
- Explain its practical effect.
- State when a higher or lower value is actually better.
- Warn when the metric is incomplete or mainly marketing.

Include important category-standard features even when absent from a product; mark those cells `Unspecified` or `Absent`.

### 4. Calculate Total Cost

For each candidate, calculate the comparable cost over a sensible ownership period. Show the arithmetic and currency.

- State the ownership period used for every total-cost calculation.
- When a required cost remains unknown, show the known-minimum calculation and label full total cost `Insufficient evidence`.

Include when relevant:

- Purchase price
- Required accessories or components
- Delivery, installation, activation, or platform fees
- Subscriptions
- Consumables and replacement parts
- Energy or operating costs
- Likely maintenance
- Warranty extensions with an analysis of their value

Label regional prices, currencies, tax treatments, and bundle contents separately. Record every price with the date observed.

### 5. Score Transparently

Create category-appropriate criteria and show their weights before scoring. The weights must reflect the user's default priorities and any explicit requirements.

For every score:

- Show the factual basis.
- Distinguish measured evidence from manufacturer claims.
- Explain penalties for missing or unverified information.
- Match scoring precision to the available evidence.

Use `Insufficient evidence` when the available facts are too limited to support a rating.

Use this scoring table:

| Criterion | Weight | Evidence basis | Candidate score | Confidence |
| --- | --- | --- | --- | --- |

When a high-weight criterion has insufficient evidence, report the overall score as `Insufficient evidence`.

### 6. Compare Side by Side

Use a Markdown table with one product per column and one feature or cost per row.

Required row groups:

1. Exact model and package
2. Mandatory features
3. Recommended features
4. Optional features
5. Performance evidence
6. Compatibility and ecosystem
7. Reliability, support, and warranty
8. Privacy, security, or safety where relevant
9. Upfront and recurring costs
10. Total cost of ownership
11. Red flags and unknowns
12. Weighted value score

Each product cell must contain the actual value, a brief practical interpretation, and a citation when externally researched.

### 7. Recommend

Lead with a clear verdict:

- **Best value:** The strongest balance of essentials, reliability, performance, and total cost
- **Budget pick:** The least expensive option that still meets mandatory requirements
- **Upgrade pick:** A more expensive option where the added cost buys material value
- **Evidence pending:** A candidate awaiting material condition, support, price, or compatibility evidence
- **Unsuitable:** A candidate with verified risks or missing mandatory requirements that outweigh its price advantage

If only one product was supplied, compare it against current category norms and at most two researched alternatives: one from the same price band and one nearest feature-equivalent option. Explain why each alternative was selected.

## Output Structure

1. **Verdict**
2. **Assumptions and decision criteria**
3. **Technical-term guide**
4. **Side-by-side comparison table**
5. **Cost calculation**
6. **Red flags, unknowns, and warranty/support findings**
7. **Recommendation and rationale**
8. **Sources**

## Verification

Before delivery, confirm:

- Every fact matches the exact model and variant shown in its column.
- Prices include dates, currency, region, and bundle context.
- Mandatory category requirements are present in the table.
- Warranty and recurring costs were researched.
- Ratings follow the displayed criteria and weights.
- Unknowns remain visible.
- Every researched factual claim has a supporting citation.
- The recommendation balances price, essentials, reliability, performance, and ownership cost.
