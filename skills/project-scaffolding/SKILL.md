---
name: project-scaffolding
description: Plan and establish minimal repository structure, technical foundations, testing harnesses, and development continuity for new projects or young repositories. Grounds requirements, validates smallest viable stacks, selects proportionate layouts, and embeds durable project memory. Use at project inception or when repairing missing repository foundations. Do not invoke for routine feature development, ordinary handoffs, or established project restructuring.
---

[LOOKOUT: This skill has an identify crisis. I want it when say starting a new project. I say...this is my idea and I want to develop it further. So then immediately there are a few things that should happen e.g. a readme with blah blah content, areehctureal decision records are tracked, plan is tracked and updated, etc. I have mentioned many of these things already in the skill below. But you see we can't anticipate every kind of project. Each project has different requirements and needs different things. So this skill does not say always do this and that. But gives sufficient isnutrcitons to the human or ai agent scaffolding the new project to go find out and do things on its own and then to scaffold the project. ]

# Project Scaffolding & Development Continuity

Establish the minimal viable technical foundation, directory layout, verification harness, and operational memory required for an initial feature slice and seamless multi-session continuity. Prevent starter-stack bloat and premature governance by anchoring every file, dependency, and convention in verified project requirements.

---

## 1. Operating Modes & Scope Discipline

Operate under one of three distinct authorization modes:

- **Discovery & Planning Mode:**
  - Inspect requirements, target platforms, operational constraints, and technical assumptions.
  - Formulate the minimal viable architecture, stack selection, and directory layout proposal.
  - Formulate bounded technical probes for high-risk runtime assumptions.
  - Zero filesystem writes or package installations occur in this mode.
- **Drafting Mode:**
  - Generate reviewable project configuration manifests, instruction drafts, or structural layouts in scratchpad artifacts.
  - Do not apply changes to active repository source paths without user approval.
- **Foundation Implementation Mode:**
  - Materialize the authorized directory structure, initialize manifests, provision the test harness via `test-strategist`, implement the walking skeleton or first feature increment, and verify execution.
  - Confine implementation strictly to approved project boundaries.

Preserve user approval gates before provisioning infrastructure, creating files, installing external toolchains, or executing git operations.

---

## 2. Phase 1: Context Grounding & Boundary Definition

Inspect repository state, version control history, existing documentation, and available local tools. Ground the project across three core vectors:

- **Operational Context:**
  - Target audience, primary workflows, and execution environments (CLI, web service, library, background worker, desktop app).
  - Supported platforms, runtime versions, and deployment destinations.
  - Firm constraints, language/tooling preferences, and explicit out-of-scope exclusions.
- **Architectural Boundaries:**
  - Persistence locations, data ownership, filesystem mutations, network egress, and security boundaries.
  - Consequence of failure: data corruption, credential leakage, network partition vulnerabilities.
- **Scope Gating:**
  - Isolate the first deliverable increment ("Walking Skeleton") from downstream roadmap items.
  - Define clear, observable acceptance criteria for the initial release.
  - Do not treat speculative future possibilities as current requirements.

---

## 3. Phase 2: Foundation Validation & Dependency Gating

Identify runtime boundaries and the riskiest assumptions that could invalidate the architectural plan:

### Smallest Viable Stack Invariant

Choose the leanest possible technical stack that fulfills verified requirements. Favor runtime built-ins and standard libraries over heavy third-party meta-frameworks.

### Dependency Gating Protocol

Before adding external packages, runtimes, or database engines:

- **Validate Compatibility via Web Research:** Activate `web-research` to inspect current primary documentation, verify release stability, check platform support, and identify breaking changes in target toolchain versions.
- **Audit Lifetime Friction via Worth-the-Squeeze:** Activate `worth-the-squeeze` for major framework additions or complex dependencies. Balance immediate developer utility against long-term operational friction, security update burden, and migration blast radius.
- **Deterministic Dependency Pinning:** Always record explicit, reproducible dependency versions using standard package manifests and lockfiles.

### Bounded Technical Probes

When documentation leaves critical gaps regarding runtime behavior, external API contracts, or platform integration, design a minimal technical probe:

- Author a self-contained, throwaway test script isolated from production code.
- Run the probe only when operating under an authorized execution mode.
- Never claim feasibility based on an unexecuted probe.

---

## 4. Phase 3: Initial Verification Harness Integration

Integrate testing into the initial architectural design before writing domain code:

- **Delegate Strategy to test-strategist:** Activate `test-strategist` during project planning. Pass workflows, observable acceptance criteria, execution surfaces, and data risk profiles to formulate an adaptive test strategy.
- **Materialize Baseline Harness:** When implementation is authorized, establish a runnable test harness alongside the first implemented feature slice. Ensure tests execute via a single standard command.
- **Zero Synthetic Tests:** Do not generate artificial or trivial unit tests for static configuration files or boilerplate manifests that contain no executable domain logic.

---

## 5. Phase 4: Proportionate Repository Layout

Structure the repository using a two-tiered, necessity-driven layout model. Scale structure only when justified by codebase evolution:

### Tier 1: Core Essentials (Mandatory for All Projects)

| File or Directory     | Purpose & Invariant                                                                                                                 |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`           | Canonical repository entry point: purpose, current capabilities, quickstart setup, operational commands, and known limitations.     |
| `.gitignore`          | Prevent generated artifacts, local environment state, build caches, and sensitive files from polluting version control.             |
| Manifests & Lockfiles | Manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) defining reproducible runtime and dependency constraints. |
| Source Tree           | Domain-bounded source directories matching ecosystem conventions (e.g., `src/`, `cmd/`, `internal/`).                               |
| Test Harness          | Dedicated test directory (e.g., `tests/`) or co-located test files matching project harness conventions.                            |

### Tier 2: Continuity & Context Scaling (Proportionate Scaling)

Scale repository memory and governance documentation based on operational complexity:

- **Embedded-First Principle:** Keep agent instructions, testing strategy, architecture decisions, and roadmap milestones as structured sections inside `README.md` or a root `AGENTS.md`.
- **Extraction Threshold:** Extract dedicated markdown files (`TESTING.md`, `DECISIONS.md`, or a `docs/` index) **only** when documentation volume exceeds single-file scannability or requires distinct operational ownership.
- **Layout Anti-Patterns:**
  - Never create empty directories, placeholder files, or stub documents to satisfy a speculative enterprise template.
  - Never generate separate documentation directories (`docs/`) for small projects where `README.md` is sufficient.
  - Never commit local developer tooling state or transient machine paths.

---

## 6. Phase 5: Canonical Project Memory

Maintain unambiguous project memory to ensure future agent sessions execute with full context:

- **Single Source of Truth Invariant:** Every project fact, configuration parameter, and architectural boundary must have exactly one authoritative location. Never duplicate assertions across disparate files.
- **Active Present State Invariant:** Living files describe current system reality. Historical evolution, changelogs, and discarded paths belong exclusively in Git commit history.
- **Durable Project Instructions (`AGENTS.md`):** Record non-obvious constraints, mandatory workflows, prohibited modifications, and required skill routing rules:
  - Embed this standard testing directive:

> During planning and changes to code, features, dependencies, runtime or build configuration, or packaging, invoke test-strategist at a depth appropriate to the change. Reconcile tests (add, update, prune, retain) and execute applicable verification before declaring completion.

- **Reversible Decision Records:** When a consequential architectural fork is chosen, record the problem, chosen mechanism, trade-offs, and revisit conditions. Mark superseded decisions immediately.

---

## 7. Phase 6: Milestone Sequencing & Incremental Delivery

Decompose the initial project implementation into small, testable milestones with observable outcomes:

1. **Milestone 1: Risk Probe & Verification Spike:** Validate high-risk assumptions with minimal isolated scripts.
2. **Milestone 2: Walking Skeleton:** Materialize the core repository structure, build configuration, minimal test harness, and one end-to-end executable path.
3. **Milestone 3: Incremental Feature Expansion:** Implement domain features sequentially, reconciling code, tests, and documentation at each milestone.

### Scope Drift & Plan Re-anchoring

When implementation uncovers unexpected blockers or runtime drift:

- Differentiate between requirement changes, implementation adjustments, and newly uncovered constraints.
- Re-anchor live project state and acceptance criteria before writing further code.
- Prompt the user for steering only when a decision crosses an approval boundary or permanently alters project scope.

---

## 8. Phase 7: Verification & Multi-Session Continuity Protocol

Before closing an initial scaffolding session, verify foundation integrity and record continuity state:

### Foundation Verification

- Verify that documented installation, bootstrap, and run commands succeed cleanly in a fresh shell.
- Run the full test suite and confirm zero failing assertions.
- Confirm all build and package commands produce valid, executable artifacts.
- Verify Markdown links and documentation navigation using portable relative paths.

### Four-Step Session Continuity Protocol

Establish this operational protocol in project documentation for future sessions:

1. **Context Grounding:** At session start, inspect repository constraints, version control diffs, and live roadmap state before executing tasks.
2. **External Revalidation:** Revalidate third-party dependencies and external assumptions before beginning dependent feature work.
3. **Synchronized Evolution:** Reconcile code, tests, and living documentation in lockstep during every development increment.
4. **Handoff State Capture:** At session conclusion, document completed milestones, outstanding tasks, verification evidence, and the immediate next actionable step.

### Git Hygiene & Handoff

When version control initialization or commits are authorized:

- Initialize repository and configure `.gitignore` before staging code.
- Activate `commit-scribe` to generate structured, contextual commit messages.
- Never push upstream without explicit user authorization.

---

## 9. Completion Criteria

- **In Discovery & Planning Mode:** Deliver a justified minimal stack, layout proposal, de-risked milestone sequence, and identified unknowns. Zero unapproved file modifications exist.
- **In Implementation Mode:**
  - The repository contains only necessary files, manifests, and source code.
  - The test harness is provisioned and passes initial baseline checks.
  - Setup and execution commands run cleanly without undocumented prerequisites.
  - Project memory (`README.md`, `AGENTS.md`) is established and provides sufficient context for subsequent sessions to continue without friction.
