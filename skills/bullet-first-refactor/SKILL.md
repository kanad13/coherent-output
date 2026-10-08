---
name: bullet-first-refactor
description: Ingests dense or poorly organized text and refactors it into an ultra-clean, highly scannable, bullet-first Markdown document with 100% semantic fidelity and zero informational loss. Use when refactoring messy documents, cleaning up text, or applying ASD-STE100 bullet-first structure.
---

# Bullet-First & Plain Text Refactoring Engine

Follow this 3-phase deterministic pipeline to restructure dense, disorganized, or complex technical material into clean, bullet-first Markdown.

---

## 1. Core Mandates & Invariants

- **The Zero-Loss Invariant:** Preserve 100% of substantive information from the source text:
  - Every factual assertion, role, entity, technology, metric, and SLA.
  - Every condition, prerequisite, and causal dependency (`A causes B under C`).
  - Exact modal certainty (`must`, `should`, `may`, `target` — never dilute or amplify).
  - Every caveat, warning, error condition, and unresolved ambiguity.
  - **Orphaned Thought Integration:** Integrate stray notes or draft thoughts into their proper conceptual sections; never discard valid information.
- **Immutable Syntax Elements:** Strictly preserve non-prose blocks in their native formatting: code fences, Mermaid definitions, markdown tables, and metadata headers. Re-insert them unedited beneath corresponding category anchors.

---

## 2. Deterministic 3-Phase Execution Pipeline

Execute the following three phases sequentially:

### Phase 1: Ingest & Partition (Atomic Inventory Ledger)

Parse source text into a two-partition inventory ledger before drafting:

- **Editable Partition:** Deconstruct all paragraphs, lists, and freeform text into atomic factual propositions, definitions, metrics, constraints, and business rules.
- **Protected Partition:** Catalogue code fences, Mermaid diagrams, tables, and frontmatter to preserve them verbatim without modification.

### Phase 2: Refactored Synthesis

Deconstruct dense multi-clause paragraphs into scannable hierarchical units instead of transferring verbatim prose. Draft the transformed content enforcing the Bullet-First standard:

- **Category Anchors:** Bold category anchors (`- **Anchor:**`) with zero trailing sentence on the anchor line.
- **Declarative Child Bullets:** Place each discrete assertion or action on a single un-bolded declarative child bullet conforming to ASD-STE100 principles (one main idea per sentence, active voice, under 25 words).
- **Depth Limit:** Cap list nesting at three levels to maintain visual scannability.
- **Syntax Re-attachment:** Re-attach protected code blocks, tables, and diagrams immediately below their governing category anchors.

### Phase 3: Verification & Delivery Gate

Perform a parallel audit for semantic parity and structural compliance before releasing the document:

- **Semantic Parity Audit:** Cross-check synthesized text against the Phase 1 inventory to guarantee 100% information preservation (zero dropped metrics, constraints, or exceptions).
- **Structural Compliance Gate:** Confirm zero violations of structural invariants:
  1. Zero walls of plain paragraph text.
  2. Zero bold labels on child bullets.
  3. Maximum nesting depth of three levels.
  4. Fenced code blocks, diagrams, and tables preserved in native syntax.
  5. All links and technical terms preserved accurately.
- Emit the final refactored document.
