---
name: repo-evergreen-sync
description: Synchronizes the entire repository after coding changes, resolving systemic drift across code, contracts, documentation, and tests. Analyzes the session diff and conversation intent, audits ripple impacts, formulates an atomic synchronization plan, adapts test suites via test-strategist, applies updates, verifies regressions, and commits via commit-scribe. Use immediately after implementing, editing, or refactoring code.
---

# Evergreen Repository Synchronization Engine

Follow this protocol immediately after a coding session to inspect recent functional changes, audit systemic ripple effects across the entire codebase, adapt tests, update documentation, and commit the reconciled state.

---

## 1. Operating Mandates & Invariants

- **Dual-Context Grounding:** Never audit in isolation from the coding session. Always ground ripple analysis in both the executable `git diff` and the conversational context (architectural rationale, trade-offs, and user preferences).
- **The Zero-Loss Invariant:** When updating documentation, manifests, or interfaces, preserve 100% of substantive technical data, parameters, prerequisites, edge cases, and architectural constraints.
- **Active Present-Tense Invariant:** Living files (`*.md`, source code, configs, schemas) must describe current operational state. Route historical changelogs, superseded frameworks, and version deltas exclusively to Git commit history.
- **ASD-STE100 & Bullet-First Standard:** All updated documentation must adhere to ASD-STE100 plain language (short active sentences, direct verbs, defined terms) and bullet-first Markdown hierarchy (bold category anchors, declarative child bullets, zero walls of plain prose).

---

## 2. Six-Phase Synchronization Protocol

Execute the following six phases sequentially:

### Phase 1: Ingest Session Context & Git Diff

Anchor the synchronization pass to the active session delta:

- **Extract Session Intent:** Review conversation history to understand _why_ code was added, modified, or removed, what requirements were satisfied, and what design choices were approved.
- **Inspect the Git Diff:** Run `git diff HEAD`, inspect unstaged/staged modifications, and identify all touched files, exported symbols, CLI arguments, and configuration keys.
- **Inline Intent & Residue Audit:** On files touched in the coding session:
  - Confirm non-obvious algorithms and invariants contain explanatory comments ("Why, Not What").
  - Purge syntax echo comments (`# loop over items`), commented-out legacy code, temporary debug logs (`console.log`, `print`), and scratchpad notes.

### Phase 2: Systemic Ripple & Test Audit

Perform a deep, diligent audit pass across the entire repository to uncover cascading drift:

- **Surface A: Code Consumers & Interface Contracts:**
  - Trace all imports, call sites, exported types, parameter signatures, and return values affected by the change.
  - Identify calling code, helper utilities, or sibling modules that require updates to maintain architectural parity.
- **Surface B: Documentation, Manifests & Navigation:**
  - Check root `README.md`, directory-level README indexes, operational runbooks, and architectural guides.
  - Verify that newly added, renamed, or deleted files, tools, rules, or skills are registered in parent manifests and documentation navigation tables.
  - Audit Markdown link integrity across touched documents using portable relative links.
- **Surface C: Test Portfolio Audit via [test-strategist](../test-strategist/SKILL.md):**
  - Evaluate existing test suites against modified functionality.
  - Identify broken assertions, obsolete test cases that need pruning, and newly introduced code paths or edge cases that lack coverage.
  - Determine the concrete testing actions required (new test cases, updated fixtures, or harness adaptations).

### Phase 3: Atomic Drift Ledger & Synchronization Plan

Construct a structured **Atomic Drift Ledger** (`D001`, `D002`, ...) detailing all identified discrepancies:

| Drift ID | Surface | Affected Component  | Drift Description                                  | Required Resolution                       |
| :------- | :------ | :------------------ | :------------------------------------------------- | :---------------------------------------- |
| `D001`   | Docs    | `README.md`         | Skill table missing newly added command            | Add entry and update total skill count    |
| `D002`   | Tests   | `tests/test_api.py` | Signature change breaks legacy parameter assertion | Adapt test fixture to new signature       |
| `D003`   | Code    | `src/client.ts`     | Consumer calls removed optional argument           | Align client method call with updated API |

Surface the synchronization plan clearly: outline what is currently drifting, which files need updates, and what tests will be adapted.

### Phase 4: Execute Synchronization Updates

Apply all required modifications across the repository:

- **Code & Contract Updates:** Update affected consumers, wrappers, configuration schemas, and environment variable references.
- **Test Suite Updates:** Implement, adapt, or prune test cases as strategized in Phase 2.
- **Documentation Refactoring:** Update affected documentation, parent tables, and operational runbooks conforming strictly to ASD-STE100 plain language and bullet-first structure.

### Phase 5: Regression Testing & Automated Verification

Verify that the synchronization pass introduced zero regressions:

- Execute the repository test suite and verification runners (`./scripts/verify.sh`).
- Verify that:
  - 100% of tests pass with 0 errors or unexpected skips.
  - 0 broken relative Markdown links exist.
  - 0 Prettier formatting errors remain.
  - Output conforms to the **Zero-Tolerance Anti-Pattern Catalog (Appendix A)**.

### Phase 6: Commit & Upstream Sync via [commit-scribe](../commit-scribe/SKILL.md)

Package the synchronized state into a clean, atomic Git commit:

- Activate [commit-scribe](../commit-scribe/SKILL.md) to stage all reconciled files (`git add <files>`).
- Construct a high-context structured commit message documenting:
  - **Problem:** Drift introduced by recent functional additions or refactors.
  - **Solution:** Reconciled documentation, adapted test suites, and synchronized consumers.
  - **Decisions:** Non-obvious trade-offs made during synchronization.
  - **Implementation:** List of touched components and surfaces.
- Push the commit to the upstream tracking remote (`git push`).
- Report back to the user with the commit hash, modified files, test verification results, and upstream status.

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
