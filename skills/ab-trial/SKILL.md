---
name: ab-trial
description: Decides whether a proposed change is better, worse, or no different by running blind, independent trials of each option and reporting adopt, reject, or inconclusive with evidence and cost. Use when the better of two or more plausible options can only be learned by running each one, and a wrong choice is costly, such as two wordings of a prompt, two ranking rules, or two caching strategies tested on the same inputs. Do not use for obvious fixes, matters of taste, or changes that a deterministic test already settles.
---

# A/B Trial: Blind Comparison of Options

Run a small, fair experiment before committing to a change whose effect is uncertain. Independent agents each receive one option and a task. A separate judge scores the outputs without knowing which option produced them. Report the evidence, its limits, and the cost. A sample is evidence for that sample, not proof.

---

## 1. Gate: Is a Trial Worth It?

- Activate `worth-the-squeeze` on the question "is testing this worth the cost?" Without it, answer in three sentences: the cost of a wrong choice, the cost of the trial, and whether a cheaper check (a deterministic test, a quick read) settles it.
- Stop and decide directly when the change is cheap to reverse, taste decides it, or an existing check already settles it. Say why no trial ran.
- Activate `claim-validator` when the hypothesis hides several claims. Without it, split the hypothesis into one testable statement per option.
- State the planned agent count and a rough token cost in the gate answer. Each agent carries tens of thousands of tokens of overhead, so a trial should cost a fraction of what the change is worth.

---

## 2. Pre-Register Before Any Run

Write these down first, and do not change them after seeing outputs.

1. **Hypothesis:** what the change should improve, and what it might harm.
2. **Arms:** one change per arm against an unchanged control. Record each arm's cost, such as prompt length in tokens or run time.
3. **Tasks:** at least eight. Cover normal use, a boundary case where the change should not apply, and an incomplete or off-distribution input. Keep them hard enough to fail. A task every arm passes carries no signal.
4. **Checks:** a short binary checklist per task. Prefer deterministic checks (required strings, length, a verifier tool). Use the judge only for what code cannot test.
5. **Decision rule:** adopt only if the arm is no worse than control on every task type, better on the boundary or incomplete tasks, and inside a stated size budget. A tie keeps the cheaper arm.

---

## 3. Run Independent Arms

- **Agents:** use one independent subagent per arm, and no more than three agents in total, judge included. Each arm agent gets its own copy of the arm and the full task list, treats each task as a separate request, and writes each output to its own file. Never tell an agent about the hypothesis, the other arms, or the checks. Use a fresh agent per task only when a task needs tools or a multi-turn dialogue, or must not see the other tasks.
- **Order:** shuffle the task order separately for each arm, so an order effect does not line up with one arm.
- **Blinding:** name each output file with a random ID, and keep the ID-to-arm map away from the judge.
- **Models:** run a second model strength only when the artifact will run on different hosts. A strong model can hide a weakness that a weaker one shows. Each extra strength adds one agent per arm, so keep the total small.
- **Judge:** use a model from a different family than the agents when one is available. Score each output against its checklist, one run at a time. Send content to an external service only when the cross-family judge adds signal.
- **Scratch space:** keep arms, outputs, and scores outside the repository.

---

## 4. Read the Results Honestly

1. Compute deterministic checks first. Then judge scores. Then size and length per arm.
2. Audit every output where the judge and the deterministic checks or the length disagree. Judges miss real defects and invent false ones. Correct the verdict and say so.
3. Check for copying: text from an example appearing in unrelated outputs.
4. State the sample size, the ceiling effect if nearly everything passed, that tasks within an arm shared one agent's context, and what the trial could not detect.

---

## 5. Deliverable

Return:

1. **Verdict:** adopt, reject, or inconclusive, tied to the pre-registered rule.
2. **Evidence table:** per arm and task type, checks passed, size, and length.
3. **Cost:** tokens added or time spent, against the observed benefit.
4. **Limits:** sample size, models used, judge audit notes, and the next test that would settle an inconclusive result.

Inconclusive is a valid result. It means keep the control and do not claim a benefit.
