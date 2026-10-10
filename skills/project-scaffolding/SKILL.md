---
name: project-scaffolding
description: Guides autonomous discovery, technical foundation setup, test harness provisioning, and project memory tracking for new projects. Use when bootstrapping a project from an idea, scaffolding repository foundations, or establishing multi-session continuity. Do not invoke for routine feature development, ordinary handoffs, or established project restructuring.
---

# Project Scaffolding & Development Continuity

Guide autonomous discovery, minimal technical foundation setup, baseline verification, and durable project memory for new projects or young repositories. Projects differ substantially across operational domains (CLI tools, backend APIs, libraries, web services, desktop applications). This skill does not impose an inflexible starter template or anticipate speculative complexity. Instead, it equips the engineer or AI agent with universal discovery checklists and scaffolding protocols: discover operational drivers, validate the smallest viable stack, scaffold proportionate layout, provision baseline verification via `test-strategist`, and embed living project memory (`README.md`, `DECISIONS.md`, `PLAN.md`, `AGENTS.md`) so the project tracks its evolution seamlessly.

---

## 1. Grounding & Project Memory Triage

A project must track its evolution as it develops through canonical living files rather than relying on ephemeral chat context.

Upon invocation, execute the following triage:

1. **Audit Existing Project State:**
   - Inspect the current working directory, existing manifests, repository layout, version control history, and available toolchains.
   - Determine whether the task is a greenfield initialization (0 files) or repairing missing foundations in a young project.
2. **Establish the Evolution Tracking Contract:**
   - Confirm that the project has designated homes for project memory:
     - Canonical entry point and commands (`README.md`).
     - Architectural drivers, trade-offs, and decision records (`DECISIONS.md` or a dedicated section in `README.md`).
     - Implementation plan, walking skeleton scope, and milestones (`PLAN.md` or a dedicated section in `README.md`).
     - Testing strategy, execution surfaces, and commands (`TESTING.md`, established via `test-strategist`).
     - Operational instructions and agent constraints (`AGENTS.md`).

---

## 2. Phase 1: Operational Drivers & Boundary Discovery Checklist

Inspect user requirements and context to discover the foundational project drivers:

- **Operational Context:**
  - Target audience, primary workflows, and operational environments (CLI, HTTP service, library, background worker, desktop UI).
  - Target platforms, runtime versions, and packaging/distribution expectations.
  - Hard constraints, language/tooling boundaries, and explicit out-of-scope exclusions.
- **Architectural Drivers & Risk Boundaries:**
  - Persistence locations, filesystem mutations, data ownership, network egress, and security trust boundaries.
  - Consequence of failure: data loss, persistent state corruption, security exposure, unhandled crashes.
- **Scope Gating & The Walking Skeleton:**
  - Isolate the first minimal end-to-end slice ("Walking Skeleton") from downstream roadmap desires.
  - Define clear, observable acceptance criteria for the initial release increment.
  - Reject premature feature bloat and speculative enterprise complexity.

---

## 3. Phase 2: Canonical Project Memory & Continuity Setup

Scaffold the durable project memory files to ensure that subsequent development sessions operate with complete context:

- **Canonical Repository Entry Point (`README.md`):**
  - Project purpose, core capabilities, prerequisite setup, quickstart commands, and architectural overview.
- **Architectural Drivers & Decision Records (`DECISIONS.md`):**
  - Record foundational architectural drivers and non-obvious constraints.
  - Document major forks using Architecture Decision Records (ADRs): Problem, Considered Alternatives, Chosen Mechanism, Non-obvious Trade-offs, and Revisit Triggers.
  - Mark superseded decisions explicitly when project architecture evolves.
- **Roadmap & Milestone Tracking (`PLAN.md`):**
  - Sequence implementation milestones from the initial Walking Skeleton to incremental feature releases.
  - Record the active plan, completed increments, and immediate next actionable steps.
- **Operational Directives (`AGENTS.md`):**
  - Embed durable instructions, prohibited patterns, mandatory workflows, and skill routing rules.
  - Include mandatory testing invocation directing agents to `test-strategist` during code changes.

---

## 4. Phase 3: Smallest Viable Stack & Dependency Gating

Avoid starter-stack bloat by selecting the leanest technical stack that satisfies verified requirements:

### Smallest Viable Stack Invariant

Favor runtime built-ins, standard libraries, and minimal utilities over heavy meta-frameworks or multi-tier boilerplate templates.

### Dependency Gating Protocol

Before adding external libraries, frameworks, or database engines:

- **Validate Compatibility via Web Research:** Activate `web-research` to inspect current documentation, check platform stability, and verify breaking changes in the target runtime.
- **Audit Lifetime Friction via Worth-the-Squeeze:** Activate `worth-the-squeeze` for major framework additions or complex dependencies. Balance immediate utility against long-term upgrade friction, security tax, and blast radius.
- **Deterministic Pinning:** Always pin reproducible dependency versions using standard package manifests and lockfiles.

### Bounded Technical Probes

When documentation leaves critical gaps regarding runtime behavior or external API contracts:

- Author a self-contained, throwaway probe script isolated from project code.
- Run the probe to observe actual behavior before committing to an architectural approach.

---

## 5. Phase 4: Initial Verification Harness Integration via `test-strategist`

Testing foundations must exist before domain feature implementation begins:

- **Activate `test-strategist`:** Delegate test architecture definition to `test-strategist`. Formulate `TESTING.md`, define verification tiers, map execution surfaces, and determine runner commands.
- **Materialize Baseline Test Harness:** Establish a runnable test harness matching the project ecosystem (e.g., Python `unittest`, Node `node:test`, Go `testing`, Rust `cargo test`).
- **Prove Execution:** Implement a minimal baseline smoke test proving that the runner executes cleanly and returns accurate exit codes.
- **Zero Synthetic Tests:** Do not generate trivial or mock tests for static configuration manifests that contain no domain logic.

---

## 6. Phase 5: Proportionate Repository Layout

Structure the repository using a necessity-driven layout model:

### Core Essentials (Mandatory for All Projects)

| File or Directory     | Purpose & Invariant                                                                                |
| :-------------------- | :------------------------------------------------------------------------------------------------- |
| `README.md`           | Canonical entry point: purpose, capabilities, quickstart, commands, and architecture.              |
| `.gitignore`          | Prevent build caches, runtime artifacts, local state, and sensitive credentials from entering git. |
| Manifests & Lockfiles | Manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) defining pinned dependencies. |
| Source Tree           | Domain-bounded source directories matching ecosystem idioms (e.g., `src/`, `cmd/`, `internal/`).   |
| Test Harness          | Dedicated test directory (`tests/`) or co-located tests, with instructions in `TESTING.md`.        |

### Layout Anti-Patterns

- Never create empty directories, placeholder files, or stub documents to satisfy a speculative enterprise template.
- Never extract separate documentation directories (`docs/`) for small projects where `README.md` or single files suffice.
- Never commit transient developer tooling state, local editor settings, or machine-specific absolute paths.

---

## 7. Phase 6: Milestone Sequencing & Walking Skeleton

Decompose early project implementation into minimal, testable milestones:

1. **Milestone 1: Risk Probe & Spike:** Validate high-risk technical assumptions with throwaway probe scripts.
2. **Milestone 2: Walking Skeleton:** Materialize the core repository layout, build configuration, baseline test harness, and one end-to-end executable path.
3. **Milestone 3: Incremental Feature Expansion:** Implement domain features sequentially, updating code, tests (`TESTING.md`), and decisions (`DECISIONS.md`) in lockstep.

---

## 8. Phase 7: Foundation Verification & Continuity Protocol

Before concluding a scaffolding session, verify foundation integrity and record continuity state:

### Foundation Verification Checklist

- [ ] Installation and bootstrap commands execute cleanly in a fresh shell without undocumented prerequisites.
- [ ] Test harness runs and passes initial baseline checks via a single standard command.
- [ ] Build and package commands produce valid executable artifacts without warnings.
- [ ] All relative Markdown links resolve to valid files.

### Four-Step Session Continuity Protocol

Document this operational rhythm in project documentation for future sessions:

1. **Context Grounding:** Inspect repository constraints, version control diffs, and live roadmap state before executing tasks.
2. **External Revalidation:** Revalidate third-party dependencies and external assumptions before beginning dependent feature work.
3. **Synchronized Evolution:** Reconcile code, tests, and living documentation (`README.md`, `TESTING.md`, `DECISIONS.md`) in lockstep.
4. **Handoff State Capture:** Document completed milestones, outstanding tasks, verification evidence, and the immediate next actionable step.

### Git Hygiene & Handoff

When version control is initialized or changes are staged:

- Ensure `.gitignore` excludes build artifacts and local state before staging files.
- Activate `commit-scribe` to create structured, high-context commits.

---

## 9. Completion Criteria

- Project memory files (`README.md`, `TESTING.md`, `DECISIONS.md`, `AGENTS.md`) are established and reflect project reality.
- The repository layout contains only necessary, purposeful files and manifests.
- The test harness is provisioned, verified, and passing baseline checks.
- Setup and run commands execute cleanly without undocumented requirements.
- The next actionable milestone is clearly identified.
