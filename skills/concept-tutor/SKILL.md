---
name: concept-tutor
description: Teaches technical concepts through self-contained explanations, baseline knowledge calibration, premise steelmanning, and structured learning trajectories. Use when explaining unfamiliar technical concepts, breaking down complex mechanisms, or validating technical mental models. Do not use for brief factual lookups or code debugging.
---

# Technical Concept Tutor & Pedagogical Workflow

Follow this pedagogical workflow to explain complex technical concepts, bridge knowledge gaps, and validate architectural hypotheses in a single comprehensive response. Calibrate explanations to layperson accessibility under ASD-STE100 plain language, anchoring every abstract concept in physical analogies and concrete system models.

---

## 1. Core Pedagogical Mandates

- **ASD-STE100 Plain Language:** Write direct, affirmative sentences in active voice. Define technical terms on first use. Discard buzzwords, filler, and corporate jargon.

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

- **Concept Dependency Sequence:** Order concepts so every prerequisite is grounded before introducing downstream abstractions.
- **Explanatory Devices:** Select high-leverage physical analogies, mechanical metaphors, or concrete system models to make abstract mechanisms tangible.
- **Concrete Scenarios:** Select minimal, real-world examples or code snippets demonstrating the concept in action.

### Step 4: Scaffolded First-Principles Exposition

- Invoke the cognitive-clarity-refactor skill and provide the final output to the user.
