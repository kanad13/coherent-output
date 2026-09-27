---
trigger: always_on
description: "Production code documentation invariants: the Intent Imperative ('Why, not What'), syntax echo elimination, dead-code removal, and docstring contract parity."
---

# Code Documentation & Comment Invariants

These standards govern all code commenting, docstrings, and inline technical explanations in production codebases.

---

## 1. The Intent Imperative ("Why, Not What")

- **State Intent & Invariants:** Document the underlying business rationale, algorithm invariants, safety constraints, and non-obvious engineering choices that make the code necessary.
- **Purge Syntax Echoes:** Never write comments that merely narrate what the programming syntax mechanically executes (e.g., delete `# check if user is admin` or `# loop through items`). Code syntax already explains _what_ is happening; comments must explain _why_ it is happening.
- **Eliminate Tutorial Narratives:** Eradicate stream-of-consciousness narration (e.g., `# Here we need to make sure...` or `# Now let's handle the response`). Use direct, concise affirmative statements.

---

## 2. Hygiene & Artifact Purge

- **Dead Code Graveyards:** Delete commented-out code blocks completely (e.g., `# def old_calculation(): ...`). Rely entirely on Git version control for historical code retrieval.
- **Scratchpad Residue:** Remove preliminary planning notes, task lists, and scratchpad markers (e.g., `# Step 1: parse`, `# Check edge case`) before concluding the task.
- **Attribution & Turn Tags:** Remove assistant attribution stamps, author tags, and ticket annotations (e.g., `# Fixed by AI Assistant`, `# Bugfix #1234`). Attribution belongs strictly in Git commit history.

---

## 3. Docstring Contract Parity & Completeness

- **Parameter & Type Parity:** Docstring parameter lists must match actual function signatures 100%. Never leave docstrings with outdated, missing, or inverted parameter names.
- **Return & Exception Parity:** Document exact return types, empty/null conditions, and all explicitly raised exceptions.
- **Uniform Style:** Adhere strictly to the established docstring convention of the target language and project (e.g., Google Python style, JSDoc, Rustdoc, Go doc comments).

---

## 4. Educational Exception Clause

- **Default Invariant:** The production "Why, Not What" standard is always on.
- **Explicit Override:** Comprehensive line-by-line explanations and syntax-teaching comments apply _only_ when the user explicitly invokes the `/code-beginner-comments` skill.
