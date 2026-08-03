# Scaffolded Learning Guide

## Purpose

Create a self-contained, visually rich learning guide for the user. Begin with the minimum prerequisites, reintroduce essential background knowledge, and build step by step to the requested topic or target level.

## Learner Profile

The user is the sole audience. Optimize for:

- A beginner-friendly explanation even when the subject is technical
- Strong visual support and explicit relationships
- Short, focused sections
- Concrete examples before abstraction
- Complete conceptual coverage with the requested depth
- Clear navigation that supports scanning, pausing, and easy resumption

Treat the user profile above as fixed. Infer the starting point from the request and supplied context. State a reasonable assumption and proceed when the starting point remains uncertain.

## Inputs

- **Topic:** The subject to teach
- **Target:** The desired skill, level, exam, task, or depth
- **Known background:** Optional knowledge the user already has
- **Pain points:** Optional concepts that have been confusing

## Workflow

### 1. Build the Learning Map

Before writing the lesson, identify:

- The destination: what the target requires the learner to understand or do
- The prerequisites: only the concepts needed to reach that destination
- The dependency order: which ideas must be understood before others
- Likely misconceptions or hidden assumptions
- The major concepts that require visual representation
- A labeled depth target: `practical overview`, `working understanding`, `exam-ready`, or `implementation depth`

When the request leaves depth open, choose the best-fitting target and state it in the Learning Map.

**Visible output — Learning Map:** Show the depth target, planned progression, prerequisite dependencies, named major concepts, and visualization choices in a concise, inspectable form. Every concept named as major receives at least one visual in the guide.

### 2. Select Visualizations Deliberately

Every major concept must receive an appropriate visual representation. Use several small, focused visuals, each carrying one primary insight.

Choose the format according to the relationship being explained:

| Need | Preferred formats |
| --- | --- |
| Sequence or workflow | Mermaid flowchart, activity diagram, or ASCII flow |
| Interaction over time | Mermaid sequence diagram or timeline |
| State changes | State diagram or transition table |
| Hierarchy or composition | Tree, Mermaid mind map, Graphviz, or indented ASCII tree |
| Decision logic | Decision tree, flowchart, or decision table |
| Exact comparison | Markdown table or comparison matrix |
| Quantitative pattern | Matplotlib, Plotly, Vega-Lite, or a simple chart |
| Network or dependency graph | Graphviz, Mermaid, or a node-link diagram |
| Spatial relationship | Annotated image, map, coordinate plot, or ASCII sketch |
| Formula or transformation | Worked equation, aligned derivation, or annotated pipeline |

- Prefer formats the current interface can render.
- If the best format is unsupported, provide a Markdown table or clean ASCII fallback.
- Label every visual and explain how to read it.
- Keep one visual focused on one relationship or insight.

### 3. Write the Guide

Build the lesson in this order:

1. **Orientation:** What the topic is, why it matters, and where it fits
2. **Prerequisites:** The minimum foundation, explained from first principles
3. **Core mechanism:** How the central idea works
4. **Major concepts:** One focused section per concept, with its visual and examples
5. **Connections:** How the concepts depend on or affect each other
6. **Target-level nuance:** Advanced rules, exceptions, trade-offs, or edge cases required by the target
7. **Misconceptions:** Common wrong models and how to correct them
8. **Integrated example:** A complete worked example that connects the major concepts
9. **Recap:** A compact visual summary and short checklist of what the learner should now understand

For each major concept:

- Define it in plain language.
- Explain why it exists or what problem it solves.
- Show how it works step by step.
- Include a focused visual.
- Give at least one concrete example and explain why the example demonstrates the concept.
- Contrast it with a common misconception when useful.
- Connect it to the preceding and following concepts.

### 4. Verify the Guide

Before delivery, confirm that:

- Every prerequisite used later was introduced earlier.
- Every major concept has an appropriate visual.
- Visuals are readable and explained.
- Every essential concept, rule, condition, and relationship is present.
- Examples are correct and actually teach the associated concept.
- Jargon is defined at first use.
- Sections remain focused and navigable.

## Follow-Up Clarification Mode

If the user says part of the guide is unclear:

1. Isolate the exact concept or step causing confusion.
2. Identify the prerequisite or mental model that may be missing.
3. Re-explain only that part from a different angle.
4. Use a different visual form from the original when possible.
5. Add a new worked example or counterexample.
6. Ask one focused comprehension question.
7. Return to the larger learning path after resolving the unclear point.

Focus each follow-up on the unclear aspect and return to the larger guide after resolving it.

## Output Structure

1. Learning Map and depth target
2. Orientation
3. Prerequisites
4. Core mechanism
5. Major-concept sections with their visuals
6. Connections between concepts
7. Target-level nuance
8. Misconceptions
9. Integrated worked example
10. Visual recap and understanding checklist
