---
name: conversation-notes
description: Synthesizes multi-turn conversations into comprehensive, self-contained, book-like notes capturing all decisions, explanations, code snippets, and rationale. Use when wrapping up a session, summarizing a long discussion, or compiling project documentation from chat history.
---

# Conversation to Comprehensive Notes

Follow this 6-phase protocol to transform a multi-turn conversation into structured, book-like reference documentation.

---

## 1. Scope & Primary Deliverable

- **Timing:** Invoked during the final turn of a task or upon explicit request to synthesize a discussion.
- **Primary Deliverable:** One comprehensive, stand-alone reference document that an independent reader can understand completely without accessing the original chat transcript.
- **Intellectual Content Captured:**
  - Core questions, problem statements, and evolving requirements.
  - Explanations, architectural decisions, and conceptual models.
  - Discarded alternatives, failed experiments, and why they were abandoned.
  - Commands, flags, code diffs, configuration keys, and verified tool findings.
  - Unresolved issues, remaining uncertainties, and future roadmap items.

---

## 2. Six-Phase Synthesis Protocol

### Phase 1: Atomic Conversation Audit

- Review every turn, prompt, tool execution result, and file inspected in the session.
- For deep syntheses, construct an atomic ledger using the **Atomic Conversation Ledger Schema (Appendix A)** (`A001`, `A002`, ...), cataloging speaker, type, resolution status, and dependencies.

### Phase 2: Canonical Conceptual Index

- Reorganize chronological turns into an optimal conceptual learning dependency order (e.g., Fundamentals → Architecture → Implementation → Verification → Runbook).
- Merge fragmented discussions from separate turns into authoritative, unified sections.
- Position rejected alternatives and failure analyses directly beside the final chosen decisions.

### Phase 3: Structural Blueprint & Micro-Formatting

- Establish a clean, shallow heading hierarchy ($H_2 / H_3$).
- Apply Bullet-First micro-formatting to technical specifications, command parameters, and analysis.

### Phase 4: Autonomously Fill Understanding Gaps

- Identify logical leaps, missing prerequisites, or unexplained background details assumed during conversation.
- Close these gaps with concise, first-principles explanations so the document is completely self-contained.
- Label substantial background additions with `[Added for completeness]` in analysis summaries.

### Phase 5: Draft the Comprehensive Notes

- Draft the full documentation, preserving exact technical nomenclature, command flags, configuration keys, and code samples.
- Structure with Title, Executive Purpose, Chapter Sections, Decision History, and Next Steps.

### Phase 6: Completeness & Traceability Audit

- Verify that 100% of decisions, tool discoveries, code changes, and rationale from the chat history are accurately represented without silent omission.

---

## Appendix A: Atomic Conversation Ledger Schema

When capturing atomic contributions before drafting:

| Field              | Description                            | Allowed Values / Examples                                                                          |
| :----------------- | :------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **Atomic ID**      | Stable unique identifier               | `A001`, `A002`, `A003`                                                                             |
| **Turn**           | Message number or origin index         | `Turn 1`, `Turn 3`                                                                                 |
| **Source**         | Originating speaker or tool            | `User`, `Assistant`, `Tool: run_command`, `File`                                                   |
| **Type**           | Conceptual classification              | `Question`, `Fact`, `Definition`, `Explanation`, `Example`, `Decision`, `Failure`, `Open Question` |
| **Atomic Content** | Exact substantive statement or finding | Concise statement of the contribution                                                              |
| **Topic Thread**   | Conceptual category                    | `Architecture`, `Testing`, `Configuration`, `Debugging`                                            |
| **Status**         | Resolution state                       | `Introduced`, `Accepted`, `Revised`, `Rejected`, `Resolved`, `Unresolved`                          |
| **Relationships**  | Dependencies and causal links          | `Depends on A001`, `Contradicts A004`, `Alternative to A010`                                       |
