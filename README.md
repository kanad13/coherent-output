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

| Location                        | Purpose                                                                     |
| :------------------------------ | :-------------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)          | Universal baseline parent directive: persona, workflow loop, and boundaries |
| [skills/](skills/)              | Situational child playbooks formatted to the Agent Skills open standard     |
| [rules/](rules/)                | Scoped file-pattern policies activated conditionally via glob triggers      |
| [adapters/](adapters/README.md) | Tool-specific configuration blueprints, hook templates, and runtime bridges |
| [scripts/](scripts/README.md)   | Deployment, synchronization, and automated verification scripts             |
| [.prettierrc](.prettierrc)      | Repository formatting standards                                             |

Local templates are generated into `.generated/` during installation and are excluded from Git.

---

## 3. Architecture: The Parent-Child Operating Pattern

This repository organizes agent steering into a high-signal hierarchy that prevents instruction bloat and cognitive friction:

```
┌────────────────────────────────────────────────────────────────────────┐
│ THE PARENT CONTRACT: AGENTS.md (Universal Baseline)                    │
│ "Stay safe, communicate clearly, and follow the 4-step workflow."       │
│ • Universal Communication Register (ASD-STE100, zero filler, visuals)   │
│ • The 4-Step Workflow Progression (Ground ➔ Plan ➔ Execute ➔ Verify)   │
│ • Escalation Boundaries (Autonomous by default; 3 explicit pause gates) │
│ • Decision Rationale ("Why, Not What")                                 │
│ • Situational-Agnostic: Governs coding, research, writing, and chat    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Activates on demand:
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ Situational     │        │ Situational     │        │ Scoped Rules    │
│ Skills (Child)  │        │ Skills (Child)  │        │ (rules/*.md)    │
│ • commit-scribe │        │• test-strategist│        │• Glob-triggered │
│ • repo-evergreen│        │• bullet-first-  │        │  rules loaded   │
│   -sync         │        │  refactor       │        │  only on match  │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

1. **The Parent Baseline (`AGENTS.md`):** High-level, positive, and situational-agnostic. It sets the baseline posture independent of domain. It avoids micro-managing mechanical actions ("crossing the street") to prevent attention degradation and instruction straightjacketing.
2. **The Situational Skills (`skills/*/SKILL.md`):** Deep, specialized playbooks equipped for specific scenarios ("when swimming, do this; when on a train, do this"). They contain step-by-step checklists, command sequences, and verification gates. Loaded strictly on demand, they never burn standing prompt tokens during everyday turns.
3. **The Scoped Rules (`rules/*.md`):** Reserved exclusively for file-pattern adaptations (`trigger: glob`, e.g. `*.py` or `*.tsx`) that load only when the agent touches matching file paths.

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

---

## 7. Skills Inventory

| Skill                                                            | Purpose                                                      |
| :--------------------------------------------------------------- | :----------------------------------------------------------- |
| [bullet-first-refactor](skills/bullet-first-refactor/SKILL.md)   | Refactor text into structured bullets without losing meaning |
| [claim-validator](skills/claim-validator/SKILL.md)               | Evaluate claims against evidence                             |
| [code-beginner-comments](skills/code-beginner-comments/SKILL.md) | Explain code for learners                                    |
| [commit-scribe](skills/commit-scribe/SKILL.md)                   | Write structured Git commits and push to remote              |
| [concept-tutor](skills/concept-tutor/SKILL.md)                   | Teach technical concepts                                     |
| [concise-answer](skills/concise-answer/SKILL.md)                 | Give concise technical answers                               |
| [conversation-notes](skills/conversation-notes/SKILL.md)         | Turn conversations into standalone notes                     |
| [deidentify-document](skills/deidentify-document/SKILL.md)       | Remove identifying information                               |
| [discovery-advisor](skills/discovery-advisor/SKILL.md)           | Clarify requirements and architecture choices                |
| [email-rewrite](skills/email-rewrite/SKILL.md)                   | Rewrite professional correspondence                          |
| [german-tutor](skills/german-tutor/SKILL.md)                     | Support German language learning                             |
| [markdown-audit](skills/markdown-audit/SKILL.md)                 | Inspect documentation structure and links                    |
| [mermaid-architect](skills/mermaid-architect/SKILL.md)           | Create Mermaid diagrams                                      |
| [product-comparison](skills/product-comparison/SKILL.md)         | Compare products and ownership costs                         |
| [repo-evergreen-sync](skills/repo-evergreen-sync/SKILL.md)       | Synchronize repository and resolve cascading drift           |
| [test-strategist](skills/test-strategist/SKILL.md)               | Strategize test coverage and adapt harnesses mid-development |
| [web-research](skills/web-research/SKILL.md)                     | Research external questions using primary evidence           |

---

## 8. Lifecycle Hooks and Local Settings

- **Antigravity Hooks:** Implements a destructive command gate (`safety-gate.sh` on `PreToolUse` for `run_command`) and a Prettier auto-formatter (`prettier-format.sh` on `PostToolUse` for file write operations). See [adapters/README.md](adapters/README.md) for contract details.
- **Codex Approvals:** Codex retains its native command approval policies. Codex's hook contract does not support `force_ask`, so native prompts govern command execution.
