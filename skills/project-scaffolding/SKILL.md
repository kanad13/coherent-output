---
name: project-scaffolding
description: Audits and establishes project foundations that satisfy requirements and support durable development continuity. Defines and implements needed setup, plans, decisions, verification, and agent maintenance instructions. Use when bootstrapping a project, repairing foundations in a young repository, or establishing multi-session continuity. Do not invoke for routine feature work, ordinary handoffs, or unrelated restructuring.
---

# Project Foundations & Development Continuity

Turn project requirements and existing practices into verified foundations and a working continuity process. Follow stages 1–7 in order, carrying each stage's findings into the next, and revisit a stage when later evidence changes it. The project records its concrete files, tools, layout, and maintenance instructions; this skill supplies the audit, decision, implementation, and verification sequence.

**Size the work to the project.** A script or single-session task needs a `README.md` section and one verification command, nothing more. Add `[docs/010-plan.md](docs/010-plan.md)`, `[docs/020-decisions.md](docs/020-decisions.md)` (or `docs/020-decisions/`), and `[tests/README.md](tests/README.md)` only when work will span sessions or involves non-obvious decisions.

## 1. Establish the Project Baseline

Inspect repository instructions, the entry document, manifests, source layout, toolchains, version control state, existing plans, decisions, and testing guidance. Determine the scope: initialization, foundation repair, or continuity.

- **Compare instructions with practice:**
  - Find how the project records changes, active work, decisions, verification evidence, and next steps.
  - Check that project instructions tell future agents where that information lives and when to update it.
  - Compare the current plan and documented commands with recent changes and observed repository state.
- **Classify gaps:**
  - Retain practices that already work. Repair stale, contradictory, or missing records.
  - Report material unresolved choices or inaccessible context; label inferred requirements as inferred.

## 2. Define Requirements and Acceptance Criteria

Answer four questions from the baseline and the agreed scope:

1. **Who runs it, where?** Callers, primary workflows, target platforms, runtime constraints, explicit exclusions.
2. **What can go wrong?** Persistence, filesystem mutation, network access, trust boundaries, and the consequence of failure (data loss, corruption, exposure).
3. **What must work for the current milestone?** Functionality, integration, reliability, and the runnable workflows that expose the main technical risks.
4. **What evidence declares it ready?** Observable acceptance criteria, ordered by dependency and risk. Record later work separately from the current commitment.

For continuity-only work, define acceptance criteria around existing workflows, records, and the ability to resume.

## 3. Establish Discoverable Project Memory

Give each needed kind of information one canonical home that future agents can find. Link shared facts to that home.

- **Clean root layout:** place primary entrypoints (`README.md`, `AGENTS.md`), project manifests (such as `package.json` or `pyproject.toml`), and standard tool configurations (`.gitignore`, `LICENSE`) in the repository root. Place operational records in designated subdirectories: active plans and decisions in `docs/`, and verification guides in `tests/`.
- **File references:** format all repository file paths as clickable markdown links with relative paths (such as `[docs/010-plan.md](docs/010-plan.md)`).

| Information           | What Must Be Discoverable                                                                                       | Possible Home                                                                                         |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| Purpose and operation | Scope, setup, run commands, prerequisites, and architecture overview                                            | `README.md` or existing entry document                                                                |
| Change history        | Inspectable implementation changes and meaningful reasons                                                       | Version control history or an existing change record                                                  |
| Active plan           | Current goal, acceptance criteria, progress, blockers, and next action                                          | `[docs/010-plan.md](docs/010-plan.md)`, a `README.md` section, or an accessible project tracker       |
| Decisions             | Each non-obvious choice as one current rule: where it applies, the approach, rejected options, revisit triggers | `[docs/020-decisions.md](docs/020-decisions.md)` (or `docs/020-decisions/`), or a `README.md` section |
| Verification          | Real workflows, expected outcomes, checks, commands, and execution triggers                                     | `[tests/README.md](tests/README.md)` or existing test documentation                                   |
| Agent workflow        | Where to read context and when to update canonical records                                                      | `AGENTS.md` or an existing project instruction file                                                   |

- **Instruction file:** use `AGENTS.md` as the canonical file. Link shared facts from `AGENTS.md` to `docs/` and `[tests/README.md](tests/README.md)`.
- **Active plan upkeep and pruning:** maintain the active plan in `[docs/010-plan.md](docs/010-plan.md)` as an execution steering aid. Bounded size: keep under 35 lines. Pruning rule: at each new increment or end of turn, prune completed items older than the immediately preceding step. Record historical achievements in git commit messages.
- **Single home for architecture and decisions:**
  - Place a concise, high-level architecture overview (component topology, entry points) directly in `README.md`.
  - Record all concrete architectural rules, boundaries, component choices, invariants, and trade-offs in `[docs/020-decisions.md](docs/020-decisions.md)` (or `docs/020-decisions/`), numbered sequentially (`001`, `002`).
  - Decisions represent active current state: write every decision as an active governing rule (the chosen approach, its operational constraints, and factual rejection reasons), preserving historical context via commit history.
  - Decision lineage: when requirements change, update the decision status to `Status: Superseded by Decision XXX` and link to the replacement record.
- **Version control:** initialize local version control when it is missing and within scope. Commits and remote publication follow the authorized Git workflow.
- **Minimal shapes** (extend only when the project needs more):

````markdown
# <Project Name>: Repository Instructions

This document defines project-specific paths, files, and working agreements. Universal agent operating directives apply globally and are not repeated here.

## Where things live

| Path                                           | Role                                           |
| :--------------------------------------------- | :--------------------------------------------- |
| [README.md](README.md)                         | Project overview, setup, and run instructions. |
| [docs/010-plan.md](docs/010-plan.md)           | Active milestone, progress, and next step.     |
| [docs/020-decisions.md](docs/020-decisions.md) | Active architectural decisions and rules.      |
| [tests/README.md](tests/README.md)             | Verification commands and expected outcomes.   |

## Working agreements

- **Start of turn:** inspect `[docs/010-plan.md](docs/010-plan.md)`, latest decisions in `[docs/020-decisions.md](docs/020-decisions.md)`, and recent `git log`; reconcile stale state before editing.
- **Before an increment:** record the concrete goal, acceptance check, and next step in `[docs/010-plan.md](docs/010-plan.md)`.
- **After an increment:** prune completed items older than the immediate prior step, update blockers, and run verification.
- **Consequential design choice:** add an active rule to `[docs/020-decisions.md](docs/020-decisions.md)` before implementing.
- **Behavioral or tooling change:** update `[tests/README.md](tests/README.md)` and `[README.md](README.md)` in the same change.
- **End of turn:** ensure `Next action` in `[docs/010-plan.md](docs/010-plan.md)` is runnable by a reader with no prior context.

## Verification

```bash
<canonical test command>
```
````

````

```markdown
# Active Plan

Goal: <one sentence defining active milestone>
Acceptance: <observable checks>
Next action: <one concrete, runnable step>
Blockers: <none | list>

Recent context:

- [x] <immediately preceding completed step>
````

```markdown
# Architectural Decision Records

## Decision 001 - <the chosen approach, named as a noun phrase>

Status: Accepted <!-- or Superseded by Decision XXX -->

### Decision context

<The situation in which this decision governs: what is being decided and the constraint forcing the choice.>

### Selected approach

<The rule. State the active requirement, operational approach, and governing constraints.>

### Rejected approaches

- `<Option>`: <the property that rules it out, as a fact.>

### Revisit decision when

- <An observable condition or threshold that reopens the decision.>
```

Write a decision record as an active current rule, not a story:

- **Title:** names the chosen approach. Number records sequentially in order (`001`, `002`).
- **Status:** explicitly states `Status: Accepted` or `Status: Superseded by Decision XXX`.
- **Context:** states where the decision applies and the constraint that forced the choice.
- **Selected approach:** gives instructions a reader can follow without the other sections.
- **Rejected approaches:** states one fact-based line per option, focusing on the technical property that eliminated it.
- **Revisit:** names an observable condition or threshold that reopens the decision.
- **Changes:** edit the record in place or mark as superseded to preserve continuity.

## 4. Encode and Audit the Maintenance Contract

Write project-specific instructions in `AGENTS.md` following the template above. Global policies define universal agent habits; `AGENTS.md` binds those habits to the concrete layout, commands, and rules of this project.

Ensure the working agreements in `AGENTS.md` cover these operational points:

| Trigger                                             | Required Project Practice                                                                                                                 |
| :-------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| Start or resume work                                | Read the canonical plan, relevant decisions, testing guidance, and version control changes; reconcile stale state before dependent work.  |
| Select the next increment                           | Record the intended outcome, acceptance criteria, scope, and necessary verification in the active plan; prune older completed tasks.      |
| Complete an increment or encounter a blocker        | Update progress, verification status, blockers, and the next actionable step.                                                             |
| Discover a changed requirement or failed assumption | Revise the affected plan and record the reason before continuing work that depends on the old assumption.                                 |
| Make a consequential design choice                  | Add a decision record: its context, selected approach, rejected approaches, and revisit conditions.                                       |
| Change behavior, interfaces, tooling, or setup      | Update affected tests and canonical instructions alongside implementation; audit the testing strategy when its assumptions change.        |
| End a session or hand off work                      | Record completed work, remaining work, unresolved decisions, verification evidence, and the next action; prune completed checklist items. |

**Check effectiveness:** compare a recent work item with repository changes and recorded progress. Repair stale records and missing triggers within the authorized task.

## 5. Implement the Required Technical Foundations

Focus implementation on undecided requirements or failing workflows: compare requirements with the current stack and layout, then retain, add, or change.

As an orchestrating workflow, this skill delegates focused audits to specialized lenses. If a lens is unavailable, apply the inline fallback:

- **Stack & Dependencies:**
  - Choose tools that meet functional, deployment, reliability, and maintenance needs at the lowest integration cost. Use ecosystem-standard manifests, version constraints, and lockfiles.
  - Activate `web-research` for unfamiliar dependencies, current compatibility, or external contracts. Without it, check official documentation and state what remains unverified.
  - Activate `worth-the-squeeze` for major frameworks or heavy dependencies. Without it, weigh the benefit against installation and long-term upkeep.
- **Unknowns:** run a bounded, isolated probe when documentation cannot settle a critical runtime assumption. Record the finding; discard the probe.
- **Layout and Hygiene:**
  - Use the ecosystem's conventional source, test, and documentation layout.
  - Track untracked runtime artifacts, build outputs, and secrets in `.gitignore`. Provide a `.env.example` template when environment variables are needed.
  - Ensure shared configurations use project-relative or environment paths. For a public repository, include a license.
- **Automation & Tooling:**
  - Add standard format and lint configurations where appropriate for the language ecosystem.
  - Add a CI workflow definition that runs the documented verification check on push.

## 6. Establish Verification for Real Behavior

Activate `test-strategist` for the strategy, harness, and `[tests/README.md](tests/README.md)`. Without it, define for each acceptance criterion the real entry point, the action, the expected observable result, and the command or manual procedure, and record them in `[tests/README.md](tests/README.md)`. Resolve high-risk assumptions early, and revise milestone order when evidence changes the risks.

## 7. Verify Foundations and Demonstrate Continuity

- **Run it:** execute documented setup, launch, test, and packaging commands in a clean or isolated environment where practical. Disclose environment-dependent prerequisites. Validate runtime behavior by executing the actual artifact and inspecting output directly.
- **Cold-start test:** start a fresh agent or subagent with only the repository. Ask it for the current goal, the last verified result, and the next action, and have it run the documented check. If subagents are unavailable, simulate a cold start by evaluating whether a fresh reader with only the working tree can execute the next step without conversational context. Each wrong or missing answer marks a gap in the records or instructions. Repair it and repeat.
- **Report honestly:** name failed or blocked checks, the exact barrier, and the unverified outcome. Hand any staging, committing, or pushing to `commit-scribe` with the user's Git instructions.

## 8. Completion Criteria

Confirm the scaffolding satisfies both positive deliverables and negative constraints:

- **Practices & Records:** Canonical records hold current scope, plan, decisions, verification status, and next action. Existing effective practices remain.
- **Instruction Contract:** `AGENTS.md` names those records, their roles, and working agreements for project lifecycle triggers.
- **Clean Root Audit:** The repository root contains only primary entrypoints and manifests; verify that no secondary operational files (such as `PLAN.md`, `architecture.md`, `DECISIONS.md`, `TESTING.md`, or `TODO.md`) remain at the bare root.
- **Unified Architecture Audit:** Architectural rules and invariants reside in `[docs/020-decisions.md](docs/020-decisions.md)` and `README.md`; verify that no separate `architecture.md` or duplicate documentation file exists.
- **Decision Lineage Audit:** Superseded decisions remain in place with explicit links to successor records; verify that no past decisions were erased.
- **Foundations & Tooling:** Foundations added within scope support a demonstrated real outcome with usable setup, run, and CI commands.
- **Cold-Start Verification:** The cold-start test passes: a fresh reader or agent with only the repository can identify the current goal, last verified result, and next action, and run the documented check.

If runtime proof or continuity evidence is blocked, report the foundations as incomplete and name the missing requirement and the action needed.
