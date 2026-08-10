# Technical Text Simplification

## Purpose

Apply this methodology when transforming complex technical material into self-contained explanations users can understand. Preserve every fact, concept, condition, example, qualification, relationship, and technical detail from the source.

The goal is complete comprehension with full content preservation.

## Audience and Accessibility Requirements

The user is the sole audience. Assume general education and limited prior knowledge of the topic.

- Explain from first principles.
- Use short, direct sentences.
- Keep one main idea per sentence or bullet.
- Define unfamiliar terms where they first become necessary.
- Make source-supported dependencies and causal relationships explicit.
- Use focused visuals for every major concept.
- Preserve precise names, numbers, formulas, commands, examples, exceptions, warnings, and uncertainty.
- Prefer completeness and navigability over brevity.

## Visible Analysis Standard

Show the artifacts of careful analysis so the user can review whether the source was understood correctly. Provide inventories, mappings, assumptions, evidence, decisions, and verification results.

## Workflow and Required Outputs

### Phase 1: Source Analysis

Read the complete source before rewriting any part.

Create a **Preservation Ledger** containing:

- Main message
- Every distinct concept or claim
- Definitions and terminology
- Rules, conditions, exceptions, and edge cases
- Steps and dependencies
- Numbers, dates, formulas, commands, and named entities
- Examples, scenarios, analogies, and counterexamples
- Warnings, caveats, uncertainty, and disputed statements
- Relationships that are explicit in the source
- Ambiguities or contradictions that must remain visible

Assign stable identifiers such as `P001`, `P002`, and `P003` to ledger items. Combine exact repetitions while recording every occurrence and preserving meaningful variations.

**Required output 1:** The document-level analysis and Preservation Ledger.

### Phase 2: Comprehension and Visualization Map

Plan how the explanation will become easier to understand while preserving its substance.

For each major concept, determine:

- Which prerequisites must be introduced first
- Which terms need inline definitions
- Which relationships need explicit connecting language
- Which examples need additional explanation
- Which visual form best exposes the concept

Select among:

- ASCII diagrams
- Mermaid flowcharts, sequence diagrams, state diagrams, or mind maps
- Markdown tables, decision tables, and matrices
- Graphviz, D2, or PlantUML diagrams
- Matplotlib, Seaborn, Plotly, or Vega-Lite charts
- Timelines, annotated equations, trees, maps, or spatial sketches

Provide an ASCII or Markdown fallback when a preferred format is unavailable.

**Required output 2:** A concise section and visualization plan that maps every major concept to its intended explanation and visual.

### Phase 3: Rewrite for Understanding

Rewrite the source using these rules:

#### Preserve the Substance

- Preserve every item in the ledger.
- Preserve source claims and flag suspected errors separately.
- Use causes, intentions, dependencies, and examples grounded in the source.
- Preserve uncertainty and modality exactly across `may`, `should`, and `must`.
- Keep code, formulas, commands, identifiers, measurements, and technical names exact. Label every source correction explicitly.

#### Make the Language Accessible

- Lead each section with its main point.
- Use short, active sentences.
- Replace unnecessary jargon with common words.
- Retain necessary technical terms and define them.
- Split dense sentences into focused units.
- Use connecting words such as `because`, `therefore`, `requires`, and `enables` for source-supported relationships.
- Explain what each example demonstrates.
- Use comparisons and counterexamples to distinguish easily confused concepts.

#### Define Terms Clearly

- Define a term immediately when the reader needs it.
- Use a short parenthetical definition for simple terms.
- Use an indented definition bullet when the explanation needs more space.
- Use a small glossary when it improves the flow more than repeated inline definitions.

#### Visualize Every Major Concept

- Place each visual immediately after the concept it explains.
- Use one visual for one primary insight.
- Label the visual and explain how to read it.
- Use several progressive visuals for a complex concept.
- Pair every visual with a written explanation.

#### Preserve Structure Intelligently

- Preserve the source's useful headings, sequence, and formatting.
- Add headings when necessary to make a long unstructured source navigable.
- Support plain text, a single section, or a complete Markdown document with any heading structure.

**Required output 3:** The complete simplified document.

### Phase 4: Preservation Audit

Compare the rewritten document against the Preservation Ledger.

Use this traceability table:

| Ledger ID | Source content | Target location | Treatment | Preserved? |
| --- | --- | --- | --- | --- |
| `P001` | [Concept or detail] | [Section] | Exact / Simplified wording / Defined / Visualized | Preserved / Gap |

Then verify:

- Every ledger item has a target location.
- Every technical detail and qualifier retains its original strength.
- Every added fact and causal relationship is supported by the source.
- Every major concept has both an explanation and a visual.
- Every visual matches the written explanation.
- The output can stand alone for a beginner.

If anything is missing or distorted, correct the document and repeat the affected audit rows.

## Delivery Rules

- If the user supplied text in chat, show all required outputs in sequence.
- For file edits, place the simplified document in the target file and show the analysis, plan, and audit in the conversation. Store analysis artifacts in the file when the user requests them there.
- Create a separate output file by default. Use in-place editing after the user explicitly requests it.
- End with every suspected source error or irreducible ambiguity preserved for review.
