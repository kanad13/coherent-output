---
name: repo-evergreen-sync
description: Executes autonomous, delta-anchored audit, documentation reconciliation, and intent synchronization across a repository. Use when synchronizing docs with code changes, cleaning doc drift, or performing evergreen repository audits.
---

# Evergreen Repository & Documentation Reconciliation

Follow this multi-phase protocol to synchronize repository documentation, specifications, docstrings, and inline rationale comments with actual code state.

---

## 1. Operational Mandate & Scoping Zones

Enforce two distinct operational zones:

- **Zone 1: Active Session Delta & Direct Blast Radius:**
  - Files, symbols, docs, and configurations modified or added during the active session.
  - _Mandate:_ Mandatory intent synthesis. Update all docstrings, READMEs, and specifications to achieve 100% parity with code changes.
- **Zone 2: Untouched Legacy Surface:**
  - Pre-existing code and documentation outside immediate session modifications.
  - _Mandate:_ Conservative sanitation. Remove syntax echoes, dead code, and temporal tombstones. If non-obvious logic lacks evidence, log `[Unverified Intent]` in the Technical Debt catalog rather than speculating.

---

## 2. The Three-Lens Analytical Framework

Apply three analytical lenses to every target file:

1. **Operational Drift & Contract Parity:** Do docstrings, CLI examples, schemas, and README instructions match executable reality?
2. **Temporal Sanitation & Evergreen Architecture:** Are there backward-looking archaeology notes ("new in sprint 4", "fixed bug 123", sunset notices)? Purge them in favor of present-tense evergreen descriptions.
3. **Signal-to-Noise & Intent Grounding:** Are code comments explaining _Why, not What_? Are syntax echoes, dead code, and attribution tags eradicated?

---

## 3. Phased Execution Protocol

### Phase 0: Grounding & Delta Ingestion

- Inspect git status, working tree diffs, and recent commits to identify the session delta.
- Catalog all modified functions, endpoints, classes, and architectural components.

### Phase 1: Content Inventory & Defect Diagnosis

- Map all documentation files and docstrings that reference modified components.
- Flag drift defects: stale parameter types, broken examples, outdated architecture diagrams, and missing rationale.

### Phase 2: Structural Blueprint Design

- Plan necessary in-place modifications across docs and docstrings.
- Ensure cross-repo consistency: verify that changes in one document do not contradict sibling documents.

### Phase 3: Code & Intent Sanitation (In-Place)

- Update affected function/module docstrings to reflect exact runtime parameters, return types, and errors.
- Clean inline comments: replace mechanistic syntax narration with business logic rationale and invariants.
- Eradicate commented-out code and scratchpad notes.

### Phase 4: Evergreen Document Synthesis (In-Place)

- Update user guides, architectural specs, and directory READMEs.
- Apply the Bullet-First Micro-Formatting standard to updated technical documentation.
- Maintain the Zero-Loss invariant: preserve all configuration parameters, limits, and modal constraints.

### Phase 5: Verification & Deliverables

- Verify all relative Markdown links, code snippets, and docstrings.
- Ensure runtime code logic remains completely intact.
- Emit the final deliverable report:
  1. **Executive Reconciliation Summary:** Files updated and drift issues resolved.
  2. **Technical Debt & Architectural Findings:** Unverified legacy logic or code defects cataloged for future refactoring.
  3. **Verification Certificate:** Explicit confirmation of code logic immunity, link integrity, and evergreen compliance.
