---
name: test-strategist
description: Assesses repository topology, evaluates testing gaps, formulates or adapts test strategies, provisions test harnesses, and evolves test suites alongside code changes without dogmatic tooling bias. Use when strategizing test coverage, setting up a test harness, or reconciling tests mid-development.
---

# Adaptive Test Strategy & Harness Evolution

Use this skill mid-development or during repository bootstrapping to formulate a test strategy, audit the test harness against codebase evolution, identify verification deltas, and adapt test suites without dogmatic tooling bias.

---

## 1. Operating Protocol & Non-Dogmatic Philosophy

Every repository has distinct architectural boundaries, constraints, and runtime characteristics. Do not enforce rigid, one-size-fits-all testing tools or pre-canned stacks (e.g., never mandate a specific runner purely because of a language).

Instead, operate as an adaptive QA strategist using this 6-phase checklist:

1. **Topology Discovery:** Map the codebase's interfaces, execution surfaces, and isolation boundaries.
2. **Harness & Strategy Audit:** Compare existing test infrastructure against current architectural reality to identify the delta.
3. **Adaptive Harness Provisioning:** Research lightweight, idiomatic tooling matching the specific ecosystem and constraints when a harness is missing or outgrown.
4. **Test Portfolio Reconciliation:** Add, update, or prune test cases to mirror recent functional evolution.
5. **Execution & Assertion Integrity:** Run tests directly in the environment and enforce non-negotiable assertion integrity.
6. **Living Documentation:** Document or update the test strategy in `TESTING.md` or the repository index.

---

## 2. Phase 1: Repository Topology & Interface Discovery

Before writing or modifying tests, inspect the repository to map its actual runtime boundaries:

1. **Interface Surfaces:**
   - What surfaces does this system expose?
   - Command-line interfaces (CLI flags, subcommands, exit codes, stdin/stdout pipelines).
   - HTTP, REST, RPC, GraphQL endpoints, middleware, and request/response schemas.
   - Database schemas, migrations, transactional boundaries, and persistence layers.
   - Background workers, event queues, pub/sub topics, scheduled jobs, and daemons.
   - Reusable libraries, exported modules, classes, and public API function signatures.
   - User interfaces (web frontends, desktop clients, headless browser rendering).
2. **Isolation Boundaries & External Dependencies:**
   - What external resources does the code touch? Network APIs, filesystem paths, system clocks, subprocesses, databases, hardware peripherals.
   - What mechanisms exist to isolate or simulate these boundaries during automated testing (mocks, stubs, testcontainers, ephemeral sqlite/in-memory stores, recorded fixtures)?
3. **Existing Tooling & Conventions:**
   - What test runners, assertion libraries, or test directories already exist in the repository (e.g., `tests/`, `__tests__/`, `spec/`, test configuration files like `pytest.ini`, `jest.config.js`, `Cargo.toml`, or custom shell test runners)?
   - Adhere to established project testing conventions before introducing new tooling.

---

## 3. Phase 2: Strategy Delta & Test Harness Audit

Determine the delta between current code reality and existing test capabilities:

1. **Strategy Assessment:**
   - Does a written test strategy exist (e.g., `TESTING.md` or a section in `README.md`)?
   - Does the strategy still match the codebase, or has the application evolved (e.g., added an async layer, added an HTTP API, added a frontend, or converted a script into an installable CLI)?
2. **Harness Capability Audit:**
   - Does the repository have an executable test harness that can run in a clean environment?
   - Can tests be executed with a single, fast command?
   - Does the harness support required test tiers:
     - **Unit:** Pure logic, algorithms, state machines (in-memory, sub-millisecond).
     - **Integration:** Subsystem boundaries, database interactions, serialization, subprocesses.
     - **End-to-End / Contract:** Critical user flows, full CLI invocations, browser interactions, API schema validation.
3. **Delta Identification:**
   - Explicitly define the gap:
     - Missing harness (zero automated runner exists).
     - Outgrown harness (e.g., backend tests exist, but a new web UI was added without component or browser testing).
     - Brittle harness (tests rely on unmocked remote network services or hardcoded local paths).
     - Missing test tier (100% unit tests with zero integration verification across boundaries).

---

## 4. Phase 3: Adaptive Harness Provisioning (Research-Driven)

When the harness is missing or outgrown, do **not** jump to heavy frameworks by default. Research and select the right solution:

1. **Ecosystem & Dependency Audit:**
   - Inspect existing project dependencies. Prefer runners and testing utilities that require minimal new dependencies and zero global system pollution.
   - Check project runtime versions (e.g., Python 3.11 `unittest`, Node 20 built-in test runner `node:test`, Go standard `testing`, Rust `cargo test`).
2. **Research Targeted Tooling:**
   - If an external tool is required (e.g., Playwright for a browser UI, WireMock / respx for HTTP simulation), research the current standard, lightweight option for that specific ecosystem.
3. **Scaffold the Harness:**
   - Create or update test runner scripts or configuration files (e.g., `scripts/test.sh`, `pytest.ini`, `package.json` test scripts).
   - Set up common fixtures, test helpers, or ephemeral resource teardown logic.
   - Provide a working baseline test proving that the harness executes cleanly.

---

## 5. Phase 4: Test Portfolio Reconciliation (Add / Update / Prune)

Reconcile the test suite against recent functional modifications:

1. **Update Tests for Changed Behavior:**
   - If a function signature, CLI argument, error code, or API response format changed, update the corresponding test assertions to match the new contract.
2. **Add Tests for Verification Gaps:**
   - Focus on high-risk, high-value surfaces:
     - Edge cases: Empty inputs, boundary values, malformed payloads, unicode, large payloads.
     - Failure modes: Unreachable services, timeouts, permission errors, invalid credentials.
     - Core business logic invariants and state transitions.
3. **Prune Obsolete or Redundant Tests:**
   - Delete tests covering deleted features.
   - Refactor or remove brittle tests that test implementation details (syntax-level mocking) rather than observable behavior.
   - Eliminate duplicated tests that slow down the test suite without providing additional defect protection.

---

## 6. Phase 5: Provoke Execution & Enforce Assertion Integrity

Never declare tests complete without executing them:

1. **Execute Tests Directly:**
   - Run the test suite via the command runner tool in the project environment.
   - Observe stdout, stderr, execution duration, and exit codes.
2. **Test Integrity Invariant:**
   - **Never relax, weaken, or delete a failing test assertion merely to force a green test suite.**
   - When a test fails:
     - Diagnose whether the implementation has a defect. If so, fix the code.
     - If the test itself made incorrect assumptions about the intended contract, correct the test to accurately reflect verified requirements.
3. **Determinism & Performance Check:**
   - Confirm tests produce deterministic results across multiple runs (zero race conditions, no leaked files, no reliance on ordering).
   - Ensure unit test suites remain fast and local.

---

## 7. Phase 6: Living Strategy Documentation & Commit

1. **Update Living Strategy:**
   - If the repository has a `TESTING.md` (or testing section in `README.md`), ensure setup instructions, test commands, and architectural testing tiers reflect reality.
2. **Commit Test Evolution:**
   - Stage test files, test fixtures, and harness configuration.
   - Commit and push using [commit-scribe](../commit-scribe/SKILL.md):
     ```text
     test(suite): reconcile test strategy and harness to match current architecture
     ```
3. **Deliverable Summary:**
   - Summarize the discovered topology, resolved harness deltas, added/updated/pruned tests, and execution verification evidence.
