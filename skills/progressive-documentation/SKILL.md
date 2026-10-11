---
name: progressive-documentation
description: Creates or restructures explanatory documents so readers understand the whole subject before exploring mechanisms, relationships, and detail. Use for multi-topic guides, system overviews, proposals, and documents that exhaust one topic before introducing the next. Do not expand brief answers or impose layers on procedure-only runbooks, chronological narratives, or lookup references.
---

# Progressive Documentation: The Blooming Flower Architecture

Follow this protocol to create or restructure explanatory documents across any domain—technical systems, strategy proposals, business cases, policy memos, or architectural guides. Build understanding in concentric, progressive layers so readers grasp the whole subject before exploring deep mechanisms, trade-offs, and granular parameters.

---

## 1. Core Philosophy: The Blooming Flower Principle

An explanatory document must unfold like a blooming flower:

1. **The Whole Form First (The Bud Silhouette):** When a flower blooms, the outer form and silhouette of the entire flower appear first. The reader sees the complete picture, all major components, and their relationship immediately. A flower does not grow by fully forming Petal 1 down to its darkest inner pigments while Petals 2 and 3 do not yet exist.
2. **Concentric Unfolding (The Petals Opening):** As the flower opens, the petals reveal their interconnections, how they overlap, and how they support the core structure.
3. **The Inner Heart (Deep Textures & Granular Mechanics):** Only after the overarching structure is completely clear does the flower reveal its deep interior—the intricate veins, delicate stamens, exact measurements, and fine details.

### The Fatal Anti-Pattern: Topic Exhaustion (Siloing)

The primary failure mode in documentation is **Topic Exhaustion**: taking Topic A from introduction down to its deepest weeds and configuration parameters before Topic B is even introduced. When readers are dragged through Topic A in isolation, they lack the global context to understand why those details matter, and cannot evaluate how Topic A affects Topic B.

**Invariant:** Introduce every major theme, component, or actor at a high level before taking any single topic into depth.

---

## 2. Non-Negotiable Operational Invariants

1. **Global Silhouette Before Local Detail:**
   - Always establish the entire system or thesis, all major actors or themes, and their overarching relationship in the opening layer before examining any single part in depth.
   - Never silo the document into isolated, exhaustive chapters that explore one topic completely before introducing the others.
2. **Universal Scope:**
   - Apply progressive layering to any multi-topic explanatory document: technical architectures, strategy memos, policy designs, business proposals, and analytical guides.
   - **Do not apply** to linear step-by-step procedures, runbooks, chronological narratives, release notes, or concise direct answers. Keep procedures in executable sequence.
3. **Strict Verbatim Asset Preservation:**
   - Preserve all code blocks, commands, data tables, numerical constants, formulas, and quoted source material **byte-for-byte**.
   - Never truncate, invent, or mutate functional code, parameters, or schema definitions during restructuring.
4. **Understated Register & Plain Language:**
   - Use direct verbs, consistent terminology, and define domain concepts on first use.
   - Use Gunning Fog index (~10) as an informal clarity heuristic, not a measured compliance score.

---

## 3. The 4 Concentric Progressive Layers

Structure multi-topic explanations across four progressive strata:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Global Silhouette (The Whole Picture)              │
│ • Core purpose, problem solved, or strategic thesis         │
│ • Complete topology: all major actors, themes, or pillars   │
│ • Unifying end-to-end workflow, narrative, or lifecycle     │
│ • Immediate bottom line, governing boundary, or key risk    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 2: Structural Interconnections (How Parts Relate)     │
│ • Cross-component collaboration, flows, and relationships   │
│ • Unifying walkthrough connecting all pillars in action     │
│ • Causal dynamics: triggers, dependencies, state transitions│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 3: Dynamics, Trade-Offs & Drivers (Nuance & Rationale)│
│ • Strategic trade-offs, constraints, and decision rationale │
│ • Failure modes, edge cases, risks, and recovery paths      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Layer 4: Granular Mechanics & Execution Reference           │
│ • Exact specifications, configurations, formulas, and data  │
│ • Verbatim code blocks, CLI commands, and reference tables  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Four-Phase Execution Workflow

```
┌────────────────────┐     ┌─────────────────────┐     ┌───────────────────────┐     ┌───────────────────┐
│ Phase 1:           │ ──► │ Phase 2:            │ ──► │ Phase 3:              │ ──► │ Phase 4:          │
│ Ingest & Protect   │     │ Map Depth Strata    │     │ Draft Concentric Bloom│     │ Verify & Audit    │
└────────────────────┘     └─────────────────────┘     └───────────────────────┘     └───────────────────┘
```

### Phase 1: Ingest & Protect

1. **Triage Document:**
   - Confirm the document is an explanatory guide, proposal, memo, or system overview.
   - If it is a chronological runbook or linear execution guide, preserve chronological execution order and exit.
2. **Catalog Protected Assets:**
   - Identify and isolate all code blocks, commands, data tables, metrics, and exact values to guarantee zero mutation.
3. **Identify Full Subject Topology:**
   - Extract the complete roster of primary themes, components, actors, or strategic pillars.

### Phase 2: Map Depth Strata

1. **Assign Facts to Layers:**
   - Distribute concepts across Layers 1–4.
   - Confirm that _every_ major theme has an entry in Layer 1 before _any_ theme receives Layer 2 or Layer 3 depth.
2. **Design the Unifying Thread:**
   - Select an end-to-end trace (e.g., user request lifecycle, strategic initiative timeline, transaction flow) that touches all major parts in a single coherent story.

### Phase 3: Draft Concentric Bloom

1. **Draft Layer 1 (Global Silhouette):**
   - Provide the complete mental model in the opening section.
   - State the core thesis/purpose, define all primary pillars, trace the high-level workflow, and surface the critical boundary or takeaway.
2. **Draft Layer 2 (Structural Interconnections):**
   - Deepen how the parts collaborate and exchange information. Ground interactions in the unifying thread.
3. **Draft Layer 3 (Dynamics & Trade-offs):**
   - Address why choices were made, operational constraints, trade-offs against alternatives, and failure modes.
4. **Draft Layer 4 (Granular Reference):**
   - Place exact specifications, formulas, data tables, and verbatim code/command snippets here for readers who need implementation precision.

### Phase 4: Verify & Audit

Run the **Progressive Bloom Quality Gate**:

1. **Whole-Picture Test:** Can a reader understand the entire subject, all major actors, and the core conclusion from Layer 1 alone?
2. **No Topic Silos:** Did we avoid exhausting one topic's details before introducing the remaining topics?
3. **Natural Reading Progression:** Does each successive layer deepen understanding without requiring the reader to jump ahead to understand current concepts?
4. **Asset Integrity Check:** Confirm that all code blocks, data tables, commands, and numbers match the source material byte-for-byte.
