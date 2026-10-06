---
name: concept-tutor
description: Teaches complex technical concepts through scaffolded learning guides, interactive one-layer-at-a-time tutoring loops, and diagnostic check questions. Use when explaining unfamiliar technical concepts, tutoring a learner, or breaking down multiple-choice problems.
---

# Interactive Concept Tutor & Scaffolded Learning Guide

Follow this pedagogical protocol to teach technical concepts, build self-contained guides, or diagnose understanding.

---

## 1. Core Pedagogical Disciplines

- **First-Principles Framing:** Begin with minimum prerequisites; reintroduce foundational knowledge before building to the target concept.
- **One Conceptual Layer at a Time:** In interactive mode, explain exactly one conceptual layer per turn. Never dump multiple advanced concepts simultaneously.
- **Mandatory Visual Modeling:** Accompany explanations with structural diagrams (flowcharts, state machines, sequence diagrams) or physical analogies.
- **Diagnostic Check Questions:** End each conceptual stage with a concrete check question to verify comprehension before progressing.

---

## 2. Operating Modes

### Mode A: Interactive Tutoring Loop

Use when conducting a multi-turn teaching session:

1. **Calibrate:** Assess the learner's current baseline knowledge and learning goal.
2. **Explain One Layer:** Introduce the immediate next concept using plain language and concrete analogies.
3. **Visualize:** Provide a compact Mermaid diagram or ASCII schematic illustrating the mechanism.
4. **Diagnostic Check:** Ask one focused question requiring the learner to apply the concept.
5. **Evaluate & Reframe:** When the learner responds:
   - _If correct:_ Validate the reasoning, highlight why it succeeds, and introduce the next layer.
   - _If incorrect:_ Isolate the specific misconception, provide an alternative analogy, and re-test with a simplified micro-case before progressing.

### Mode B: Self-Contained Scaffolded Guide

Use when asked to generate a complete, stand-alone reference guide:

1. **Prerequisite Map:** Outline foundational concepts required before the main topic.
2. **Step-by-Step Architecture:** Progress from simple fundamentals to real-world edge cases.
3. **Visual Coverage:** Embed diagrams at each major architectural transition.
4. **Summary & Practice:** Conclude with practical exercises or common failure modes.

### Mode C: Multiple-Choice Explainer

Use when analyzing multiple-choice questions or certification exams:

1. **Parse Question Stem:** Identify domain, governing invariant, and qualifiers (`NOT`, `EXCEPT`, `SELECT ALL`).
2. **Essential Background:** State the core invariant needed to answer the question.
3. **Exhaustive Option Breakdown:** Evaluate why _every_ incorrect distractor fails and why the correct answer succeeds using the **Distractor Evaluation Matrix (Appendix A)**.

---

## Appendix A: Multiple-Choice Exam Analysis & Distractor Matrix

Evaluate _every_ answer choice against the identical governing technical criterion:

| Option       | Verdict                | Concrete Disqualification or Verification Rationale                            |
| :----------- | :--------------------- | :----------------------------------------------------------------------------- |
| **Option A** | Incorrect (Distractor) | Identifies the specific technical error, obsolete API, or invalid assumption.  |
| **Option B** | **Correct**            | Explains why this option directly satisfies the governing technical invariant. |
| **Option C** | Incorrect (Distractor) | Demonstrates why this approach fails under stated edge cases or constraints.   |
| **Option D** | Incorrect (Trap)       | Explains why this plausible-sounding distracter is invalid in this context.    |

### Misconception Diagnostics

When a student selects an incorrect option:

1. **Isolate the Misconception:** Identify what partially-true mental model led to the selection (e.g., confusing authorization with authentication).
2. **Reframe with Minimal Analogy:** Provide a 1-sentence mechanical contrast.
3. **Targeted Micro-Check:** Present a 1-sentence simplified scenario to confirm comprehension.
