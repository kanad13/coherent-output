---
name: mermaid-architect
description: Ingests technical documents, formulates a visual coverage plan, constructs native Mermaid diagrams, verifies compilation, and inserts them cleanly without altering existing text. Use when creating architecture diagrams, visualizing workflows, or enhancing docs with Mermaid. Do not use for rendering external UI widgets or modifying surrounding prose.
---

# Mermaid Visualization Architect & Inserter

Follow this protocol to design, verify, and insert native Mermaid diagrams into technical documents. Enforce strict insertion-only editing—leaving pre-existing text 100% immutable—and verify diagram syntax compilation before saving.

---

## 1. Non-Negotiable Directives

- **Strict Insertion-Only Editing:** Pre-existing text in the source document is 100% immutable. Never modify, rephrase, delete, reorder, or reformat existing headings, paragraphs, tables, or code fences.
- **Insertion Payload Structure:** Every inserted diagram block must contain strictly:
  1. Exactly one bold, insight-driven caption: `**Diagram: <Actionable Insight>**`
  2. Exactly one fenced Mermaid code block (` ```mermaid ` ... ` ``` `) placed at a valid block boundary immediately following the passage introducing the concept.
  - **No Headings for Captions:** Never use Markdown headings (`#`, `##`, `###`) for captions to protect document Table of Contents hierarchy.
  - **No Prose Injections:** Never inject introductory summaries or transitions into the source document.
- **Cross-Theme Styling Directives (Appendix B):** Ensure full visual contrast and legibility in both light and dark editor themes. Apply categorical token classes (`c1` through `c5`) defined in Appendix B. Never hardcode font colors (`color:#...`) or connector stroke colors (`linkStyle`); leave text and connectors unassigned so the host viewer automatically applies native theme styling.
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
  - Cap individual diagrams at a maximum of 10–12 nodes. Break larger systems into separate overview and subsystem diagrams ("peel the onion").
  - Default to `TD` for lifecycles, hierarchies, and decision trees; default to `LR` for pipelines and time sequences.
  - Enclose all display labels containing spaces, parentheses, or punctuation in explicit double quotes: `id["Service (v2)"]`.
- **Absolute Factual Grounding:** Ground every entity, state, transition, and relationship directly in the source text. Never invent components. Explicitly label necessary bridging assumptions with `[Inferred]`.

---

## 2. Five-Phase Execution Pipeline

### Phase 1: Ingest & Model Source Content

- Analyze the document to identify core processes, state lifecycles, entity relationships, and architectural boundaries.
- Extract actors, states, decisions, data flows, and concurrency.
- **The Progressive Zoom Principle ("Peel the Onion"):** Audit sections by central theme. Provide an orientation diagram ("forest view") at the parent section level to establish the upcoming mental model; introduce focused subsystem diagrams ("tree view") inside subsections. Never cram a multi-layered concept into one giant diagram; limit each individual diagram to a single cognitive tier and a maximum of 10–12 nodes.

### Phase 2: Formulate Visual Coverage Plan

- Consult the **Mermaid Grammar Selector Matrix (Appendix A)** to choose the authoritative grammar and fallback.
- Classify planned diagrams by **Zoom Tier**:
  - **Macro Orientation:** Placed at section roots to visualize high-level routing, lifecycles, or architectural topology.
  - **Micro Subsystem:** Placed within subsections to detail localized branching logic, RPC protocols, or data structures.
- Map planned diagrams into the structured Visual Coverage Plan table:

| Target Section / Topic | Zoom Tier (Macro / Micro) | Visual Question Addressed | Core Insight Delivered | Mermaid Grammar Selected | Placement Block Boundary | Design Rationale |
| :--------------------- | :------------------------ | :------------------------ | :--------------------- | :----------------------- | :----------------------- | :--------------- |

### Phase 3: Construct Native Mermaid Diagrams

- Apply the semantic shape grammar and subgraphs.
- Bind all nodes to categorical theme classes (`c1` through `c5`) from Appendix B based on logical component tier.
- Include the active theme definitions (defaulting to Theme A) at the head of every flowchart.
- Keep node labels concise (2–6 words) and enclose them in double quotes.

### Phase 4: Active Tool Verification & Compilation

- Validate syntax before inserting diagrams.
- Locate helper scripts in the `scripts/` directory sibling to this `SKILL.md`:
  - Single `.mmd` preview validation:
    `<skill_dir>/scripts/verify-mmdc.sh <diagram_file.mmd>`
  - Markdown batch verification:
    `python3 <skill_dir>/scripts/verify-markdown.py <target_document.md>`
    _(Resolve `<skill_dir>` to this skill's folder, e.g. `~/.gemini/config/skills/mermaid-architect` or `skills/mermaid-architect`)_.

### Phase 5: Structured Delivery & File Application

- **Disk Target:** Insert the verified diagram blocks directly into the source file.
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

---

## Appendix B: Cross-Theme Styling Directive

When generating Mermaid diagrams, ensure visual contrast and legibility across both light and dark editor themes by adhering to these rules:

### 1. Text Inheritance

- Never add `color:#...` to any `classDef` or `style` definition.
- Leave text color unassigned so the host Markdown viewer automatically applies its dark-theme or light-theme font styling.

### 2. Connector Preservation

- Never define `linkStyle` with hardcoded stroke colors. Let connectors follow host theme defaults.

### 3. Categorical Token Roles (`c1` through `c5`)

Assign nodes to categorical classes according to logical tier or component type:

- `c1`: Ingress / Client / Primary Flow / Entrypoint
- `c2`: Compute / Internal Services / Transform / Core Engine
- `c3`: Persistence / Data Store / State / Caches
- `c4`: Messaging / Buffers / Queues / Streaming / Decision Gates
- `c5`: External Systems / Third-Party Services / Egress / Boundaries
- `default`: Uncategorized or utility nodes

### 4. Subgraphs

Style subgraphs explicitly using dashed neutral boundaries:
`style <cluster_id> fill:<hex_subgraph>,stroke:<hex_stroke>,stroke-width:1px,stroke-dasharray:4 4`

### 5. Theme Definitions

When instructed to use Theme A (default when no preference is specified), Theme B, or Theme C, include the corresponding block at the top of the diagram and apply the classes to all nodes:

#### Theme A (Cool Slate — Default)

```text
classDef default fill:#64748B1F,stroke:#64748B,stroke-width:1.5px;
classDef c1 fill:#2563EB24,stroke:#3B82F6,stroke-width:2px;
classDef c2 fill:#7C3AED24,stroke:#8B5CF6,stroke-width:1.5px;
classDef c3 fill:#05966924,stroke:#10B981,stroke-width:1.5px;
classDef c4 fill:#D9770624,stroke:#F59E0B,stroke-width:1.5px;
classDef c5 fill:#DC262624,stroke:#EF4444,stroke-width:2px;
```

Subgraph style: `style <id> fill:#64748B12,stroke:#64748B,stroke-width:1px,stroke-dasharray:4 4`

#### Theme B (Warm Earth)

```text
classDef default fill:#78716C1F,stroke:#78716C,stroke-width:1.5px;
classDef c1 fill:#36694E24,stroke:#4C8565,stroke-width:2px;
classDef c2 fill:#556B2F24,stroke:#7B9E4B,stroke-width:1.5px;
classDef c3 fill:#2D7A5824,stroke:#3E9970,stroke-width:1.5px;
classDef c4 fill:#B8860B24,stroke:#D49B35,stroke-width:1.5px;
classDef c5 fill:#C25E3E24,stroke:#D97757,stroke-width:2px;
```

Subgraph style: `style <id> fill:#78716C12,stroke:#78716C,stroke-width:1px,stroke-dasharray:4 4`

#### Theme C (Vibrant Modern)

```text
classDef default fill:#6B72801F,stroke:#6B7280,stroke-width:1.5px;
classDef c1 fill:#7E22CE24,stroke:#9333EA,stroke-width:2px;
classDef c2 fill:#0284C724,stroke:#0EA5E9,stroke-width:1.5px;
classDef c3 fill:#05966924,stroke:#10B981,stroke-width:1.5px;
classDef c4 fill:#D9770624,stroke:#F59E0B,stroke-width:1.5px;
classDef c5 fill:#E11D4824,stroke:#F43F5E,stroke-width:2px;
```

Subgraph style: `style <id> fill:#6D28D910,stroke:#7C3AED,stroke-width:1px,stroke-dasharray:4 4`
