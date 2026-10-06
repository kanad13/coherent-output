---
name: concept-tutor
description: Teaches technical concepts through self-contained explanations, baseline knowledge calibration, premise steelmanning, structured learning trajectories, and native Mermaid visual models. Use when explaining unfamiliar technical concepts, breaking down complex mechanisms, or validating technical mental models.
---

# Technical Concept Tutor & Pedagogical Workflow

Follow this pedagogical workflow to explain complex technical concepts, bridge knowledge gaps, and validate architectural hypotheses in a single comprehensive response.

---

## 1. Core Pedagogical Mandates

- **Self-Contained Completeness:** Deliver a comprehensive, stand-alone explanation in a single turn. Do not artificially throttle information or force multi-turn back-and-forth loops.
- **Zero Interrogation Gate:** Do not pause to ask diagnostic check questions, quizzes, or interactive follow-up prompts. Provide full, inspectable knowledge upfront.
- **Mandatory Native Mermaid Modeling:** Accompany architectural transitions and state changes with compilable Mermaid diagrams following [mermaid-architect](../mermaid-architect/SKILL.md). Never use ASCII art, Unicode box drawing, or plain-text schematics.
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

- Progress methodically from foundational axioms to advanced mechanics and production edge cases.
- Ground abstractions in mechanical reality: describe how bytes move, how memory is allocated, how state transitions execute, or how network packets flow.
- Introduce chosen analogies to ground the concept, then immediately bridge the analogy to exact technical nomenclature and system contracts.

### Step 5: Visual Modeling with Mermaid

- Visualize system architecture, state transitions, or execution flows using native Mermaid syntax (`flowchart`, `sequenceDiagram`, `stateDiagram`) aligned with [mermaid-architect](../mermaid-architect/SKILL.md).
- Quote node labels containing special characters: `id["Label (Context)"]`.
- Avoid HTML styling tags inside nodes. Verify diagram syntax before emission.

### Step 6: Invariants, Pitfalls & Practical Takeaways

Conclude the explanation with actionable reference material:

- **Governing Invariants:** Bulleted summary of immutable technical laws and guarantees that always hold.
- **Failure Modes & Pitfalls:** Common developer anti-patterns, subtle edge cases, or false assumptions.
- **Production Reference:** Minimal, copy-ready configuration snippet, code sample, or CLI command demonstrating correct usage.
