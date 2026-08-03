# Commit Scribe

## Purpose

Inspect the complete dirty Git worktree, understand why every change exists, stage every intentional changed or untracked file, write a detailed commit message, and create the commit. Do not leave valid dirty changes behind.

Do not push, amend, rebase, reset, discard, or rewrite history unless the user explicitly asks.

## Safety Boundary

Before staging, stop and report a blocker if the worktree contains:

- Likely credentials, private keys, access tokens, or sensitive personal data
- Unresolved merge conflicts
- A nested repository or submodule state that cannot be safely included
- Files so large or unusual that committing them is likely accidental
- Evidence that the current directory is not the intended repository

These checks exist to prevent irreversible disclosure or repository damage. Do not silently omit suspicious files; show the user exactly what prevented the all-files commit.

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

Read every dirty file closely enough to understand its contribution. Do not assume the existing staged set represents the full requested commit.

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

Do not invent business rationale or rejected alternatives. If intent remains uncertain, describe only what the evidence supports.

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
- Confirm the diff does not contain accidental debug output or unrelated sensitive data.
- Include all dirty changes in the commit even when they span several concerns; do not split or omit them unless the user explicitly asks.

If validation fails, report the failure. Fix it only when the current task authorizes code changes.

### 4. Write the Commit Message

Follow the repository's established convention when one exists. Otherwise use Conventional Commits.

Choose among:

- `feat`: New user-visible capability
- `fix`: Bug correction
- `refactor`: Structural code change without a feature or bug fix
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
- Omit this section when there are no meaningful insights.

MODIFIED FILES
- `path`: Explain what changed and how it contributes to the overall intent.
```

The subject must summarize the complete commit, not only the largest file.

### 5. Stage and Commit Everything

1. Stage the complete worktree, including deletions and untracked files, with `git add -A` or the safe equivalent.
2. Re-run `git status --short` and inspect the staged diff.
3. Confirm the staged set matches the Change Inventory.
4. Create one commit using the validated message.
5. Inspect the resulting commit and final worktree status.

Do not declare completion if valid dirty changes remain. If tooling recreates files after the commit, identify why and either include them in a follow-up commit or report the blocker.

## Handoff

Report:

- Commit hash and subject
- High-level rationale
- Files included
- Verification results
- Final worktree status
- Anything blocked by the safety boundary
