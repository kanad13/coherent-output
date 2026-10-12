---
name: test-strategist
description: Audits and evolves project-specific testing strategies against real user workflows, runtime surfaces, and failure risks. Reuses effective checks and repairs gaps in coverage, harnesses, and verification instructions. Use when defining test strategies, auditing coverage after changes, establishing harnesses, or resolving brittle tests. Do not invoke for routine single-test runs or prose-only edits.
---

# Test Strategy & Behavioral Verification

Turn the project's requirements, existing checks, and runtime evidence into a testing strategy that proves the behavior users and callers rely on. Follow stages 1–6 in order, carrying findings forward, and revisit a stage when execution exposes a changed assumption. This skill owns the content of the project's canonical testing document (`TESTING.md` or a testing section in `README.md`); other skills only point to it. Use the smallest strategy that supports the claim: a small project may need one command and a short workflow table.

## 1. Establish Scope and Baseline

Inspect project instructions, testing documentation, entry points, existing tests, build scripts, and CI configuration.

- **Scope:** name the behavior under review and the completion claim verification must support. Identify how users or callers reach it, which runtime or artifact they use, and the cost of failure (data loss, corruption, security exposure, broken public contracts, silent wrong results).
- **Existing practice:**
  - Locate the canonical testing document and designate it for strategy updates. If none exists, create it from discovered commands and requirements.
  - Read representative assertions and recent results against intended behavior. Record effective coverage, missing checks, stale instructions, and checks that give false confidence.

## 2. Map Workflows to Observable Evidence

For each critical or affected workflow, record in the testing document:

| Field            | Content                                                                       |
| :--------------- | :---------------------------------------------------------------------------- |
| Caller and start | The user or caller, starting state, and actual entry point                    |
| Action           | Inputs or steps that exercise the behavior                                    |
| Expected result  | Observable outcome and relevant side effects                                  |
| Boundaries       | Runtime and system boundaries the check must cross                            |
| Evidence         | Existing check or required addition, execution trigger, and any remaining gap |

Inspect the surfaces users operate: command-line arguments, pipelines and exit codes; service endpoints and consumers; library exports; browser interfaces; native views; packaged distributions. Trace boundaries such as storage, filesystem, network, subprocesses, permissions, clocks, and randomness.

- **Test through actual use:**
  - For an editor that must persist text, launch it, open a file, change text through the interface, save, and reopen. A parser unit test proves parsing; this workflow proves input, state, and storage work together.
  - Use browser or native interaction for the surface users operate, including focus, navigation, state transitions, and error handling where they affect the workflow.
- **Require defect-sensitive checks:**
  - **Sabotage check:** deliberately break the behavior (revert the fix, invert a condition, remove a call) and confirm the check fails. A check that cannot fail proves nothing; restore the code afterward.
  - Assert on public results and observable side effects, not private structure.
  - Cover relevant boundaries and failure paths: empty or malformed input, boundary values, Unicode, oversized payloads, timeouts, permission errors, cancellation, unavailable dependencies.

## 3. Select Methods That Support the Claim

For each mapped outcome, choose the cheapest method that crosses the real boundary and gives sufficient evidence. Default to fast, deterministic unit and component checks for isolated logic, and integration or contract checks wherever storage, subprocesses, networks, or public schemas are involved. Escalate to these only when the claim requires them:

- **Browser interaction:** web journeys that depend on rendering, focus, and events.
- **Native end-to-end:** OS dialogs, menus, file associations, windowing, permissions, packaging.
- **Package smoke:** compiled or bundled artifacts launch and run a critical path.
- **Deployment smoke:** reachability, configuration binding, and connectivity of a deployed service, against an authorized target.
- **Performance, scale, security:** high-frequency paths, resource limits, hostile input, authorization.

Rules that decide the choice:

- **Match the runtime:** browser results do not establish native behavior, source-level results do not establish packaged behavior, and mocks do not establish boundary compatibility. Use real dependencies or representative controlled environments for critical boundaries.
- **Exercise delivered artifacts:** before claiming a package is ready, launch it in its intended runtime and run a representative critical path. Build success proves only that an artifact exists.
- **Visual evidence:** pair screenshots with actions and observable outcomes. A screenshot alone verifies nothing about a workflow. Review snapshot differences before accepting a new baseline.
- **Non-deterministic output** (model, agent, or randomized results): fix the inputs, state an explicit rubric of required and forbidden properties, run more than once, and inspect the actual outputs. One passing sample is evidence for that sample only.

Record when each kind of check runs: fast checks on every change, workflow checks on affected behavior, packaging and broader checks at milestones. Map them to CI where it exists. Required runtime checks precede any readiness claim, even when they cost more than the fast suite.

## 4. Establish the Required Harness

Compare the selected methods with existing tooling and classify it as adequate, missing, outgrown, or brittle. Retain tooling that supports the strategy.

- **Callee mode:** when another skill invoked this one, make no further skill calls. Use the inline fallbacks below.
- **Tools:** prefer existing runners and ecosystem built-ins. Activate `web-research` for unfamiliar tools or version constraints; without it, read official documentation and mark unverified claims. Activate `worth-the-squeeze` before adding a substantial framework; without it, weigh defect detection against setup and upkeep.
- **Isolation:** use temporary directories, ephemeral ports, and reset shared state between runs. Control time and randomness. Investigate order dependence and intermittent failures.
- **Prove the harness:** confirm a new runner executes checks and reports failures accurately, then run a representative project behavior through it. Runner health alone does not establish product correctness. When automation is unavailable or disproportionate, write a repeatable manual procedure with its scope, expected results, and limits.

## 5. Reconcile Tests Without Masking Defects

Give each affected outcome or gap one disposition: **add** (unprotected outcome), **update** (intentional change), **prune** (deleted behavior or redundant cost), or **retain** (still proves the outcome, with the reason).

- **Defects:** reproduce the failure before fixing it, preferably as an automated regression test that fails before the fix and passes after. If automation is blocked, record the blocker and a repeatable manual reproduction.
- **Assertion integrity:**
  - Never relax, skip, comment out, or delete a failing assertion to get a green run. Fix the implementation.
  - Change a test expectation only after checking the intended requirement.
  - Never mask an intermittent failure with retries or baseline changes. Find the cause. If it cannot be fixed now, quarantine the test visibly with an owner and a revisit date, and count it as an unverified outcome.

## 6. Execute, Inspect, and Maintain the Strategy

Run the selected checks, or execute manual procedures directly, and compare actual results with the mapped expectations. Use failures to revise the tests, harness, or strategy, then rerun.

- **Record evidence:** the behavior checked, runtime or artifact, exact commands, expected and observed results, and exit codes, counts, and duration when relevant. Report passed, failed, deferred, and blocked checks separately, with the exact blocker and the unverified outcome.
- **Keep it durable:** keep the workflow map, commands, prerequisites, fixtures, environment constraints, and triggers current. Ensure project instructions send future agents to the strategy and require review when workflows, contracts, surfaces, or tooling change.
- **Git scope:** never stage, commit, or push. Leave version-control actions to the caller.

## 7. Completion Criteria

- The testing document reflects actual workflows, checks, commands, prerequisites, and triggers.
- Each critical or affected outcome has sufficient verification or an explicit unresolved gap.
- Required checks ran on the relevant runtime, and delivered artifacts were exercised where applicable.
- New checks fail when the behavior breaks, and no assertion was weakened to pass.
- Future agents can find when to run checks and when to revise the strategy.

If a required check fails or is blocked, report the audit and repairs separately from product readiness, and do not declare the affected behavior verified.
