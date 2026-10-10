# Agent Skills Library

This directory contains the situational skill library for AI coding agents. Every skill conforms to the open [Agent Skills specification](https://agentskills.io) and is shared across development environments (Google Antigravity and OpenAI Codex).

---

## 1. Architecture: The Progressive Disclosure Model

AI agents do not search arbitrary directories to locate skills. Instead, runtime harnesses manage skills through a three-tier **Progressive Disclosure** pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: HARNESS STARTUP CATALOG (~50-100 tokens per skill)             │
│ Harness scans ~/.agents/skills or ~/.gemini/config/skills.             │
│ Reads YAML frontmatter (name + description) and injects into prompt:   │
│   <skills>                                                             │
│   - commit-scribe (/path/to/commit-scribe/SKILL.md): Creates ...       │
│   </skills>                                                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Task matches skill description
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 2: ON-DEMAND INSTRUCTION ACTIVATION                               │
│ Agent reads SKILL.md via file view tool using harness-supplied path.   │
│ Full procedural instructions enter context only when actively needed.  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Workflow requires scripts or data
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 3: RESOURCE EXECUTION                                             │
│ Agent inspects local scripts/, references/, or assets/ only if called. │
└────────────────────────────────────────────────────────────────────────┘
```

### The Dual Ingestion Model

Skills are activated through two complementary channels:

1. **Autonomous Policy Routing (`AGENTS.md` Section 5):**
   - The harness pre-loads skill names and paths in the system prompt.
   - The parent policy in `AGENTS.md` tells the agent _when_ it must not improvise (e.g., `"When committing, use commit-scribe"`).
   - The model matches the named policy to its pre-loaded skills catalog and reads the instructions without requiring user intervention.
2. **Explicit User Invocations (Slash Commands):**
   - The user explicitly calls a skill in chat (e.g., `/commit-scribe`, `/repo-evergreen-sync`, `/web-research`).
   - This bypasses model autonomy and deterministically forces the harness and agent to execute the requested playbook.

---

## 2. Skill Authoring Contract

When adding or updating a skill, adhere strictly to the following standards:

### Directory Structure

```text
skills/<skill-name>/
├── SKILL.md              # Required: Main instruction file with YAML frontmatter
├── scripts/              # Optional: Helper shell or Python scripts
├── references/           # Optional: Deep reference manuals, schemas, or docs
└── resources/            # Optional: Templates, vocabularies, or static data
```

### Frontmatter Schema

Every `SKILL.md` must start with valid YAML frontmatter containing exactly `name` and `description`:

```yaml
---
name: example-skill
description: Concise, third-person trigger criteria explaining WHAT the skill does, WHEN to invoke it, and WHEN NOT to invoke it. Maximum 1024 characters.
---
```

- **`name`:** Lowercase alphanumeric with hyphens (`kebab-case`). Must match the parent directory name.
- **`description`:** High-signal trigger statement. Harnesses pre-load only this text into the system prompt during Tier 1 discovery.

### Authoring Guidance: Frontmatter `description` vs. Post-H1 Paragraph

Because AI harnesses use progressive disclosure, the frontmatter `description` and the post-H1 introductory paragraph fulfill two fundamentally distinct roles:

1. **Frontmatter `description` (Tier 1: Routing & Discovery Contract):**
   - **Audience:** The routing model deciding _whether_ to activate a skill before reading its body.
   - **Required Three-Part Anatomy:**
     - **Capabilities:** Direct statement of what technical outcome or artifact the skill produces.
     - **Positive Triggers:** Explicit user intents, phrasing, task stages, or symptoms signaling invocation (e.g., `"Use when reviewing drafts...", "Activate before staging git changes..."`).
     - **Negative Triggers (Boundaries):** Explicit exclusions preventing false-positive activations (e.g., `"Do not use for code blocks...", "Omit during intermediate WIP iterations..."`).
   - **Constraints:** Maximum 1,024 characters. Write in concise third-person or imperative register.

2. **Post-H1 Introductory Paragraph (Tier 2: Operational Grounding Contract):**
   - **Audience:** The active agent that has _already_ loaded the skill into context.
   - **Required Three-Part Anatomy:**
     - **Operational Mission:** Direct executive directive setting the agent's professional posture.
     - **Transformation Contract:** Clear statement of input $\rightarrow$ output guarantees (e.g., converting disorganized drafts into two-tier Markdown while preserving 100% of substantive facts).
     - **Behavioral Invariants:** Non-negotiables governing the execution (e.g., zero sycophancy, verbatim code protection, ASD-STE100 active voice).
   - **Anti-Pattern to Avoid:** Never repeat routing cues (`"Use this skill when..."`) in the post-H1 paragraph. Focus strictly on execution standards and invariants.

### Portability & Linking Rules

- **Sibling Skills:** Reference sibling skills by name without relative Markdown paths (e.g., `activate the commit-scribe skill`). AI coding agents match skill names against their runtime skills catalog rather than resolving relative filesystem links.
- **No External Relative Links:** Never use relative paths to files outside the `skills/` directory (e.g., `../AGENTS.md` or `../../README.md`). Deployed skills reside in separate configuration directories where those relative paths do not exist. Refer to external standards conceptually.

### Style & Content Standards

- **Understated Engineering Register:** Write affirmative, active-voice instructions compliant with ASD-STE100 plain language.
- **Why, Not What:** Document invariants, safety constraints, and decision rationale.
- **Zero Residue:** Ensure execution steps clean up scratchpads, temporary files, and debug logging.

### Scripts vs. Lifecycle Hooks: Architectural Rule

When adding executable code or validation logic, use the appropriate mechanism:

| Mechanism               | Location                                              | Invocation Model                                                                | Primary Purpose                                                        | Examples                                                                                                                                                            |
| :---------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------ | :--------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Skill Helper Script** | `skills/<skill>/scripts/`                             | **Probabilistic / On-Demand** (Agent invokes via `run_command` during workflow) | Task-specific helpers, interactive tools, or specialized runbook steps | Compiling a single `.mmd` preview, generating domain scaffolding, parsing specialized fixtures                                                                      |
| **Lifecycle Hook**      | `adapters/antigravity/hooks/` (`hooks.template.json`) | **Deterministic / Runtime-Enforced** (Fired automatically on lifecycle events)  | Mandatory invariants, universal guardrails, and formatters             | Prettier auto-formatting on file write (`PostToolUse`), Mermaid syntax validation on Markdown save (`PostToolUse`), destructive command safety gates (`PreToolUse`) |

**Script Authoring Invariants:**

1. **No CWD Assumptions:** Never assume the agent's Current Working Directory is the repository root or skill folder. Always instruct agents to resolve scripts relative to the skill directory (e.g., `<skill_dir>/scripts/<script_name>`).
2. **Enforce Invariants via Hooks:** If a rule or check is non-negotiable and must execute every single time without relying on model memory or prompt adherence, register it as a Lifecycle Hook rather than a skill script alone.

---

## 3. Skills Inventory

The library provides 14 situational skills organized by operational domain:

### Repository Operations & Git Hygiene

| Skill                                               | Description                                                                                     |
| :-------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| [commit-scribe](commit-scribe/SKILL.md)             | Structured Git commits (problem, solution, decisions, notes) and upstream pushing.              |
| [repo-evergreen-sync](repo-evergreen-sync/SKILL.md) | Propagate recent changes across the repository to eliminate drift, split-brain, and stale docs. |
| [markdown-audit](markdown-audit/SKILL.md)           | Audit documentation numbering, index coverage, and link integrity.                              |

### Engineering Strategy & Quality Assurance

| Skill                                           | Description                                                                                            |
| :---------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| [test-strategist](test-strategist/SKILL.md)     | Assess repository topology, evaluate harness deltas, and adapt test portfolios.                        |
| [claim-validator](claim-validator/SKILL.md)     | Stress-test claims, proposals, and strategies against verified evidence.                               |
| [worth-the-squeeze](worth-the-squeeze/SKILL.md) | Audit proposals, migrations, and refactors against empirical ROI and friction without compliance bias. |
| [web-research](web-research/SKILL.md)           | Conduct multi-source web research with strict source hierarchy and citation trails.                    |

### Content Refactoring & Writing

| Skill                                                             | Description                                                                                                |
| :---------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| [articulation-review](articulation-review/SKILL.md)               | Review document wording from user feedback, offer three inline alternatives, and apply selections.         |
| [cognitive-clarity-refactor](cognitive-clarity-refactor/SKILL.md) | Refactor text into low-cognitive-load, scannable Markdown with 100% semantic fidelity.                     |
| [conversation-notes](conversation-notes/SKILL.md)                 | Synthesize multi-turn conversations into self-contained, book-like documentation.                          |
| [email-rewrite](email-rewrite/SKILL.md)                           | Transform rough drafts into three ASD-STE100 candidate emails via atomic audit and radical reorganization. |

### Architecture, Design & Discovery

| Skill                                               | Description                                                                                                            |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| [project-scaffolding](project-scaffolding/SKILL.md) | Plan and establish minimal repository structure, technical foundations, testing harnesses, and development continuity. |
| [mermaid-architect](mermaid-architect/SKILL.md)     | Design and insert compilable native Mermaid architecture and workflow diagrams.                                        |

### Learning & Pedagogy

| Skill                                   | Description                                                                                               |
| :-------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| [concept-tutor](concept-tutor/SKILL.md) | Teach technical concepts through self-contained explanations, steelmanned premises, and structured paths. |

---

## 4. Maintenance & Validation Checklist

Before committing additions or modifications to skills:

1. **Frontmatter Validation:** Verify `name` matches directory name and `description` is concise and actionable.
2. **Link Audit:** Verify all internal relative links point to valid sibling files.
3. **Format Check:** Run `npx prettier --check skills/<skill-name>/SKILL.md`.
4. **Deploy & Test:** Execute `./scripts/deploy.sh` followed by `./scripts/verify.sh` to confirm deployment sync and test suite passage.
