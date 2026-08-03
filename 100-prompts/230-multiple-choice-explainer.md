# Multiple-Choice Answer Explainer

## Purpose

Answer a multiple-choice question accurately and teach the minimum background needed to understand why each relevant option succeeds or fails.

## Analysis Workflow

Complete the analysis before presenting the final answer. Express the reasoning through visible evidence, governing criteria, option evaluations, assumptions, and verification results.

### 1. Parse the Question

- Identify the domain.
- Detect qualifiers such as `EXCEPT`, `NOT`, `BEST`, `MOST LIKELY`, or `SELECT ALL`.
- Determine whether the question expects one answer, several answers, or an ordered selection.
- Extract the governing rule, fact, calculation, or criterion.
- Flag missing context or ambiguous wording.

### 2. Verify Required Knowledge

Use external research when:

- The answer depends on current laws, standards, regulations, events, product behavior, or software versions.
- The topic is specialized enough that unsupported recall would be unreliable.
- The options conflict with one another in a way that requires authoritative resolution.
- Confidence in the answer falls below high.

Prefer official or primary sources. Cite every factual claim obtained through research.

### 3. Evaluate the Options

For each option:

- Apply the same governing criterion.
- State the decisive fact or rule.
- Explain the specific reason the option qualifies or fails.

Validate the question itself. Report explicitly when multiple answers are defensible, every option fails, or the wording is materially ambiguous.

### 4. Verify the Decision

Check that:

- The response honors qualifiers in the stem.
- Every selected answer satisfies the governing criterion.
- Every rejected option has a specific reason for rejection.
- Every material assumption is stated explicitly.
- Current or specialized claims are cited where necessary.

## Output Format

```markdown
### Answer

- **Question type and qualifier:** [Single answer / Select all / Ordered selection; quote any decisive qualifier such as NOT or BEST]
- **Selection:** [Option label and text, or multiple selections]
- **Status:** [Clear answer / Ambiguous question / Invalid option set]
- **Why:** [Concise decisive explanation]

### Option Analysis

- **[Option label and text] — Correct / Incorrect / Conditionally correct**
  - [Specific rule, fact, calculation, or condition]

### Essential Background

- **[Concept]:** [Only the background needed to understand the decision]

### Caveat or Source

[Include when ambiguity, assumptions, or external research affected the answer.]
```

Write in English by default. Preserve important non-English technical terms in parentheses when they aid understanding.
