---
name: d2-architect
description: Draws a set of verified D2 diagrams, laid out with TALA, for one concept, plan, or architecture the user names. It draws a 30,000-foot overview first, then zooms in one part at a time, and offers extra views so the user picks what to keep. Use only when the user explicitly asks for D2 or invokes this skill. Do not use for default or unspecified diagram requests (use mermaid-architect), for giving every heading of a document a diagram, for icons or images, or for producing image files.
---

# D2 Diagram Architect

Turn one concept, plan, or architecture that the user names into a numbered set of D2 diagrams. The set starts at 30,000 feet and zooms in one part at a time. It also offers extra views, because the user decides which diagrams to keep. Every diagram uses TALA, carries one insight, and is compiled and looked at before it reaches the user.

Mermaid is the default diagram tool. D2 is the tool the user reaches for when the picture needs what Mermaid cannot give: nested boundaries, a dense architecture, a schema, or a class model, with a layout that stays readable.

---

## 1. Activation and Scope

- **Explicit only:** Run when the user asks for D2 or invokes this skill. A generic "draw a diagram" request goes to mermaid-architect.
- **Targeted, not a sweep:** The user names a scenario, concept, plan, or architecture. Draw that. Do not walk a whole document heading by heading; that job belongs to mermaid-architect.
- **The user's request for D2 wins:** When the user asks for D2 for a flow, state, or comparison, draw it in D2. Section 4 lists where D2 is strongest.
- **Missing subject:** When the user invokes the skill without a subject, ask what to draw.

---

## 2. Output Contract

- **A set, not one picture:** Deliver the overview, the zoom ladder (Section 3), and extra views. More diagrams are welcome, as long as each carries its own insight. The user is the judge: number every diagram, mark nothing as dropped, and never prune silently.
- **Insertion block:** Each diagram is exactly two parts:
  1. A caption line, `**Diagram <number>: <Insight>**`, written as a statement of the diagram's single message.
  2. One fenced `d2` block that starts with the standard header from Section 5.
- **Where it goes:** A new Markdown file named for the subject (for example `payments-architecture-diagrams.md`) in the folder the user names, or the current folder. The file holds the diagrams in reading order. Headings, if any, group levels; they are not required.
- **Existing document:** Only when the user asks for diagrams inside an existing file, insert at block boundaries and leave every pre-existing byte unchanged (Section 6, steps 6-8).
- **Self-contained:** Diagrams contain no icons, images, links, tooltips, or imports. No image files are delivered; the user's previewer renders the fences. The review images from the helper go in a temporary folder outside the deliverable folder, never beside the Markdown file.
- **Response:** Return three sections: **A** the numbered plan table, **B** the file location (or the updated document), **C** verification results: the helper's exit code, any warnings, the contact-sheet path, and what you saw in it.

---

## 3. Zoom Ladder and Extra Views

### Ladder

| Level | Shows                                                     | Size                    |
| :---- | :-------------------------------------------------------- | :---------------------- |
| 0     | The whole concept from 30,000 feet: its major parts only. | 3-7 nodes or containers |
| 1     | One part of level 0, opened up.                           | Up to 15 nodes          |
| 2+    | One part of the previous level, opened up the same way.   | Up to 15 nodes          |

- **Order of drawing:** Draw level 0 first. Then follow one part down through its levels until the subject runs out. Then return to level 0 and open the next part.
- **Continuity:** A container or node being opened keeps its exact label in the parent diagram. In the child it becomes the outer container, and the caption begins with that label, for example `**Diagram 2: Storefront splits search from identity**`. A zoom caption that never names the opened part leaves the reader lost.
- **One part per diagram:** A level-1 diagram opens one part. Opening three parts at once makes three diagrams.
- **Node count:** Count leaf nodes. Containers group them and do not count. A reader takes in a ladder diagram at a glance.
- **Size:** Each diagram renders inside 1200 by 1000 pixels. A `Full picture` diagram may reach 1800 by 1800. The helper warns above these limits.
- **Open generously:** Open every part that has two or more stated internals or relations, even when the diagram is small. The user prunes, so more diagrams is better than fewer. Do not skip a zoom because it "would restate" the parent; skip it only when the subject states nothing inside the part.
- **Stop rule:** Stop opening a part when the subject states no more structure there. A diagram of one edge belongs inside its neighbor.

### Extra views

After the ladder, add views that show the same subject through a different lens. Each lens is its own diagram with its own insight. Useful lenses:

- **Boundaries:** which parts sit inside which trust, ownership, or deployment boundary.
- **Data path:** how one request or record travels through the parts.
- **Failure path:** what happens to the neighbors when one part fails.
- **Lifecycle or change:** how the structure grows or is replaced over time.
- **Data model:** the schema behind the architecture.

Offer a lens only when the subject supports it. A lens that needs invented content is skipped, and the plan says so.

### Full picture

One all-in-one diagram of the whole subject is allowed after the ladder. It is optional: when it renders above 1800 by 1800 pixels, or sprawls with long edges crossing containers, leave it out rather than ship it. Put `Full picture` in its caption so it reads as a convenience, not as the main explanation. The verification helper warns above 40 nodes for it and above 15 for every other diagram.

---

## 4. Diagram Principles and Patterns

- **One message:** A diagram carries one insight, and that insight is its caption. A caption that needs "while", "whereas", or "but" holds two insights: split it.
- **Connected:** A diagram is one connected structure. Groups that the subject compares, pairs, or contrasts connect through a hub node, a labelled edge, or one named outer container.
- **Faithful structure:** Edges and nesting carry only relations the subject states. Nest a container only for stated membership. Draw a tree only for a stated hierarchy.
- **Independence:** A reader who sees only the diagram understands it. Name actors, states, and systems in full inside the labels.
- **Consistency:** Use one term per concept, one box style, and the same edge conventions across every diagram in the set.
- **Grounding:** Every node, edge, and attribute traces to the user's description, the files or code the user named, or a source they pointed at. Never invent content. Mark `[Inferred]` only on an element a diagram needs to stay connected or to name a relation the subject implies, and quote the label. List every inference in the plan table so the user can reject it.
- **Use D2's strengths:**

  | Content                  | Pattern                                                                                                        |
  | :----------------------- | :------------------------------------------------------------------------------------------------------------- |
  | System architecture      | Nested containers for stated boundaries, plain boxes, labelled edges between tiers.                            |
  | Trust or ownership zones | One container per zone, edges that cross zones declared at the root.                                           |
  | Database schema          | `shape: sql_table` per entity when the subject names columns, otherwise plain boxes; one edge per foreign key. |
  | Class hierarchy, types   | `shape: class` per type, edges for stated inheritance or composition.                                          |
  | Message protocol         | `shape: sequence_diagram` with actors in order of first appearance. Use when the user asks for it in D2.       |
  | Flow, state, comparison  | A plain chain, a node per state, or a hub. Use when the user asks for it in D2.                                |

Reuse the subject's own verbs and figures in labels.

---

## 5. Syntax and Style Rules

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

### No icons, images, or links

- Never write `icon`, `shape: image`, `link`, `tooltip`, or an import. The user does not use them, and the offline renderer rejects remote assets.
- Boxes, containers, and labels carry all meaning.

### Plain boxes only

Draw every node as the default rectangle. Never write `shape:` with another value (`cylinder`, `queue`, `cloud`, `diamond`, `person`, `document`, `circle`, and the rest): they render at uneven sizes and make diagrams look odd. The only `shape:` values allowed are `sql_table`, `class`, and `sequence_diagram`, and only when the subject is a schema, a class model, or a message protocol.

- **Meaning comes from containers and labels:** A data store is a box labelled "Orders database". An external system is a box with `style.stroke-dash: 4` inside no container of the platform. A decision is a box whose label asks the question.
- **Color:** Leave `fill` and `stroke` at their theme defaults. A fixed color breaks text contrast in the other color scheme, and D2 colors accept only named or six-digit hex values (no alpha).
- **Allowed emphasis:** `style.stroke-dash` and `style.opacity` only.

### Classes and legends

- **Classes:** When three or more nodes share a style, declare a `classes` entry once and assign `class:` to each node. Keep the class meaning identical across the set.
- **Legend:** When a diagram uses dashed edges or `[Inferred]` labels, add a small legend container with `near: bottom-center` that names each convention. Skip the legend when nothing needs explaining.

### House palette

The palette lives in `assets/house-palette.d2` beside this `SKILL.md`. A previewer or the helper prepends it to a block, and D2 merges the repeated `vars` blocks, so the block's own configuration still governs the layout. The palette recolors D2's named theme slots, so the boxes keep their tint in light and dark: containers get a blue ramp from outer to inner, and boxes, edges, and text get slate and blue. Pass it to the helper with `--palette`.

### Names, labels, and edges

- **Keys:** Use lowercase snake_case identifiers and put the display text after the colon: `order_api: Orders API`.
- **Reserved words:** Keywords such as `class`, `classes`, `style`, `label`, `shape`, `icon`, `link`, `near`, `direction`, `width`, `height`, `top`, `left`, `constraint`, `vars`, `steps`, `layers`, and `scenarios` are never node keys. Pick another identifier.
- **Dots:** A dot in a key creates a container path. Quote any key or reference that holds a literal dot.
- **Quoting:** Double-quote any label that contains `:`, `;`, `#`, `{`, `}`, `|`, `&`, `[`, or a leading `-`. Single-quote a label that contains `$`, because D2 reads `$` in a double-quoted label as a substitution and fails to compile.
- **Edges:** Write `a -> b: verb phrase`. Arrows point from provider, cause, or earlier step to consumer, effect, or later step. Reserve dashed edges (`style.stroke-dash: 4`) for asynchronous, optional, or `[Inferred]` relations.
- **Containers:** Write `group: Title { ... }`. Declare edges that cross containers at the root with full dotted paths.
- **Edge labels and titles:** Keep each edge label to 1-4 words and each container title short enough to clear its border. Long labels collide with lines and container borders. Never put `[Inferred]` in a container title; list inferred groupings in the plan table. Number steps only when the subject numbers them.
- **Boards:** Do not use `layers`, `scenarios`, or `steps`. A fenced block shows only the root board, so each ladder level is its own block.
- **Direction:** Arrows read left to right or top to bottom. Leave direction to TALA, but when it draws a chain bottom to top or right to left, add `direction: down` or `direction: right` and confirm the result in the diagram's image.

---

## 6. Procedure

1. **Frame:** State the subject in one sentence and list the parts it names. Ask the user only when the subject is missing or two readings would give different diagrams.
2. **Plan:** Write the numbered plan table. Every row is one diagram. Include the ladder rows, the extra views, and the optional full picture.

   | #   | Level or lens | Opens which part | Insight (becomes the caption) | Pattern | Inferences |
   | :-- | :------------ | :--------------- | :---------------------------- | :------ | :--------- |

3. **Build:** Write each diagram to Sections 4-5. Reread it against its insight and delete nodes that do not carry it. Read each caption aloud as a sentence and fix its grammar before verifying.
4. **Verify:** Write the set to the target file (or a temporary copy for an existing document) and run the helper with `--sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`. Fix every reported error and warning, then rerun until the exit code is `0`.
5. **Look:** The helper writes `diagram-N.png` beside the contact sheet. View each PNG one at a time, and view every diagram, not a sample. A long page of diagrams hides the ones below the fold; the contact sheet (`index.html`) is for the user.
   - For each diagram, confirm that containers hold exactly their members and the picture states its caption. Fail a diagram when text is clipped, text overlaps a box or another label, a line or border runs through a label, the layout sprawls, or the flow reads backwards (right to left or bottom to top). A label or container title that only touches a border is cramped: shorten it.
   - The PNG shows light mode. The SVG carries both themes, so check dark mode in a browser with `prefers-color-scheme: dark` emulated when one is available, and otherwise report it as unchecked.
   - Redraw or simplify any diagram that fails.
   - When you cannot view images, report the visual check as not performed.
6. **Apply (existing document only):** Keep the original bytes and the insertion boundaries, including the file's line endings: a CRLF file stays CRLF, so write the inserted lines with CRLF too, and keep the trailing-newline state. Read and write in binary mode or with `newline=""`. Write the verified candidate to the source through a path that preserves bytes, then read the saved file after hooks and formatters finish.
7. **Check the saved result (existing document only):** Remove only the inserted blocks from a comparison copy and compare the remaining bytes with the original, with `cmp` on the real files, not on normalized text.
8. **Formatting conflict (existing document only):** When post-processing changed existing text, restore the original bytes through a byte-preserving write and verify the restoration. Hooks, formatter settings, and ignore comments stay as they are. When preservation cannot be verified, report the conflict and the actual saved state.

### Verification helper

The script lives in `scripts/` beside this `SKILL.md`. Resolve `<skill_dir>` to this skill's folder (`skills/d2-architect` in this checkout, or `d2-architect` inside the installed skills directory).

- Document: `python3 <skill_dir>/scripts/verify-d2.py <document.md> --sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`
- Raw diagram: `python3 <skill_dir>/scripts/verify-d2.py --diagram <diagram.d2> --sheet <temp_dir> --palette <skill_dir>/assets/house-palette.d2`
- Renderer order: `COHERENT_D2_RENDERER_URL` (a running d2-renderer service, for example `http://localhost:8080`), then `COHERENT_D2_BIN`, then a `d2` on `PATH`, then the Docker image `d2lang/d2:v0.9.0` run without network access. D2 v0.9.0 or later bundles TALA. The helper never downloads during verification; provision once with `docker pull d2lang/d2:v0.9.0` or `brew install d2`.
- The helper renders each block without a layout flag, so the block's own `layout-engine` governs.
- Checks before the report: the header names TALA; no `icon`, link, tooltip, import, or `shape:` other than a box, `sql_table`, `class`, or `sequence_diagram`; each block compiles; each diagram is one connected structure. Warnings cover compound captions, color overrides, node count (above 15 leaf nodes, or above 40 for a `Full picture` diagram), and rendered size (above 1200 by 1000 pixels). `--strict` fails on warnings.
- Palette: `--palette` prepends the file to every render, and error line numbers still point into your block.
- Images: `--sheet` writes each diagram as `diagram-N.svg` and `diagram-N.png` (through `rsvg-convert`, `magick`, or a headless Chrome named by `COHERENT_CHROME_BIN`), plus an HTML contact sheet for the user. With no rasterizer, the helper says so and only the SVG files exist.
- Exit codes: `0` compiled (or the document has no D2 fences), `1` invalid syntax, header, content rule, or structure, `2` verification could not run (no renderer). Report exit `2` as an unverified result. Each render has a timeout, and temporary files are removed.
