---
name: test-strategist
description: Formulates, audits, and maintains project-specific testing strategies in TESTING.md. Enforces universal verification invariants, tier selection, and assertion integrity. Use when defining test architectures, reviewing coverage gaps after changes, or resolving brittle tests. Do not invoke for routine single-test runs or prose-only documentation edits.
---

# Adaptive Test Strategy & Verification Protocol

Formulate, audit, and evolve repository test strategies using universal verification invariants and structured checklists. This skill does not prescribe a static, hardcoded test plan for all systems. The canonical test strategy belongs in the target project's `TESTING.md` (or the testing section in `README.md`). When invoked, evaluate project reality, formulate or reconcile `TESTING.md`, enforce universal verification invariants, and verify user-facing features directly.

---

## 1. The Canonical Testing Strategy Invariant (`TESTING.md`)

The target repository's `TESTING.md` is the single source of truth for how that specific project is verified. This skill does not replace project documentation; it formulates, audits, and maintains it.

Upon invocation, execute the following triage:

1. **Check Strategy Presence:**
   - Inspect the repository for a canonical `TESTING.md` (or a dedicated testing section within `README.md`).
2. **If `TESTING.md` is Missing:**
   - Formulate and scaffold `TESTING.md`.
   - Inspect the codebase to discover execution surfaces, runtime requirements, and existing test commands.
   - Define verification tiers, runner commands, failure modes, test vector matrices, and environment setup required for this project.
   - Establish the project's invocation workflows (e.g., local fast unit tests vs. milestone end-to-end runs).
3. **If `TESTING.md` Exists:**
   - Audit current repository reality against `TESTING.md`.
   - Identify drift: new endpoints, modified function signatures, changed runtime dependencies, brittle mocks, or coverage gaps.
   - Reconcile the test portfolio (Add, Update, Prune, Retain) and synchronize `TESTING.md` with new test commands, fixtures, or contracts.

---

## 2. Phase 1: Repository Topology & Surface Mapping Checklist

Before designing or modifying tests, inspect the repository to map observable behavior, execution surfaces, and system boundaries:

- **Execution Surfaces:**
  - Command-line interfaces (flags, subcommands, arguments, stdin/stdout pipelines, exit codes).
  - HTTP, REST, RPC, WebSocket, or GraphQL endpoints and serialization schemas.
  - Background workers, event queues, pub/sub consumers, and scheduled tasks.
  - Reusable libraries, exported functions, type signatures, and public module contracts.
  - User interfaces (browser components, web applications, native desktop views).
- **System Boundaries & External Dependencies:**
  - Persistence layers, relational databases, document stores, key-value caches.
  - Filesystem access, temporary directories, file locks, disk quotas.
  - Network calls, external third-party APIs, webhooks, cloud services.
  - System clocks, timers, randomness, process spawning, OS signals, hardware resources.
- **Consequence Severity:**
  - Evaluate the impact of failure: data loss, persistent state corruption, security vulnerability, broken public API contract, or silent computation errors. Focus high-rigor checks on critical failure surfaces.

---

## 3. Phase 2: Verification Tier Selection Checklist

Select verification methods proportionate to changed behavior and risk profile. Treat the following taxonomy as a decision matrix for what belongs in `TESTING.md`:

| Verification Tier         | Primary Target                                               | Trigger Condition                                                                   |
| :------------------------ | :----------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| **Unit**                  | Isolated pure logic, algorithms, state machines, parsers     | Fast, deterministic checks without external I/O or boundary mocks.                  |
| **Component**             | UI widgets, isolated subsystems, self-contained modules      | State rendering, event handling, or sub-tree composition in isolation.              |
| **Integration**           | Boundary interactions across storage, subprocesses, networks | Data persistence, schema migrations, protocol serialization, cross-module flows.    |
| **Contract**              | Public APIs, client/provider expectations, schemas           | Breaking changes to API payload formats, exported types, or wire protocols.         |
| **Browser Interaction**   | Web interfaces, user navigation, DOM state, focus            | Critical end-to-end user journeys requiring layout rendering and browser events.    |
| **Native End-to-End**     | Desktop applications, OS integration, packaging              | OS dialogs, system menus, file associations, desktop windowing, native permissions. |
| **Build & Package Smoke** | Bundled artifacts, CLI distributions, wheels, binaries       | Verifying that compiled or packaged artifacts launch and run critical paths.        |
| **Deployment Smoke**      | Staging environments, live services, infra configuration     | Post-deployment reachability, environment variable binding, database connectivity.  |
| **Performance & Scale**   | Throughput, latency, memory ceilings, payload scaling        | High-frequency code paths, resource-constrained runtimes, heavy batch workloads.    |
| **Security & Robustness** | Trust boundaries, authorization, hostile payloads            | Unsanitized user inputs, permission escalations, path traversal, authentication.    |

### Verification Invariants

- **Cost-to-Evidence Parity:** Select the lowest-cost, fastest verification tier that yields conclusive evidence. Do not substitute slow end-to-end tests for logic easily validated with sub-millisecond unit checks.
- **Surface Fidelity:** Browser tests do not prove native desktop runtime correctness. Source-level tests do not prove bundled binaries execute. Match checks to actual deployment surfaces.
- **Boundary Reality:** Unit mocks do not validate boundary compatibility. Critical persistence and network boundaries require real or high-fidelity containerized integration tests.
- **Artifact Launchability:** Successful compilation or bundling does not prove runtime health. Always execute a smoke check against packaged distribution artifacts.

---

## 4. Phase 3: Harness Audit & Adaptive Provisioning

Inspect existing test tooling before introducing new dependencies:

### Capability Delta Assessment

Categorize the harness state into one of four conditions:

- **Adequate:** Existing runners, fixtures, and configuration fully support required verification. Proceed directly to portfolio reconciliation.
- **Missing:** Zero automated test harness exists in the repository.
- **Outgrown:** The codebase has expanded (e.g., added an async service, CLI, or UI) beyond the capabilities of the current runner.
- **Brittle:** Existing tests depend on unmocked external networks, rigid absolute paths, non-deterministic timers, or polluted shared state.

### Adaptive Provisioning Protocol

When provisioning or upgrading a test harness:

- **Prefer Ecosystem Built-ins:** Leverage standard library or minimal runners (e.g., Python `unittest`, Node `node:test`, Go `testing`, Rust `cargo test`) before adding third-party frameworks.
- **Research External Dependencies:** When specialized tools are necessary (e.g., Playwright for browsers, Testcontainers for databases), activate `web-research` to verify current version compatibility and platform constraints.
- **Gate Additions via Worth-the-Squeeze:** Activate `worth-the-squeeze` before adding heavy testing frameworks or complex mocking libraries. Balance defect prevention dividends against installation overhead and CI maintenance tax.
- **Ensure Test Isolation:**
  - Execute destructive filesystem operations inside isolated temporary directories with deterministic cleanup.
  - Bind network tests to ephemeral ports or loopback addresses.
  - Reset database and in-memory caches between test runs.
- **Materialize Baseline Proof:** Validate any newly provisioned harness by running a minimal baseline test that confirms the runner executes cleanly and reports accurate exit codes.

---

## 5. Phase 4: Test Portfolio Reconciliation (Add / Update / Prune / Retain)

For every modified or proposed behavior, assign one of four explicit dispositions:

- **Add:** Create new test cases to cover unprotected acceptance criteria, new failure modes, edge conditions, or interface contracts.
- **Update:** Modify existing assertions or fixtures to match intentionally changed requirements, updated interfaces, or schema evolutions.
- **Prune:** Delete tests for removed features, obsolete implementations, or duplicate tests that add runtime cost without increasing defect detection.
- **Retain:** Confirm that existing coverage protects the modified surface without modification. Document the rationale for retention.

### Defect Reproduction Invariant

When resolving a defect, write an automated regression test reproducing the failure **before** implementing the fix. Verify that the test fails on current code, apply the minimal fix, and verify that the test passes. If reproduction cannot be automated, document the technical blocker and the manual verification procedure.

### Risk-Driven Test Vector Matrix

Audit changed surfaces against concrete edge cases and failure modes:

- **Input Boundaries:** Empty collections, zero values, null/nil inputs, malformed structures, extreme Unicode characters, off-by-one boundary values, oversized payloads.
- **Fault Injections:** Network dropouts, connection timeouts, unavailable dependencies, filesystem permission denials, process cancellation, storage exhaustion.
- **Contract Preservation:** Anchor assertions to public behavior and observable side effects. Never assert on private implementation details or fragile internal syntax structures.

---

## 6. Phase 5: Universal Execution Invariants & Assertion Discipline

Never declare testing complete without executing the relevant suite and inspecting actual outputs:

- **Direct Execution:** Execute test commands directly in the environment using project-idiomatic runners. Inspect exit codes, stdout, and stderr.
- **Fast vs. Milestone Cadence:** Run fast unit and component suites on every local edit. Defer slow end-to-end, native package, and performance suites to milestone verification.

### Non-Negotiable Assertion Invariants

- **Zero Assertion Weakening:** Never relax, skip, comment out, or delete a failing assertion merely to obtain a green run.
- **Root-Cause Defect Resolution:** When a test fails:
  - If the implementation has a defect, fix the source code.
  - If the test expectation is incorrect, update the assertion only after verifying against intended product requirements.
- **Determinism & Flake Eradication:** Tests must produce identical results across repeated runs. Investigate intermittent failures, race conditions, global state leakage, and execution-order dependencies immediately.
- **Visual & Interactive Verification:** When introducing new features or validating UI/layout surfaces, capture representative states (e.g., screenshots or rendered element trees) and perform hands-on interactive validation: execute inputs, observe runtime state transitions, and verify observable system responses. Never update baseline snapshots blindly to mask visual regressions.
- **Transparent Blocker Reporting:** If an authorized check cannot run due to missing environment dependencies, credentials, or hardware constraints, document the blocker and remaining risk explicitly. Do not disguise omitted checks as passing verification.

---

## 7. Phase 6: Living Strategy Synchronization in `TESTING.md`

Keep repository documentation aligned with test suite evolution:

- **Living Strategy Synchronization:**
  - Record active test runner commands, setup prerequisites, fixture management, and verification tiers in `TESTING.md` (or the testing section in `README.md`).
  - Document environment prerequisites and platform-specific runner behaviors.
- **Evidence Reporting:**
  - Surface affected behavior and selected verification tiers.
  - Itemize tests added, updated, pruned, or retained.
  - Report exact commands executed, exit codes, test run counts, and runtime duration.
  - Disclose all deferred, skipped, or blocked checks alongside mitigation rationale.
- **Git Handoff:**
  - Do not automatically commit or push changes unless operating under an authorized workflow that mandates git finalization.
  - When committing test changes, activate `commit-scribe` to record structured commit metadata.

---

## 8. Completion Criteria

- `TESTING.md` exists (or is updated) in the target repository and accurately reflects current runner commands, tiers, and setup.
- Test dispositions (add, update, prune, retain) are justified and implemented.
- Affected test suites run cleanly with passing assertions.
- Zero weakened assertions or masked defects exist.
- Visual and interactive verification is performed for user-facing surfaces.
