---
name: code-beginner-comments
description: Adds comprehensive, line-by-line educational comments to code so beginners can understand syntax, mechanics, and domain purpose. Use when documenting code for learners, explaining code line-by-line, or adding detailed instructional comments.
---

# Beginner-Focused Code Comments

Apply this methodology when adding comprehensive, educational comments that allow beginners to understand code line by line.

---

## 1. Scope & Educational Override

- **Educational Purpose:** Verbosity is intentional. Unlike production code comments (which focus strictly on _Why, not What_), this skill explains both **what the syntax mechanics mean** and **why the application requires the step**.
- **Scope Restriction:** Strictly focuses on documenting existing code. Do not refactor, rename variables, or alter runtime execution behavior.

---

## 2. Documentation Coverage

### 1. File-Level Header

At the start of each file, explain:

- File purpose and architectural role.
- Where and how it is executed or imported.
- Main inputs, outputs, and external dependencies.
- Prerequisite programming concepts required before reading.

### 2. Function & Class Blocks

For every function, class, and method, document:

- Overall purpose and domain responsibility.
- Parameters: type, format, and real-world meaning.
- Return value: type and expected state.
- Errors: exceptions raised and edge-case handling.

### 3. Section & Line-by-Line Annotations

- **Section Comments:** Precede logical blocks with an overview of what the block prepares to accomplish.
- **Line-by-Line Comments:** Annotate individual lines or smallest format-safe units:
  - State domain intent before syntax mechanics (explain what business logic is updated before syntax details).
  - Explain data transformations, state changes, and side effects.
  - Avoid keyword parroting: explain what the construct achieves in the application.

---

## 3. Format-Safe Execution

- Use the target language's native, valid comment delimiters (`#`, `//`, `/* */`).
- Preserve 100% of executable code, formatting, and indentation.
- If code logic is ambiguous, flag the uncertainty in an outer note without altering executable code.
