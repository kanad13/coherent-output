# Visualization Generator

## Purpose

Transform written or structured content into a comprehensive set of clear visualizations. Every major concept must be visualized, using the representation that best reveals its structure, behavior, comparison, magnitude, or relationship.

## Audience and Design Priorities

The user relies heavily on visuals for comprehension and attention. Visual coverage is a functional requirement, not decoration.

- One visualization communicates one primary insight.
- Use several small visuals instead of one dense visual.
- Visualize every major concept, but not every sentence or minor detail.
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

Choose formats available in the current environment. If the preferred format cannot be rendered or embedded, provide a Mermaid, Markdown, or ASCII fallback.

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

Do not force all four views when fewer communicate the concept completely.

### 3. Create the Visuals

General rules:

- Keep labels brief and use terminology consistent with the source.
- Use nouns for entities and verbs for relationships where applicable.
- Prefer left-to-right flow for sequences and top-to-bottom flow for hierarchies.
- Limit visual clutter. If a visual becomes difficult to scan, split it.
- Use captions that state the insight, not merely the chart type.
- Provide a one- or two-sentence reading guide below each visual.
- Do not invent relationships or values absent from the source.

For diagram code:

- Use stable, simple identifiers.
- Quote labels when syntax requires it.
- Avoid parser-sensitive characters unless escaped correctly.
- Keep styling separate from content when the language supports it.

#### Mermaid

- Use a fenced code block with the `mermaid` language tag.
- Use the diagram type that matches the relationship: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `classDiagram`, `mindmap`, `timeline`, or `gantt`.
- Keep node IDs simple and stable; keep displayed labels brief.
- Use nouns for node labels and verbs for labeled relationships when applicable.
- Quote labels containing punctuation or syntax-sensitive characters.
- Use `<br/>` only when a short line break materially improves readability.
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
- Use a legend when symbols are not self-evident.
- Test alignment in a monospace code block.
- Prefer ASCII as a dependable fallback, not as an excuse to omit a better primary visual when rendering tools are available.

For quantitative charts:

- Label axes, units, series, and sources.
- Use honest scales and meaningful baselines.
- Show uncertainty or missing data.
- Avoid three-dimensional effects that distort comparison.

### 4. Style Accessibly

- Use readable contrast and do not rely on color alone.
- Combine color with labels, shapes, line styles, or patterns.
- Keep a consistent semantic palette across the visual set.
- Avoid emojis as structural symbols.
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
- A fallback is present when the primary format may not render.

End with a coverage check that maps every major concept to at least one completed visual.

## Output

Return:

1. Coverage plan
2. Visualizations in source order
3. Reading guide for each visualization
4. Coverage and validation summary

When asked to insert visuals into an existing document, preserve the surrounding content and place each visual immediately after the section it clarifies.
