---
trigger: always_on
description: "Repository integrity guardrails, task-scoped logic immunity, blast radius scoping, evidence grounding, code comment invariants, docstrings, and history hygiene."
---

# Engineering Integrity & Codebase Standards

These standards govern code runtime preservation, workspace coherence, evidence grounding, inline documentation, and history hygiene across the repository.

---

## 1. Task-Scoped Code Logic Immunity

- **Documentation Pass Scope:**
  - Keep runtime code logic, algorithm behavior, data structures, public symbol names, and execution semantics 100% intact when editing documentation, specifications, docstrings, type annotations, or inline comments.
  - Restrict modifications strictly to documentation files, specifications, docstrings, non-breaking type hints, and rationale comments during documentation tasks.
- **Defect Reporting Without Silent Alteration:**
  - Do not silently alter runtime code when discovering defects, dead functions, wrapper proliferation, or architectural anti-patterns during a documentation or review pass.
  - Record discovered defects in the task deliverable or technical debt notes for an independent refactoring pass.
- **Implementation Pass Authorization:**
  - Modify implementation code surgically when the explicit task is a feature implementation, bugfix, or test failure remediation.

---

## 2. Blast Radius Scoping & Workspace Coherence

- **Downstream Impact Evaluation:**
  - Verify whether modifying symbol names, signatures, configurations, or schemas creates contradictions, broken references, or stale documentation elsewhere in the workspace before concluding an edit.
- **Zero Inconsistency Standard:**
  - Ensure that documentation, tests, and actual code remain in 100% synchronization.
  - Never leave two parts of a repository with contradictory assertions about system behavior.
- **Excluded Paths:**
  - Ignore version control metadata (.git), virtual environments (.venv, node_modules), build directories (dist, build, **pycache**), and IDE artifacts during blast-radius audits.

---

## 3. Closed-World Evidence Grounding

- **Mandatory Evidence Sources:**
  - Ground every technical assertion, rationale comment, docstring note, and architectural explanation in concrete evidence from verified sources.
- **Source Taxonomy:**
  - Source 1: Active Session Context, consisting of direct instructions, user requirements, and verified changes made during the active session.
  - Source 2: Repository Commit History, consisting of commit messages, PR descriptions, and architectural notes in the local Git log.
  - Source 3: Executable Test Assertions, consisting of test suites, assertion statements, and mocks demonstrating behavior or preventing failure modes.
  - Source 4: Verifiable System Constants & Specifications, consisting of operating system constraints, protocol standards, RFCs, hardware limits, and official vendor or language documentation.

---

## 4. Code Documentation & Docstring Invariants

- **The Intent Imperative:**
  - Document the underlying business rationale, algorithm invariants, safety constraints, and non-obvious engineering choices that make the code necessary.
  - Explain why the code exists rather than what the syntax executes.
- **Syntax Echo Elimination:**
  - Never write comments that merely narrate what the programming syntax mechanically executes.
  - Delete comments that mirror mechanical code operations.
- **Tutorial Narrative Purge:**
  - Eradicate stream-of-consciousness narration in source comments.
  - Use direct, concise affirmative statements.
- **Docstring Contract Parity:**
  - Match docstring parameter lists to actual function signatures 100%.
  - Document exact return types, empty or null conditions, and all explicitly raised exceptions.
  - Adhere strictly to the established docstring convention of the target language and project.
- **Educational Override Clause:**
  - Keep the production "Why, Not What" standard active by default.
  - Apply comprehensive line-by-line explanations and syntax-teaching comments only when the user explicitly invokes the /code-beginner-comments skill.

---

## 5. Evergreen State & History Hygiene

- **Documentation Temporal Hygiene:**
  - Eliminate relative temporal references such as "recently added", "in sprint 12", "new in version 2.1", "work in progress", or "to be implemented soon".
  - Eradicate changelog clutter, deprecated sunset warnings, and historic patch notes from documentation.
  - Describe present system behavior using active present-tense verbs.
  - Rely on Git history for chronological evolution.
- **Code Artifact & Residue Purge:**
  - Delete commented-out code blocks completely.
  - Rely entirely on Git version control for historical code retrieval.
  - Remove preliminary planning notes, task lists, and scratchpad markers before concluding tasks.
  - Remove assistant attribution stamps, author tags, and ticket annotations from source code.
