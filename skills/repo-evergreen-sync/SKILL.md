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
   - **Inline Intent Audit ("Why, Not What"):** For every code file, logic block, algorithmic step, or configuration branch touched in this session, verify that comments explain the underlying rationale, architectural invariant, or constraint.
   - **Syntax Echo Purge:** Eradicate comments that merely narrate what programming syntax mechanically executes (e.g., `# loop over items`, `// return result`).
   - **Residue Purge:** Delete commented-out code blocks completely, remove temporary debug statements (`print`, `console.log`), and purge scratchpad notes.
   - **Scope Clarity:** While runtime code logic in untouched legacy files is immune from silent refactoring, _comments and docstrings on files touched in the active session must be made pristine before anchoring_.
2. **Anchor the Functional Change:**
   - Commit the verified functional work using [commit-scribe](../commit-scribe/SKILL.md).
   - The resulting commit (or `HEAD` if already committed) serves as the **Anchor Delta**.
3. **Route Historical Context to Git:**
   - Record why components were superseded, why migrations occurred, or what technical debt was addressed in the Git commit message body.
   - Keep living files (`*.md`, source code, configs, schemas, templates) strictly present-tense and operational.

---

## 2. Adaptive Execution Topologies: Mode A vs. Mode B

Select execution topology based on repository scale:

### Mode A: Direct Multi-Lens Execution (Small to Medium Codebases / 1–15 Files)

The executing agent runs all reconciliation lenses directly in an atomic, unified pass:

1. **Lens A (Code & Docstring Sanitation):** Inspects touched files, purges comment smells, synchronizes docstrings, and catalogs technical debt.
2. **Lens B (Documentation & Index Sync):** Reconciles repository markdown, parent README indexes, and operational guides against runtime code.
3. **Lens C (Contract Reconciliation):** Verifies CLI flags, schemas, error states, and relative link integrity.

### Mode B: Orchestrated Multi-Agent Swarm (Large Codebases / >15 Files or Monorepos)

For large multi-module repositories, the orchestrating agent spawns read-only auditor subagents before central synthesis:

1. **Lens A Auditor Subagent (Read-Only):** Scans code files, extracts real signatures/types/flags, identifies lying docstrings and comment smells.
2. **Lens B Auditor Subagent (Read-Only):** Scans documentation, catalogs structural defects, and flags middle-loss thinning.
3. **Lens C Auditor Subagent (Read-Only):** Compares code contracts against doc claims, identifies asymmetric drift and broken links.
4. **Synthesis & Execution (Orchestrator — Write Access):** Merges findings, executes atomic in-place disk modifications, runs test suite, and commits changes.

---

## 3. Systemic Ripple Inquiries

Do not limit inspection to the files modified in the anchor delta. Reason about the entire repository as an interconnected graph using these inquiries:

1. **Conceptual & Architectural Coherence:** Did this change alter a fundamental mechanism, convention, or domain model? Resolve any architectural split-brain between old and new files.
2. **Operational & Workflow Parity:** Do documented setup steps, onboarding runbooks, environment variables, dependencies, and CLI flags match executable reality?
3. **Interface & Contract Surface:** Do consumers, imports, schemas, templates, and tests agree with modified parameter types, default values, and error modes?
4. **Redundancy, Shadowing & Supersession:** Does this change make an existing helper, utility, or document obsolete? Merge redundant documentation and log dead code in the Technical Debt catalog.
5. **Truth Parity & Contradiction Audit:** Eliminate diverging assertions across files so no two documents assert contradictory facts about system behavior.
6. **Discoverability & Navigation:** Ensure newly created files, tools, rules, or skills are registered in parent directory indexes and root documentation with valid relative links.
7. **Test Contract Parity & Gap Detection:** Run the test suite (`./scripts/verify.sh`). Log test coverage gaps and invoke or recommend [test-strategist](../test-strategist/SKILL.md).

---

## 4. Adaptive Information Accounting: Content Unit Tracking (`C001...`)

- **Routine Session Updates:** Apply lightweight diff-anchored updates directly.
- **Deep Repository Reconciliations / Major Rewrites:** To guarantee zero loss of technical nuance, extract all distinct factual statements, parameters, exceptions, and rules into unique Content IDs (`C001`, `C002`, ...):
  - Map each unit to a single canonical home in the Structural Blueprint.
  - Complete a Traceability Matrix verifying that 100% of units survive into revised docs or the Technical Debt catalog.

---

## 5. Technical Debt Taxonomy

When code defects, architectural fragmentation, or legacy anti-patterns are uncovered, do not alter runtime code logic. Record them in the **Technical Debt & Architectural Findings** catalog under these classifications:

1. **Shadow Logic & Wrapper Proliferation:** Redundant helper functions or wrappers bypassing existing implementations.
2. **Defensive Over-Engineering:** Excessive abstraction, factories, or complex patterns in simple local tools.
3. **Dependency Fragmentation:** Third-party imports used where standard library primitives or existing sibling utilities suffice.
4. **Hardcoded Machine-Specific Paths:** Local absolute paths (`/Users/...`, `C:\...`) that should be dynamic or relative.
5. **Prior Collapse & Modal Defaulting:** Bypassing repository-native schemas or conventions in favor of generic patterns.
6. **Unverified Legacy Intent:** Complex, non-obvious logic lacking tests where intent cannot be verified from evidence.
7. **Test Coverage Gaps:** Untested public interfaces, missing edge-case assertions, or absent integration harnesses flagged for [test-strategist](../test-strategist/SKILL.md).

---

## 6. Verification & Final Checklist

Before completing execution, verify that:

- [ ] Code runtime logic, algorithms, control flow, and variable names are 100% unmodified.
- [ ] All docstring signatures match actual parameters, types, defaults, and exceptions.
- [ ] All patch notes, version deltas, and backward-looking archaeology are eliminated.
- [ ] All enterprise bureaucracy and multi-tenant fluff are purged from single-developer repos.
- [ ] All heading/prose echoing and code block narrative paraphrasing are eliminated.
- [ ] All ghost references, deleted flags, and phantom capability claims are removed.
- [ ] Intermediate documentation sections maintain uniform depth without middle-loss thinning.
- [ ] All ordinary body lines follow the bullet-first Markdown specification with bold labels.
- [ ] All repository documentation links use portable relative paths and resolve correctly.
- [ ] Syntax compilation and runtime tests on modified code files pass with 0 errors.

---

## Appendix A: Zero-Tolerance Anti-Pattern Catalog

Enforce zero tolerance for these specific drift modes during reconciliation passes:

### 1. Documentation Drift Anti-Patterns

- **Patch-Note Infiltration:** Never append inline changelog notes or version deltas into living reference docs (e.g., `*Note: Updated in v2 to use DuckDB*`). Write exclusively in active present tense.
- **Backward-Looking Code Archaeology:** Never explain superseded architectures or dead frameworks in reference docs. Route historical context to Git commit messages.
- **Enterprise & Multi-Tenant Bureaucracy:** Omit multi-stage production tiers (`staging/prod`), PR contributor guidelines, SLA disclaimers, SOC2 checklists, or multi-tenant permission models from single-developer repos.
- **Hedging & Conversational Padding:** Purge weak modals (`You might want to consider...`), filler, apologies, and closing pleasantries. Use direct operational modality (`must`, `should`, `may`).
- **Echoing & Redundant Stating:** Never restate heading titles in the first sentence beneath them. Never write prose paragraphs before or after a code block that merely narrate what the code demonstrates.
- **Ghost & Orphan References:** Eliminate markdown links, CLI flag descriptions, environment variables, or imports referencing deleted files, removed flags, or dead functions.
- **Attention Thinning & "Middle-Loss":** Maintain identical rigor, tabular detail, and constraint completeness across every section; never allow intermediate reference sections to collapse into generic prose.
- **Semantic Duplication across Files (DRY Violation):** Establish a Single Source of Truth in one canonical file and link to it using portable relative Markdown links.

### 2. Code & Comment Drift Anti-Patterns

- **Trivial Echo Comments:** Purge comments that merely restate visible syntax mechanics (e.g., `i += 1  # increment i`, `// return result`).
- **Tutorial & Narrative Comments:** Purge stream-of-consciousness narrative comments (e.g., `# Here we loop over items to check if...`).
- **Session & Attribution Tags:** Purge assistant attribution markers, turn tags, author stamps, and bugfix tickets (e.g., `# Fixed by Assistant on Turn 4`).
- **Dead Code Graveyards:** Purge commented-out legacy code blocks completely (`# def old_impl(): ...`). Rely entirely on Git for version history.
- **Inconsistent Docstrings:** Enforce uniform docstrings matching host language: Google style (Python), JSDoc/TSDoc (JS/TS), Rustdoc (Rust), Go doc (Go).
- **Lying Docstrings:** Parameter types, return types, exceptions, and defaults must match actual runtime code with 100% precision.
