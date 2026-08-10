# Visualization Generator

## Purpose

Use this approach when transforming written or structured content into comprehensive sets of clear visualizations. Visualize every major concept using representations that best reveal structure, behavior, comparison, magnitude, or relationship.

## Audience and Design Priorities

The user relies heavily on visuals for comprehension and attention. Visual coverage is a central comprehension aid.

- One visualization communicates one primary insight.
- Use several small, focused visuals, each carrying one primary insight.
- Visualize every major concept and incorporate its supporting sentences and minor details into the relevant visual set.
- Use consistent names, direction, colors, and symbols across related visuals.
- Explain how to read each visualization.
- Pair a detailed visual with a simpler overview when complexity requires both.

## Visualization Selection Guide

| Information relationship | Preferred formats |
| --- | --- |
| Linear process | Mermaid flowchart, PlantUML activity diagram, D2, or ASCII flow |
| Actor or service interaction | Mermaid or PlantUML sequence diagram |
| State and transitions | State diagram or transition table |
| Decision logic | Decision tree, flowchart, or decision table |
| Hierarchy or taxonomy | Tree, mind map, Graphviz, or indented ASCII tree |
| System architecture | C4-style diagram, Mermaid, PlantUML, D2, Graphviz, or Structurizr |
| Dependencies or networks | Graphviz, Mermaid, D2, or node-link graph |
| Data model | ER diagram, schema diagram, or relationship table |
| Exact comparison | Markdown table, matrix, heatmap, or small multiples |
| Time | Timeline, Gantt chart, sequence diagram, or line chart |
| Quantitative distribution or trend | Matplotlib, Seaborn, Plotly, Vega-Lite, histogram, scatter plot, or line chart |
| Spatial arrangement | Annotated image, SVG, map, coordinate plot, or ASCII sketch |
| Formula or transformation | Annotated equation, worked derivation, or pipeline diagram |
| UI or document layout | Wireframe, box diagram, annotated screenshot, or HTML/SVG mockup |

Choose formats available in the current environment. Provide a Mermaid, Markdown, or ASCII fallback when the preferred format is unavailable.

## Workflow

### 1. Map the Content

- Read the complete source before drawing.
- Identify the major concepts, their relationships, and their dependency order.
- Distinguish conceptual, structural, behavioral, temporal, comparative, quantitative, and spatial information.
- Identify repeated concepts that should share one canonical visualization.

**Visible output — Coverage Plan:**

| Major concept | Insight to communicate | Chosen format | Placement | Reason |
| --- | --- | --- | --- | --- |

Every major concept must appear in this plan.

### 2. Design Progressive Views

When a concept is complex, use progressive disclosure:

1. **Overview:** The minimal mental map
2. **Structure:** Components and relationships
3. **Behavior:** Flow, sequence, or state changes
4. **Detail:** Data, rules, exceptions, or quantitative evidence

Use the subset of views required to communicate the concept completely.

### 3. Create the Visuals

General rules:

- Keep labels brief and use terminology consistent with the source.
- Use nouns for entities and verbs for relationships where applicable.
- Prefer left-to-right flow for sequences and top-to-bottom flow for hierarchies.
- Limit visual clutter. If a visual becomes difficult to scan, split it.
- Use captions that state the visual's primary insight.
- Provide a one- or two-sentence reading guide below each visual.
- Use relationships and values grounded in the source.

For diagram code:

- Use stable, simple identifiers.
- Quote labels when syntax requires it.
- Escape parser-sensitive characters correctly.
- Keep styling separate from content when the language supports it.

#### Mermaid

- Use a fenced code block with the `mermaid` language tag.
- Use the diagram type that matches the relationship: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `classDiagram`, `mindmap`, `timeline`, or `gantt`.
- Keep node IDs simple and stable; keep displayed labels brief.
- Use nouns for node labels and verbs for labeled relationships when applicable.
- Quote labels containing punctuation or syntax-sensitive characters.
- Use `<br/>` for short line breaks that materially improve readability.
- Keep subgraphs limited and give each one a clear direction.
- Define reusable `classDef` styles and assign a class to every node when custom styling is used.
- Add a title using supported frontmatter or place a Markdown caption immediately above the diagram.
- Render or parse-check the final Mermaid source when tools are available.

#### Graphviz and D2

- Set the graph direction deliberately, such as `rankdir=LR` or the D2 direction equivalent.
- Use clusters or containers only for meaningful boundaries.
- Keep identifiers separate from human-readable labels.
- Define shared node and edge styles once.
- Export SVG when possible so text remains sharp and searchable.

#### PlantUML

- Use the smallest diagram type that communicates the concept.
- Apply a consistent theme and direction.
- Use notes sparingly; move long explanations into surrounding Markdown.
- Validate the complete `@startuml` to `@enduml` block.

#### ASCII

- Keep line widths suitable for the target document.
- Use a legend for symbols that require explanation.
- Test alignment in a monospace code block.
- Use ASCII as a dependable fallback and use richer primary visuals when rendering tools are available.

For quantitative charts:

- Label axes, units, series, and sources.
- Use honest scales and meaningful baselines.
- Show uncertainty or missing data.
- Use two-dimensional forms with accurate visual proportions.

### 4. Style Accessibly

- Use readable contrast together with labels, shapes, line styles, or patterns.
- Combine color with labels, shapes, line styles, or patterns.
- Keep a consistent semantic palette across the visual set.
- Use plain text labels, shapes, lines, and patterns as structural symbols.
- Provide alt text or a textual interpretation for image-based output.

Suggested semantic palette:

| Meaning | Fill | Stroke |
| --- | --- | --- |
| Primary actor or concept | `#e3f2fd` | `#0066cc` |
| Normal operation or success | `#e5ffe5` | `#388e3c` |
| Decision or attention | `#fff9c4` | `#b26a00` |
| System or data component | `#d9f3ef` | `#167c6b` |
| Risk, failure, or blocker | `#ffe5e5` | `#c0392b` |
| Context or inactive element | `#f5f5f5` | `#6b7280` |

### 5. Validate

For every visual, verify:

- It covers the intended major concept.
- It communicates one primary insight.
- Labels and relationships match the source.
- It is readable at the expected display size.
- Syntax renders successfully when rendering tools are available.
- Colors and symbols remain understandable in grayscale.
- A fallback accompanies every primary format with uncertain rendering support.

End with a coverage check that maps every major concept to at least one completed visual.

## Output

Return:

1. Coverage plan
2. Visualizations in source order
3. Reading guide for each visualization
4. Coverage and validation summary

When asked to insert visuals into an existing document, preserve the surrounding content and place each visual immediately after the section it clarifies.
