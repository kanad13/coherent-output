# Document Formatting

## Purpose

Apply this approach when formatting documents and repository files according to preferred plain, bullet-first Markdown style. Improve scanability and consistency while preserving meaning, technical detail, order, and intent.

Formatting is the primary job. Limit simplification and structural changes to small local adjustments required by the specified format.

## Non-Negotiables

- Preserve every fact, instruction, qualification, example, and technical term.
- Preserve the strength of every obligation.
- Preserve the author's position, tone, and chronology while applying the specified direct instructional phrasing.
- Keep one idea per sentence, bullet, or grouped unit.
- Make relationships visible through nesting.
- Use one canonical term per concept.

## Preferred Markdown Style

### 1. Headings

- Use descriptive Markdown headings.
- Remove bold markers from inside headings.
- Maintain a contiguous, valid heading hierarchy.
- Use headings for real topic changes and bullets for individual sentences.

```markdown
## Project Budget
```

Incorrect form:

```markdown
## **Project Budget**
```

### 2. Bullet-First Body Text

- Every ordinary body line must be a bullet. Headings, numbered steps, tables, blockquotes, frontmatter, and code blocks retain their native forms.
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
- Use unordered bullets for nonsequential groups.
- Preserve numbered formatting for every ordered procedure.
- Use a table or separate subsection when it communicates a deep hierarchy more clearly.

### 4. Tables

- Use tables for exact mappings, repeated-field comparisons, matrices, or compact reference data.
- Keep prose explanations outside tables when cells would become difficult to read.
- Preserve every value and unit.

### 5. Terms and Definitions

- Use one term consistently for each concept.
- Define technical terms at first use when the source provides or clearly implies the definition.
- Use definitions grounded in the source.
- Use `code` formatting for commands, file paths, identifiers, configuration keys, and literal values.

### 6. Operational Language

When the source is operational policy or instruction:

- Use direct action language.
- Use `must` only for requirements that are mandatory in the source.
- Use `should` for strong recommendations with legitimate exceptions.
- Use `may` for optional actions.
- Express settled current rules directly when the source establishes them as current policy.

### 7. Single Source of Truth

- Keep the full explanation of a concept in one primary location.
- Use Markdown links to reference that location elsewhere.
- Preserve repeated statements that serve as warnings or local prerequisites.

## Protected Elements

Preserve the internal layout of these protected elements:

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

An audit or approval-gate request concludes with the plan. A formatting request proceeds into the requested file changes.

### 3. Apply the Format

- Edit only the requested text or files.
- Preserve protected elements.
- Apply the preferred style consistently.
- Keep wording changes within the requested formatting scope.

### 4. Audit

Verify:

- Every source statement remains represented.
- Modality and meaning are unchanged.
- Every ordinary body line begins with an appropriate bullet marker.
- Heading hierarchy is valid.
- List nesting shows the intended relationships.
- Tables, code, links, anchors, and frontmatter remain valid.
- Every content addition serves the requested format and remains source-grounded.

## Delivery

- Provide a concise change summary in chat and reproduce the complete edited file when the user asks.
- Lead with the file or text that was formatted.
- End with a brief preservation and formatting audit.
