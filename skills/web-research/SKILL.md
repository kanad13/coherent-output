---
name: web-research
description: Conducts rigorous, multi-source web research with strict source hierarchy, fact/inference classification, and verifiable citation trails. Use when researching external topics, investigating technical questions online, or validating claims against authoritative documentation.
---

# Web Research & Evidence Synthesis

Follow this 5-step protocol when researching questions using external online sources.

---

## 1. Research Protocol

### Step 1: Frame the Research Scope

- Identify the underlying decision or technical information requirement.
- Extract the core topic, timeframe, constraints, and required depth.
- **Clarification Gate:** If an unknown parameter materially changes the search direction, ask exactly one focused clarifying question. Otherwise, state reasonable assumptions explicitly and proceed.

### Step 2: Build & Execute Search Queries

- Decompose broad questions into targeted sub-queries.
- Prioritize sources according to the authoritative hierarchy:
  1. **Tier 1:** Primary documentation, official specifications, RFCs, regulatory filings, and peer-reviewed research.
  2. **Tier 2:** Specialist engineering publications, institutional analysis, and reputable vendor docs.
  3. **Tier 3:** High-quality technology journalism.
  4. **Tier 4:** Community discussions (strictly for lived experience or anecdotal troubleshooting).
- For fast-moving technical domains, compare publication dates and event dates.
- Actively execute queries to uncover both confirming and contradictory evidence.

### Step 3: Evaluate Evidence & Separate Categories

Classify all gathered information into four discrete categories:

- **Verified Facts:** Directly corroborated by authoritative primary sources.
- **Source Claims:** Asserted by secondary parties awaiting independent confirmation.
- **Reasonable Inferences:** Logical deductions grounded in verified facts.
- **Evidence Gaps / Unknowns:** Areas where data is missing, conflicting, or inconclusive.

### Step 4: Synthesize & Format Deliverable

Deliver the research findings using this structure:

1. **Direct Answer:** Concrete summary of findings addressing the core question.
2. **Key Findings:** Prioritized points supported by direct inline markdown links to sources.
3. **Evidence & Sources Table:**
   | Claim / Topic | Finding | Source / Tier | Confidence |
   | ------------- | ------- | ------------- | ---------- |
4. **Uncertainties & Gaps:** Explicit limitations or unverified edge cases.

### Step 5: Verification Gate

- Confirm that every link points to a real, relevant primary URL.
- Ensure no speculative inferences are stated as established facts.
