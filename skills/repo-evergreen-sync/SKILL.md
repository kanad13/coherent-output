---
name: repo-evergreen-sync
description: Synchronizes the entire repository after coding changes, resolving systemic drift across code, contracts, documentation, and tests. Analyzes session diff and conversation intent, enforces Google-style module prefacing and "Why, Not What" comment standards, audits ripple impacts, adapts test suites via test-strategist, refactors docs with ASD-STE100, verifies regressions, and commits via commit-scribe. Use immediately after implementing, editing, or refactoring code.
---

# Evergreen Repository Synchronization Engine

Follow this protocol immediately after a coding session to inspect recent functional changes, audit systemic ripple effects across the entire codebase, adapt tests, update documentation, and commit the reconciled state.

---

## 1. Code Commenting & Documentation Standards

Apply these standards across all code and documentation modified or created during synchronization:

### Google-Style File Prefacing & Docstring Standards

- **Top-Level Module Docstrings:** Every source code file (`*.py`, `*.ts`, `*.go`, `*.rs`, etc.) must begin with a top-level module docstring/header explaining:
  - **Single-Line Summary:** Concise definition of the module's core responsibility.
  - **Architectural Purpose ("Why It Exists"):** Why this file exists, what system role it fulfills, and how it collaborates with sibling components.
  - **Approach & Invariants:** High-level algorithmic approach, key invariants, and domain constraints.
- **Function & Class Docstrings (Google Style):**
  - Imperative summary line describing the operational contract.
  - Detail block describing non-obvious design assumptions, edge cases, or side effects.
  - Structured sections: `Args:` / `@param`, `Returns:` / `@returns`, `Raises:` / `@throws`.
  - **Zero Lying Docstrings:** Parameter names, types, defaults, and return signatures must match runtime code with 100% precision.

### Strict "Why, Not What" Commenting Standard

- **The Purpose & Approach Invariant:** Code syntax already demonstrates _what_ happens and _how_ it executes. Comments must exclusively capture the _why_—the underlying intent, business logic, algorithmic approach, performance trade-off, or architectural invariant.
- **Trivial Syntax Echo Purge:** Eradicate comments that merely narrate visible syntax mechanics (e.g., `# loop over items`, `// return true`, `count += 1  # increment count`).
- **Residue Purge:** Delete commented-out legacy code blocks completely, purge temporary debug statements (`console.log`, `print`, `debugger`), and delete scratchpad notes.

### Living Documentation & ASD-STE100 Standards

- **Active Present-Tense Invariant:** Living files (`*.md`, source code, configs, schemas) must describe current operational state. Never append changelog notes or version deltas into living reference docs (e.g., `*Note: Updated in v2 to use DuckDB*`). Route historical context exclusively to Git commit messages.
- **ASD-STE100 Plain Language:** Write short, active sentences in affirmative voice. Limit each sentence to one main idea. Define technical terms on first use. Maintain a single consistent term for each concept; never rotate synonyms.
- **Bullet-First Hierarchy:** Structure lists using bold category anchors (`- **Anchor:**`) with un-bolded declarative child bullets. Eliminate walls of dense paragraph prose. Eliminate heading echoing (never restate heading titles in the first sentence beneath them).
- **Single Source of Truth:** Establish canonical documentation in one location and link to it using portable relative Markdown links. Avoid duplicate assertions across disparate files.

---

## 2. Six-Phase Synchronization Protocol

Execute the following six phases sequentially:

### Phase 1: Ingest Session Context & Git Diff

Anchor the synchronization pass to the active session delta:

- **Extract Session Intent:** Review conversation history to understand _why_ code was added, modified, or removed, what requirements were satisfied, and what design choices were approved.
- **Inspect the Git Diff:** Run `git diff HEAD`, inspect unstaged/staged modifications, and identify all touched files, exported symbols, CLI arguments, and configuration keys.
- **Audit Code Comments & Docstrings:** On all files touched in the coding session, enforce Section 1 standards (module headers, Google-style docstrings, "Why, Not What" comments, and dead-code removal).

### Phase 2: Systemic Ripple & Test Audit

Perform a deep, diligent audit pass across the entire repository to uncover cascading drift:

- **Surface A: Code Consumers & Interface Contracts:**
  - Trace all imports, call sites, exported types, parameter signatures, and return values affected by the change.
  - Identify calling code, helper utilities, or sibling modules that require updates to maintain architectural parity.
- **Surface B: Documentation, Manifests & Navigation:**
  - Check root `README.md`, directory-level README indexes, operational runbooks, and architectural guides.
  - Verify that newly added, renamed, or deleted files, tools, rules, or skills are registered in parent manifests and documentation navigation tables.
  - Audit Markdown link integrity across touched documents using portable relative links.
- **Surface C: Test Portfolio Audit via test-strategist skill:**
  - Activate the test-strategist skill to evaluate existing test suites against modified functionality.
  - Identify broken assertions, obsolete test cases that need pruning, and newly introduced code paths or edge cases that lack coverage.
  - Determine the concrete testing actions required (new test cases, updated fixtures, or harness adaptations).

### Phase 3: Atomic Drift Ledger & Synchronization Plan

Construct a structured **Atomic Drift Ledger** (`D001`, `D002`, ...) detailing all identified discrepancies:

| Drift ID | Surface | Affected Component  | Drift Description                                  | Required Resolution                       |
| :------- | :------ | :------------------ | :------------------------------------------------- | :---------------------------------------- |
| `D001`   | Docs    | `README.md`         | Skill table missing newly added command            | Add entry and update total skill count    |
| `D002`   | Tests   | `tests/test_api.py` | Signature change breaks legacy parameter assertion | Adapt test fixture to new signature       |
| `D003`   | Code    | `src/client.ts`     | Consumer calls removed optional argument           | Align client method call with updated API |

Surface the synchronization plan clearly to the user before proceeding: outline what is currently drifting, which files need updates, and what tests will be adapted.

### Phase 4: Execute Synchronization Updates

Apply all required modifications across the repository:

- **Code & Contract Updates:** Update affected consumers, wrappers, configuration schemas, and environment variable references conforming to Section 1 commenting standards.
- **Test Suite Updates:** Implement, adapt, or prune test cases as strategized in Phase 2.
- **Documentation Refactoring:** Update affected documentation, parent tables, and operational runbooks conforming strictly to Section 1 ASD-STE100 and Bullet-First standards.

### Phase 5: Automated Verification & Regression Testing

Verify that the synchronization pass introduced zero regressions:

- Execute the repository test suite and verification runners (e.g., `<repo_root>/scripts/verify.sh`, `npm test`, or `pytest` from the repository root).
- Audit the change set against the **Pre-Commit Verification Checklist (Section 3)**.
- Confirm:
  - 100% of tests pass with 0 errors or unexpected skips.
  - 0 broken relative Markdown links exist.
  - 0 Prettier formatting errors remain.

### Phase 6: Commit & Upstream Sync via commit-scribe skill

Package the synchronized state into a clean, atomic Git commit:

- Activate the commit-scribe skill to stage all reconciled files (`git add <files>`).
- Construct a high-context structured commit message documenting:
  - **Problem:** Drift introduced by recent functional additions or refactors.
  - **Solution:** Reconciled documentation, adapted test suites, and synchronized consumers.
  - **Decisions:** Non-obvious trade-offs made during synchronization.
  - **Implementation:** List of touched components and surfaces.
- Push the commit to the upstream tracking remote (`git push`).
- Report back to the user with the commit hash, modified files, test verification results, and upstream status.

---

## 3. Pre-Commit Verification Checklist

Before completing execution, confirm that all items are satisfied:

### Code & Comments

- [ ] Top-level Google-style module docstring present on every touched or created file.
- [ ] Class and function docstrings follow Google style with accurate parameters and return types.
- [ ] All comments explain "Why, Not What"; zero syntax echo comments exist.
- [ ] Zero dead code blocks, zero temporary debug statements, and zero scratchpad files remain.

### Documentation & Navigation

- [ ] All updated docs written in active present tense (zero patch notes or backward-looking deltas).
- [ ] All lists use Bullet-First hierarchy (bold category anchors, declarative child bullets, max 3 levels).
- [ ] Zero heading echoing (first sentence beneath a heading does not restate the heading title).
- [ ] Parent README manifests and root documentation index newly created or modified files.
- [ ] All relative Markdown links resolve to valid sibling files.

### Contracts & Tests

- [ ] CLI flags, schemas, configurations, and environment variables align across code, docs, and tests.
- [ ] Test suites adapted and passing with 0 errors via project verification runners (e.g., `<repo_root>/scripts/verify.sh` or local test runner).
- [ ] Prettier formatting verified with 0 warnings or syntax errors.
- [ ] Changes staged cleanly and committed via commit-scribe skill.
