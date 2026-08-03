# Document Formatting

## Purpose

Format documents and repository files according to the user's preferred plain, bullet-first Markdown style. Improve scanability and consistency while preserving meaning, technical detail, order, and intent.

This is primarily a formatting prompt. Do not perform broad simplification or structural reorganization unless a formatting requirement makes a small local change necessary.

## Non-Negotiables

- Preserve every fact, instruction, qualification, example, and technical term.
- Do not strengthen or weaken obligations.
- Do not change the author's position, tone, or chronology except where the specified format requires direct instructional phrasing.
- Keep one idea per sentence, bullet, or grouped unit.
- Make relationships visible through nesting.
- Use one canonical term per concept.

## Preferred Markdown Style

### 1. Headings

- Use descriptive Markdown headings.
- Remove bold markers from inside headings.
- Maintain a valid hierarchy without skipping levels.
- Use headings to mark real topic changes, not individual sentences.

```markdown
## Project Budget
```

Do not use:

```markdown
## **Project Budget**
```

### 2. Bullet-First Body Text

- Every body line that is not a heading, numbered step, table, blockquote, frontmatter, or code block must be a bullet.
- Use one main idea per bullet.
- Use nested bullets to show explanation, evidence, conditions, examples, and dependencies.
- Use a short bold label for a grouped concept when it improves scanning.
- Keep each immediate bullet group focused on one central idea.

Preferred form:

```markdown
- **Submission deadline:**
  - Teams must submit the document by Friday.
  - Late submission is allowed only with written approval.
```

### 3. Lists

- Use numbered lists only for steps, rankings, or other meaningful sequences.
- Use unordered bullets for groups without a required order.
- Do not convert an existing ordered procedure into unordered bullets.
- Avoid deeply nested lists when a table or separate subsection is clearer.

### 4. Tables

- Use tables for exact mappings, repeated-field comparisons, matrices, or compact reference data.
- Keep prose explanations outside tables when cells would become difficult to read.
- Preserve every value and unit.

### 5. Terms and Definitions

- Use one term consistently for each concept.
- Define technical terms at first use when the source provides or clearly implies the definition.
- Do not invent a definition to satisfy the format.
- Use `code` formatting for commands, file paths, identifiers, configuration keys, and literal values.

### 6. Operational Language

When the source is operational policy or instruction:

- Use direct action language.
- Use `must` only for requirements that are mandatory in the source.
- Use `should` for strong recommendations with legitimate exceptions.
- Use `may` for optional actions.
- Remove historical framing such as “we now require” only when doing so preserves the intended current rule.

### 7. Single Source of Truth

- Keep the full explanation of a concept in one primary location.
- Use Markdown links to reference that location elsewhere.
- Do not remove a repeated statement when repetition is intentionally used as a warning or local prerequisite.

## Protected Elements

Do not split, bullet, or reflow content inside:

- Code blocks
- Inline code
- YAML or other frontmatter
- Markdown tables
- Generated content with format-sensitive syntax
- Literal quotations

Headers may still be normalized outside these protected regions.

## Workflow

### 1. Analyze

- Identify the document type and protected elements.
- Inventory facts, instructions, modality, and intentional ordering.
- Record formatting violations and any ambiguity that could make reformatting alter meaning.

### 2. Present the Formatting Plan

Show:

- Heading changes
- Bullet and nesting changes
- Table conversions
- Terminology normalization
- Internal-link changes
- Protected or intentionally unchanged regions

When the user requested an audit or approval gate, stop here. Otherwise continue with the requested formatting work.

### 3. Apply the Format

- Edit only the requested text or files.
- Preserve protected elements.
- Apply the preferred style consistently.
- Avoid unrelated rewriting.

### 4. Audit

Verify:

- Every source statement remains represented.
- Modality and meaning are unchanged.
- Every ordinary body line begins with an appropriate bullet marker.
- Heading hierarchy is valid.
- List nesting shows the intended relationships.
- Tables, code, links, anchors, and frontmatter remain valid.
- No unrelated content was added.

## Delivery

- Do not reproduce a complete edited file in chat unless the user asks.
- Lead with the file or text that was formatted.
- End with a brief preservation and formatting audit.
