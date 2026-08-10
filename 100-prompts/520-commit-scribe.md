# Commit Scribe

Use this approach when creating local Git commits for current repository changes. Write commit messages that explain why changes exist.

## Understand the Change

Use the strongest available context:

1. The user's current request.
2. Relevant context from the current conversation.
3. Repository instructions and commit conventions.
4. The working-tree diff, untracked files, and recent commit history.

When this prompt is used in an ongoing conversation, use the conversation actively. Recover the problems discussed, discoveries made, decisions taken, fixes implemented, and checks performed. Do not reconstruct the commit from the diff alone when the conversation already explains the intent.

When this prompt is used in a new conversation, infer the intent from the repository and its history.

Before committing, understand:

- The problem or goal.
- What changed.
- Why the chosen approach addresses the problem or requirements.
- Important discoveries, decisions, constraints, or trade-offs.

## Inspect the Change Set

Inspect the repository root, current branch, status, staged and unstaged diffs, untracked files, deleted files, recent commits, and relevant repository instructions.

Treat all staged, unstaged, deleted, and untracked changes as one candidate change set.

Run relevant tests, linters, builds, or focused checks. Report checks that failed, were skipped, or were unavailable.

## Write the Commit Message

Select a commit type from the following list:

- `feat` — new capability
- `fix` — bug correction
- `refactor` — structural change without intended behavior change
- `perf` — performance improvement
- `docs` — documentation change
- `test` — test change
- `build` — build or dependency change
- `ci` — continuous-integration change
- `chore` — other maintenance

Use this structure for the commit message:

```text
<type>(<scope>): <concise summary of the complete change>

Problem
- What problem, need, or goal led to this change?

Solution
- What changed?
- How does it address the problem or requirements?

Decisions
- Important non-obvious decisions, discoveries, constraints, or trade-offs.

Implementation
- Briefly describe the implementation, architecture, or approach.

Notes
- Any relevant notes not covered above.
```

## Create the Commit

1. Stage the complete intentional change set, including deletions and untracked files.
2. Re-check the staged diff and confirm it matches the understood change.
3. Create one local commit.
4. Inspect the resulting commit and final worktree status.

Do not push, amend, rebase, reset, discard changes, or rewrite history unless the user explicitly requests it.

## Report the Result

Report the commit hash and subject, the problem addressed, the solution, important decisions, verification results, included files, final worktree status, and any unresolved limitation or excluded file.
