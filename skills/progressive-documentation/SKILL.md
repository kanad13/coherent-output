---
name: progressive-documentation
description: Creates or restructures explanatory documents so readers understand the whole subject before exploring mechanisms, relationships, and detail. Use for multi-topic guides, system overviews, proposals, and documents that exhaust one topic before introducing the next. Do not expand brief answers or impose layers on procedure-only runbooks, chronological narratives, or lookup references.
---

# Progressive Documentation: Top-Down Explanatory Architecture

Follow this protocol to create or restructure explanatory technical documents into progressive layers of understanding. Establish a robust mental model of the entire system first, then systematically deepen mechanisms, relationships, operational trade-offs, and implementation details.

---

## 1. Non-Negotiable Operational Invariants

1. **Top-Down Mental Model First:**
   - Always establish the complete system, its primary actors, and their end-to-end relationship in the opening layer before examining any single component in depth.
   - Never silo the document into isolated, exhaustive topic chapters that explore one module completely before introducing the others.
2. **Strict Asset Preservation:**
   - Preserve all code blocks, commands, configuration payloads, tables, equations, and explicit user-provided data **byte-for-byte**.
   - Never truncate, invent, or mutate functional code, parameters, or schema definitions during restructuring.
   - If Prettier or post-processing mutates a protected Markdown table or code block, wrap it with `<!-- prettier-ignore -->`.
3. **Scope Guard & Boundary Discipline:**
   - Apply progressive layering **only** to multi-topic explanatory documents, architecture overviews, technical specifications, and system guides.
   - **Do not apply** to linear step-by-step procedures, runbooks, chronological narratives, release notes, or concise direct answers. Keep procedures in executable sequence.
4. **Understated Register & Plain Language:**
   - Use direct verbs, consistent terminology, and define domain concepts on first use. Maintain necessary technical vocabulary.
   - Use Gunning Fog index (~10) as an informal clarity heuristic, not a measured compliance score.

---

## 2. The 4-Layer Progressive Architecture

Structure multi-topic explanations across four distinct conceptual strata:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Orientation & Global Mental Model                  │
│ • System identity, core purpose, and primary problem solved │
│ • Complete component topology (all major actors introduced) │
│ • Foundational end-to-end data/control flow                 │
│ • Bottom-line conclusion, immediate boundary, or key risk   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 2: Mechanisms & Systemic Interactions                 │
│ • Inter-component collaboration, protocols, and interfaces  │
│ • Concrete walkthrough or running example tracing all parts │
│ • Causal relationships: triggers, dependencies, state changes│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 3: Constraints, Trade-Offs & Failure Modes            │
│ • Architectural trade-offs, decision drivers, bottlenecks   │
│ • Failure modes, edge cases, recovery paths, invariants     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 4: Implementation Parameters & Operational Reference  │
│ • Exact configuration schemas, environment flags, options   │
│ • Verbatim CLI commands, code listings, data tables         │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Four-Phase Execution Workflow

```
┌────────────────────┐     ┌─────────────────────┐     ┌───────────────────────┐     ┌───────────────────┐
│ Phase 1:           │ ──► │ Phase 2:            │ ──► │ Phase 3:              │ ──► │ Phase 4:          │
│ Ingest & Protect   │     │ Map Depth Layers    │     │ Draft Layered Content │     │ Verify & Audit    │
└────────────────────┘     └─────────────────────┘     └───────────────────────┘     └───────────────────┘
```

### Phase 1: Ingest & Protect

1. **Triage Input Document:**
   - Verify document type: Confirm the source is an explanatory guide or multi-topic design. If it is a runbook or linear procedure, preserve chronological execution order and exit.
2. **Isolate Protected Assets:**
   - Catalog all code blocks, CLI snippets, formulas, data tables, and structured schemas.
   - Mark assets as immutable to guarantee zero degradation during drafting.
3. **Identify System Topology:**
   - Extract the core system actors, their high-level responsibilities, and their interactions.

### Phase 2: Map Depth Layers

1. **Construct Layer Allocation Map:**
   - Assign source facts and sections to their appropriate strata (Layers 1–4).
   - Ensure every major component is assigned a brief introductory definition in Layer 1 before any component receives Layer 2/3 deep-dives.
2. **Design the Unifying Narrative:**
   - Select a concrete end-to-end workflow (e.g., request lifecycle, data ingestion pipeline) that touches all components simultaneously to demonstrate their relationships.

### Phase 3: Draft Layered Content

1. **Draft Layer 1 (Global Orientation):**
   - Open with system identity, problem solved, and high-level component map.
   - Trace the single end-to-end workflow connecting the actors.
   - State immediate constraints or critical conclusions upfront.
2. **Draft Layer 2 (Mechanisms & Interactions):**
   - Explain how components communicate, transition state, and exchange data.
   - Ground interactions in the unifying walkthrough.
   - Ensure every concept referenced was defined in Layer 1.
3. **Draft Layer 3 (Trade-offs & Resilience):**
   - Address architectural trade-offs, scalability boundaries, and failure modes.
   - Explain why specific approaches were chosen over alternatives.
4. **Draft Layer 4 (Operational Details):**
   - Place exact configuration flags, parameter tables, and reference specs here.
   - Insert protected code blocks and commands verbatim.

### Phase 4: Verify & Audit

Run the **Progressive Quality Gate** before finalizing:

1. **Orientation Check:** Can a reader understand the overall purpose and all major parts from Layer 1 alone without reading further?
2. **No Forward References:** Does any layer rely on concepts or terms defined only in a subsequent layer?
3. **No Isolated Silos:** Did we avoid exhausting module A's implementation parameters before introducing module B?
4. **Asset Integrity Audit:** Compare code blocks, commands, tables, and numerical constants byte-for-byte against the source. Confirm zero accidental modifications or hallucinations.
5. **Formatting Safety:** Confirm Prettier compliance. If table formatting risks mutation, verify `<!-- prettier-ignore -->` presence.
