---
name: commit-scribe
description: Creates structured, high-context git commits for repository changes with problem, solution, decisions, implementation, and notes, and pushes them to the upstream remote. Use when staging changes, writing commit messages, finalizing git commits, or pushing commits to remote. Do not use during intermediate WIP coding before verification passes.
---

# Commit Scribe

Follow this protocol when creating Git commits and pushing changes for repository updates. Enforce pre-commit hygiene, inspect staged diffs, and construct structured five-section commit messages that document architectural intent, trade-offs, and verification results.

---

## 1. Inspect the Change Set & Pre-Commit Hygiene

1. **Evaluate Unified Status:**
   - Inspect current branch, git status, staged and unstaged diffs, untracked files, deleted files, and recent commit history.
2. **Pre-Commit Hygiene & Residue Audit:**
   - Audit the candidate diff for temporary residue before staging:
     - **Commented-Out Code:** Eradicate commented-out code blocks entirely; rely on Git version history for retrieval.
     - **Debug Residue:** Purge temporary debugging statements (`console.log`, `print`, `debugger`, dumps).
     - **Attribution Stamps:** Purge assistant attribution stamps, author tags, and ticket annotations.
     - **Temporary Files:** Ensure untracked scratchpad notes, log dumps, and temp files are excluded or deleted.
3. **Intent Comment Verification ("Why, Not What"):**
   - Confirm that non-obvious algorithms, edge cases, and design choices in the diff contain comments explaining the underlying rationale, constraints, or invariants rather than narrating syntax.
4. **Execute Pre-Commit Verification:**
   - Run project test suites, linters, and type checkers. Report any check that fails, is skipped, or is unavailable. Never commit code that breaks tests.
5. **Understand Intent:**
   - Synthesize intent from the ongoing conversation (problems diagnosed, decisions made, fixes tested).
   - If invoked in a fresh conversation, infer intent from the diff, file context, and recent commit history.

---

## 2. Commit Message Structure

Use this exact conventional structure:

```text
<type>(<scope>): <single-line concise summary in the present imperative mood>

Problem
- What problem, business need, or technical goal led to this change?

Solution
- What changed in the codebase?
- How does it address the problem and satisfy requirements?

Decisions
- What non-obvious engineering decisions, trade-offs, or constraints shaped the approach?

Implementation
- Briefly describe the architecture, data flow, or components touched.

Notes
- Any remaining limitations, follow-ups, or excluded files.
```

### Commit Types

- `feat` — new user-facing capability or functionality
- `fix` — bug correction
- `refactor` — structural code reorganization without changing behavior
- `perf` — performance improvement
- `docs` — documentation creation or update
- `test` — adding or modifying test suites
- `build` — build system, packaging, or dependency update
- `ci` — continuous integration configuration
- `chore` — maintenance, tooling, or repository hygiene

---

## 3. Execution & Safety Boundary

1. **Stage Atomic Changes:** Stage only intended modifications relevant to this logical unit of work (`git add <files>`). Avoid blanket staging that catches unintended dirty files.
2. **Verify Staged Diff:** Check `git diff --cached` to verify that only intentional modifications are staged and no residual debug statements slipped through.
3. **Commit Locally:** Create exactly one local commit with the structured message.
4. **Push to Remote:** Push committed changes to the tracking upstream remote branch (`git push`). If no upstream branch is configured, push with `-u origin <branch>` to establish tracking.
5. **Safety Gate:** Do **not** force push (`--force` or `--force-with-lease`), amend previously pushed commits, rebase public history, or reset history unless explicitly requested by the user.
6. **Report Result:** Output the commit hash, upstream tracking branch, subject line, included files, and final working tree status.
