# Prompt Audit

## Purpose

Apply this methodology when auditing AI prompts to produce evidence-based improvement reports. Identify what the prompt is trying to do, whether it does that job reliably, and which specific changes would improve it.

Produce the audit first. A rewrite follows after the user reviews the findings and requests implementation. The audit must contain enough concrete guidance for a capable AI agent to perform that rewrite later.

## Audit Principles

- Judge the prompt against its intended user, use case, and contract.
- Treat personal output preferences as requirements and flag any direct conflict with the prompt's purpose.
- Prefer one clear job per prompt.
- Supporting analysis and verification are allowed when they directly improve that job.
- Include examples, workflows, length rules, and visible progress when they materially help this prompt.
- Require inspectable artifacts such as assumptions, evidence, decisions, plans, and validation results.
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
- **Focus boundaries:** Adjacent tasks reserved for another prompt or follow-up

Record an unclear contract as a finding and identify the missing information.

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

Assess each dimension as `Strong`, `Needs attention`, or `Context-dependent`.

| Dimension                | What to examine                                                                  |
| ------------------------ | -------------------------------------------------------------------------------- |
| Purpose                  | Is there one clear primary job?                                                  |
| Activation               | Is it clear when this prompt applies?                                            |
| Inputs                   | Are required inputs and missing-data behavior defined?                           |
| Workflow                 | Are steps necessary, ordered, and executable?                                    |
| Decision support         | Are important choices supported near the point of use?                           |
| Output contract          | Is the deliverable explicit and usable?                                          |
| Scope control            | Are focus boundaries and handoff points clear?                                   |
| Instruction consistency  | How well do the requirements reinforce one another?                              |
| Tool realism             | Are tool, browsing, file, and permission assumptions realistic?                  |
| Accuracy and uncertainty | How effectively does it ground claims and expose uncertainty?                    |
| User fit                 | Does it honor the intended user's accessibility, detail, tone, and format needs? |
| Efficiency               | Is the prompt complete and as concise as its purpose allows?                     |
| Verification             | Does it validate the promised result using observable checks?                    |
| Maintainability          | Can a future editor understand and update it safely?                             |

### 4. Test Representative Scenarios

Mentally simulate at least:

- A normal input
- A minimal or incomplete input
- An ambiguous or conflicting input
- A large or complex input
- A tool or evidence failure, when relevant

Report scenario findings that demonstrate a real strength or failure mode. Use sample outputs when they provide evidence for the finding.

Record the results in a scenario table:

| Scenario | Expected behavior | Prompt support observed | Finding |
| -------- | ----------------- | ----------------------- | ------- |

### 5. Determine Disposition

Choose one:

- **Keep:** Ready as written
- **Update:** Same job, targeted improvements needed
- **Major rework:** Same job, unreliable current design
- **Split:** Contains independently invokable jobs
- **Merge:** Substantially duplicates another named prompt
- **Retire:** Superseded by another prompt or incompatible with the library

Recommend merging for true duplication and preserve purpose-built boundaries across distinct jobs.

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
- **Tools or permissions:**
- **Focus boundaries:**

## Overall Assessment

- **Disposition:** [Keep / Update / Major rework / Split / Merge / Retire]
- **Readiness:** [Ready / Minor revisions / Major revisions]
- [Short summary]

## Component Map

- [Concise map of the current prompt]

## Scorecard

| Dimension | Assessment | Evidence from the prompt | Impact |
| --------- | ---------- | ------------------------ | ------ |

## Scenario Tests

| Scenario | Expected behavior | Prompt support observed | Finding |
| -------- | ----------------- | ----------------------- | ------- |

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
