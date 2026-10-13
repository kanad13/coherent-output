---
name: mermaid-architect
description: Gives every heading of a technical document a verified native Mermaid diagram that delivers one insight, and inserts the diagrams without altering existing text. Use when creating architecture diagrams, visualizing workflows, or enhancing docs with Mermaid. Do not use for rendering external UI widgets or modifying surrounding prose.
---

# Mermaid Diagram Architect

Add compilable Mermaid diagrams to a document by insertion only. Every pre-existing byte of the source stays unchanged. Every heading (H1-H6) receives at least one diagram, and every diagram delivers one insight.

---

## 1. Output Contract

- **Insertion only:** Leave existing headings, paragraphs, tables, and code fences unmodified, unreordered, and unreformatted.
- **Insertion block:** Each insertion is exactly two parts:
  1. A caption line, `**Diagram: <Insight>**`, written as a statement of the diagram's single message.
  2. One fenced `mermaid` block.
- **Caption format:** Write the caption in bold text. Headings stay out of captions so the document's table of contents stays intact. Prose summaries and transitions stay out of the document.
- **Placement:** Insert at a block boundary right after the passage that introduces the concept. When a heading has no text before its first subheading, insert directly under the heading.
- **Response:** Return three sections: **A** the coverage plan table, **B** the updated document (or the verified candidate when a formatting conflict blocks saving), **C** compilation and preservation results, including any conflict.

---

## 2. Diagram Principles

- **One message:** A diagram carries one insight, and that insight is its caption. A passage with several insights gets several diagrams.
- **Simplicity:** Every node advances the message. Cut any node that does not. Use at most 10 nodes.
- **Independence:** A reader who sees only the diagram understands it. Name actors, states, and systems in full inside the labels, because the contract allows no explanatory prose.
- **Consistency:** Use one term per concept, one class meaning per color, and one direction convention across every diagram in the document.
- **Coverage:** Every heading (H1-H6) has at least one diagram, and no content is skipped.
  - A thin section gets a small diagram (2-4 nodes) of what its text states.
  - A section with no text of its own diagrams the relationship between its title and its subsections.
- **Grounding:** Every node and edge traces to the source text. Mark a necessary bridging assumption with `[Inferred]` in its label.

---

## 3. Syntax Rules

- **Labels:** Put every node label and every edge label in double quotes. Write plain text: no emojis or decorative symbols, and a hyphen in place of parentheses (`"Request - data"`).
- **Line breaks:** Use `<br/>` for multi-line labels and keep each line brief (2-6 words). To separate a title from detail, use `━━━`, the only permitted symbol: `"Title<br/>━━━<br/>Detail"`.
- **Edge labels:** Put the label after the arrow operator in pipe form: `A -->|"calls"| B`.
- **Subgraphs:** Use at most 3 per diagram. Declare an identifier plus a quoted title, and begin the body with a direction: `subgraph SvcId ["Service Tier"]` then `direction TB`.
- **Direction:** `TD` for lifecycles, hierarchies, and decision trees. `LR` for pipelines and time sequences.
- **Titles:** The caption carries the title. Leave frontmatter titles out of the fence.

---

## 4. Styling

- **Classes:** In flowcharts and `stateDiagram-v2`, assign every node one class from the theme block (Appendix B) by logical tier:
  - `c1`: Ingress, client, entrypoint, primary flow
  - `c2`: Compute, internal services, transforms, core engine
  - `c3`: Persistence, data stores, state, caches
  - `c4`: Messaging, queues, streaming, decision gates
  - `c5`: External systems, third parties, egress, boundaries
  - `default`: Uncategorized or utility nodes
- **Theme:** Paste the Theme A block (the default) at the top of each flowchart, or the theme the user names. In `stateDiagram-v2`, declare only the `c1`-`c5` classes in use and omit `classDef default`, which fails to compile.
- **Other grammars:** Sequence diagrams and the remaining grammars use native styling without classes.
- **Host colors:** Leave text and connector colors to the host theme. `classDef` and `style` carry fill and stroke only, with no `color:` and no `linkStyle`, so contrast holds in light and dark editors.
- **Subgraph boundary:** `style <id> fill:<hex>,stroke:<hex>,stroke-width:1px,stroke-dasharray:4 4`, with the values from the active theme.

---

## 5. Procedure

1. **Map:** List every heading outside fenced code, with the text under it. Note which sections already contain Mermaid diagrams; those stay untouched, and a heading without one still gets one.
2. **Plan:** Write the coverage table, one row per diagram. Every heading appears in at least one row. Pick each grammar from Appendix A.

   | Heading | Insight (becomes the caption) | Grammar | Placement |
   | :------ | :---------------------------- | :------ | :-------- |

3. **Build:** Write each diagram to Sections 2-4. Reread it against its insight and delete nodes that do not carry it.
4. **Verify:** Copy the document to a temporary location, add all blocks to the copy, and compile once with the batch helper. The helper names the failing diagram by its position in the document; fix it and recompile until the exit code is `0`. If a grammar still fails to compile, redraw the same insight as a flowchart.
5. **Apply:** Keep the original bytes and the insertion boundaries. Write the verified candidate to the source through a path that preserves bytes, then read the saved file after hooks and formatters finish.
6. **Check the saved result:** Remove only the inserted blocks from a comparison copy and compare the remaining bytes with the original. Confirm every heading has a diagram in the saved file. A successful tool call or compilation does not establish text preservation.
7. **Formatting conflict:** When post-processing changed existing text, restore the original bytes through a byte-preserving write and verify the restoration. Deliver the candidate through that path or as a separate artifact. Hooks, formatter settings, and ignore comments stay as they are, because changing them exceeds this contract. When preservation cannot be verified, report the conflict and the actual saved state.

### Verification helpers

The scripts live in `scripts/` beside this `SKILL.md`. Resolve `<skill_dir>` to this skill's folder (`skills/mermaid-architect` in this checkout, or `mermaid-architect` inside the installed skills directory).

- Document batch: `python3 <skill_dir>/scripts/verify-markdown.py <document.md>`
- Single diagram: `<skill_dir>/scripts/verify-mmdc.sh <diagram.mmd>`
- Provisioning: the helper needs `@mermaid-js/mermaid-cli@12.0.0` and never downloads during verification. In this checkout, run `npm ci` at the repository root. For a separate install, place that exact version in the skill folder or on `PATH`. `COHERENT_MMDC_BIN` selects an explicit executable, and `COHERENT_PUPPETEER_CONFIG` passes a Puppeteer configuration file (for example `--no-sandbox` on a CI runner).
- Exit codes: `0` compiled (or the document has no Mermaid fences), `1` invalid syntax, `2` verification could not run (missing tooling or browser dependencies). Report exit `2` as an unverified result. Each renderer call has a timeout, and temporary files are removed.

---

## Appendix A: Grammar Selector

Choose the grammar that matches the visual question. When the first choice fails to compile, redraw as a flowchart.

| Visual Question                       | Grammar          | Declaration                       | Use                                                      |
| :------------------------------------ | :--------------- | :-------------------------------- | :------------------------------------------------------- |
| Process, decision, pipeline           | Flowchart        | `flowchart TD` / `flowchart LR`   | Algorithms, branching logic, CI/CD, execution pipelines  |
| Actor protocol, time sequence         | Sequence         | `sequenceDiagram`                 | API interactions, RPC handshakes, auth flows, messaging  |
| Object lifecycle, state transitions   | State            | `stateDiagram-v2`                 | State machines, connection states, order status, retries |
| Database schema, entity relationships | ER               | `erDiagram`                       | SQL/NoSQL schemas, foreign keys, cardinality             |
| Class hierarchy, domain types         | Class            | `classDiagram`                    | Interfaces, typing models, design patterns               |
| Project phases, durations             | Gantt            | `gantt`                           | Schedules, concurrent tasks, milestones                  |
| Category proportions                  | Pie              | `pie`                             | A few non-negative parts of one whole                    |
| System architecture, boundaries       | C4, Architecture | `C4Context` / `architecture-beta` | Microservice topology, cloud infrastructure, trust zones |
| Controlled spatial grid               | Block            | `block-beta`                      | Deliberate spatial component layouts                     |
| Magnitude and flow transfers          | Sankey           | `sankey-beta`                     | Energy, cost allocation, conversion funnels              |
| Quantitative trends, comparisons      | XY Chart         | `xychart-beta`                    | Time series metrics, bar charts, benchmarks              |
| Branching, version control            | Git Graph        | `gitGraph`                        | Branch and merge strategies, trunk-based development     |
| Chronology, milestones, releases      | Timeline         | `timeline`                        | Release history, incident timelines, migration phases    |
| Taxonomy, concept breakdown           | Mindmap          | `mindmap`                         | Category trees, feature breakdowns, mental models        |
| User experience, journey              | User Journey     | `journey`                         | Onboarding and step-by-step flows with satisfaction      |
| Tradeoffs, 2x2 matrix                 | Quadrant         | `quadrantChart`                   | Risk versus value, priority matrices                     |
| Binary protocol, header layout        | Packet           | `packet-beta`                     | Network headers (IP/TCP), binary file structures         |

---

## Appendix B: Theme Blocks

Theme A is the default.

### Theme A (Cool Slate)

```text
classDef default fill:#64748B1F,stroke:#64748B,stroke-width:1.5px;
classDef c1 fill:#2563EB24,stroke:#3B82F6,stroke-width:2px;
classDef c2 fill:#7C3AED24,stroke:#8B5CF6,stroke-width:1.5px;
classDef c3 fill:#05966924,stroke:#10B981,stroke-width:1.5px;
classDef c4 fill:#D9770624,stroke:#F59E0B,stroke-width:1.5px;
classDef c5 fill:#DC262624,stroke:#EF4444,stroke-width:2px;
```

Subgraph style: `style <id> fill:#64748B12,stroke:#64748B,stroke-width:1px,stroke-dasharray:4 4`

### Theme B (Warm Earth)

```text
classDef default fill:#78716C1F,stroke:#78716C,stroke-width:1.5px;
classDef c1 fill:#36694E24,stroke:#4C8565,stroke-width:2px;
classDef c2 fill:#556B2F24,stroke:#7B9E4B,stroke-width:1.5px;
classDef c3 fill:#2D7A5824,stroke:#3E9970,stroke-width:1.5px;
classDef c4 fill:#B8860B24,stroke:#D49B35,stroke-width:1.5px;
classDef c5 fill:#C25E3E24,stroke:#D97757,stroke-width:2px;
```

Subgraph style: `style <id> fill:#78716C12,stroke:#78716C,stroke-width:1px,stroke-dasharray:4 4`

### Theme C (Vibrant Modern)

```text
classDef default fill:#6B72801F,stroke:#6B7280,stroke-width:1.5px;
classDef c1 fill:#7E22CE24,stroke:#9333EA,stroke-width:2px;
classDef c2 fill:#0284C724,stroke:#0EA5E9,stroke-width:1.5px;
classDef c3 fill:#05966924,stroke:#10B981,stroke-width:1.5px;
classDef c4 fill:#D9770624,stroke:#F59E0B,stroke-width:1.5px;
classDef c5 fill:#E11D4824,stroke:#F43F5E,stroke-width:2px;
```

Subgraph style: `style <id> fill:#6D28D910,stroke:#7C3AED,stroke-width:1px,stroke-dasharray:4 4`
