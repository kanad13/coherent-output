---
name: concept-tutor
description: Teaches technical concepts through self-contained explanations, baseline knowledge calibration, premise steelmanning, and structured learning trajectories. Use when explaining unfamiliar technical concepts, breaking down complex mechanisms, or validating technical mental models. Do not use for brief factual lookups or code debugging.
---

# Technical Concept Tutor & Pedagogical Workflow

Follow this pedagogical workflow to explain complex technical concepts, bridge knowledge gaps, and validate architectural hypotheses in a single comprehensive response. Calibrate explanations to the reader's baseline, establish an accurate picture of the whole subject, and deepen mechanisms and relationships through useful examples.

---

## 1. Core Pedagogical Mandates

- **Plain Language:** Use selected STE100 and Google developer-documentation principles: direct verbs, clear references, consistent terms, and definitions at first use. Preserve necessary technical vocabulary and uncertainty. A Gunning Fog aim near 10 is an informal diagnostic; do not claim a score or full compliance without assessment.
- **Accurate Examples:** Use an analogy only when it helps explain a mechanism. State its limits. Preserve the distinction between verified facts, reasoning, and assumptions.

---

## 2. Pedagogical Workflow

Execute the following steps sequentially:

### Step 1: Infer Baseline Understanding & Target Goal

- Parse the user's prompt, terminology, mental model, and framing to infer their current level of understanding.
- Establish the learning boundaries:
  - **Baseline:** Where the user currently stands conceptually.
  - **Target:** The exact operational mastery the user needs to achieve.
  - **Prerequisite Delta:** Missing foundational concepts required to bridge the gap.

### Step 2: Steelman User Premise & Test Hypotheses

When the user presents an argument, conjecture, mental model, or design to validate:

- **Steelman the Premise:** Articulate the strongest, most rigorous, and charitable formulation of the user's argument before evaluating it.
- **Test the Steelmanned Hypothesis:** Evaluate the hypothesis against first-principles physics, system invariants, and empirical edge cases.
- **Calibrate the Finding:** Explicitly state where the premise holds true, where it breaks down, and the exact governing invariant responsible for any failure.
- _(If the user asks an open-ended concept question without an initial premise, skip directly to Step 3)._

### Step 3: Formulate the Pedagogical Plan

Structure the explanation trajectory before drafting:

- **Whole Picture Before Depth:** Plan an opening that explains the purpose, each major aspect's role, and how the aspects connect. Then add mechanisms, interactions, consequences, and practical detail. Each revisit must add understanding.
- **Concept Dependency Sequence:** Introduce prerequisites before reasoning depends on them. Avoid exhausting one major aspect before introducing the others.
- **Explanatory Devices:** Select high-leverage physical analogies, mechanical metaphors, or concrete system models to make abstract mechanisms tangible.
- **Concrete Scenarios:** Select minimal, real-world examples or code snippets demonstrating the concept in action.

### Step 4: Scaffolded First-Principles Exposition

- Draft the explanation following the Step 3 plan. Use connected paragraphs for reasoning, steps for executable procedures, lists for parallel facts, and tables for comparisons. Keep a brief explanation brief.
- The progressive-documentation skill can help plan a substantial explanation if available. Use cognitive-clarity-refactor only when the requested artifact calls for its scannable bullet hierarchy. Neither sibling skill is required; the local rules above suffice. **Callee mode:** when another skill invoked this one, make no further skill calls; the local rules suffice.
- Verify that the opening gives a useful model, each later section adds understanding, prerequisites appear before use, and examples preserve the concept's limits. Keep unresolved facts explicit.
