---
name: project-scaffolding
description: Audits and establishes project foundations that satisfy requirements and support durable development continuity. Defines and implements needed setup, plans, decisions, verification, and agent maintenance instructions. Use when bootstrapping a project, repairing foundations in a young repository, or establishing multi-session continuity. Do not invoke for routine feature work, ordinary handoffs, or unrelated restructuring.
---

# Project Foundations & Development Continuity

Turn project requirements and existing practices into verified foundations and a working continuity process. Follow stages 1–7 in order, carrying each stage's findings into the next, and revisit a stage when later evidence changes it. The project records its concrete files, tools, layout, and maintenance instructions; this skill supplies the audit, decision, implementation, and verification sequence.

**Size the work to the project.** A script or single-session task needs a README section and one verification command, nothing more. Add `PLAN.md`, `DECISIONS.md`, and `TESTING.md` only when work will span sessions or involves non-obvious decisions. Never create a record that has nothing current to say.

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

Give each needed kind of information one canonical home that future agents can find. Link shared facts to that home instead of repeating them.

| Information           | What Must Be Discoverable                                                                | Possible Home                                                  |
| :-------------------- | :--------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| Purpose and operation | Scope, setup, run commands, prerequisites, and architecture overview                     | `README.md` or existing entry document                         |
| Change history        | Inspectable implementation changes and meaningful reasons                                | Version control history or an existing change record           |
| Active plan           | Current goal, acceptance criteria, progress, blockers, and next action                   | `PLAN.md`, a README section, or an accessible project tracker  |
| Decisions             | Non-obvious constraints, alternatives, chosen approach, trade-offs, and revisit triggers | `DECISIONS.md`, existing decision records, or a README section |
| Verification          | Real workflows, expected outcomes, checks, commands, and execution triggers              | `TESTING.md` or existing testing documentation                 |
| Agent workflow        | Where to read context and when to update the canonical records                           | `AGENTS.md` or an existing project instruction file            |

- **Instruction file:** use `AGENTS.md` as the canonical file. Claude Code reads it directly when no `CLAUDE.md` exists; if a `CLAUDE.md` already exists, have it import `AGENTS.md` (`@AGENTS.md`) rather than copying it.
- **Keep records current:** update plans and operating guidance in place, retain decision rationale, and mark superseded decisions explicitly. Route history to version control, not to living documents.
- **Version control:** initialize local version control when it is missing and within scope. Commits and remote publication follow the authorized Git workflow.
- **Minimal shapes** (extend only when the project needs more):

```markdown
# Plan

Goal: <one sentence>
Acceptance: <observable checks>
Done: <items>
Next action: <one concrete, runnable step>
Blockers: <none | list>
```

```markdown
## <date> — <decision>

Context: <constraint or problem>
Chosen: <approach> Alternatives: <rejected options and why>
Revisit when: <condition>
```

## 4. Encode and Audit the Maintenance Contract

Write project-specific instructions in the instruction file. They must tell future agents to act at these points:

| Trigger                                             | Required Project Practice                                                                                                                |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| Start or resume work                                | Read the canonical plan, relevant decisions, testing guidance, and version control changes; reconcile stale state before dependent work. |
| Select the next increment                           | Record the intended outcome, acceptance criteria, scope, and necessary verification in the active plan.                                  |
| Complete an increment or encounter a blocker        | Update progress, verification status, blockers, and the next actionable step.                                                            |
| Discover a changed requirement or failed assumption | Revise the affected plan and record the reason before continuing work that depends on the old assumption.                                |
| Make a consequential design choice                  | Record the rationale, considered alternatives, trade-offs, and conditions for revisiting the choice.                                     |
| Change behavior, interfaces, tooling, or setup      | Update affected tests and canonical instructions alongside implementation; audit the testing strategy when its assumptions change.       |
| End a session or hand off work                      | Record completed work, remaining work, unresolved decisions, verification evidence, and the next action.                                 |

Name the project's real files and commands, not generic advice. Reference a skill only where its workflow is needed, and carry forward project constraints without repeating universal agent policy. A sample of the finished text:

```markdown
## Working agreements

- Start: read PLAN.md, the latest DECISIONS.md entries, and `git log -10`; fix stale items first.
- Before an increment: write its goal and acceptance check in PLAN.md.
- After it: update PLAN.md, then run `<test command>`.
- A design choice with trade-offs: add a DECISIONS.md entry.
- A behavior or tooling change: update TESTING.md and the README in the same change.
- End of session: leave "Next action" runnable by a reader with no chat history.
```

**Check effectiveness:** compare a recent work item with repository changes and recorded progress. Repair stale records and missing triggers within the authorized task.

## 5. Implement the Required Technical Foundations

Act only on what is undecided or broken: compare requirements with the current stack and layout, then retain, add, or change.

- **Stack:**
  - Choose tools that meet the functional, deployment, reliability, and maintenance needs at the lowest integration cost.
  - Activate `web-research` for unfamiliar dependencies, current compatibility, or external contracts. Without it, check official documentation and state what remains unverified.
  - Activate `worth-the-squeeze` for major frameworks or heavy dependencies. Without it, weigh the benefit against installation and long-term upkeep.
  - Use ecosystem-standard manifests, version constraints, and lockfiles.
- **Unknowns:** run a bounded, isolated probe when documentation cannot settle a critical runtime assumption. Record the finding; discard the probe.
- **Layout and hygiene:**
  - Use the ecosystem's conventional source, test, and documentation layout.
  - Ignore generated artifacts, runtime state, and secrets. Keep machine-specific paths out of shared files.
  - For a public repository, decide the license. Add a CI job that runs the documented verification command.

## 6. Establish Verification for Real Behavior

Activate `test-strategist` for the strategy, harness, and `TESTING.md`. Without it, define for each acceptance criterion the real entry point, the action, the expected observable result, and the command or manual procedure, and record them in the testing document. Resolve high-risk assumptions early, and revise milestone order when evidence changes the risks.

## 7. Verify Foundations and Demonstrate Continuity

- **Run it:** execute the documented setup, launch, test, and packaging commands in a clean or isolated environment where practical. Disclose environment-dependent prerequisites. For a produced package, launch the actual artifact. Build success and screenshots alone do not establish runtime behavior.
- **Cold-start test:** start a fresh agent or subagent with only the repository. Ask it for the current goal, the last verified result, and the next action, and have it run the documented check. Each wrong or missing answer marks a gap in the records or instructions. Repair it and repeat.
- **Report honestly:** name failed or blocked checks, the exact barrier, and the unverified outcome. Hand any staging, committing, or pushing to `commit-scribe` with the user's Git instructions.

## 8. Completion Criteria

- Existing practices are audited; effective ones remain and gaps are repaired.
- Canonical records hold current scope, plan, decisions, verification status, and the next action.
- The instruction file names those records and the points where they change.
- Foundations added within scope support a demonstrated real outcome with usable setup and run commands.
- The cold-start test passes.

If runtime proof or continuity evidence is blocked, report the foundations as incomplete and name the missing requirement and the action needed.
