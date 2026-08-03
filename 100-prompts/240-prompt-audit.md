# Prompt Audit

## Purpose

Audit one AI prompt and produce an evidence-based improvement report. Identify what the prompt is trying to do, whether it does that job reliably, and which specific changes would improve it.

Do not rewrite the prompt unless the user asks after reviewing the audit. The audit must contain enough concrete guidance for a capable AI agent to perform that rewrite later.

## Audit Principles

- Judge the prompt against its intended user and use case, not generic prompt-writing fashion.
- Treat personal output preferences as requirements unless they directly undermine the prompt's purpose.
- Prefer one clear job per prompt.
- Supporting analysis and verification are allowed when they directly improve that job.
- Do not require examples, rigid workflows, fixed lengths, or visible progress unless they materially help this prompt.
- Do not request private chain-of-thought. Require inspectable artifacts such as assumptions, evidence, decisions, plans, and validation results.
- Distinguish genuine conflicts from mere verbosity.

## Workflow

### 1. Establish the Prompt Contract

Identify:

- **Objective:** The single primary job
- **User:** Who will use the output and what they need from it
- **Trigger:** When the prompt should be invoked
- **Inputs:** Required and optional information
- **Primary output:** The main deliverable
- **Completion condition:** How success can be observed
- **Tools or permissions:** Browsing, code execution, file reads, edits, external actions
- **Non-goals:** Adjacent tasks the prompt should not perform

If the contract cannot be inferred reliably, mark that as a finding rather than silently inventing it.

### 2. Map the Prompt

Create a concise component map:

- Role or expertise
- Workflow phases
- Decision rules
- Output format
- Guardrails
- Examples and reference material
- Validation steps

Identify duplicated, conflicting, unreachable, or misplaced instructions.

### 3. Evaluate the Prompt

Assess each dimension as `Strong`, `Needs attention`, or `Not applicable`.

| Dimension | What to examine |
| --- | --- |
| Purpose | Is there one clear primary job? |
| Activation | Is it clear when this prompt applies? |
| Inputs | Are required inputs and missing-data behavior defined? |
| Workflow | Are steps necessary, ordered, and executable? |
| Decision support | Are important choices supported near the point of use? |
| Output contract | Is the deliverable explicit and usable? |
| Scope control | Are non-goals and handoff points clear? |
| Instruction consistency | Do requirements reinforce rather than contradict one another? |
| Tool realism | Are tool, browsing, file, and permission assumptions realistic? |
| Accuracy and uncertainty | Does it prevent invention and expose uncertainty appropriately? |
| User fit | Does it honor the intended user's accessibility, detail, tone, and format needs? |
| Efficiency | Is the prompt as long and rigid as necessary, but no more? |
| Verification | Does it validate the promised result using observable checks? |
| Maintainability | Can a future editor understand and update it safely? |

### 4. Test Representative Scenarios

Mentally simulate at least:

- A normal input
- A minimal or incomplete input
- An ambiguous or conflicting input
- A large or complex input
- A tool or evidence failure, when relevant

Report only scenario findings that expose a real strength or failure mode. Do not fabricate sample outputs merely to fill the report.

### 5. Determine Disposition

Choose one:

- **Keep:** Ready as written
- **Update:** Same job, targeted improvements needed
- **Major rework:** Same job, unreliable current design
- **Split:** Contains independently invokable jobs
- **Merge:** Substantially duplicates another named prompt
- **Retire:** Adds no distinct value or conflicts with the library

Recommend merging only for true duplication. Do not create a larger general-purpose prompt merely to reduce file count.

## Output Format

```markdown
# Prompt Audit Report

## Contract

- **Objective:**
- **User:**
- **Trigger:**
- **Inputs:**
- **Primary output:**
- **Completion condition:**
- **Non-goals:**

## Overall Assessment

- **Disposition:** [Keep / Update / Major rework / Split / Merge / Retire]
- **Readiness:** [Ready / Minor revisions / Major revisions]
- [Short summary]

## Component Map

- [Concise map of the current prompt]

## Scorecard

| Dimension | Assessment | Evidence from the prompt | Impact |
| --- | --- | --- | --- |

## What Works

- [Specific strength and why it matters]

## Findings and Recommended Changes

1. **[Finding]**
   - **Evidence:** [Relevant instruction or omission]
   - **Impact:** [How it affects actual use]
   - **Change:** [Concrete revision]

## Overlap and Placement

- **Related prompts:**
- **Merge or split recommendation:**
- **Filename or ordering recommendation:**

## Rewrite Brief

- **Preserve:** [Effective requirements]
- **Change:** [Prioritized changes]
- **Remove:** [Instructions that undermine the contract]
- **Add:** [Missing safeguards or decision rules]
```

Every recommendation must be traceable to the prompt's intended contract or a demonstrated failure mode.
