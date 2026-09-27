---
name: conversation-notes
description: Synthesizes multi-turn conversations into comprehensive, self-contained, book-like notes capturing all decisions, explanations, code snippets, and rationale. Use when wrapping up a session, summarizing a long discussion, or compiling project documentation from chat history.
---

# Conversation to Comprehensive Notes

Follow this 6-phase protocol to transform a multi-turn conversation into structured, book-like reference documentation.

---

## 1. Scope & Primary Deliverable

- **Timing:** Invoked during the final turn of a task or upon explicit request to summarize the conversation.
- **Primary Deliverable:** One comprehensive, stand-alone reference document that an independent reader can understand completely without accessing the original chat transcript.
- **Intellectual Content Captured:**
  - Core questions and evolving requirements.
  - Explanations, visual models, and architectural decisions.
  - Rejected alternatives and why they were abandoned.
  - Code snippets, commands, and verified tool findings.
  - Remaining uncertainties and future roadmap items.

---

## 2. Six-Phase Synthesis Protocol

### Phase 1: Atomic Conversation Audit

- Review every conversation turn, user prompt, and assistant response.
- Create an atomic ledger of contributions: problems solved, discoveries, decisions, and checks.

### Phase 2: Canonical Conceptual Index

- Reorganize the chronological discussion into a logical conceptual outline (e.g., Fundamentals → Architecture → Implementation → Operational Runbook).
- Merge repeated discussions into single authoritative sections.

### Phase 3: Articulation Blueprint

- Establish a consistent heading structure ($H_2 / H_3$).
- Apply Bullet-First micro-formatting to technical specifications and analysis.

### Phase 4: Autonomously Fill Understanding Gaps

- Identify any minor logical leaps or unexplained background details that were assumed in conversation.
- Expand explanations so the final notes stand completely self-contained.

### Phase 5: Draft the Comprehensive Notes

- Draft the full documentation, preserving exact technical nomenclature, command flags, configuration keys, and code samples.
- Structure with Title, Executive Purpose, Chapter Sections, and Next Steps.

### Phase 6: Completeness Audit

- Verify that 100% of decisions, code changes, and rationale from the chat history are accurately represented.
