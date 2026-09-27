---
name: mermaid-architect
description: Ingests technical documents or codebases, formulates a visual coverage plan, constructs native Mermaid diagrams, verifies compilation, and inserts them cleanly without altering existing text. Use when creating architecture diagrams, visualizing workflows, or enhancing docs with Mermaid.
---

# Mermaid Visualization Architect & Inserter

Follow this protocol to design, verify, and insert Mermaid diagrams into technical documents.

---

## 1. Non-Negotiable Directives

- **Strict Insertion-Only Editing:** The pre-existing text of the source document is 100% immutable. Never modify, rephrase, delete, reorder, or reformat existing headings, paragraphs, tables, or code fences.
- **Pre-Existing Diagram Immutability:** Never modify or delete pre-existing Mermaid diagrams in the document.
- **Insertion Payload Structure:** Every inserted diagram block must consist strictly of:
  1. Exactly one bold, insight-driven caption: `**Diagram: <Actionable Insight>**`
  2. Exactly one fenced Mermaid code block (` ```mermaid ` ... ` ``` `) placed immediately after the paragraph introducing the concept.
- **Clean Native Styling:** Use standard Mermaid shapes, layout directions, and subgraphs. Avoid brittle inline CSS styling (`style`, `linkStyle`, `fill:`, `stroke:`).
- **Absolute Factual Grounding:** Every entity, state, transition, and relationship must be directly grounded in the source text. Never invent components or causal connections. Label necessary bridging assumptions with `[Inferred]`.

---

## 2. End-to-End 5-Phase Pipeline

### Phase 1: Ingest & Model Source Content

- Analyze the document to identify core processes, state lifecycles, entity relationships, and architectural boundaries.
- Extract actors, states, decisions, data flows, and concurrency.

### Phase 2: Formulate Visual Coverage Plan

- Select the authoritative Mermaid grammar for each concept:
  - **Process / Decision Trees / Pipelines:** `flowchart TD` or `flowchart LR`
  - **Inter-service Messages / API Protocols:** `sequenceDiagram`
  - **Entity Lifecycles / Transitions:** `stateDiagram-v2`
  - **Data Models / Schemas:** `erDiagram`
  - **Object Architecture / Inheritance:** `classDiagram`
  - **Quantitative Distributions:** `xychart-beta`
- Determine optimal insertion points at valid block boundaries between sections.

### Phase 3: Construct Native Mermaid Diagrams

- Format node labels with clean syntax: quote labels containing parentheses or special characters (`id["Service (v2)"]`).
- Keep diagrams compact and readable: limit flowcharts to 12–15 nodes per diagram; decompose larger flows into subgraphs or sequential diagrams.

### Phase 4: Syntax Verification

- Validate the syntax of every diagram before inserting.
- Run the headless Mermaid CLI verification script:
  [`./scripts/verify-mmdc.sh`](./scripts/verify-mmdc.sh) `<diagram_file.mmd>`
- If syntax errors occur, adjust node identifiers, quote special characters, or simplify relationship arrows.

### Phase 5: Insertion & Delivery

- Insert the verified diagram blocks into the source document at planned block boundaries.
- Present the deliverable with:
  - **Section A:** Visual Coverage Plan.
  - **Section B:** Updated source document.
  - **Section C:** Compilation verification report.
