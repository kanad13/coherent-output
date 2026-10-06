---
name: bullet-first-refactor
description: Ingests dense or poorly organized text and refactors it into an ultra-clean, highly scannable, bullet-first Markdown document with 100% semantic fidelity and zero informational loss. Use when refactoring messy documents, cleaning up text, or applying ASD-STE100 bullet-first structure.
---

# Bullet-First & Plain Text Refactoring Engine

Follow this 5-phase deterministic pipeline to restructure dense, disorganized, or complex technical material into clean, bullet-first Markdown.

---

## 1. Core Mandates & Invariants

- **The Zero-Loss Invariant:** Preserve 100% of substantive information from the source text:
  - Every factual assertion, role, entity, technology, metric, and SLA.
  - Every condition, prerequisite, and causal dependency (`A causes B under C`).
  - Exact modal certainty (`must`, `should`, `may`, `target` — never dilute or amplify).
  - Every caveat, warning, error condition, and unresolved ambiguity.
  - **Orphaned Thought Integration:** Integrate stray notes or draft thoughts into their proper conceptual sections; never discard valid information.
- **Protected Elements:** Never convert Markdown tables, fenced code blocks, CLI commands, Mermaid diagrams, equations, frontmatter, or literal blockquotes into bullets. Preserve them verbatim in native syntax.

---

## 2. Deterministic 5-Phase Execution Pipeline

Execute the following five phases sequentially:

### Phase 1: Atomic Inventory Ledger

- Ingest the raw source and extract distinct assertions, constraints, definitions, metrics, and rules.
- For dense or legally sensitive texts, use the [Preservation Ledger Schema](./references/preservation-ledger.md) (`P001`, `P002`, ...) to track entities systematically.

### Phase 2: Structural Blueprint & Re-Sequencing

- Group extracted assertions into logical conceptual domains.
- Eliminate circular reasoning and redundant repetitions while preserving distinct nuances.
- Establish a clean, shallow heading hierarchy ($H_2 / H_3$).

### Phase 3: Refactored Synthesis

- Draft the transformed content enforcing the Bullet-First standard:
  - Top-level bullets: bold category anchors (`- **Anchor:**`) with **no** trailing sentence.
  - Nested child bullets: un-bolded declarative sentences conforming to ASD-STE100 principles.
  - Depth capped at three levels.
- Re-attach protected code blocks, tables, and diagrams immediately below their relevant category bullets.

### Phase 4: Reconciliation & Parity Audit

- Perform a cross-check comparing the synthesized text against the Phase 1 Atomic Inventory Ledger.
- Verify that every metric, prerequisite, and rule from the source text is represented in the output.

### Phase 5: Verification Gate & Delivery

- Confirm compliance with formatting invariants:
  1. Zero walls of plain paragraph text.
  2. Zero bold labels on child bullets.
  3. Fenced code blocks and tables preserved in native syntax.
  4. All links and technical terms preserved accurately.
- Emit the final refactored document.
