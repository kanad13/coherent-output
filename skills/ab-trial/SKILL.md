---
name: ab-trial
description: Compares competing instruction variants or high-blast-radius changes through a controlled A/B/n hypothesis tournament with isolated subagents and reports an adopt, reject, or inconclusive verdict. Use when deciding between two to five plausible options whose effect is uncertain and a wrong choice is costly. Do not use for obvious bug fixes, trivial edits, or changes that a deterministic test already settles.
---

# A/B/n Hypothesis Tournament: Controlled Trial of Competing Options

Run an empirical experiment before committing a high-blast-radius change to instructions, behavioral rules, or architecture. The coordinator frames 2 to 5 competing hypotheses (including an unchanged control arm), runs each arm in an isolated subagent on the identical model to prevent context contamination, executes a standard benchmark battery, and grades results through deterministic checks and blinded scoring.

---

## 1. Gate: Is a Trial Worth the Squeeze?

- **High-Stakes Trigger:** Run when changing foundational instructions, system prompts, or behavioral directives with wide downstream impact, or when explicitly requested by the user. Do not run for obvious bug fixes, routine code refactors, or changes already settled by deterministic unit tests.
- **Cost & Value Audit:** Activate `worth-the-squeeze` on the question: "Does testing these candidate options justify the token cost?" Without it, answer in three sentences: the cost of a wrong choice, the token budget of the tournament, and whether a cheaper read or existing test settles it.
- **Decompose Hypotheses:** Activate `claim-validator` when candidate proposals conflate multiple independent changes. Without it, isolate one distinct mechanism or coherent strategy per candidate arm.
- **Tournament Topology:** Limit the tournament to $K \in [2, 5]$ hypotheses: Arm 0 is always the unchanged Control; Arms 1 through $K-1$ are candidate variants. Bound total subagent count strictly to $K$ (one agent per arm).

---

## 2. Pre-Registration Protocol

Before launching any subagent or generating outputs, record these four items. Do not alter them after observing outputs:

1. **Hypotheses & Arms ($K \in [2, 5]$):**
   - `Arm 0 (Control)`: Unchanged status quo.
   - `Arm 1..N (Variants)`: Competing articulations, permutations, additions/removals of directives, or structural reorganizations.
2. **Benchmark Test Battery (3 to 4 Tasks):**
   - `Task 1 (Happy Path)`: Typical input representing core workflow.
   - `Task 2 (Boundary Case)`: Edge condition where the instruction must gracefully abstain, preserve assets, or enforce negative constraints.
   - `Task 3 (Adversarial / Stress)`: Ambiguous, malformed, or out-of-distribution input designed to surface failure modes.
   - `Task 4 (Optional)`: Domain-specific regression scenario.
3. **Scoring Checklist:**
   - Define a binary pass/fail rubric per task.
   - Order checks deterministically first (length bounds, exit codes, required strings, format compliance, AST/schema validity).
   - Reserve qualitative checks for aspects programmatic code cannot verify.
4. **Decision Rule:**
   - Define the explicit condition required to adopt a variant (for example: pass 100% of deterministic checks, outperform Control on at least two tasks with zero regressions, and remain within a token size budget).
   - Inconclusive default: If no variant demonstrably beats Control, retain Control.

---

## 3. Hermetic Execution Protocol

- **Single Model Invariant:** Run every arm on the **exact same model** and environment configuration. Never mix model tiers or families across arms in a trial; holding the model constant guarantees observed variance is caused strictly by the candidate instructions.
- **Isolated Subagents (1 Subagent per Arm):**
  - Spawn exactly one independent subagent per hypothesis arm ($K$ subagents total).
  - Provide each subagent only its assigned arm variant and the full benchmark battery.
  - Never disclose the hypothesis, other candidate arms, scoring rubrics, or Control identity to the subagent.
  - Subagents execute all battery tasks in isolation and write raw responses to temporary scratch files outside the repository checkout (such as `.scratch/ab-trial-<id>/arm-<k>/task-<m>.txt`).
- **Single-Agent Fallback:** When the host environment does not support subagents, execute arms sequentially in separate temporary scratch directories, wiping working memory between arms to prevent context pollution.
- **Blinding:** Assign each output a random anonymous hash ID (`run-a1`, `run-b2`, etc.). Retain the hash-to-arm lookup map privately in coordinator memory away from the evaluation step.

---

## 4. Evaluation & Verification

1. **Deterministic Audit First:** Evaluate code, character/token counts, formatting integrity, and regex assertions against blinded files. Mark hard failures immediately.
2. **Blinded Qualitative Audit:** Evaluate remaining blinded outputs against the pre-registered checklist. Evaluate one output at a time with a binary pass/fail rubric to prevent position bias.
3. **Discrepancy & Hallucination Check:** Inspect any output where qualitative scoring conflicts with deterministic indicators. Check for copied text, circular reasoning, or rule evasion.
4. **Follow-Up Round (Optional):** If two candidate variants tie or a clear hybrid emerges, run one targeted head-to-head playoff between the top two variants using two fresh boundary tasks.

---

## 5. Deliverable: Tournament Ledger

Return the evaluation in this format:

```markdown
### A/B/n Tournament: [Topic / Directive Evaluated]

#### 1. Pre-Registered Hypotheses & Protocol

- **Arm 0 (Control):** [Description of current status quo]
- **Arm 1 (Variant A):** [Description of hypothesis 1]
- **Arm 2 (Variant B):** [Description of hypothesis 2]
- **Decision Rule:** [Explicit adoption condition]

#### 2. Benchmark Evaluation Matrix

| Arm                   | Task 1 (Happy) | Task 2 (Boundary) | Task 3 (Stress) | Deterministic Pass % | Size / Cost Delta |
| :-------------------- | :------------- | :---------------- | :-------------- | :------------------- | :---------------- |
| **Arm 0 (Control)**   | Pass / Fail    | Pass / Fail       | Pass / Fail     | %                    | Baseline          |
| **Arm 1 (Variant A)** | Pass / Fail    | Pass / Fail       | Pass / Fail     | %                    | +/- tokens        |
| **Arm 2 (Variant B)** | Pass / Fail    | Pass / Fail       | Pass / Fail     | %                    | +/- tokens        |

#### 3. Juice vs. Squeeze Analysis

- **Observed Benefit:** [Concrete functional gain over Control]
- **Operational Squeeze:** [Instruction bloat, token overhead, maintenance friction]

#### 4. Final Verdict

- **Verdict:** [ADOPT (Arm X) | REJECT | INCONCLUSIVE]
- **Rationale:** [How the evidence met or failed the pre-registered decision rule]
- **Repository Landing:** [Exact file modifications to commit, or none if Control retained]
```
