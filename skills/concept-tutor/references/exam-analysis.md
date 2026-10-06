# Multiple-Choice Exam Analysis & Distractor Evaluation Matrix

When explaining multiple-choice questions or certification exams, apply this protocol to evaluate options and diagnose student misconceptions.

---

## 1. Stem Parsing & Qualifier Detection

Scan the question stem for decisive qualifiers:

- **Negative Inversion:** `EXCEPT`, `NOT`, `LEAST LIKELY`.
- **Optimization:** `BEST`, `MOST EFFECTIVE`, `FIRST STEP`, `PRIMARY`.
- **Cardinality:** Single answer vs. multi-select (`SELECT TWO`, `SELECT ALL THAT APPLY`).
- **Governing Invariant:** Extract the core technical invariant, specification rule, or protocol constraint that governs the question.

---

## 2. Exhaustive Distractor Evaluation Matrix

Evaluate _every_ answer choice against the identical governing criterion:

| Option       | Verdict                | Concrete Disqualification or Verification Rationale                            |
| :----------- | :--------------------- | :----------------------------------------------------------------------------- |
| **Option A** | Incorrect (Distractor) | Identifies the specific technical error, obsolete API, or invalid assumption.  |
| **Option B** | **Correct**            | Explains why this option directly satisfies the governing technical invariant. |
| **Option C** | Incorrect (Distractor) | Demonstrates why this approach fails under stated edge cases or constraints.   |
| **Option D** | Incorrect (Trap)       | Explains why this plausible-sounding distracter is invalid in this context.    |

---

## 3. Misconception Diagnostics

When a student selects an incorrect option:

1. **Isolate the Misconception:** Identify what partially-true mental model led to the selection (e.g., confusing authorization with authentication, or synchronous RPC with event streaming).
2. **Reframe with Minimal Analogy:** Provide a 1-sentence mechanical contrast.
3. **Targeted Micro-Check:** Present a 1-sentence simplified scenario to confirm the student has corrected the specific misconception.
