---
name: project-scaffolding
description: Audits and establishes project foundations that satisfy requirements and support durable development continuity. Defines and implements needed setup, plans, decisions, verification, and agent maintenance instructions. Use when bootstrapping a project, repairing foundations in a young repository, or establishing multi-session continuity. Do not invoke for routine feature work, ordinary handoffs, or unrelated restructuring.
---

# Project Foundations & Development Continuity

Turn project requirements and existing practices into verified foundations and a working continuity process. Follow stages 1–7 in order, carrying each stage's result into the next. Revisit the affected stage when implementation or verification changes the evidence. The project records its concrete files, tools, layout, milestones, and maintenance instructions; this skill supplies the audit, decision, implementation, and verification sequence.

## 1. Establish the Project Baseline

Inspect repository instructions, the entry document, manifests, source layout, available toolchains, version control state, existing plans, decisions, and testing guidance. Determine the requested scope: project initialization, foundation repair, or development continuity.

- **Compare Instructions With Practice:**
  - Identify how the project records implementation changes, active work, decisions, verification evidence, and next steps.
  - Check whether project instructions tell future agents where to find that information and when to maintain it.
  - Compare the current plan and documented commands with recent changes and observed repository state.
  - Check whether a new session can resume without reconstructing essential context from chat history.
- **Classify Gaps:**
  - Retain practices that already meet the requirements.
  - Identify stale, contradictory, missing, or ineffective instructions and records that require repair.
  - Identify existing record locations and information that lacks a canonical home.
  - Report material unresolved choices or inaccessible context; label inferred requirements rather than treating them as confirmed.

- **Stage Result:**
  - Record the current foundations, continuity practices, evidence of effectiveness, and gaps within the requested scope. Use this baseline to define requirements in stage 2.

## 2. Define Foundation Requirements and Acceptance Criteria

Use the baseline and agreed scope to define what the foundations must support:

- **Operational Context:**
  - Identify users or callers, primary workflows, and intended environments: command line, service, library, worker, browser, or desktop.
  - Establish target platforms, runtime constraints, packaging expectations, and explicit exclusions.
- **Risk Boundaries:**
  - Identify persistence, filesystem mutations, data ownership, network access, and trust boundaries.
  - Assess failure consequences such as data loss, corruption, security exposure, and crashes.
- **Required Outcomes:**
  - Identify the functionality, runtime integration, reliability, and development practices required for the current milestone.
  - Define runnable workflows that demonstrate those requirements and expose the principal technical risks.
  - State observable acceptance criteria and evidence required to declare the foundations ready.
  - Sequence milestones by dependencies and risk, and record later work separately from the current commitment.

For development continuity work, define acceptance criteria around the project's existing workflows, records, and ability to resume work.

- **Stage Result:**
  - Record foundation requirements, acceptance criteria, required evidence, and milestone dependencies. Incorporate these requirements into the canonical project records in stage 3.

## 3. Establish Discoverable Project Memory

Use the requirements to designate and populate a canonical home for each needed kind of information. Choose sections, files, or project tools that future agents can access. The table identifies the required information and possible locations.

| Information           | What Must Be Discoverable                                                                | Possible Home                                                  |
| :-------------------- | :--------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| Purpose and operation | Scope, setup, run commands, prerequisites, and architecture overview                     | `README.md` or existing entry document                         |
| Change history        | Inspectable implementation changes and meaningful reasons                                | Version control history or an existing change record           |
| Active plan           | Current goal, acceptance criteria, progress, blockers, and next action                   | `PLAN.md`, a README section, or an accessible project tracker  |
| Decisions             | Non-obvious constraints, alternatives, chosen approach, trade-offs, and revisit triggers | `DECISIONS.md`, existing decision records, or a README section |
| Verification          | Real workflows, expected outcomes, checks, commands, and execution triggers              | `TESTING.md` or existing testing documentation                 |
| Agent workflow        | Where to read context and when to update the canonical records                           | `AGENTS.md` or an existing project instruction file            |

- **Maintain Canonical Records:**
  - Choose record locations according to the amount of information, navigation needs, and maintenance responsibilities.
  - Link canonical homes from the project entry point and agent instructions.
  - Keep plans and operational guidance current; retain decision rationale and mark superseded decisions explicitly.
  - Use version control for implementation history where appropriate. Initialize missing local version control when within scope; commits and remote publication require an authorized Git workflow.
  - Populate records with current project facts and decisions, and link shared information to its canonical home.

- **Stage Result:**
  - Provide populated canonical records and an entry point that identifies their locations. Use these locations to write maintenance instructions in stage 4.

## 4. Encode and Audit the Maintenance Contract

Write project-specific instructions in the designated agent instruction file, or another location the project uses for agent guidance. The instructions must tell future agents to perform these actions at the relevant points:

| Trigger                                             | Required Project Practice                                                                                                                |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| Start or resume work                                | Read the canonical plan, relevant decisions, testing guidance, and version control changes; reconcile stale state before dependent work. |
| Select the next increment                           | Record the intended outcome, acceptance criteria, scope, and necessary verification in the active plan.                                  |
| Complete an increment or encounter a blocker        | Update progress, verification status, blockers, and the next actionable step.                                                            |
| Discover a changed requirement or failed assumption | Revise the affected plan and record the reason before continuing work that depends on the old assumption.                                |
| Make a consequential design choice                  | Record the rationale, considered alternatives, trade-offs, and conditions for revisiting the choice.                                     |
| Change behavior, interfaces, tooling, or setup      | Update affected tests and canonical instructions alongside implementation; audit the testing strategy when its assumptions change.       |
| End a session or hand off work                      | Record completed work, remaining work, unresolved decisions, verification evidence, and the next action.                                 |

- **Make the Contract Executable:**
  - Name the project's actual record locations and commands rather than copying generic instructions.
  - Specify applicable verification and skill triggers; reference available skills only where their workflows are needed.
  - Route to `test-strategist` for strategy or harness gaps when available. Routine checks follow the established project strategy.
  - Carry forward project constraints and prohibited patterns without duplicating universal agent policy.
- **Check Effectiveness:**
  - Compare an active or recent work item with repository changes and recorded progress.
  - Confirm that changed assumptions, completed work, and remaining gaps are reflected where the instructions require them.
  - Repair stale records and missing maintenance triggers within the authorized task.

Verify the maintenance contract against actual record updates and project state. For a new project, establish the initial records and verify that the instructions explain how the first increment will update them.

- **Stage Result:**
  - Install project-specific maintenance instructions and reconcile the records with current state. Use the resulting plan and constraints to guide implementation in stage 5.

## 5. Implement the Required Technical Foundations

Compare the foundation requirements with the current stack and layout. Decide which capabilities to retain, add, or change, and implement the decisions covered by the agreed scope.

- **Select a Suitable Stack:**
  - Select tools that satisfy the functional, deployment, reliability, and maintenance requirements.
  - Compare suitable approaches by complexity, integration effort, and long-term cost.
  - Use `web-research` to validate unfamiliar dependencies, current compatibility, or external contracts before relying on them.
  - Use `worth-the-squeeze` for major frameworks or complex dependencies; account for installation and long-term maintenance.
  - Use ecosystem-appropriate manifests, version constraints, and lockfiles to make dependency resolution reproducible.
- **Resolve Critical Unknowns:**
  - Run a bounded, isolated probe when documentation cannot establish a critical runtime assumption.
  - Use the result to choose or revise the approach; discard throwaway probes after capturing relevant findings.
- **Establish the Project Layout:**
  - Use source organization appropriate to the ecosystem and current domain boundaries.
  - Add manifests and build configuration when the project needs them.
  - Configure ignore rules for generated artifacts, runtime state, and secrets when using version control.
  - Place source, tests, and documentation where project conventions make them discoverable.
  - Organize files around implemented capabilities and maintained documentation.
  - Keep transient developer state and machine-specific paths out of shared foundations.

- **Stage Result:**
  - Provide the agreed setup, stack, layout, and runnable capabilities, with decisions and commands recorded. Identify any blocked requirement before configuring verification in stage 6.

## 6. Establish Verification for Real Behavior

Use the requirements and technical foundations to establish checks for the agreed outcomes. Activate `test-strategist` for gaps in the project's verification strategy or harness. Record the workflows, commands, expected results, and execution triggers in the canonical testing instructions.

- **Match Actual Use:**
  - Verify the real entry point, actions, expected results, and relevant system boundaries.
  - Include browser or native interaction when the outcome depends on a user interface.
  - Assert on project outcomes and relevant side effects so the checks detect broken behavior.
- **Sequence Work by Evidence:**
  - Resolve high-risk assumptions early when probes are needed.
  - Connect the checks to the agreed runnable workflows and acceptance criteria.
  - Update the plan, relevant decisions, and testing strategy as implementation and evidence change.
  - Revise milestone sequencing when project dependencies or risks change.

- **Stage Result:**
  - Provide executable checks or repeatable manual procedures tied to the acceptance criteria. Use these procedures to verify foundations and continuity in stage 7.

## 7. Verify Foundations and Demonstrate Continuity

Run applicable documented setup, launch, test, and packaging commands. Inspect results against the acceptance criteria. Check reproducibility in a clean or isolated environment where practical; disclose environment-dependent prerequisites.

- **Verify Usability:**
  - Exercise the agreed workflows and confirm their observable results.
  - When a package is produced, launch or load the actual artifact and exercise a representative path in its intended runtime.
  - Build success and screenshots alone do not establish runtime behavior.
  - Verify that documentation references lead to existing canonical records and usable commands.
- **Verify Continuity:**
  - Reconcile the plan with completed work, blockers, and the next action.
  - Capture consequential decisions and verification evidence in their designated homes.
  - Confirm that another agent can locate the current state and follow the maintenance contract without private chat context.
- **Report Limits and Git Status:**
  - Identify failed or blocked checks, the exact barrier, and the remaining unverified outcome.
  - Commit or push only when the authorized workflow includes Git finalization.
  - Activate `commit-scribe` before staging, committing, or pushing.

- **Stage Result:**
  - Record observed results, completed requirements, unresolved gaps, and the next action in the canonical records. Report foundation readiness and continuity status against the acceptance criteria.

## 8. Completion Criteria

- Existing foundations and continuity practices are audited; effective practices remain and identified gaps are repaired.
- Canonical records capture current scope, changes, plan, decisions, verification status, and the next action.
- Project instructions identify those records and require updates at the points where project state changes.
- Technical foundations added within scope support a demonstrated real outcome with usable setup and run commands.
- Another session can resume from discoverable project state.

Report incomplete foundations explicitly when required runtime proof or continuity evidence is blocked. Identify the remaining requirement and the action needed to establish it.
