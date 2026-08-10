# Document Restructuring

## Purpose

Use this approach when reorganizing disordered, repetitive, or poorly sequenced material into coherent documents. Preserve terminology, substantive meaning, and authorial voice.

This methodology changes information architecture. Use the technical-text simplification prompt separately when vocabulary and explanations must also be made easier.

## Non-Negotiables

- Preserve every distinct fact, concept, example, qualification, and intentional emphasis.
- Deduplicate repeated ideas while preserving meaningful variations.
- Keep each section focused on one primary question.
- Sequence content by dependency, chronology, general-to-specific progression, or problem-to-resolution—whichever best fits the source.
- Preserve the source's tone and level of technical detail.
- Use transitions grounded in relationships established by the source.

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
- Orphan details lacking context
- Headings mismatched with their content
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

Use the shallowest hierarchy that expresses the document's structure. Prefer descriptive headings over generic labels such as `Overview` or `Details`.

Begin drafting after every content unit has exactly one primary home.

### 4. Rebuild the Document

- Move each content unit to its approved primary home.
- Merge duplicate wording while preserving distinct facts and nuances.
- Add minimal transitions needed for flow.
- Use cross-references to reduce repeated full explanations.
- Preserve examples, evidence, terminology, modality, and voice.
- Lead sections and paragraphs with their controlling point when the source supports it.

Preserve the original language level during this step. Use the technical-text simplification prompt for a subsequent plain-language rewrite.

### 5. Audit Preservation and Structure

Build a traceability matrix:

| Content ID | Source location(s) | New location | Preserved? | Deduplication or move notes |
| ---------- | ------------------ | ------------ | ---------- | --------------------------- |

Verify:

- Every content ID appears in the new document.
- Every section answers one main question.
- Prerequisites precede dependent ideas.
- Duplicates were consolidated with every meaningful distinction preserved.
- The factual set and obligation strength match the source.
- Heading hierarchy and cross-references are valid.

Correct failures before delivery.

## Output

Return:

1. Content inventory
2. Structural diagnosis
3. Structural blueprint
4. Reorganized document
5. Traceability and quality audit

For file edits, keep analysis artifacts in the conversation by default and store them in the document when the user requests that placement.
