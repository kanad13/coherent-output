---
name: repo-evergreen-sync
description: Synchronizes an entire repository against recent changes, resolving systemic ripple effects, obsolete conventions, contract drift, and temporal documentation clutter. Use when synchronizing docs with code changes, propagating modifications across dependent assets, or performing repository-wide evergreen audits.
---

# Evergreen Repository Synchronization

Use this skill to propagate recent changes across the entire repository, resolve cascading drift, eliminate architectural split-brain, and ensure living files describe current operational reality.

---

## 1. Operating Protocol & Session Intent Audit

Every evergreen synchronization pass is anchored to a specific functional delta:

1. **Pre-Commit Session Diff Audit (Inline Intent & Comments):**
   - Before finalizing or committing functional code, inspect the active session's git diff (`git diff HEAD` or unstaged changes).
   - **Inline Intent Audit ("Why, Not What"):** For every non-obvious logic block, new algorithmic step, configuration branch, or error handling path introduced in this session, verify that comments explain the underlying business rationale, architectural invariant, or constraint.
   - **Syntax Echo Purge:** Eradicate any comments that merely narrate what the programming syntax mechanically executes (e.g., `# loop over items`, `// return result`).
   - **Residue Purge:** Delete commented-out code blocks completely, remove temporary debug statements (`print`, `console.log`), and purge scratchpad notes.
   - **Scope Clarity:** While runtime code logic in untouched legacy files is immune from silent refactoring, _comments and docstrings on files touched in the active session must be made pristine before anchoring_.
2. **Anchor the Functional Change:**
   - Commit the verified functional work using [commit-scribe](../commit-scribe/SKILL.md).
   - The resulting commit (or `HEAD` if already committed) serves as the **Anchor Delta**.
3. **Route Historical Context to Git:**
   - Record why components were superseded, why migrations occurred, or what technical debt was addressed in the Git commit message body.
   - Keep living files (`*.md`, source code, configs, schemas, templates) strictly present-tense and operational.

---

## 2. Systemic Ripple Investigation

Do not limit inspection to the files modified in the anchor delta. Reason about the entire repository as an interconnected graph of assets (code, documentation, schemas, templates, configs, scripts, and tests).

Audit the repository using these investigative inquiries:

### 1. Conceptual & Architectural Coherence

- What fundamental mechanism, convention, or domain model did this change alter?
- Did this change introduce a new paradigm or pattern? If so, does the repository now have split-brain syndrome where older files follow a conflicting pattern?
- Synchronize architecture diagrams, sequence flows, and Architecture Decision Records (ADRs) to match the new reality.

### 2. Operational & Workflow Parity

- If a developer or automated agent clones this repository right now, do the documented setup steps, onboarding guides, and runbooks work?
- Were environment variables, runtime versions, dependencies, build commands, CLI flags, or configuration keys altered?
- Update all affected usage examples, onboarding guides, and configuration references to match executable reality.

### 3. Interface & Contract Surface

- What consumers, imports, schemas, templates, prompt contracts, or tests depend on the modified components?
- Verify that parameter types, default values, error modes, and response formats are in 100% agreement across both implementation and documentation.

### 4. Redundancy, Shadowing & Supersession

- Does this new addition make an existing utility, script, helper, or document obsolete?
- **In Source Code:** Leave runtime code logic intact per engineering integrity standards. Record duplicate helpers, wrapper proliferation, or dead implementations in the **Technical Debt & Architectural Findings** catalog.
- **In Documentation & Assets:** Eliminate semantic duplication. Merge redundant materials into a single source of truth and delete superseded documentation files.

### 5. Truth Parity & Contradiction Audit

- Search the entire repository for claims, assertions, or diagrams that the anchor change rendered inaccurate.
- Correct all diverging statements so that no two files assert contradictory facts about system behavior.

### 6. Discoverability & Navigation

- Are newly created files, tools, rules, or skills registered in their parent directory index and the root `README.md`?
- Ensure every index entry has an accurate, concise summary and a valid relative link.

### 7. Test Contract Parity & Gap Detection

- **Regression Check:** Run the repository test suite (`./scripts/verify.sh` or the repo's test runner) to ensure recent changes introduced no regressions.
- **Contract Agreement:** Verify that modified function signatures, schemas, or CLI flags did not leave behind broken mocks, stale assertions, or skipped tests.
- **Scope Boundary:** Do not attempt full test strategy redesign or test harness overhaul inside an evergreen pass. If a newly added feature or architectural tier lacks test coverage, log a **Test Coverage Gap** in the deliverables and invoke or recommend [test-strategist](../test-strategist/SKILL.md).

---

## 3. Evergreen Sanitation Discipline

Apply these holistic standards to every touched and dependent asset:

- **Timeless Present Reality:**
  - Eradicate inline changelogs, version deltas, and patch notes (e.g., `*Added in v2*`, `[Fixed in Sprint 4]`).
  - Purge references, diagrams, and tombstones of superseded or sunset components from living documentation.
  - Describe what the system _is_, not how it historically arrived here.
- **Intent Grounding ("Why, not What"):**
  - Ensure code comments and specifications capture design invariants, non-obvious business rationale, and safety constraints.
  - Eradicate syntax narration (`# loop over items`) and leftover scratchpads.
  - If legacy code intent cannot be verified from evidence, log `[Unverified Intent]` in the Technical Debt catalog rather than guessing.
- **Contract Precision:**
  - Match docstrings, parameter tables, and schema declarations to runtime reality with 100% precision.
  - Preserve syntax-critical headers (shebangs, frontmatter) and non-commentable formats (JSON) intact.

---

## 4. Technical Debt Taxonomy

When code defects, architectural fragmentation, or legacy anti-patterns are uncovered during the synchronization pass, do not alter runtime logic. Record them in the **Technical Debt & Architectural Findings** catalog under these classifications:

1. **Shadow Logic & Wrapper Proliferation:** Redundant helper functions or wrappers bypassing existing implementations.
2. **Defensive Over-Engineering:** Excessive abstraction, factories, or complex patterns in simple local tools.
3. **Dependency Fragmentation:** Third-party imports used where standard library primitives or existing sibling utilities suffice.
4. **Hardcoded Machine-Specific Paths:** Local absolute paths (`/Users/...`, `C:\...`) that should be dynamic or relative.
5. **Prior Collapse & Modal Defaulting:** Bypassing repository-native schemas or conventions in favor of generic patterns.
6. **Unverified Legacy Intent:** Complex, non-obvious logic lacking tests or documentation where intent cannot be verified from evidence.
7. **Test Coverage Gaps:** Untested public interfaces, missing edge-case assertions, or absent integration harnesses flagged for [test-strategist](../test-strategist/SKILL.md).

---

## 5. Verification & Reconciliation Commit

1. **Execute Verification:**
   - Run the project test suite, linters, and verification scripts.
   - Verify link integrity and confirm runtime logic is unmodified.
2. **Commit Synchronization Pass:**
   - Stage all updated documentation, docstrings, indexes, and cross-references.
   - Commit and push using [commit-scribe](../commit-scribe/SKILL.md):
     ```text
     docs(repo): synchronize repository documentation and contracts to evergreen standard
     ```
3. **Deliverable Summary:**
   - Summarize the synchronized files, resolved cascading impacts, and cataloged technical debt.
