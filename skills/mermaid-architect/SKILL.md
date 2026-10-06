---
name: mermaid-architect
description: Ingests technical documents or codebases, formulates a visual coverage plan, constructs native Mermaid diagrams, verifies compilation, and inserts them cleanly without altering existing text. Use when creating architecture diagrams, visualizing workflows, or enhancing docs with Mermaid.
---

# Mermaid Visualization Architect & Inserter

Follow this protocol to design, verify, and insert native Mermaid diagrams into technical documents.

---

## 1. Non-Negotiable Directives

- **Strict Insertion-Only Editing:** Pre-existing text in the source document is 100% immutable. Never modify, rephrase, delete, reorder, or reformat existing headings, paragraphs, tables, or code fences.
- **Pre-Existing Diagram Immutability:** Never edit or delete pre-existing Mermaid blocks in the source document.
- **Insertion Payload Structure:** Every inserted diagram block must contain strictly:
  1. Exactly one bold, insight-driven caption: `**Diagram: <Actionable Insight>**`
  2. Exactly one fenced Mermaid code block (` ```mermaid ` ... ` ``` `) placed at a valid block boundary immediately following the passage introducing the concept.
  - **No Headings for Captions:** Never use Markdown headings (`#`, `##`, `###`) for captions to protect document Table of Contents hierarchy.
  - **No Prose Injections:** Never inject introductory summaries or transitions into the source document.
- **Clean Native Styling:** Use standard Mermaid shapes, layout directions, and subgraphs. Avoid brittle inline CSS styling (`style`, `linkStyle`, `fill:`, `stroke:`).
- **Flowchart Semantic Shape Grammar:** Use standard semantic shapes consistently:
  - `([Stadium / Pill])`: Terminal endpoints, external callers, client applications, start/end states.
  - `[Rectangle]`: Processing steps, computations, actions, microservice handlers.
  - `{Diamond}`: Decision points, conditional branches, guard evaluations.
  - `[(Cylinder)]`: Persistent databases, caches, session stores, disk storage.
  - `((Circle))`: Event triggers, pub/sub messages, signals, event stream topics.
  - `{{Hexagon}}`: Business rules, policy evaluations, cryptographic operations.
  - `[/Parallelogram/]`: Input / Output payloads, external network data.
  - `subgraph Name ["Display Title"] ... end`: System boundaries, namespaces, VPCs, trust zones.
- **Layout & Anti-Noodle Rules:**
  - Break single-axis linear flows (>12 nodes) into logical subgraphs, parallel branches, or phased grids.
  - Default to `TD` for lifecycles, hierarchies, and decision trees; default to `LR` for pipelines and time sequences.
  - Enclose all display labels containing spaces, parentheses, or punctuation in explicit double quotes: `id["Service (v2)"]`.
- **Absolute Factual Grounding:** Ground every entity, state, transition, and relationship directly in the source text. Never invent components. Explicitly label necessary bridging assumptions with `[Inferred]`.

---

## 2. Five-Phase Execution Pipeline

### Phase 1: Ingest & Model Source Content

- Analyze the document to identify core processes, state lifecycles, entity relationships, and architectural boundaries.
- Extract actors, states, decisions, data flows, and concurrency.

### Phase 2: Formulate Visual Coverage Plan

- Consult the **Mermaid Grammar Selector Matrix (Appendix A)** to choose the authoritative grammar and fallback.
- Apply the **Progressive Visual Hierarchy** when a topic has multi-layered complexity:
  1. _Level 1 (Simple Model):_ Core entry points and high-level routing.
  2. _Level 2 (Expanded Model):_ Surrounding components, trust boundaries, and data stores.
  3. _Level 3 (Behavioral Model):_ Sequences, state transitions, decisions, or data movement.
  4. _Level 4 (Detail/Edge Cases):_ Constraints, failure branches, exceptions, or packet layouts.
- Map planned diagrams into the structured Visual Coverage Plan table:

| Target Section / Topic | Visual Question Addressed | Core Insight Delivered | Mermaid Grammar Selected | Placement Block Boundary | Design Rationale |
| :--------------------- | :------------------------ | :--------------------- | :----------------------- | :----------------------- | :--------------- |

### Phase 3: Construct Native Mermaid Diagrams

- Apply the semantic shape grammar and subgraphs.
- Keep node labels concise (2–6 words) and enclose them in double quotes.

### Phase 4: Active Tool Verification & Compilation

- Validate syntax before inserting diagrams.
- For single `.mmd` files, run:
  [`./scripts/verify-mmdc.sh`](./scripts/verify-mmdc.sh) `<diagram_file.mmd>`
- For batch validation of Markdown documents containing embedded Mermaid blocks, run:
  `python3 ./skills/mermaid-architect/scripts/verify-markdown.py <target_document.md>`
- If compilation fails, diagnose the exact syntax error, close unescaped quotes, or fall back to standard grammar per Appendix A.

### Phase 5: Structured Delivery & File Application

- **Disk Target:** When modifying an existing file on disk, apply the verified diagram blocks directly using file modification tools (`replace_file_content` or `write_to_file`).
- **Response Format:** Structure output in three distinct sections:
  - **Section A:** Visual Coverage Plan (including the plan table).
  - **Section B:** Updated source document.
  - **Section C:** Compilation verification report.

---

## Appendix A: Mermaid Grammar Selector Matrix & Fallbacks

| Visual Question / Domain                   | Primary Mermaid Grammar | Keyword / Declaration             | Ideal Use Case                                                | Fallback Grammar              |
| :----------------------------------------- | :---------------------- | :-------------------------------- | :------------------------------------------------------------ | :---------------------------- |
| **Process / Decision / Pipeline**          | Flowchart               | `flowchart TD` / `flowchart LR`   | Algorithms, branching logic, CI/CD, execution pipelines       | `graph TD`                    |
| **Actor Protocol / Time Sequence**         | Sequence Diagram        | `sequenceDiagram`                 | API interactions, RPC handshakes, auth flows, event messaging | Flowchart LR                  |
| **Object Lifecycle / State Transitions**   | State Diagram           | `stateDiagram-v2`                 | FSMs, connection states, order status lifecycles, retries     | Flowchart TD                  |
| **Database Schema / Entity Relationships** | ER Diagram              | `erDiagram`                       | SQL/NoSQL schemas, foreign keys, cardinality, data models     | Class Diagram                 |
| **Class Hierarchy / Domain Types**         | Class Diagram           | `classDiagram`                    | OOP structures, interfaces, typing models, design patterns    | ER Diagram                    |
| **Project Phases / Durations**             | Gantt Chart             | `gantt`                           | Project schedules, concurrent task execution, milestones      | Timeline                      |
| **Category Proportions**                   | Pie Chart               | `pie`                             | Small number of non-negative parts of one whole               | Markdown Table                |
| **System Architecture / Boundaries**       | C4 / Architecture       | `C4Context` / `architecture-beta` | Microservices topology, cloud infrastructure, trust zones     | Flowchart with Subgraphs      |
| **Controlled Spatial Grid**                | Block Diagram           | `block-beta`                      | Deliberate spatial component layouts                          | Flowchart with Subgraphs      |
| **Magnitude & Flow Transfers**             | Sankey Diagram          | `sankey-beta`                     | Energy, cost allocation, conversion funnels                   | Flowchart with labeled widths |
| **Quantitative Trends / Comparisons**      | XY Chart                | `xychart-beta`                    | Time series metrics, bar charts, benchmarks, throughput       | Markdown Table                |
| **Branching / Version Control**            | Git Graph               | `gitGraph`                        | Branch/merge strategies, trunk-based development              | Flowchart LR                  |
| **Chronology / Milestones / Releases**     | Timeline                | `timeline`                        | Release history, incident timelines, migration phases         | Gantt Chart                   |
| **Taxonomy / Concept Breakdown**           | Mindmap                 | `mindmap`                         | Category trees, feature breakdowns, mental models             | Flowchart TD                  |
| **User Experience / Journey**              | User Journey            | `journey`                         | User onboarding, step-by-step UX flows with satisfaction      | Flowchart LR                  |
| **Tradeoffs / 2x2 Matrix**                 | Quadrant Chart          | `quadrantChart`                   | Risk vs. Value, Priority matrix, Capability evaluation        | Flowchart with Grid Subgraphs |
| **Binary Protocol / Header Layout**        | Packet Diagram          | `packet-beta`                     | Network headers (IP/TCP), binary file structures              | Markdown Table or Flowchart   |
