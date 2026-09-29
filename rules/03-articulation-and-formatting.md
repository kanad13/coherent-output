---
trigger: always_on
description: "Communication clarity, plain language, adaptive structural formatting, Zero-Loss invariant, Protected Elements, and relative link integrity."
---

# Articulation, Communication & Formatting Standards

These standards govern communication clarity, structural presentation, and link integrity across all agent responses and repository documentation.

---

## 1. Plain Language & Expressive Clarity

- **First-Principles Plain Language:**
  - Explain mechanisms, components, and workflows in direct, natural language.
  - Avoid artificial jargon, academic posturing, buzzwords, and contrived taxonomic labels.
  - Define unfamiliar or domain-specific terminology in plain language upon first use.
- **Natural Syntactic Flow:**
  - Write direct, affirmative sentences.
  - Preserve natural grammatical flow, transitional phrases, and connective reasoning without artificial fragmentation or run-on sprawl.
- **Active Voice & Explicit Actors:**
  - Ensure every sentence names a clear actor performing the action.
  - State what a component is, has, or does directly using ordinary verbs such as use, build, run, check, or store.
- **Terminological Determinism:**
  - Use one canonical term for each system concept consistently throughout.

---

## 2. Adaptive Structural Formatting

- **Medium-Matched Layout:**
  - Select the layout structure that optimizes scannability and comprehension for the specific task:
    - Use clean, cohesive paragraphs for explanations, narrative context, and conceptual overviews.
    - Use bulleted lists for discrete items, prerequisites, options, and non-sequential collections. Avoid nesting beyond three levels.
    - Use numbered lists strictly for sequential steps, chronological phases, or execution algorithms.
    - Use comparison tables for multi-attribute trade-offs, schemas, and evaluations.
- **High-Signal Scannability:**
  - Structure prose and lists according to the natural cohesion of the content.
  - Break up dense sections with logical headings, code fences, and lists to maximize clarity.

---

## 3. Zero-Loss Invariant & Protected Elements

- **Zero-Loss Invariant:**
  - Preserve 100% of substantive facts, numbers, units, dates, formulas, parameters, and configuration settings.
  - Preserve exact modal certainty without weakening or strengthening modal force.
- **Protected Elements:**
  - Retain native syntax and formatting for tables, fenced code blocks, Mermaid diagrams, LaTeX math blocks, frontmatter, and blockquotes.
  - Never convert protected elements into list items.

---

## 4. Link Integrity & Markdown Navigation

- **Portable Relative Links:**
  - Use portable relative Markdown links exclusively inside repository documentation files (e.g., `[Auth Service](../services/auth.md)`).
  - Prohibit machine-local absolute paths (`file:///Users/...`) in committed repository markdown.
- **Clickable File References:**
  - Ensure every document filename referenced in an index or guide is a valid, clickable Markdown link.
- **Target Verification:**
  - Verify that all relative paths, file anchors, and image references resolve to existing targets before completing tasks.
- **Asset Alt-Text:**
  - Include meaningful descriptive alt text for every informative image or diagram.
