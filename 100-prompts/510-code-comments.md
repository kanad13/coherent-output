# Beginner-Focused Code Comments

## Purpose

Add comprehensive comments and documentation that allow the user, a beginner, to understand the code line by line and see how each part contributes to the larger program.

Verbosity is intentional. Comment every code line or smallest format-safe unit. Explain both what it does and why it is needed.

## Scope

This prompt focuses exclusively on documenting existing code. General code-quality review, refactoring, defect correction, behavior changes, and alternative implementations begin through separate user requests.

If the code appears incorrect and prevents an accurate explanation, flag the uncertainty outside the code and preserve the executable code unchanged.

## Documentation Principles

- Write from first principles for a beginner encountering the codebase for the first time.
- Use plain language before technical terminology.
- Define technical terms at first use.
- Explain syntax, data flow, control flow, side effects, and dependencies.
- Explain both why a line or construct is present and what its syntax means.
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

Comment every executable or declarative line using an inline comment when valid and readable. Place the explanation immediately above the line in other cases.

For each line or smallest format-safe unit, explain as applicable:

- The syntax in plain language
- The value being created, read, changed, or returned
- Why the operation is needed
- Where inputs came from
- Where outputs go next
- How it affects control flow or program state
- Any beginner-relevant language or framework behavior

Make every comment add purpose or context beyond the visible syntax. For `counter += 1`, explain what the counter represents and why advancing it matters.

### Closing or Flow Summaries

After a long or complex block, add a brief comment summarizing the state produced for the next block when the language and file format permit it.

## Format-Safe Handling

- Insert comments exclusively in syntax-safe positions.
- For JSON or another format lacking comment syntax, preserve the file and create an adjacent annotated Markdown explanation or another user-specified safe format.
- Preserve shebangs, encoding declarations, frontmatter, generated markers, and required file headers in their valid positions.
- Place explanations around string literals, serialized data, regular expressions, and generated code while preserving their contents.
- For compact expressions, templates, or fluent call chains, comment the smallest unit that preserves valid syntax.

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

Use beginner-focused, comprehensive detail as the default.

### 2. Add Documentation

- Add file-level documentation.
- Add documentation to every declared unit.
- Add section-level orientation.
- Comment every line or smallest safe unit.
- Keep terminology consistent across files.
- Preserve executable behavior exactly.

### 3. Verify

Run or perform all relevant checks:

- Compare executable code before and after to confirm only comments or documentation changed.
- Parse, compile, lint, or test the files when tools are available.
- Confirm every code line or safe unit has a useful explanation.
- Confirm comments match actual behavior and context.
- Confirm every comment is valid, accurate, purposeful, and richer than a syntax restatement.
- Confirm a beginner can trace inputs, control flow, state changes, outputs, and system connections.

## Handoff

For code supplied directly in chat:

- Return the complete documented code for every comment-capable file in a copy-ready fenced block.
- For formats lacking comment syntax, return the unchanged source and the complete adjacent annotated Markdown document.

Report:

- Files documented
- Context inspected
- Verification performed
- Any line documented adjacently because its format prevented a safe inline comment
- Any uncertainty that prevented a reliable explanation
