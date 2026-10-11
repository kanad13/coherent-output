---
name: web-research
description: Conducts rigorous, multi-source web research to validate internal model knowledge against authoritative online documentation, investigate external APIs, or verify empirical claims. Use at task inception or iteratively during execution when encountering unfamiliar external dependencies, APIs, or version-specific behaviors. Do not invoke for standard language primitives, trivial shell commands, or purely internal codebase logic.
---

# Web Research & Evidence Synthesis

Follow this protocol when researching technical questions, validating model knowledge against primary documentation, or gathering external empirical evidence. Prioritize primary sources according to the authoritative evidence hierarchy, classify findings into facts, claims, and inferences, and enforce zero hallucination.

---

## 1. Invocation Triggers & Operational Scope

- **Initial Grounding Trigger:** When user requests involve external frameworks, third-party APIs, SDK specifications, or empirical claims, steelman the query and search authoritative sources to validate internal model knowledge against current ground truth.
- **Iterative In-Flight Trigger:** When executing tasks and encountering unfamiliar library methods, syntax deprecations, or unexpected tool/compiler errors, search immediately rather than guessing or hallucinating fixes.
- **Exclusion Boundaries:** Do not invoke for trivial standard operations (e.g., standard language primitives, basic shell commands) or purely internal codebase refactors that do not cross system boundaries.
- **Scope Discipline:** Avoid search rabbit holes. Limit in-flight queries to resolving the immediate blocking unknown before resuming the primary workflow.

---

## 2. Five-Step Research Protocol

Execute the following five steps sequentially:

### Step 1: Steelman & Frame the Research Scope

- Identify the underlying decision or technical information requirement.
- Steelman the query: formulate the core technical inquiry into its most precise, falsifiable, and search-optimized terminology.
- Extract timeframe constraints, version boundaries, and required depth.
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

### Step 3: Evaluate Evidence & Classify Categories

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
