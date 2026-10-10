---
name: test-strategist
description: Audits and evolves project-specific testing strategies against real user workflows, runtime surfaces, and failure risks. Reuses effective checks and repairs gaps in coverage, harnesses, and verification instructions. Use when defining test strategies, auditing coverage after changes, establishing harnesses, or resolving brittle tests. Do not invoke for routine single-test runs or prose-only edits.
---

# Test Strategy & Behavioral Verification

Turn the project's requirements, existing checks, and runtime evidence into an implemented testing strategy that proves the behavior users and callers rely on. Follow stages 1–6 in order, carrying each stage's result into the next. Revisit the affected stage when execution exposes a changed assumption or evidence gap. Record concrete workflows, tools, commands, and execution triggers in the project's canonical testing documentation, such as `TESTING.md` or a testing section in `README.md`.

## 1. Establish the Verification Baseline

Inspect project instructions, testing documentation, source entry points, existing tests, build scripts, and continuous integration configuration. Compare the outcomes required by the project with the outcomes established by its actual checks.

- **Establish Scope:**
  - Identify the behavior under review and the completion claim that verification must support.
  - Determine how users or callers reach that behavior and which runtime or distributed artifact they use.
  - Identify critical failure consequences, including data loss, state corruption, security exposure, broken public contracts, and silent incorrect results.
- **Assess Existing Practice:**
  - Locate the canonical testing instructions and designate that location for strategy updates.
  - Inspect representative assertions and recent results against intended behavior.
  - Record effective coverage, missing checks, stale instructions, and checks that give misleading confidence.
  - Establish a canonical home when testing instructions are missing, and populate it with discovered commands and requirements.

- **Stage Result:**
  - Record the verification scope, canonical strategy location, established evidence, and identified gaps. Use this baseline to select workflows in stage 2.

## 2. Map User Workflows to Observable Evidence

Use the baseline to map each critical or affected workflow in the project's testing documentation. Record:

- The user or caller, starting state, and actual entry point.
- The actions or inputs that exercise the behavior.
- The expected observable result and relevant side effects.
- The runtime and boundaries the check must exercise.
- The existing check or required addition, execution trigger, and any remaining evidence gap.

Inspect applicable surfaces: command-line arguments, pipelines and exit codes; service endpoints and message consumers; library exports; browser interfaces; native desktop views; and packaged distributions. Trace relevant boundaries such as storage, filesystem access, network protocols, subprocesses, permissions, clocks, and randomness.

- **Check Behavior Through Actual Use:**
  - For a code editor whose requirements include persistent editing, launch the app, open a file, change text through the interface, save, and reopen the file to verify persistence.
  - A parser unit test can prove parsing behavior; the editor workflow also requires evidence that input, application state, and storage work together.
  - Use browser or native interaction checks for the surface users operate. Include focus, navigation, state transitions, and error handling where those affect the workflow.
- **Require Defect-Sensitive Checks:**
  - Ask whether the check would fail if the intended behavior broke.
  - Assert on public results and observable side effects rather than private syntax or implementation structure.
  - Include relevant input boundaries and failure paths: empty or malformed input, boundary values, Unicode, oversized payloads, timeouts, permission errors, cancellation, and unavailable dependencies.

Derive the project's concrete workflows from its requirements and actual use.

- **Stage Result:**
  - Produce a workflow-to-evidence map containing expected outcomes, runtime surfaces, boundaries, and coverage gaps. Use this map to select methods in stage 3.

## 3. Select Methods That Support the Claim

Select verification methods that establish each mapped outcome at the required runtime and system boundaries. Compare methods that provide sufficient evidence by execution cost, reliability, and maintenance effort. Use the table to select the methods needed for the project.

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

- **Match the Runtime:**
  - Browser results do not establish native desktop behavior.
  - Source-level results do not establish packaged artifact behavior.
  - Unit mocks do not establish boundary compatibility; use real dependencies or representative controlled environments for critical boundary checks.
- **Verify Delivered Artifacts:**
  - When producing or claiming readiness of a package, launch or load that artifact in its intended runtime and exercise a representative critical path.
  - Confirm the expected result and relevant runtime errors. Build success proves artifact creation; it does not prove that the artifact works.
  - Run deployment checks against an authorized target when the claim concerns a deployed service.
- **Inspect Visual Evidence:**
  - Use screenshots or rendered states to assess appearance against a stated expectation.
  - Pair visual evidence with actions and observable outcomes when the claim concerns interaction or state changes.
  - Capturing a screenshot alone does not verify a workflow. Review snapshot differences before accepting a new baseline.

Record project-specific triggers for fast checks, workflow checks, packaging checks, and broader milestone checks. Base cadence on affected behavior and risk. Required runtime checks must precede a readiness claim even when they cost more than the fast suite.

- **Stage Result:**
  - Record the selected methods and execution triggers for each mapped outcome, with the evidence each method must establish. Use these requirements to assess the harness in stage 4.

## 4. Establish the Required Harness Capabilities

Compare the selected verification methods with existing tooling. Classify the harness as adequate, missing, outgrown, or brittle, then implement the required capability changes. Retain tooling that supports the strategy.

- **Select Tools:**
  - Select runners that support the required checks, runtime, isolation, and failure reporting. Evaluate existing runners and ecosystem built-ins alongside specialized tools.
  - Activate `web-research` for unfamiliar external tools, version compatibility, or platform constraints.
  - Activate `worth-the-squeeze` before substantial framework additions; weigh defect detection against setup and ongoing maintenance.
- **Isolate Checks:**
  - Use temporary directories and deterministic cleanup for destructive filesystem tests.
  - Use ephemeral ports or loopback addresses for local network tests.
  - Reset persistent and shared state between runs.
  - Control time and randomness where necessary; investigate intermittent failures, races, and execution-order dependence.
- **Prove Harness Capability:**
  - Verify that a newly provisioned runner executes checks and reports failures accurately.
  - Exercise a representative project behavior through that runner. Runner health alone does not establish product correctness.
  - Use a repeatable manual procedure when automation is unavailable or disproportionate; document its scope, expected results, and limitations.

- **Stage Result:**
  - Provide runnable checks or documented manual procedures for the selected methods, and identify blocked capabilities. Use the available capabilities to implement test dispositions in stage 5.

## 5. Reconcile Tests Without Masking Defects

Use the workflow map and available harness to implement a disposition for each affected outcome or coverage gap:

- **Add:** Cover an unprotected outcome, failure mode, or public contract.
- **Update:** Align checks with an intentionally changed requirement or interface.
- **Prune:** Remove checks for deleted behavior or redundant checks that add cost without detecting distinct defects.
- **Retain:** Identify existing checks that still prove the required outcome and explain why they suffice.

When fixing a defect, reproduce the failure before applying the fix. Prefer an automated regression test; confirm failure before the fix and success afterward. If automation is blocked, record the blocker and a repeatable manual reproduction and verification procedure.

- **Preserve Assertion Integrity:**
  - Never relax, skip, comment out, or delete a failing assertion merely to obtain a green run.
  - Fix implementation defects in the source.
  - Change an incorrect test expectation only after checking the intended product requirement.
  - Investigate intermittent failures rather than masking them with retries or baseline changes.

- **Stage Result:**
  - Implement and record the test dispositions. Confirm defect reproduction and assertion integrity before executing the selected verification in stage 6.

## 6. Execute, Inspect, and Maintain the Strategy

Run the selected checks and inspect their actual results against the mapped expectations. Execute manual procedures directly when those are the selected method. Use failures to revise the affected tests, harness, or strategy, then rerun the relevant checks.

- **Record Evidence:**
  - Report the behavior checked, runtime or artifact, exact commands or actions, expected results, and observed results.
  - Include exit codes, test counts, and duration when available and relevant.
  - Distinguish passed, failed, deferred, and blocked checks. State the exact blocker and remaining unverified outcome.
- **Update Durable Instructions:**
  - Keep the workflow map, commands, prerequisites, fixtures, environment constraints, and execution triggers current in the canonical testing documentation.
  - Ensure project instructions point future agents to that strategy and require review when workflows, contracts, runtime surfaces, or tooling change.
  - Record the evidence supporting retained coverage and the resolution of identified gaps.
- **Respect Git Scope:**
  - Commit or push only when the authorized workflow includes Git finalization.
  - Activate `commit-scribe` before staging, committing, or pushing.

- **Stage Result:**
  - Update the canonical strategy and report observed results for each required outcome. Identify unresolved gaps and the resulting readiness status.

## 7. Completion Criteria

- The canonical project strategy reflects actual workflows, applicable checks, commands, prerequisites, and execution triggers.
- Each critical or affected outcome has sufficient verification or an explicit unresolved gap.
- Required checks execute and establish observable results on the relevant runtime; delivered artifacts are exercised when applicable.
- Test changes preserve assertion integrity and address the identified gaps.
- Future agents can discover when to run checks and when to revise the strategy.

If a required check fails or is blocked, report the audit and completed repairs separately from product readiness. Do not declare the affected behavior verified.
