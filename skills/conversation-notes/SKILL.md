---
name: conversation-notes
description: Synthesizes multi-turn conversations into comprehensive, self-contained, book-like notes capturing all decisions, explanations, code snippets, and rationale adhering to ASD-STE100 plain language. Use when wrapping up a session, summarizing a long discussion, or compiling project documentation from chat history.
---

# Conversation to Comprehensive Notes

Follow this protocol to transform a multi-turn conversation into structured, book-like reference documentation that an independent reader can understand without the original chat transcript.

---

## 1. Scope & Primary Deliverable

- **Timing:** Invoked during the final turn of a task or upon explicit request to synthesize a discussion.
- **Primary Deliverable:** One comprehensive, stand-alone reference document containing full technical context, architectural rationale, and verified artifacts.
- **Intellectual Content Captured:**
  - Core questions, problem statements, and evolving requirements.
  - Explanations, architectural decisions, and conceptual models.
  - Discarded alternatives, failed experiments, and why they were abandoned.
  - Commands, flags, code diffs, configuration keys, and verified tool findings.
  - Unresolved issues, remaining uncertainties, and future roadmap items.

---

## 2. Five-Phase Synthesis Protocol

Execute the following five phases sequentially:

### Phase 1: Atomic Conversation Audit

- Review every turn, prompt, tool execution result, and file inspected in the session.
- Construct an atomic ledger using the **Atomic Conversation Ledger Schema (Appendix A)** (`A001`, `A002`, ...), cataloging speaker, type, substantive contribution, resolution status, and dependencies.

### Phase 2: Conceptual Index & Gap Deduction

- Reorganize chronological turns into an optimal conceptual learning dependency order.
- Merge fragmented discussions from separate turns into unified thematic sections.
- Position rejected alternatives and failure analyses directly beside the final chosen decisions.
- **Deduce Understanding Gaps Before Blueprinting:**
  - Identify logical leaps, unstated prerequisites, missing definitions, or unexplained background details assumed during conversation.
  - Determine exactly what background information is missing and identify where it fits within the conceptual dependency order.
  - Label background additions with `[Added for completeness]` in analysis sections so readers distinguish session discoveries from inferred context.

### Phase 3: Structural Blueprint & Micro-Formatting

- Construct a clean, shallow heading hierarchy ($H_2 / H_3$) incorporating both the audited discussion items and the deduced gap-fillers into their canonical positions.
- Establish standard section structure:
  1. **Executive Purpose & Scope:** High-level problem statement and final outcome.
  2. **System Context & Prerequisites:** Background concepts and environment assumptions.
  3. **Architecture & Decisions:** Ordered technical choices and trade-offs.
  4. **Implementation Artifacts:** Exact code diffs, CLI commands, and configuration keys.
  5. **Discarded Alternatives:** Explicit record of rejected options and failure rationales.
  6. **Unresolved Gaps & Next Steps:** Concrete future work items.
- Plan Bullet-First micro-formatting: bold category anchors for technical specifications, parameters, and analysis.

### Phase 4: Draft Comprehensive Notes (ASD-STE100 Standard)

Draft the full documentation adhering strictly to ASD-STE100 plain language principles:

- **Active Voice & Affirmative Sentences:** State mechanisms and data flows directly. Avoid passive voice and roundabout constructions.
- **Short Sentences:** Restrict sentences to one primary technical idea.
- **Explicit Terminology:** Define technical terms and acronyms on first use. Use a single consistent word for a given technical concept; never rotate synonyms for stylistic variation.
- **Unambiguous Referents:** Replace ambiguous pronouns (`it`, `this`, `they`) with explicit entity names. Purge conversational filler, hollow affirmations, and corporate buzzwords.
- **Exact Technical Fidelity:** Preserve exact command flags, configuration keys, file paths, code snippets, and error strings verbatim.

### Phase 5: Completeness & Traceability Audit

Before finalizing the deliverable, verify that:

- 100% of decisions, tool discoveries, code changes, and rationales from the Phase 1 ledger are accurately represented without silent omission.
- All deduced understanding gaps from Phase 2 reside in their appropriate blueprint sections.
- All prose adheres to the ASD-STE100 plain language standard with zero walls of dense narrative text.

---

## Appendix A: Atomic Conversation Ledger Schema

When capturing atomic contributions before drafting:

| Field              | Description                            | Allowed Values / Examples                                                 |
| :----------------- | :------------------------------------- | :------------------------------------------------------------------------ |
| **Atomic ID**      | Stable unique identifier               | `A001`, `A002`, `A003`                                                    |
| **Turn**           | Message number or origin index         | `Turn 1`, `Turn 3`                                                        |
| **Source**         | Originating speaker or tool            | `User`, `Assistant`, `Tool: run_command`, `File`                          |
| **Atomic Content** | Exact substantive statement or finding | Concise statement of the contribution                                     |
| **Status**         | Resolution state                       | `Introduced`, `Accepted`, `Revised`, `Rejected`, `Resolved`, `Unresolved` |
| **Relationships**  | Dependencies and causal links          | `Depends on A001`, `Contradicts A004`, `Alternative to A010`              |
