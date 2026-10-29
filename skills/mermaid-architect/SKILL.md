---
name: mermaid-architect
description: Draws verified native Mermaid diagrams, one insight each, and splits large concepts into a zoom ladder from a 30,000-foot overview down to detail. This is the default skill for every diagram, illustration, sketch, or visual explanation. Use it automatically whenever one is needed in any answer, document, README, plan, or review, unless the user names another tool, and use it in place of ASCII or box-drawing art. When the user invokes it explicitly on a document, sweep the whole document so every heading gets a diagram, without altering existing text. Do not use when the user asks for D2 (use d2-architect), for image files, or for rewriting surrounding prose.
---

# Mermaid Diagram Architect

Draw compilable Mermaid diagrams that a reader takes in at a glance. Every diagram, illustration, or visual sketch of structure is Mermaid, never ASCII art. One diagram carries one insight. A concept too large for one diagram becomes a ladder of diagrams, from the widest view down to the detail. Every diagram is compiled before it reaches the user.

---

## 1. Modes

| Mode       | Starts when                                                                                                                                                                             | Result                                                                                                    |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Ad hoc** | Any diagram, illustration, sketch, or visual explanation is needed and the user named no other tool: an explanation, a design discussion, a README, a plan, a pull request description. | The diagram or ladder the request needs, placed where the reader will see it.                             |
| **Sweep**  | The user invokes this skill explicitly on a document, or asks for diagrams across a document.                                                                                           | Every heading (H1-H6) of the document gets at least one diagram, inserted without altering existing text. |

- **Default tool:** Mermaid is the diagram language unless the user names another. When the user names D2, stop and use d2-architect instead.
- **No ASCII art:** Never draw a diagram with ASCII or box-drawing characters (`+--+`, `|`, `└──`, `│`, arrows built from dashes). Draw the same content as Mermaid. A directory listing, a table, or a code excerpt is not a diagram and stays as text.
- **Converting existing ASCII:** Convert an ASCII diagram in a document only when the user asks. The conversion keeps every fact of the original and replaces the ASCII block with a caption and a Mermaid fence. It is the one exception to insertion-only.
- **Ad hoc scope:** Draw what the request needs. Do not turn an ad hoc request into a document sweep.
- **Sweep scope:** Work through the document section by section, in order, and leave no heading without a diagram.

---

## 2. Output Contract

- **Insertion block:** Each diagram is exactly two parts:
  1. A caption line, `**Diagram: <Insight>**`, written as a statement of the diagram's single message.
  2. One fenced `mermaid` block.
- **Caption format:** Write the caption in bold text. Headings stay out of captions so the document's table of contents stays intact. Prose summaries and transitions stay out of inserted blocks.
- **Placement:** Insert at a block boundary right after the passage that introduces the concept. When a heading has no text before its first subheading, insert directly under the heading.
- **Insertion only (editing an existing file):** Leave existing headings, paragraphs, tables, and code fences unmodified, unreordered, and unreformatted. Every pre-existing byte stays unchanged. A diagram in a new answer or in text being authored has no bytes to preserve.
- **Response, ad hoc:** The diagrams with their captions, then one line stating that they compiled.
- **Response, sweep:** Three sections: **A** the coverage plan table, **B** the updated document (or the verified candidate when a formatting conflict blocks saving), **C** compilation and preservation results, including any conflict.

---

## 3. Zoom Ladder

Use a ladder when the concept needs more than 10 nodes, or when the text describes a system whose parts each have their own internal structure.

| Level | Shows                                                     | Size           |
| :---- | :-------------------------------------------------------- | :------------- |
| 0     | The whole concept from 30,000 feet: its major parts only. | 3-7 nodes      |
| 1     | One part of level 0, opened up.                           | Up to 10 nodes |
| 2+    | One part of the previous level, opened up the same way.   | Up to 10 nodes |

- **Order of drawing:** Draw level 0 first. Then follow one part down through its levels until its text runs out. Then return to level 0 and open the next part. A reader follows one aspect to its depth before meeting the next.
- **Continuity:** The part being opened keeps its exact label in the parent diagram, and the child diagram's caption begins with that exact label. A caption that does not start with the label leaves the reader lost. Example: `**Diagram: Order Service splits intake from fulfilment**`.
- **Zoom one part per diagram:** A level-1 diagram opens one node. Opening three nodes at once is three diagrams.
- **Stop rule:** Stop opening when the source text gives no more structure, or when the next level would only restate one node. Do not invent depth.
- **Fit the size:** A concept that fits in one diagram of at most 10 nodes stays one diagram. A ladder of one rung is a diagram.
- **Sweep mode:** Headings already form levels. An H1 or H2 diagram is the wide view of its section, and deeper headings zoom into their parts.

---

## 4. Diagram Principles

- **One message:** A diagram carries one insight, and that insight is its caption. A passage with several insights gets several diagrams.
- **Caption test:** The caption has one subject and one relation. A caption that needs "while", "whereas", or "but" holds two insights: split it into two diagrams, or state the one relation that joins both halves ("A customer's plan decides the support channel").
- **Connected:** A flowchart is one connected structure. Groups that the text compares, pairs, or contrasts connect through a hub node, a labelled edge, or one named outer box.
- **Faithful structure:** Edges and layout carry only relations the source states. Draw a tree only for a stated hierarchy; peers point at the same target or share one box; a pool that serves several groups is one node with an edge to each.
- **Simplicity:** Every node advances the message. Cut any node that does not. Use at most 10 nodes. When the content needs more, build a ladder (Section 3) instead of cramming.
- **Size:** Each diagram renders inside 1200 by 1000 pixels and is no more than 3 times wider than tall, or tall than wide. A long chain in `LR` becomes a wide strip that readers squint at. Use `TD`, or split the chain into a ladder. The helper warns above these limits.
- **Independence:** A reader who sees only the diagram understands it. Name actors, states, and systems in full inside the labels, because inserted blocks carry no explanatory prose.
- **Consistency:** Use one term per concept, one class meaning per color, and the direction convention of Section 6 across every diagram in the answer or document.
- **Grounding:** Every node and edge traces to the source: the document, the code or files the user pointed at, or the user's own description. Mark a necessary bridging assumption with `[Inferred]` in its label.
- **Coverage (sweep only):** Every heading (H1-H6) has at least one diagram, and no content is skipped.
  - A thin section gets a small diagram (2-4 nodes) of what its text states.
  - A section with no text of its own diagrams the relationship between its title and its subsections.

---

## 5. Default Structures

Pick the structure from the content type. Each is one connected structure.

| Content                  | Structure                                                                                   |
| :----------------------- | :------------------------------------------------------------------------------------------ |
| Comparison, alternatives | Hub: a root naming the thing compared, one edge per option labelled with the condition.     |
| Lookup of pairs          | Two named column boxes (one per kind), one labelled edge per pair.                          |
| Flat team, peers         | Peers point at the shared target, or sit in one box with one edge. Use `LR`, never a tree.  |
| Flow                     | One `LR` chain from source to consumer, with verbs on the edges.                            |
| Before and after         | Hub with `old` and `new` edges, or two named boxes joined by a labelled "replaced by" edge. |
| System with many parts   | A zoom ladder (Section 3): overview first, then one part per diagram.                       |

Reuse the passage's own verbs and figures in labels.

## 6. Syntax Rules

- **Labels:** Put every flowchart node label and edge label in double quotes. Sequence message text stays unquoted, because quotes print literally there. Write plain text: no emojis or decorative symbols, and a hyphen in place of parentheses (`"Request - data"`).
- **Line breaks:** Use `<br/>` for multi-line labels and keep each line brief (2-6 words). To separate a title from detail, use `━━━`, the only permitted symbol: `"Title<br/>━━━<br/>Detail"`.
- **Edge labels:** Put the label after the arrow operator in pipe form: `A -->|"calls"| B`.
- **Subgraphs:** Use at most 3 per diagram. Declare an identifier plus a quoted title, and begin the body with a direction: `subgraph SvcId ["Service Tier"]` then `direction TB`.
- **Direction:** Arrows point from provider, cause, or earlier step to consumer, effect, or later step, with sources on the left (`LR`) or on top (`TD`). `RL` and `BT` are not used.
  - `LR`: pipelines of up to 5 boxes, comparisons, before-to-after, flat peers.
  - `TD`: stated multi-level hierarchies, decision trees, lifecycles. A chain of more than 6 boxes splits into a ladder.
- **Titles:** The caption carries the title. Leave frontmatter titles out of the fence.

---

## 7. Styling

Color carries the tier. Every node is a plain box, because other shapes render at uneven sizes and make diagrams look odd.

- **Plain boxes only:** Draw every flowchart node as `A["Label"]`. Never use stadium, cylinder, hexagon, subroutine, circle, diamond, or any other node shape. A decision is a box whose label asks the question.
- **Classes:** In flowcharts and `stateDiagram-v2`, assign every node one class from the theme block (Appendix B) by logical tier:

  | Class     | Tier                                                |
  | :-------- | :-------------------------------------------------- |
  | `c1`      | Ingress, client, entrypoint, primary flow           |
  | `c2`      | Compute, internal services, transforms, core engine |
  | `c3`      | Persistence, data stores, state, caches             |
  | `c4`      | Messaging, queues, streaming, decision gates        |
  | `c5`      | External systems, third parties, egress, boundaries |
  | `default` | Uncategorized or utility nodes                      |

- **Theme:** Paste the Theme A block (the default) at the top of each flowchart, or the theme the user names. In `stateDiagram-v2`, declare only the `c1`-`c5` classes in use and omit `classDef default`, which fails to compile.
- **Other grammars:** Sequence diagrams and the remaining grammars use native styling without classes.
- **Host colors:** Leave text and connector colors to the host theme. `classDef` and `style` carry fill and stroke only, with no `color:` and no `linkStyle`, so contrast holds in light and dark editors.
- **Subgraph boundary:** `style <id> fill:<hex>,stroke:<hex>,stroke-width:1px,stroke-dasharray:4 4`, with the values from the active theme.

---

## 8. Procedure

### Ad hoc mode

1. **Frame:** State the one thing the reader must understand. Count the parts the source names. If the count exceeds 10 or the parts have internal structure, plan a ladder: list each level as `Level | Opens which part | Insight`.
2. **Build:** Write each diagram to Sections 4-7. Reread it against its caption and delete nodes that do not carry it.
3. **Verify:** Write the diagrams to a temporary Markdown file and run the batch helper with `--png <temp_dir>`. Fix every failure and warning, then rerun until the exit code is `0`. If a grammar still fails to compile, redraw the same insight as a flowchart.
4. **Look:** View each `diagram-N.png` one at a time, never several at once and never a long page.
   - Confirm the picture states its caption.
   - Fail a diagram when text is clipped, text overlaps a box or another label, a line or border runs through a label, the layout sprawls, or the flow reads backwards (right to left or bottom to top).
   - A label or container title that only touches a border is cramped: shorten it.
   - Redraw any diagram that fails. When you cannot view images, report the visual check as not performed.
5. **Place:** Put each caption and fence where the reader meets the passage it explains. Return the response of Section 2.

### Sweep mode

1. **Map:** List every heading outside fenced code, with the text under it. Note which sections already contain Mermaid diagrams; those stay untouched, and a heading without one still gets one.
2. **Plan:** Write the coverage table, one row per diagram. Every heading appears in at least one row. Pick each grammar from Appendix A. Where a section needs a ladder, give its rows a level number.

   | Heading | Insight (becomes the caption) | Grammar | Level | Placement |
   | :------ | :---------------------------- | :------ | :---- | :-------- |

3. **Build:** Write each diagram to Sections 4-7. Reread it against its insight and delete nodes that do not carry it.
4. **Verify:** Copy the document to a temporary location, add all blocks to the copy, and compile once with the batch helper and `--png <temp_dir>`.
   - The helper names the failing diagram by its position in the document; fix it and recompile until the exit code is `0`.
   - Treat warnings as defects and clear them too (`--strict` fails on them).
   - If a grammar still fails to compile, redraw the same insight as a flowchart.
   - View each `diagram-N.png` one at a time, never several at once: labels readable, nothing clipped or overlapping, the picture states its caption. Redraw any that fail.
5. **Apply:** Keep the original bytes and the insertion boundaries. Write the verified candidate to the source through a path that preserves bytes, then read the saved file after hooks and formatters finish.
6. **Check the saved result:** Remove only the inserted blocks from a comparison copy and compare the remaining bytes with the original. Confirm every heading has a diagram in the saved file. A successful tool call or compilation does not establish text preservation.
7. **Formatting conflict:** When post-processing changed existing text, restore the original bytes through a byte-preserving write and verify the restoration. Deliver the candidate through that path or as a separate artifact. Hooks, formatter settings, and ignore comments stay as they are, because changing them exceeds this contract. When preservation cannot be verified, report the conflict and the actual saved state.

### Verification helpers

The scripts live in `scripts/` beside this `SKILL.md`. Resolve `<skill_dir>` to this skill's folder (`skills/mermaid-architect` in this checkout, or `mermaid-architect` inside the installed skills directory).

- Document batch: `python3 <skill_dir>/scripts/verify-markdown.py <document.md> --png <temp_dir>`; `--png` writes one image per diagram for the visual check.
- Single diagram: `<skill_dir>/scripts/verify-mmdc.sh <diagram.mmd>`
- Provisioning: the helper needs `@mermaid-js/mermaid-cli@12.0.0` and never downloads during verification. In this checkout, run `npm ci` at the repository root. For a separate install, place that exact version in the skill folder or on `PATH`. `COHERENT_MMDC_BIN` selects an explicit executable, and `COHERENT_PUPPETEER_CONFIG` passes a Puppeteer configuration file (for example `--no-sandbox` on a CI runner).
- Structure checks run before rendering: a flowchart is one connected structure, stays within 10 nodes and 3 subgraphs, and does not use `RL` or `BT`. Warnings cover compound captions, quoted sequence messages, and diagrams that render oversize or as a thin strip.
- Exit codes: `0` compiled (or the document has no Mermaid fences), `1` invalid syntax or structure, `2` verification could not run (missing tooling or browser dependencies). Report exit `2` as an unverified result. Each renderer call has a timeout, and temporary files are removed.

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
| Taxonomy, concept breakdown           | Mindmap          | `mindmap`                         | Only on request; it ignores the theme and implies a tree |
| User experience, journey              | User Journey     | `journey`                         | Onboarding and step-by-step flows with satisfaction      |
| Tradeoffs, 2x2 matrix                 | Quadrant         | `quadrantChart`                   | Risk versus value, priority matrices                     |
| Binary protocol, header layout        | Packet           | `packet-beta`                     | Network headers (IP/TCP), binary file structures         |

When the user wants nested boundaries, a dense multi-component architecture, or a precise layout that these grammars cannot give, say that d2-architect fits that job and let the user decide.

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
