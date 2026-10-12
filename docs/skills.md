# Skills Library

This library contains portable, task-specific playbooks for AI agents. A host discovers each skill's name and description, the agent reads its body when needed, and bundled resources support the workflow. Installation makes a skill available; behavior still needs to be checked against the requested result.

## 1. Discovery and execution

The [Agent Skills specification](https://agentskills.io/specification) separates lightweight metadata, the instruction body, and optional resources. Hosts choose their discovery paths, invocation syntax, consent, and caching behavior.

- Global policy in [instructions/global.md](../instructions/global.md) (installed as `AGENTS.md` or `CLAUDE.md` per application) can route a task to a named skill.
- A user's explicit invocation requests the skill's workflow.
- The agent must read the discovered `SKILL.md` and follow its applicable steps.
- A helper runs only when called. A lifecycle hook runs only for supported events with an active, trusted configuration.

Invocation does not establish that every model-directed step occurred. Hooks do not cover every write path. Verify observable outcomes through the [testing strategy](../scripts/README.md#3-verification-strategy).

## 2. Skill authoring contract

### Scope and metadata

Keep each skill focused on a distinct transformation or decision. State its input, output, preservation rules, and completion checks. Prefer extending an existing skill when the output contract matches; add a skill when a different job would otherwise distort that contract.

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/       # Optional executable helpers
├── references/    # Optional material loaded when needed
└── assets/        # Optional templates or data
```

Start `SKILL.md` with YAML frontmatter:

```yaml
---
name: example-skill
description: Produces a specific result. Use when concrete task symptoms call for it. Do not use for adjacent tasks with a different output contract.
---
```

`name` must match its directory, use lowercase letters/digits with single hyphens, and contain at most 64 characters. `description` must be nonempty and contain at most 1,024 characters. Explain capability, positive triggers, and useful exclusions. The opening paragraph after the title states how to execute and what to preserve; it does not repeat routing cues.

The open specification permits optional fields, including license, compatibility, metadata, and experimental allowed-tools. Prefer the minimal two-field header here. The installer validates this repository's flat, single-line frontmatter profile, identities, and lengths; it is not a general YAML or full specification validator. Extend that parser and tests before adopting nested or multiline headers. Optional scalar fields can be used when supported by the target hosts.

### Shared writing policy

Use selected STE100 and Google developer-documentation principles: direct verbs, clear references, consistent terms, familiar words, and definitions at first use. Preserve necessary domain vocabulary, facts, commitments, uncertainty, and protected assets. Treat a Gunning Fog aim near 10 as an informal diagnostic. Claim a measured score only with a stated assessment method; these instructions do not establish full ASD-STE100 conformance.

For substantial explanations, introduce the purpose, major aspects, and their relationships before deep implementation detail. Later sections must add mechanisms, consequences, choices, or actionable detail. Keep decision-critical limits and safety warnings early. Choose connected paragraphs, lists, tables, and diagrams for the content. Preserve executable procedure order, required chronology, lookup access, explicit templates, and short-answer limits.

[progressive-documentation](../skills/progressive-documentation/SKILL.md) owns whole-document progression. [cognitive-clarity-refactor](../skills/cognitive-clarity-refactor/SKILL.md) owns dense-text conversion into its strict two-tier bullet hierarchy. They can cooperate when both contracts apply. Neither layout is the default for every artifact.

Use this section as the canonical authoring policy. Give each portable skill a short local version of the principles needed to execute on its own. Retain artifact-specific requirements: emails preserve recipient tone and modality; notes preserve comprehensive context; explanations preserve prerequisite order. Update those local versions together when the central policy changes.

### Dependencies and portable resources

Name sibling skills without filesystem links inside a skill body. Mark each dependency as required or optional. For an optional skill, include sufficient local instructions to proceed without it. For a required dependency that is unavailable, state the blocked step and complete the supported work; do not silently claim that step was performed.

Record every reference in the [call graph](#4-routing-and-call-graph).

When composing workflows, identify which skill owns the requested result and how supporting methods contribute to it. Preserve the user's question limits and artifact requirements, keep required verification intact, and avoid appending multiple default reports unless the user asks for them.

Resolve bundled resources relative to the discovered skill directory. Do not assume the caller's current directory or access to this source checkout. Keep internal resource links inside the bundle. Do not require an installed skill to read the repository's README or global instructions.

Document helper prerequisites, versions, inputs, side effects, timeouts, cleanup, and failure meanings. Keep downloads in explicit provisioning steps. A missing required checker is an unavailable verification result, not success.

### Helpers, hooks, and completion gates

| Mechanism                                | Appropriate job                                   | Limit                                           |
| ---------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| Skill helper in `skills/<name>/scripts/` | Task-specific work called by the agent            | Availability does not guarantee invocation      |
| Host hook in `adapters/`                 | Timely feedback on configured tool events         | Coverage and trust depend on the native runtime |
| Standalone verification                  | Required completion checks on resulting artifacts | Must be run and its result inspected            |

Share checker logic where semantics match; keep input/output adapters host-specific. Use executable assertions for mandatory completion criteria. Post-edit hooks can report a failure but cannot undo the preceding edit.

### Maintenance and acceptance

When changing a skill:

1. Identify the output contract being changed and the reader or workflow benefit.
2. Audit affected routing, local policies, references, helpers, and parent inventories.
3. Preserve facts, protected assets, and artifact-specific requirements.
4. Validate metadata, formatting, links, and helper behavior. Compare protected assets in the saved result after any hooks or post-processing, not only in the submitted edit.
5. For a behavior change, run a fresh-agent trial with only the installed skill and task fixture. Include a normal case and a relevant boundary case; inspect actual outputs against explicit criteria.
6. Keep the skill snapshot, input, raw output, verdict, and limitations in a temporary directory outside the checkout while reviewing and improving the change. Summarize the tested behavior, outcome, and limits in the change description or commit message. A sample passing is evidence for that sample, not proof of universal adherence.
7. Deploy and run the canonical verification command. Use native host checks before claiming hook event delivery.

For interactive skills, test multiple turns, corrections, stopping, and unavailable tools as well as the final answer. Retain each supplied answer and observed response during review. Use the [testing strategy](../scripts/README.md#3-verification-strategy) to select cases and inspect results.

Raw transcripts, duplicated skill snapshots, and historical evaluation reports stay outside the published library by default. Keep a local archive outside the checkout when later review is useful; ignored `evaluations/` is a scratch option, but ignore rules do not control every harness's context loading. Commit a small reusable fixture, explicit acceptance criteria, or an executable regression check only when it detects a concrete recurring failure and has a documented rerun path. Fold durable lessons into the current skill or testing guidance. An unchanged historical output or a checksum match does not establish current skill behavior.

## 3. Skills inventory

The library provides 16 situational skills organized by operational domain:

### Repository Operations & Git Hygiene

| Skill                                                         | Description                                                                                     |
| :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------- |
| [commit-scribe](../skills/commit-scribe/SKILL.md)             | Structured Git commits (problem, solution, decisions, implementation, notes) and upstream push. |
| [repo-evergreen-sync](../skills/repo-evergreen-sync/SKILL.md) | Propagate recent changes across the repository to eliminate drift, split-brain, and stale docs. |
| [markdown-audit](../skills/markdown-audit/SKILL.md)           | Audit documentation numbering, index coverage, and link integrity.                              |

### Engineering Strategy & Quality Assurance

| Skill                                                     | Description                                                                                            |
| :-------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| [test-strategist](../skills/test-strategist/SKILL.md)     | Audit behavior, implement verification strategies, execute checks, and maintain test instructions.     |
| [claim-validator](../skills/claim-validator/SKILL.md)     | Stress-test claims, proposals, and strategies against verified evidence.                               |
| [worth-the-squeeze](../skills/worth-the-squeeze/SKILL.md) | Audit proposals, migrations, and refactors against empirical ROI and friction without compliance bias. |
| [web-research](../skills/web-research/SKILL.md)           | Conduct multi-source web research with strict source hierarchy and citation trails.                    |

### Content Refactoring & Writing

| Skill                                                                       | Description                                                                                           |
| :-------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| [articulation-review](../skills/articulation-review/SKILL.md)               | Review document wording from user feedback, offer three inline alternatives, and apply selections.    |
| [progressive-documentation](../skills/progressive-documentation/SKILL.md)   | Whole-picture explanations that deepen relationships, mechanisms, and detail.                         |
| [cognitive-clarity-refactor](../skills/cognitive-clarity-refactor/SKILL.md) | Refactor text into low-cognitive-load, scannable Markdown with 100% semantic fidelity.                |
| [conversation-notes](../skills/conversation-notes/SKILL.md)                 | Synthesize multi-turn conversations into self-contained, book-like documentation.                     |
| [email-rewrite](../skills/email-rewrite/SKILL.md)                           | Transform rough drafts into three clear candidate emails via atomic audit and radical reorganization. |

### Architecture, Design & Discovery

| Skill                                                         | Description                                                                                                  |
| :------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------- |
| [project-scaffolding](../skills/project-scaffolding/SKILL.md) | Establish verified project foundations and practices for tracking progress, decisions, and verification.     |
| [mermaid-architect](../skills/mermaid-architect/SKILL.md)     | Design and insert compilable native Mermaid architecture and workflow diagrams.                              |
| [grill-me](../skills/grill-me/SKILL.md)                       | Discover requirements through focused dialogue, research, option comparison, and a practical next-step plan. |

### Learning & Pedagogy

| Skill                                             | Description                                                                                               |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- |
| [concept-tutor](../skills/concept-tutor/SKILL.md) | Teach technical concepts through self-contained explanations, steelmanned premises, and structured paths. |

---

## 4. Routing and call graph

Each skill is either a **lens** or a **workflow**. A lens has a narrow input and a fixed output, and it never calls a workflow. A workflow runs a multi-step procedure and calls lenses. The user or [instructions/global.md](../instructions/global.md#5-situational-skills) routes a task to its entry skill; this table records only which skill may call which.

| Mode         | Meaning                                                                                     |
| :----------- | :------------------------------------------------------------------------------------------ |
| **Required** | The caller cannot finish without it. If it is missing, report the step as not performed.    |
| **Optional** | The caller has an inline fallback of at most three sentences and proceeds without it.       |
| **Redirect** | The skill names another skill only to say the task belongs there. A redirect is not a call. |

Rules that every skill follows:

- **Named callee and stated return:** a call names one skill, and the caller uses the callee's documented output (the Returns column).
- **Callee mode:** a skill that another skill invoked makes no further skill calls. It uses its inline fallback and reports gaps as unverified. This keeps call depth at one edge from the skill the user invoked.
- **No cycles, no called workflows:** required and optional edges form a directed acyclic graph, and a workflow is never a callee.
- **One Git owner:** only commit-scribe decides whether to stage, commit, or push. Other skills hand it the change set and the user's Git words.

| Skill                                                                       | Role     | Required calls                 | Optional calls                                                                                     | Redirects                                       | Returns                                                   |
| :-------------------------------------------------------------------------- | :------- | :----------------------------- | :------------------------------------------------------------------------------------------------- | :---------------------------------------------- | :-------------------------------------------------------- |
| [commit-scribe](../skills/commit-scribe/SKILL.md)                           | lens     | none                           | none                                                                                               | none                                            | Level used, hash, files, pushed or not, tree status       |
| [web-research](../skills/web-research/SKILL.md)                             | lens     | none                           | none                                                                                               | none                                            | Answer, tiered sources table, gaps                        |
| [claim-validator](../skills/claim-validator/SKILL.md)                       | lens     | none                           | web-research                                                                                       | worth-the-squeeze                               | Verdict per hypothesis, evidence, failure modes           |
| [worth-the-squeeze](../skills/worth-the-squeeze/SKILL.md)                   | lens     | none                           | claim-validator                                                                                    | none                                            | One of five verdicts and a juice/squeeze ledger           |
| [test-strategist](../skills/test-strategist/SKILL.md)                       | lens     | none                           | web-research, worth-the-squeeze                                                                    | none                                            | Updated testing document, check results by status         |
| [progressive-documentation](../skills/progressive-documentation/SKILL.md)   | lens     | none                           | none                                                                                               | none                                            | The same facts restructured into four layers              |
| [cognitive-clarity-refactor](../skills/cognitive-clarity-refactor/SKILL.md) | lens     | none                           | progressive-documentation                                                                          | none                                            | Two-tier bullet document, facts preserved                 |
| [mermaid-architect](../skills/mermaid-architect/SKILL.md)                   | lens     | none                           | none                                                                                               | none                                            | The document plus verified diagrams, insertion-only       |
| [markdown-audit](../skills/markdown-audit/SKILL.md)                         | lens     | none                           | none                                                                                               | articulation-review, cognitive-clarity-refactor | Findings table and correction plan                        |
| [email-rewrite](../skills/email-rewrite/SKILL.md)                           | lens     | none                           | none                                                                                               | cognitive-clarity-refactor                      | Brief, ledger, three candidate emails                     |
| [concept-tutor](../skills/concept-tutor/SKILL.md)                           | lens     | none                           | progressive-documentation, cognitive-clarity-refactor                                              | none                                            | One calibrated explanation                                |
| [conversation-notes](../skills/conversation-notes/SKILL.md)                 | lens     | none                           | progressive-documentation                                                                          | none                                            | One standalone notes document                             |
| [repo-evergreen-sync](../skills/repo-evergreen-sync/SKILL.md)               | workflow | test-strategist, commit-scribe | markdown-audit, progressive-documentation, cognitive-clarity-refactor                              | none                                            | Drift ledger outcome, check results, commit-scribe report |
| [project-scaffolding](../skills/project-scaffolding/SKILL.md)               | workflow | none                           | test-strategist, web-research, worth-the-squeeze, commit-scribe                                    | none                                            | Verified foundations and a cold-start result              |
| [grill-me](../skills/grill-me/SKILL.md)                                     | workflow | none                           | web-research, worth-the-squeeze                                                                    | none                                            | Decision plan and a tracker file                          |
| [articulation-review](../skills/articulation-review/SKILL.md)               | workflow | worth-the-squeeze              | web-research, cognitive-clarity-refactor, progressive-documentation, markdown-audit, commit-scribe | none                                            | Review with three options per issue, then final text      |

`./scripts/deploy.sh` reads this table. It fails when a listed skill does not exist, when the graph has a cycle, when a workflow is called, when a lens calls a workflow, when a lens with calls lacks a callee-mode line, or when a skill's text names another skill that its row does not list (or lists one it never names). Edit the row in the same change that adds or removes a reference.

## 5. Maintenance and validation

Follow the acceptance steps in [the authoring contract](#2-skill-authoring-contract) for every skill change. Deploy the updated sources and run `./scripts/verify.sh`. Record independent behavior trials when the output contract changes.
