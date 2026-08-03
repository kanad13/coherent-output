# Commit Scribe

## Purpose

Inspect the complete dirty Git worktree, understand why every change exists, stage every intentional changed or untracked file, write a detailed commit message, create the commit, and finish with a clean worktree.

The default scope ends with a new local commit. Push, amend, rebase, reset, discard, and history-rewrite operations begin after an explicit user request.

## Safety Boundary

Before staging, stop and report a blocker if the worktree contains:

- Likely credentials, private keys, access tokens, or sensitive personal data
- Unresolved merge conflicts
- A nested repository or submodule state requiring separate handling
- Files so large or unusual that committing them is likely accidental
- Evidence that the current directory differs from the intended repository

These checks protect against irreversible disclosure and repository damage. Surface every suspicious file and show the exact condition preventing the all-files commit.

## Workflow

### 1. Inspect the Repository

Gather:

- Repository root and current branch
- `git status --short`
- Staged diff
- Unstaged diff
- Untracked files and their relevant contents
- Diff statistics
- Recent commit history, including at least the last three commits
- Repository commit conventions or contributing instructions
- Relevant chat context, issue references, and task description

Read every dirty file closely enough to understand its contribution. Treat staged, unstaged, deleted, and untracked files as one complete candidate change set.

**Visible output — Change Inventory:**

| Path | State | What changed | Why it appears to have changed | Evidence |
| --- | --- | --- | --- | --- |

### 2. Reconstruct the Intent

Determine:

- The overall problem or goal
- How the files work together
- The primary change type and scope
- Important design decisions visible in the code or conversation
- Non-obvious discoveries or trade-offs supported by evidence
- Tests, documentation, and configuration associated with the change

Use evidence-supported business rationale, design decisions, and rejected alternatives. Describe the supported facts and remaining uncertainty when intent is incomplete.

**Visible output — Commit Rationale:**

- Problem or goal
- Selected approach and evidence-supported reason
- Technical impact
- Important insights
- Uncertainty, if any

### 3. Verify the Complete Change Set

- Search for conflict markers and obvious secret patterns.
- Inspect whether untracked files are generated artifacts or intentional source material.
- Run relevant tests, linters, builds, or validation checks when feasible.
- Confirm the diff is free of accidental debug output and unrelated sensitive data.
- Include all dirty changes in one complete commit by default, even when they span several concerns. Split or exclude changes after an explicit user request.

If validation fails, report the failure and apply fixes covered by the current task authorization.

### 4. Write the Commit Message

Follow the repository's established convention when one exists. Use Conventional Commits for repositories lacking an established convention.

Choose among:

- `feat`: New user-visible capability
- `fix`: Bug correction
- `refactor`: Structural code change that preserves user-visible behavior
- `perf`: Performance improvement
- `docs`: Documentation-only change
- `test`: Test-only change
- `style`: Non-functional formatting change
- `build`: Build system or dependency change
- `ci`: Continuous-integration change
- `chore`: Other maintenance

Use this template:

```text
<type>(<scope>): <concise present-tense description>

THE WHY
- Explain the problem, need, or goal supported by the evidence.
- Explain why the implemented approach addresses it.

KEY INSIGHTS
- Include only non-obvious, evidence-supported discoveries, constraints, or trade-offs.
- Include this section when meaningful insights exist.

MODIFIED FILES
- `path`: Explain what changed and how it contributes to the overall intent.
```

The subject must summarize the complete commit across all included files.

### 5. Stage and Commit Everything

1. Stage the complete worktree, including deletions and untracked files, with `git add -A` or the safe equivalent.
2. Re-run `git status --short` and inspect the staged diff.
3. Confirm the staged set matches the Change Inventory.
4. Create one commit using the validated message.
5. Inspect the resulting commit and final worktree status.

Completion requires a clean worktree. If tooling recreates files after the commit, identify why and either include them in a follow-up commit or report the blocker.

## Handoff

Report:

- Commit hash and subject
- High-level rationale
- Files included
- Verification results
- Final worktree status
- Anything blocked by the safety boundary
