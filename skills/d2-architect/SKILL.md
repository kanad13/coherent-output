---
name: d2-architect
description: Gives every heading of a technical document a verified D2 diagram, laid out with TALA and inserted as a fenced d2 block without altering existing text. Use only when the user explicitly asks for D2 diagrams. Do not use for Mermaid or generic diagram requests, for producing image files, or for modifying surrounding prose.
---

# D2 Diagram Architect

Add compilable D2 diagrams to a document by insertion only. Every pre-existing byte of the source stays unchanged. Every heading (H1-H6) receives at least one diagram, and every diagram delivers one insight. The user reviews the result and keeps or drops each diagram, so aim for full coverage, number every diagram in the plan, and never prune silently. The user's Markdown previewer renders the fences; no image files are created.

---

## 1. Output Contract

- **Insertion only:** Leave existing headings, paragraphs, tables, and code fences unmodified, unreordered, and unreformatted.
- **Insertion block:** Each insertion is exactly two parts:
  1. A caption line, `**Diagram: <Insight>**`, written as a statement of the diagram's single message.
  2. One fenced `d2` block that starts with the standard header from Section 4.
- **Caption format:** Write the caption in bold text. Headings stay out of captions so the document's table of contents stays intact. Prose summaries and transitions stay out of the document.
- **Placement:** Insert at a block boundary right after the passage that introduces the concept. When a heading has no text before its first subheading, insert directly under the heading.
- **Response:** Return three sections: **A** the coverage plan table, **B** the updated document (or the verified candidate when a formatting conflict blocks saving), **C** verification results: the helper's exit code, any warnings, the contact-sheet path, and what you saw in it.
- **Judge:** The user decides what stays. A thin section still gets its small diagram; mark it `Thin` in the plan so the user can drop it quickly.

---

## 2. Diagram Principles

- **One message:** A diagram carries one insight, and that insight is its caption. A passage with several insights gets several diagrams.
- **Caption test:** The caption has one subject and one relation. A caption that needs "while", "whereas", or "but" holds two insights: split it into two diagrams, or state the one relation that joins both halves.
- **Connected:** A diagram is one connected structure. Groups that the text compares, pairs, or contrasts connect through a hub node, a labelled edge, or one named outer container.
- **Faithful structure:** Edges and nesting carry only relations the text states. Nest a container only for stated membership. Draw a tree only for a stated hierarchy. A pool that serves several groups is one node with an edge to each.
- **Scale:** D2 has no node limit here; use as many nodes as the passage states. Group peers in a container before listing a dozen loose nodes. A passage that describes one whole system with more than about 20 components gets an overview diagram first, with each subsystem as one container or node and edges between subsystems, then detail diagrams that each carry one insight. A single 45-node picture compiles in under a second but is unreadable. Split a diagram when it holds two insights or when a reader cannot take it in at a glance, but never split below an insight: a diagram of one edge belongs inside its neighbor. TALA slows on very large graphs, and the helper warns above 40 nodes.
- **Independence:** A reader who sees only the diagram understands it. Name actors, states, and systems in full inside the labels.
- **Consistency:** Use one term per concept, one shape per kind of thing, and the same edge conventions across every diagram in the document.
- **Coverage:** Every heading (H1-H6) has at least one diagram, and no content is skipped.
  - A thin section gets a small diagram (2-4 nodes) of what its text states.
  - A section with no text of its own diagrams the relationship between its title and its subsections.
  - A heading with no text and no subsections gets one node that carries its title, and nothing invented.
- **Grounding:** Every node, edge, table column, and attribute traces to the source text, and an edge label or a condition the text does not state counts as invented. Never invent content. Mark `[Inferred]` only on an element a diagram needs to stay connected or to name a relation the text implies, and quote the label. Use it sparingly; a diagram full of `[Inferred]` has strayed from its passage. When the text names no column for a foreign key, label the edge instead of inventing a column.
- **Use D2's strengths:** Express hierarchy with nested containers, schemas with `sql_table`, types with `class`, and message protocols with `sequence_diagram`.

---

## 3. Default Patterns

Pick the pattern from the content type. Each is one connected structure.

| Content                     | Pattern                                                                                                     |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------- |
| System architecture         | Nested containers for stated boundaries, one shape per tier, labelled edges between tiers.                  |
| Flow, pipeline              | One chain from source to consumer with verbs on the edges.                                                  |
| Message protocol, handshake | `shape: sequence_diagram` with actors in order of first appearance.                                         |
| Database schema             | `shape: sql_table` per entity when the text names columns, otherwise plain boxes; one edge per foreign key. |
| Class hierarchy, types      | `shape: class` per type, edges for stated inheritance or composition.                                       |
| State or lifecycle          | One node per state, labelled edges for transitions, `shape: circle` for a start state.                      |
| Comparison, alternatives    | Hub: a root naming the thing compared, one edge per option labelled with the condition.                     |
| Before and after            | Two named containers joined by a labelled "replaced by" edge.                                               |
| Quantities, timelines       | D2 has no chart grammar. Diagram the structure the text states (stages, owners, groupings).                 |

Reuse the passage's own verbs and figures in labels.

---

## 4. Syntax and Style Rules

### Standard header

Start every block with this header, unchanged apart from a theme the user names:

```text
vars: {
  d2-config: {
    layout-engine: tala
    pad: 24
    theme-id: 0
    dark-theme-id: 200
  }
}
```

- **Layout:** Every block uses TALA. The block carries its own setting, so a previewer that honors D2 configuration renders the same layout. Never write another engine.
- **Theme:** `theme-id: 0` with `dark-theme-id: 200` keeps text readable in light and dark previews.
- **Padding:** `pad: 24` trims D2's 100-pixel default margin, which is too large inside a document.
- **Nothing else:** Leave out `sketch`, `center`, `theme-overrides`, and `dark-theme-overrides`. The house palette is applied by the renderer, not written into blocks.

### Shapes carry the tier, the theme carries the color

Leave `fill` and `stroke` at their theme defaults. A fixed color breaks text contrast in the other color scheme, and D2 colors accept only named or six-digit hex values (no alpha).

| Kind of node                   | Shape                                      |
| :----------------------------- | :----------------------------------------- |
| Person or actor                | `shape: person`                            |
| Service or process             | Default rectangle                          |
| Data store                     | `shape: cylinder`                          |
| Queue or stream                | `shape: queue`                             |
| External system or third party | `shape: cloud` with `style.stroke-dash: 4` |
| Decision                       | `shape: diamond`                           |
| Document or artifact           | `shape: document`                          |

### House palette

The palette lives in `assets/house-palette.d2` beside this `SKILL.md`. A previewer or the helper prepends it to a block, and D2 merges the repeated `vars` blocks, so the block's own configuration still governs the layout. The palette recolors D2's named theme slots, so each shape keeps its tint in light and dark: databases violet, documents green, people blue, queues and decisions slate, and containers a blue ramp from outer to inner. Pass it to the helper with `--palette` to see the house look in the contact sheet.

### Names, labels, and edges

- **Keys:** Use lowercase snake_case identifiers and put the display text after the colon: `order_api: Orders API`.
- **Reserved words:** Keywords such as `class`, `classes`, `style`, `label`, `shape`, `icon`, `link`, `near`, `direction`, `width`, `height`, `top`, `left`, `constraint`, `vars`, `steps`, `layers`, and `scenarios` are never node keys. Pick another identifier.
- **Dots:** A dot in a key creates a container path. Quote any key or reference that holds a literal dot.
- **Quoting:** Double-quote any label that contains `:`, `;`, `#`, `{`, `}`, `|`, `&`, `[`, or a leading `-`. Single-quote a label that contains `$`, because D2 reads `$` in a double-quoted label as a substitution and fails to compile.
- **Edges:** Write `a -> b: verb phrase`. Arrows point from provider, cause, or earlier step to consumer, effect, or later step. Reserve dashed edges (`style.stroke-dash: 4`) for asynchronous, optional, or `[Inferred]` relations.
- **Containers:** Write `group: Title { ... }`. Declare edges that cross containers at the root with full dotted paths.
- **Edge labels:** Keep each label to 1-4 words. Long labels collide with lines and container borders. Number steps only when the text numbers them.
- **Self-contained:** Use no remote icons, images, links, or imports. The helper renders offline, and a block that needs the network fails.
- **Direction:** Leave direction to TALA unless the text states left-to-right order, then add `direction: right` and confirm the result in the contact sheet.

---

## 5. Procedure

1. **Map:** List every heading outside fenced code, with the text under it. Note which sections already contain D2 diagrams; those stay untouched, and a heading without one still gets one.
2. **Plan:** Write the coverage table, one numbered row per diagram. Every heading appears in at least one row.

   | #   | Heading | Insight (becomes the caption) | Pattern | Strength | Placement |
   | :-- | :------ | :---------------------------- | :------ | :------- | :-------- |

   `Strength` is `Strong` when the text states a clear structure and `Thin` when the diagram restates little.

3. **Build:** Write each diagram to Sections 2-4. Reread it against its insight and delete nodes that do not carry it. Read each caption aloud as a sentence and fix its grammar before verifying.
4. **Verify:** Copy the document to a temporary location, add all blocks to the copy, and run the helper with `--sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`. Fix every reported error and warning, then rerun until the exit code is `0`. Then open the contact sheet it wrote and look at it. View every diagram, not a sample. For each one, confirm that labels are readable and unclipped, edges do not run through labels, containers hold exactly their members, and the picture states its caption. Redraw or simplify any diagram that fails. If the browser tool cannot open a local file, serve the folder (`python3 -m http.server -d <temp_dir> <port>`) and open the address. When you cannot view images, report the visual check as not performed.
5. **Apply:** Keep the original bytes and the insertion boundaries, including the file's line endings: a CRLF file stays CRLF, so write the inserted lines with CRLF too, and keep the trailing-newline state. Read and write in binary mode or with `newline=""`. Write the verified candidate to the source through a path that preserves bytes, then read the saved file after hooks and formatters finish.
6. **Check the saved result:** Remove only the inserted blocks from a comparison copy and compare the remaining bytes with the original, with `cmp` on the real files, not on normalized text. Confirm every heading has a diagram in the saved file. A successful tool call or compilation does not establish text preservation.
7. **Formatting conflict:** When post-processing changed existing text, restore the original bytes through a byte-preserving write and verify the restoration. Deliver the candidate through that path or as a separate artifact. Hooks, formatter settings, and ignore comments stay as they are, because changing them exceeds this contract. When preservation cannot be verified, report the conflict and the actual saved state.

### Verification helper

The script lives in `scripts/` beside this `SKILL.md`. Resolve `<skill_dir>` to this skill's folder (`skills/d2-architect` in this checkout, or `d2-architect` inside the installed skills directory).

- Document: `python3 <skill_dir>/scripts/verify-d2.py <document.md> --sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`
- Raw diagram: `python3 <skill_dir>/scripts/verify-d2.py --diagram <diagram.d2> --sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`
- Provisioning: the helper needs D2 v0.9.0 or later, the first release that bundles TALA. It uses `COHERENT_D2_BIN` when set, then a `d2` on `PATH`, then the Docker image `d2lang/d2:v0.9.0`, run without network access. It never downloads during verification; provision once with `docker pull d2lang/d2:v0.9.0` or `brew install d2`.
- The helper renders each block without a layout flag, so the block's own `layout-engine` governs.
- Checks before the report: the standard header names TALA, each block compiles, each diagram is one connected structure, and warnings cover compound captions, color overrides, and diagrams above 40 nodes (`--strict` fails on them).
- Palette: `--palette` prepends the file to every render, and error line numbers still point into your block.
- Contact sheet: an HTML page with each diagram beside its heading, caption, and source, plus the rendered SVG files.
- Exit codes: `0` compiled (or the document has no D2 fences), `1` invalid syntax, header, or structure, `2` verification could not run (missing D2 or Docker). Report exit `2` as an unverified result. Each render has a timeout, and temporary files are removed.
