# Beginner-Focused Code Comments

## Purpose

Add comprehensive comments and documentation that allow the user, a beginner, to understand the code line by line and see how each part contributes to the larger program.

Verbosity is intentional. Comment every code line or smallest format-safe unit. Explain both what it does and why it is needed.

## Scope

This prompt documents existing code. It does not perform a general code-quality review, refactor code, fix defects, change behavior, or recommend alternative implementations unless the user separately asks.

If the code appears incorrect and that prevents an accurate explanation, flag the uncertainty outside the code. Do not silently fix it.

## Documentation Principles

- Write for a beginner with no assumed familiarity with the codebase.
- Use plain language before technical terminology.
- Define technical terms at first use.
- Explain syntax, data flow, control flow, side effects, and dependencies.
- Explain why a line or construct is present, not only what its syntax means.
- Connect each local operation to the surrounding function, file, and program.
- Preserve all executable code and behavior exactly.
- Use the target language's valid documentation and comment syntax.

## Comment Coverage

### File-Level Documentation

At the beginning of each file, explain:

- The file's purpose
- Where it is used or invoked
- Its main inputs and outputs
- Important dependencies
- The major execution flow
- Concepts a beginner must know before reading it

### Type, Class, Function, and Module Documentation

For every declared unit, document:

- Purpose
- Parameters or inputs
- Return value or output
- Side effects
- Errors or exceptional outcomes
- Preconditions and assumptions
- Relationship to callers and dependencies

Use the standard doc-comment form for the language when one exists.

### Section-Level Comments

Before each logical block, explain:

- What the block is about to do
- Why that step is necessary
- What state or data enters it
- What state or data should leave it

### Line-by-Line Comments

Comment every executable or declarative line using an inline comment when valid and readable. Otherwise place the explanation immediately above the line.

For each line or smallest format-safe unit, explain as applicable:

- The syntax in plain language
- The value being created, read, changed, or returned
- Why the operation is needed
- Where inputs came from
- Where outputs go next
- How it affects control flow or program state
- Any beginner-relevant language or framework behavior

Do not use empty comments such as “increment counter” when the code already says `counter += 1`. Explain the purpose: for example, what the counter represents and why advancing it matters.

### Closing or Flow Summaries

After a long or complex block, add a brief comment summarizing the state produced for the next block when the language and file format permit it.

## Format-Safe Handling

- Never insert comments where they make the file invalid.
- For JSON or another format without comments, do not alter the file syntax. Create an adjacent annotated Markdown explanation unless the user specified another safe format.
- Preserve shebangs, encoding declarations, frontmatter, generated markers, and required file headers in their valid positions.
- Do not place comments inside string literals, serialized data, regular expressions, or generated code.
- For compact expressions, templates, or fluent call chains, comment the smallest unit that can be explained without breaking syntax.

## Workflow

### 1. Inspect Context

- Determine the language and file format.
- Read related callers, callees, types, configuration, and tests needed to explain the code accurately.
- Map the file or block's role in the execution flow.
- Identify terms and mechanisms that need beginner explanations.

**Visible output — Documentation Plan:**

- Scope
- Language and safe comment forms
- Execution-flow summary
- Related files inspected
- Concepts requiring explanation
- Any context that remains uncertain

Do not ask the user to choose a detail level; beginner-focused, comprehensive detail is the default.

### 2. Add Documentation

- Add file-level documentation.
- Add documentation to every declared unit.
- Add section-level orientation.
- Comment every line or smallest safe unit.
- Keep terminology consistent across files.
- Do not change executable behavior.

### 3. Verify

Run or perform all relevant checks:

- Compare executable code before and after to confirm only comments or documentation changed.
- Parse, compile, lint, or test the files when tools are available.
- Confirm every code line or safe unit has a useful explanation.
- Confirm comments match actual behavior and context.
- Confirm no comment is invalid, misleading, or merely a restatement.
- Confirm a beginner can trace inputs, control flow, state changes, outputs, and system connections.

## Handoff

Report:

- Files documented
- Context inspected
- Verification performed
- Any line or format that could not safely receive an inline comment and how it was documented instead
- Any uncertainty that prevented a reliable explanation
