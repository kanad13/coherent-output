---
name: project-scaffolding
description: Brings a repository to the standard project layout, with the files a project keeps, where they live, how they are named and numbered, and what each contains, and fixes the deviations it finds. Use when starting a repository or repairing one mid-way, so that work can continue across sessions. Do not invoke for routine feature work, ordinary handoffs, or unrelated restructuring.
---

# Project Scaffolding

Make the repository match the standard layout below, whether it is new or half-built. Audit what exists, keep what already works, and fix only the deviations found. The agent that later works in the repository does the searching and building; this skill leaves it records it can trust. Other skills are available when a step needs them.

**Size the layout to the project.** A script or one-session task needs a `README.md` with a run command and one verification command, and nothing more. Add the `docs/` and `tests/` files when work will span sessions or involves non-obvious decisions.

## 1. The standard layout

```text
README.md              what the project is, how to set up and run it
AGENTS.md              project instructions for agents
docs/010-plan.md       active plan
docs/020-decisions.md  active decisions
tests/README.md        how to verify the project
.gitignore             ignored artifacts and secrets
.env.example           environment variables the project reads (only if it reads any)
LICENSE                for a public repository
.github/workflows/     CI that runs the documented verification command
```

- **Root:** only entrypoints, manifests (such as `package.json`, `pyproject.toml`), and tool configuration. Plans, decisions, and testing notes live in `docs/` and `tests/`.
- **Numbering:** files in `docs/` take a three-digit prefix in steps of ten (`010-`, `020-`) so new files slot between. Names are lowercase and hyphenated.
- **Links:** write every repository path in markdown as a relative link, such as `[docs/010-plan.md](docs/010-plan.md)`.
- **One home per fact:** each fact lives in one file; other files link to it.

### README.md

Holds the purpose, prerequisites, setup and run commands, and a short architecture overview (components and entry points). Rules and trade-offs belong in the decisions file, not here.

### AGENTS.md

The single instruction file. It binds the global agent habits to this project: where records live and when to update them. It does not repeat global policy.

````markdown
# <Project Name>: Repository Instructions

## Where things live

| Path                                           | Role                                           |
| :--------------------------------------------- | :--------------------------------------------- |
| [README.md](README.md)                         | Project overview, setup, and run instructions. |
| [docs/010-plan.md](docs/010-plan.md)           | Active milestone, progress, and next step.     |
| [docs/020-decisions.md](docs/020-decisions.md) | Active architectural decisions and rules.      |
| [tests/README.md](tests/README.md)             | Verification commands and expected outcomes.   |

## Working agreements

- **Start of turn:** read the plan, the latest decisions, and recent `git log`; correct stale state before editing.
- **Before an increment:** record the goal, acceptance check, and next step in the plan.
- **After an increment:** prune completed items older than the immediately preceding step, update blockers, run verification.
- **Consequential design choice:** add a decision before implementing.
- **Behavior or tooling change:** update `tests/README.md` and `README.md` in the same change.
- **End of turn:** make `Next action` in the plan runnable by a reader with no prior context.

## Verification

```bash
<canonical test command>
```
````

### docs/010-plan.md

A steering aid for the current milestone. At each new increment, delete completed items older than the immediately preceding step; history lives in git.

```markdown
# Active Plan

Goal: <one sentence defining the active milestone>
Acceptance: <observable checks>
Next action: <one concrete, runnable step>
Blockers: <none | list>

Recent context:

- [x] <immediately preceding completed step>
```

### docs/020-decisions.md

One record per non-obvious choice, numbered `001`, `002`. Each record is an active rule, not a story. Edit it in place when it changes; when a requirement replaces it, set `Status: Superseded by Decision XXX` and keep the record.

```markdown
# Architectural Decision Records

## Decision 001 - <the chosen approach, as a noun phrase>

Status: Accepted <!-- or Superseded by Decision XXX -->

### Decision context

<Where this decision governs and the constraint that forced the choice.>

### Selected approach

<The rule, written so a reader can follow it without the other sections.>

### Rejected approaches

- `<Option>`: <the property that rules it out, as a fact.>

### Revisit decision when

- <An observable condition that reopens the decision.>
```

### tests/README.md

For each acceptance criterion: the real entry point, the action, the expected observable result, and the command or manual steps. Use `test-strategist` (optional) when the strategy needs depth.

### Supporting files

- `.gitignore` covers runtime artifacts, build output, and secrets.
- `.env.example` lists each environment variable the code reads, without values.
- Shared configuration uses project-relative or environment paths.
- CI runs the documented verification command on push.

## 2. Audit and fix

Read the repository first: instructions, entry document, manifests, layout, `git log`, existing records. Then compare it with section 1 and fix each deviation:

| Finding                                                                  | Fix                                                                                                 |
| :----------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| Standard file missing                                                    | Create it from its template, filled from repository evidence. Mark inferred content as inferred.    |
| Record in the wrong place (root `PLAN.md`, `TODO.md`, `architecture.md`) | Merge its live content into the canonical file, then remove the original.                           |
| Equivalent file under another name (`CLAUDE.md`, `docs/1-plan.md`)       | Move content to the canonical name and path. Keep a one-line pointer only when tooling requires it. |
| Stale record (done items, commands that fail)                            | Run the command, then correct the record to what is true.                                           |
| Decision written as history                                              | Rewrite as an active rule; mark replaced ones `Superseded`.                                         |
| Same fact in two files                                                   | Keep it in its canonical file and link from the other.                                              |
| `AGENTS.md` lacks working agreements                                     | Add them from the template.                                                                         |

Keep practices that already work. Report unresolved choices instead of inventing them.

## 3. Verify

- **Run it:** execute the documented setup and verification commands and read their output.
- **Cold start:** have a fresh agent or subagent read only the repository and state the current goal, the last verified result, and the next action, then run the documented check. Each wrong or missing answer marks a gap; repair it and repeat. Without subagents, check that a reader with only the working tree could do the same.
- **Report:** name any failed or blocked check, the exact barrier, and what stays unverified. Hand staging and commits to `commit-scribe` (optional).
