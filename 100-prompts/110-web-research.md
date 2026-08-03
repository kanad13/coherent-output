# Web Research

## Purpose

Research a question using current external sources and deliver a well-supported answer. Make the evidence trail easy to inspect.

## Scope

This prompt performs research and synthesis. It does not independently stress-test a strategy or produce an implementation plan unless the user explicitly requests those outputs.

## Workflow

### 1. Frame the Research Question

- Identify the user's actual decision or information need.
- Extract the topic, timeframe, geography, constraints, and desired depth.
- State any interpretation that materially affects the search.
- Ask a clarifying question only when different answers would lead to materially different research. Otherwise, make a reasonable, explicit assumption and proceed.

**Visible output:** A short research brief containing the question, scope, and assumptions.

### 2. Build and Execute the Search

- Break broad questions into focused subquestions.
- Use several targeted queries rather than one broad query.
- Prefer sources in this order when applicable:
  1. Primary evidence, official documentation, laws, standards, filings, datasets, or original research
  2. Reputable specialist or institutional analysis
  3. High-quality secondary reporting
  4. Community discussion only for lived experience or clearly labeled anecdotal evidence
- For current events, compare both publication dates and the dates on which events occurred.
- For technical questions, prefer official documentation and original specifications.
- Search for contradictory evidence, not only confirming evidence.

Do not use a fixed source count mechanically. Use enough independent, relevant sources to support the answer. For consequential or disputed claims, seek at least two independent sources when available.

### 3. Evaluate the Evidence

For each important source, consider:

- Authority and proximity to the underlying facts
- Publication date and whether the information may have changed
- Methodology or evidence quality
- Conflicts of interest or likely bias
- Whether other credible sources agree

Separate:

- Verified facts
- Source claims that cannot be independently verified
- Reasonable inference
- Opinion or interpretation
- Unknowns and evidence gaps

### 4. Synthesize and Cite

Use this default structure, adapting it to the question:

1. Direct answer
2. Key findings in priority order
3. Evidence, disagreements, and caveats
4. Practical implications or next steps, when relevant
5. Sources

Citation requirements:

- Cite every externally verifiable factual claim close to the claim it supports.
- Link to the specific supporting page, not a search-results page or generic homepage.
- Include dates when freshness matters.
- Do not cite a source for a claim it does not directly support.
- If a paragraph combines claims from different sources, attach each citation to the relevant sentence or clause.
- Clearly label uncited background knowledge and use it only for stable, well-established context.

### 5. Verify Before Delivery

Confirm that:

- The answer addresses the research brief.
- Important claims are cited.
- Source dates and authority are appropriate.
- Conflicting evidence is visible rather than averaged away.
- Inferences are labeled.
- No source, quotation, statistic, or URL was invented.
- Quotations are short, accurate, and necessary.

## Limited or Failed Research

If evidence is limited:

1. Broaden or reformulate the search.
2. Try primary, academic, archived, regional, or alternative-language sources when appropriate.
3. Report what was verified, what remains unknown, and why.
4. Suggest the most useful next search only when it could realistically resolve the gap.

Never fill an evidence gap with confident speculation.
