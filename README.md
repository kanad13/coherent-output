# Coherent Output

This repository maintains shared agent instructions, operational rules, modular skills, and deterministic hooks across multiple Macs. Git synchronizes the source files between devices. Each Mac runs the installer to link its local applications to its own repository checkout.

---

## 1. Quickstart

Run deployment from this checkout:

```bash
./scripts/deploy.sh
./scripts/verify.sh
```

- `./scripts/deploy.sh` links shared sources to application configuration paths and renders local machine templates.
- `./scripts/verify.sh` verifies link health, runs the test suite, and checks formatting compliance.

---

## 2. Source Layout

| Location                        | Purpose                                                                             |
| :------------------------------ | :---------------------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)          | Universal baseline directive: persona, workflow loop, boundaries, and policy router |
| [skills/](skills/README.md)     | Situational child playbooks formatted to the Agent Skills open standard             |
| [rules/](rules/)                | Scoped file-pattern policies activated conditionally via glob triggers              |
| [adapters/](adapters/README.md) | Tool-specific configuration blueprints, hook templates, and runtime bridges         |
| [scripts/](scripts/README.md)   | Deployment, synchronization, and automated verification scripts                     |
| [.prettierrc](.prettierrc)      | Repository formatting standards                                                     |

Local templates are generated into `.generated/` during installation and are excluded from Git.

---

## 3. Architecture: Universal Directives vs. Contextual Execution

This repository structures agent steering across two complementary operational dimensions: **Universal Directives** and **Contextual Execution**.

A parent equips a child with universal, non-negotiable principles: stay safe, maintain hydration, and seek adult guidance when facing danger. The child applies these principles in any environment—whether at home, school, or the playground. The parent does not micromanage or anticipate every isolated hazard in advance; instead, the parent prepares the child to assess and navigate changing circumstances responsibly.

Similarly, instructions in this repository divide into universal baselines and situational playbooks:

```
┌────────────────────────────────────────────────────────────────────────┐
│ UNIVERSAL DIRECTIVE: AGENTS.md (System Baseline)                       │
│ "Stay safe, communicate clearly, and follow the 4-step workflow."       │
│ • Universal Communication Register (ASD-STE100, active voice)          │
│ • The 4-Step Workflow Progression (Ground ➔ Plan ➔ Execute ➔ Verify)   │
│ • Escalation Boundaries (Autonomous by default; 3 explicit pause gates) │
│ • Decision Rationale ("Why, Not What")                                 │
│ • Domain-Agnostic: Governs coding, research, writing, and chat         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Activates on demand:
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ Situational     │        │ Scoped Rules    │        │ Lifecycle Hooks │
│ Skills          │        │ (rules/*.md)    │        │ (adapters/hooks)│
│ • test-strategist│       │ • Glob triggers │        │ • Safety gates  │
│ • project-      │        │   loaded only   │        │ • Formatters    │
│   scaffolding   │        │   on file match │        │ • Validators    │
│ • commit-scribe │        │                 │        │                 │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

### The Two Layers of Universal vs. Contextual

1. **System Layer (Directive vs. Playbook):**
   - **Universal Directives (`AGENTS.md`):** High-level, positive, and domain-agnostic. It establishes operational posture across all tools and tasks. It defines the universal 4-step workflow, communication standards, safety boundaries, and policy routing (Section 5) that directs agents to specialized skills when encountering multi-step procedures.
   - **Contextual Capabilities (`skills/`, `rules/`, `adapters/hooks`):** Activated only when context demands them:
     - **Situational Skills (`skills/*/SKILL.md`):** Specialized playbooks following the [Agent Skills standard](skills/README.md). Harnesses pre-load lightweight metadata (`name` and `description`) into the system prompt (**Progressive Disclosure**), and the agent reads full procedural bodies only when activated via `AGENTS.md` policy routing or user slash commands (e.g., `/test-strategist`).
     - **Scoped Rules (`rules/*.md`):** Loaded conditionally based on file-pattern triggers (`trigger: glob`, e.g. `*.py` or `*.tsx`) when the agent accesses matching paths.
     - **Lifecycle Hooks (`adapters/antigravity/hooks`):** Deterministic guardrails executed by the harness on runtime tool events (`PreToolUse`, `PostToolUse`).

2. **Skill Layer (Invariant Protocol vs. Project Artifact):**
   - The universal/contextual separation also recurs within individual skills. A skill such as `test-strategist` or `project-scaffolding` does not attempt to anticipate every unique project topology or hardcode a static plan.
   - Instead, the skill provides **universal invariants, discovery checklists, and verification heuristics** (e.g., mapping execution surfaces, cost-to-evidence parity, defect reproduction, zero assertion weakening).
   - The **concrete contextual strategy** belongs to the target project itself (stored in that repository's `TESTING.md`, `README.md`, or architecture records). The skill provides the repeatable protocol to formulate, audit, and evolve that contextual strategy.

---

## 4. Installed Mapping

`<repo>` represents the absolute path to this checkout on the active Mac. `~` represents the user home directory.

| Application     | Tool Configuration Path       | Target Source or Generated File            | Mechanics                                                          |
| :-------------- | :---------------------------- | :----------------------------------------- | :----------------------------------------------------------------- |
| **Codex**       | `~/.agents/skills`            | `<repo>/skills`                            | Direct directory symlink                                           |
| **Codex**       | `~/.codex/AGENTS.md`          | `<repo>/.generated/codex/AGENTS.md`        | Composed instruction file merging `AGENTS.md` and any scoped rules |
| **Antigravity** | `~/.gemini/AGENTS.md`         | `<repo>/AGENTS.md`                         | Direct file symlink                                                |
| **Antigravity** | `~/.gemini/config/rules`      | `<repo>/rules`                             | Direct directory symlink                                           |
| **Antigravity** | `~/.gemini/config/skills`     | `<repo>/skills`                            | Direct directory symlink                                           |
| **Antigravity** | `~/.gemini/config/hooks.json` | `<repo>/.generated/antigravity/hooks.json` | Rendered JSON template inserting local checkout paths              |

---

## 5. Multi-Mac Workflow

```
Primary Mac (Make Changes)                Secondary Mac (Receive Changes)
--------------------------                -------------------------------
1. Edit skills, rules, or adapters        1. git pull
2. ./scripts/deploy.sh                    2. ./scripts/deploy.sh
3. ./scripts/verify.sh                    3. ./scripts/verify.sh
4. git commit & git push                  4. Restart chat sessions
```

- **Conflict Handling:** The installer aborts before making changes if unknown existing files are found at destination paths. Use `./scripts/deploy.sh --backup-conflicts` to safely move conflicting files into `~/.local/state/coherent-output/backups/`.
- **Local Isolation:** Machine-specific state (databases, authentication, session histories, and plugin caches) remains strictly local.

---

## 6. AI Agent Operating Protocol

When any AI coding agent modifies rules, skills, or adapters in this repository, the agent must adhere to the following two-step contract before concluding work:

1. **Synchronize Local State:**

   ```bash
   ./scripts/deploy.sh
   ```

   Ensures that `.generated/codex/AGENTS.md` is re-composed from updated rules and that local hook templates match the active repository path.

2. **Execute Full Verification:**

   ```bash
   ./scripts/verify.sh
   ```

   Validates symlink integrity, executes the deployment isolation test suite, and checks Prettier formatting across all files.

## 7. Skills & Authoring Architecture

Situational agent playbooks reside in [skills/](skills/README.md) and adhere to the [Agent Skills open standard](https://agentskills.io).

To eliminate documentation drift and preserve single-source-of-truth integrity, canonical skill documentation is centralized:

- **Skills Catalog & Categorized Inventory:** For the full list of available skills by operational domain, see [skills/README.md Section 3](skills/README.md#3-skills-inventory).
- **Authoring Contract & Progressive Disclosure:** For frontmatter guidelines, directory conventions, and discovery mechanics, see [skills/README.md Section 2](skills/README.md#2-skill-authoring-contract).
- **Autonomous Policy Routing:** For universal triggers directing agents to activate specific skills, see [AGENTS.md Section 5](AGENTS.md#5-situational-skills).

---

## 8. Lifecycle Hooks and Local Settings

- **Antigravity Hooks:** Implements a destructive command gate (`safety-gate.sh` on `PreToolUse` for `run_command`), a Prettier auto-formatter (`prettier-format.sh` on `PostToolUse` for file write operations), and a Mermaid syntax validator (`mermaid-validate.sh` on `PostToolUse` for Markdown writes). See [adapters/README.md](adapters/README.md) for contract details.
- **Codex Approvals:** Codex retains its native command approval policies. Codex's hook contract does not support `force_ask`, so native prompts govern command execution.
