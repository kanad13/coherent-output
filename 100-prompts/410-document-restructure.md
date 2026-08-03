# Document Restructuring

## Purpose

Reorganize disordered, repetitive, or poorly sequenced material into a coherent document without simplifying its terminology, changing its substantive meaning, or imposing a new authorial voice.

This prompt changes information architecture. Use the technical-text simplification prompt separately when vocabulary and explanations must also be made easier.

## Non-Negotiables

- Preserve every distinct fact, concept, example, qualification, and intentional emphasis.
- Deduplicate repeated ideas without deleting meaningful variations.
- Keep each section focused on one primary question.
- Sequence content by dependency, chronology, general-to-specific progression, or problem-to-resolution—whichever best fits the source.
- Preserve the source's tone and level of technical detail.
- Do not invent transitions that assert unsupported relationships.

## Workflow

### 1. Extract the Content Inventory

Read the complete source and assign an identifier to every distinct content unit:

- Claim or idea
- Definition
- Rule or instruction
- Example or story
- Evidence or data
- Qualification, exception, or warning
- Open question

Group exact repetition while recording each occurrence and meaningful variation.

**Visible output — Content Inventory:**

```markdown
- **C001 — [Short label]**
  - Content:
  - Source location(s):
  - Related or repeated units:
  - Required context:
```

### 2. Diagnose Structural Problems

Identify:

- Duplicate or circular passages
- Concepts introduced before prerequisites
- Mixed topics within one section
- Orphan details without context
- Headings that do not match their content
- Transitions that hide logical gaps
- Examples separated from the ideas they illustrate
- Conclusions buried after supporting detail

### 3. Design the Structural Blueprint

For every proposed section, specify:

- The single core question it answers
- Content-unit IDs assigned to it
- Its dependency on earlier sections
- Why its position is appropriate
- Cross-references required elsewhere

Use a hierarchy no deeper than necessary. Prefer descriptive headings over generic labels such as `Overview` or `Details`.

Do not draft the reorganized prose until every content unit has exactly one primary home.

### 4. Rebuild the Document

- Move each content unit to its approved primary home.
- Merge duplicate wording while preserving distinct facts and nuances.
- Add minimal transitions needed for flow.
- Use cross-references instead of repeating full explanations.
- Preserve examples, evidence, terminology, modality, and voice.
- Lead sections and paragraphs with their controlling point when the source supports it.

Do not perform a general plain-language rewrite during this step.

### 5. Audit Preservation and Structure

Build a traceability matrix:

| Content ID | Source location(s) | New location | Preserved? | Deduplication or move notes |
| --- | --- | --- | --- | --- |

Verify:

- Every content ID appears in the new document.
- Every section answers one main question.
- Prerequisites precede dependent ideas.
- Duplicates were consolidated without losing distinctions.
- No new factual claim or stronger obligation was introduced.
- Heading hierarchy and cross-references are valid.

Correct failures before delivery.

## Output

Return:

1. Content inventory
2. Structural diagnosis
3. Structural blueprint
4. Reorganized document
5. Traceability and quality audit

If editing a file, keep analysis artifacts in the conversation unless the user explicitly asks to store them in the document.
