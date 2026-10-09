---
name: cognitive-clarity-refactor
description: Refactors dense, complex, or disorganized text into scannable, hierarchical Markdown with zero loss of meaning. Use when reorganizing unstructured notes, walls of text, dense documentation, or complex technical runbooks. Do not use for code blocks, tables, or text requiring pure narrative voice.
---

# Cognitive Clarity Refactoring Engine

Execute this protocol to convert high-friction prose into structured, scannable documentation. You will dismantle dense paragraphs into focused bullet clusters, enforce plain-language syntax, and retain all technical specifications, code fences, and architectural decisions verbatim.

---

## 1. Core Invariants

- **Semantic Fidelity Guarantee:** Retain every fact, technical constraint, dependency, and warning from the source text. Reorganize and clarify articulation, but never omit valid technical assertions or dilute commitments.
- **Verbatim Asset Protection:** Treat code blocks, terminal sessions, mathematical equations, tables, and Mermaid definitions as protected assets. Do not rewrite code or table contents during prose refactoring.
- **Single-Thought Structure:** Restrict every child bullet to a single assertion or instruction. Do not join unrelated actions with compound conjunctions.

---

## 2. Formatting Architecture

Structure all text using a strict two-tier hierarchical layout:

- **Section Framing Leads:** Begin major sections with an optional 1–2 sentence contextual overview before listing items.
- **Category Anchors:** Use standalone bold category anchors with zero trailing text on the anchor line:
  `- **Category Anchor:**`
- **Declarative Child Bullets:** Place each discrete assertion or action on an un-bolded child bullet indented directly beneath its category anchor:
  `  - Child declarative assertion or instruction.`
- **Single-Thought Invariant:** Limit each child bullet to exactly one complete assertion or action. Do not join unrelated operational steps with compound conjunctions.
- **Branching Matrices:** If a concept involves two or more conditional states (`if... then... else`), convert it into a Markdown table instead of nested bullets.

---

## 3. The Tri-Standard Articulation Engine

Draft every declarative child bullet by applying three standards simultaneously:

### A. Syntactic Discipline (ASD-STE100 Structural Mechanics)

- **Explicit Referents:** Never use unanchored pronouns (`it`, `this`, `that`, `which`). Explicitly name the actor, service, table, or variable on every mention.
- **Noun-Stack Limit:** Restrict noun clusters modifying a subject to a maximum of three consecutive words (e.g., convert "cloud storage bucket access policy token" to "access token for the cloud storage bucket").
- **Domain Vocabulary:** Retain natural software engineering, distributed systems, and domain terminology.

### B. Tone and Directness (Google Developer Documentation Style)

- **Voice and Tense:** Use active voice and present tense throughout.
- **Direct Address:** Address the reader as "you" where appropriate, and use imperative verbs for operational instructions (e.g., "Configure the worker pool", not "The worker pool should be configured").
- **De-nominalization:** Replace abstract zombie nouns with active verbs (e.g., use "verify the payload" instead of "perform verification of the payload").
- **Eliminate Bureaucratic Filler:** Strip conversational padding (e.g., replace "in order to" with "to", "it is important to note that" with direct statements, and "utilize" with "use").

### C. Complexity Throttle (Gunning Fog Index \~10 Cadence)

- **Layperson Accessibility:** Calibrate readability for a general technical reader. Use direct, intuitive explanations before introducing technical abstractions.
- **Zero Marketing Cadence:** Eliminate hyperbolic adjectives, speculative buzzwords, and promotional tone. Present engineering facts without overselling.
- **Linear Syntax (Right-Branching):** State the subject and primary action first; place constraints, caveats, and dependencies after the main clause.

---

## 4. Scalable Document Execution Pipeline

Execute refactoring using this three-phase operational pipeline. For files exceeding 1,500 words or containing multiple H2 (`##`) sections, execute Phases 2 and 3 iteratively per section.

### Phase 1: Pre-Flight Ingestion & Asset Isolation

1. **Boundary Segmentation:** Split the document into discrete execution chunks along primary Markdown headings (`##` / `###`).
2. **Lexicon Extraction:** Build an internal Global Entity Lexicon containing system names, environment variables, roles, and acronyms to guarantee consistent terminology across all chunks.

### Phase 2: Chunk-by-Chunk Synthesis

Process each segmented section independently:

1. Ingest the section along with the Global Entity Lexicon.
2. Group unstructured statements into thematic clusters.
3. Generate the section applying:

- Standalone bold Category Anchors (`- **Anchor:**`).
- Declarative Child Bullets complying with the Tri-Standard Articulation Engine.

### Phase 3: Asset Re-hydration & Assembly

1. Concatenate all processed sections into the master document hierarchy.
2. Validate Markdown heading depth and continuity (`#` $\rightarrow$ `##` $\rightarrow$ `###`).
3. Re-attach protected assets (code fences, schema definitions, and tables) adjacent to their related declarative bullets.

Emit the final, fully assembled Markdown document.
