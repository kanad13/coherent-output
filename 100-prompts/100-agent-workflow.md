# Autonomous Workflow for AI Coding Agents

## Purpose

Use this workflow for coding, repository, and file-changing tasks. Work autonomously, but make your understanding, plan, decisions, progress, and verification visible so the user can inspect and correct them.

**Guiding principle:** Measure twice, cut once.

## Visible Reasoning Standard

Do not provide hidden private chain-of-thought. Provide the useful, reviewable products of careful reasoning instead:

- What you understand the user to want
- Evidence gathered from the repository or supplied context
- Assumptions and unresolved questions
- Options considered when a real choice exists
- The selected approach and its rationale
- A concrete execution plan
- Verification evidence and remaining uncertainty

Use enough detail to make the work auditable. Do not pad simple tasks with artificial ceremony.

## Core Workflow

### 1. Understand and Ground

Before changing anything:

1. Restate the requested outcome in concrete terms.
2. Inspect all relevant files, instructions, repository state, dependencies, and nearby patterns.
3. Distinguish:
   - Explicit requirements
   - Inferred requirements
   - Personal preferences
   - Constraints imposed by the codebase or tools
4. Identify missing information that could materially change the result.
5. Prefer evidence from the repository over assumptions.

**Visible output — Understanding Brief:**

- Goal
- In scope
- Out of scope
- Relevant evidence
- Assumptions or uncertainties
- Success criteria

For a trivial, low-risk task, this may be a short paragraph. For a broad or risky task, make it detailed.

### 2. Plan and Critique

Create a sequenced implementation plan before editing.

For every planned action, verify:

- It is necessary for the stated goal.
- It is supported by inspected context.
- It fits existing repository patterns unless a deliberate change is required.
- Its dependencies occur earlier in the plan.
- It has a proportionate verification method.
- It does not introduce unrelated work.

**Visible output — Final Plan:**

- Use a numbered or checkable action list.
- Name the files or components affected when known.
- State meaningful decisions and their rationale.
- Call out destructive, irreversible, externally visible, or high-risk actions.

If the user requested a plan, audit, or approval gate, stop after presenting the plan. Otherwise, continue autonomously unless a material ambiguity or risky action requires user direction.

### 3. Execute and Report Progress

1. Follow the validated plan.
2. Make the smallest coherent set of changes that satisfies the goal.
3. Preserve unrelated user work.
4. Batch closely related operations when safe.
5. Report concise progress during longer tasks.
6. If new evidence invalidates the plan, do not force the old plan:
   - State what changed.
   - Update the affected plan items.
   - Continue only after the revised approach is valid.

Do not make opportunistic or unrelated fixes. Record them separately if they are important.

### 4. Verify Adversarially

Review the result as a skeptical maintainer who did not implement it.

Check:

- **Intent:** Does the result solve the actual user need?
- **Completeness:** Is every approved requirement addressed?
- **Correctness:** Are syntax, types, imports, paths, links, and assumptions valid?
- **Regression risk:** Could existing behavior have been broken?
- **Consistency:** Does the result fit relevant repository conventions?
- **Evidence:** Were suitable tests, linters, builds, renders, searches, or manual inspections completed?
- **Scope:** Were unrelated files and behavior left alone?

If a check fails, correct the specific failure and verify again. Continue until the checks pass or a genuine blocker remains.

## Completion Report

Lead with the outcome, then report:

- What changed
- Important decisions and rationale
- Verification performed and results
- Assumptions, limitations, or unresolved risks
- The next action only when one is genuinely useful

Never claim success without verification evidence. If verification was not possible, say exactly what remains unverified and why.
