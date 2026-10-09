---
name: claim-validator
description: Stress-tests claims, proposals, and strategies against verified evidence, exposes failure modes, and renders calibrated verdicts. Use when evaluating assertions, auditing proposals, fact-checking claims, or performing risk assessments. Do not use for assessing code ROI or architectural churn (use worth-the-squeeze instead).
---

# Evidence-Based Claim Validator

Follow this methodology to stress-test claims, arguments, technical proposals, and strategic assumptions against verified evidence. Execute a disconfirmation-first audit to uncover counter-examples, unstated dependencies, and failure modes, delivering a calibrated verdict with concrete source citations.

---

## 1. Core Principles & Verdict Scale

- **Hypothesis Framing:** Treat every assertion as a hypothesis requiring rigorous validation. Reformulate claims into their strongest, most falsifiable versions before testing.
- **Disconfirmation Search:** Actively seek contradictory evidence, counter-examples, and hidden failure modes as aggressively as supporting data.
- **Calibrated 5-Verdict Matrix:**

  | Verdict                 | Definition                                                                                  |
  | :---------------------- | :------------------------------------------------------------------------------------------ |
  | **SUPPORTED**           | Strong, authoritative evidence verifies the claim; material counter-arguments are resolved. |
  | **PARTIALLY SUPPORTED** | Core premise has evidence, but scope, conditions, or certainty are overstated.              |
  | **INCONCLUSIVE**        | Evidence is mixed, indirect, conflicting, or dependent on unverified assumptions.           |
  | **CONTRADICTED**        | Authoritative evidence directly conflicts with the claim or reveals a fatal defect.         |
  | **REFRAME REQUIRED**    | The claim is vague, circular, or unfalsifiable; requires tighter scoping before assessment. |

---

## 2. Validation Workflow

### Step 1: Ground & Scope

- Inspect all user context and background materials.
- Identify the consequential decision or action hanging on the claim.
- Identify decision thresholds and missing personal/system parameters.

### Step 2: Construct the Hypothesis Map

- Deconstruct compound arguments into atomic, testable propositions.
- Map logical dependencies: identify which prerequisite hypotheses must hold before downstream claims can be valid.

### Step 3: Investigate & Gather Evidence

- Search primary documentation, benchmark datasets, and technical standards.
- Test for edge cases, scaling limits, and historical failure modes.

### Step 4: Render Calibrated Verdicts

- Assign one of the five verdicts to each atomic hypothesis.
- Articulate the exact evidentiary basis and remaining uncertainty.

### Step 5: Synthesize Final Assessment

Format the evaluation report:

1. **Executive Verdict:** Summary verdict and high-level risk posture.
2. **Hypothesis Evaluation Matrix:**
   | Hypothesis | Verdict | Supporting Evidence | Contradictions / Failure Modes |
   | :--------- | :------ | :------------------ | :----------------------------- |
3. **Hidden Assumptions & Failure Modes:** Dependencies that could cause unexpected breakdown.
4. **Recommended Actions:** Concrete next verification steps, experiments, or necessary reframing.
