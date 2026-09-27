---
trigger: always_on
description: "Repository integrity guardrails, blast radius scoping, code runtime logic immunity, cross-repo consistency, and evergreen documentation standards."
---

# Repository Integrity & Drift Prevention

## 1. Code Runtime Logic Immunity

When editing documentation, specifications, docstrings, type annotations, or inline comments in a codebase:

- **Preserve Runtime Logic:** Keep runtime code logic, algorithm behavior, data structures, public symbol names, and execution semantics 100% intact.
- **Scope Restriction:** Restrict modifications strictly to documentation files, specifications, docstrings, non-breaking type hints, and rationale comments.
- **Technical Debt Cataloging:** When you discover code defects, dead functions, wrapper proliferation, or architectural anti-patterns during a documentation or review pass, do **not** silently alter runtime code. Record them in an explicit Technical Debt catalog for an independent refactoring pass.

---

## 2. Blast Radius Scoping & Cross-Repo Coherence

Every change to code or documentation carries a blast radius across the repository:

- **Evaluate Downstream Impact:** Before concluding an edit, verify whether modifying symbol names, signatures, configurations, or schemas creates contradictions, broken references, or stale documentation elsewhere in the workspace.
- **Zero Inconsistency:** Ensure that documentation, tests, and actual code remain in 100% synchronization. Never leave two parts of a repository with contradictory assertions about system behavior.
- **Excluded Paths:** Ignore version control metadata (`.git`), virtual environments (`.venv`, `node_modules`), build directories (`dist`, `build`, `__pycache__`), and IDE artifacts.

---

## 3. Closed-World Evidence Grounding

Every technical assertion, rationale comment, docstring note, and architectural explanation must cite concrete evidence from one of four verified sources:

1. **Active Session Context:** Direct instructions, user requirements, and code changes made during the active session.
2. **Repository Commit History:** Commit messages, PR descriptions, and architectural notes in the local Git log.
3. **Executable Test Assertions:** Test suites, assertion statements, and mocks demonstrating the invariant or failure mode being prevented.
4. **Verifiable System Constants:** Operating system constraints, protocol standards (e.g., RFCs), hardware limits, and official vendor API contracts.

---

## 4. Evergreen Documentation Standard

Maintain all documentation in an evergreen, perpetual-present state:

- **Temporal Marker Purge:** Eliminate relative temporal references such as _"recently added"_, _"in sprint 12"_, _"new in version 2.1"_, _"work in progress"_, or _"to be implemented soon"_.
- **Archaeology & Tombstones:** Eradicate changelog clutter, deprecated sunset warnings, and historic patch notes embedded inside architectural guides. Keep historical evolution inside Git history; documentation must reflect the definitive, present operational truth.
- **Affirmative Present Tense:** Describe what the system is, has, and does using active present-tense verbs.
