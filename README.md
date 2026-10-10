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
| [skills/](skills/README.md)     | Situational child playbooks formatted to the Agent Skills open standard     |
| [rules/](rules/)                | Scoped file-pattern policies activated conditionally via glob triggers      |
| [adapters/](adapters/README.md) | Tool-specific configuration blueprints, hook templates, and runtime bridges |
| [scripts/](scripts/README.md)   | Deployment, synchronization, and automated verification scripts             |
| [.prettierrc](.prettierrc)      | Repository formatting standards                                             |

Local templates are generated into `.generated/` during installation and are excluded from Git.

---

## 3. Architecture: The Parent-Child Operating Pattern

[LOOKOUT: The parent/child contract can benefit from better aritculaituon. Its a bit confusing read right now. Let me tell you my view: I as a parent tell my child be safe, keep yourself hydrated, when in danger seek help from grownups, etc. These are basic things my child should follow irrespective of whether they are at school, playground, home, etc. I can not anticipate every time, what new challenges they will face. The challenges may be different each time based on time, place, context. Its the same with the skills and approaches in this repo. The agents.md our sometimes rules.md will be like a set of instructions given by a parent that are universal in nature while certain skills or hooks or other things will be a certain set of instructions that get invoked based on context or based on these skills/hooks being explicitly invoked. So instructions are not parent/child, but instructions are universal/contextual. The parent wants to make their child capable of tacking any scenario, any changing circumstance, and be ready. This clarity in thinking would lead to a complete rehaul of this section as well as any other aspects of the repo that you see.]
[LOOKOUT: There is another layer of the universal/contextual too. Even within application of say skills, e.g. about saying the test-strategist skill. We dont know what all different scenarios would we encounter where we want to create test strategy from scratch, update strategy, use different tools, etc. The test-strategist skill should not anticipate of every scenario. But give sufficient instructions like a checklist...hey did you think of this, did you think of that, an ideal strategy is supposed to have this, not that. Ideally strategy and execution of tests should be invoked in these scenarios and not that, etc. And then the actual test strategy for that repo or tool or system sits in say the TESTING.MD file or whatever. Thats the real home of the test strategy. The test-strategist is the one which helps formulate and maintain the test strategy for a particular context. But does not formulate the strategy in itself. The human or ai coding tool working on the actual project should do that. Please stellman my intent and tell me your understanding of it.]

This repository organizes agent steering into a high-signal hierarchy that prevents instruction bloat and cognitive friction:

```
┌────────────────────────────────────────────────────────────────────────┐
│ THE PARENT CONTRACT: AGENTS.md (Universal Baseline)                    │
│ "Stay safe, communicate clearly, and follow the 4-step workflow."       │
│ • Universal Communication Register (ASD-STE100, zero filler)           │
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
│ • repo-evergreen│        │• cognitive-     │        │  rules loaded   │
│   -sync         │        │  clarity-       │        │  only on match  │
│                 │        │  refactor       │        │                 │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

1. **The Parent Baseline (`AGENTS.md`):** High-level, positive, and situational-agnostic. It sets the baseline posture independent of domain. It defines the universal 4-step workflow and acts as an autonomous policy router (Section 5) that directs agents toward specific skills when encountering complex procedures.
2. **The Situational Skills (`skills/*/SKILL.md`):** Deep, specialized playbooks following the [Agent Skills standard](skills/README.md). They operate via **Progressive Disclosure**: harnesses pre-load lightweight metadata (`name` and `description`) into the system prompt, and the agent reads full procedural instructions only when activated. Skills are triggered either autonomously via `AGENTS.md` policy routing or deterministically via user slash commands (e.g., `/commit-scribe`).
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

1. **Execute Full Verification:**

   ```bash
   ./scripts/verify.sh
   ```

   Validates symlink integrity, executes the deployment isolation test suite, and checks Prettier formatting across all files.

---

## 7. Skills Inventory

For authoring standards, frontmatter contracts, and progressive disclosure architecture, see [skills/README.md](skills/README.md).

| Skill                                                                    | Purpose                                                                          |
| :----------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| [articulation-review](skills/articulation-review/SKILL.md)               | Review document wording with inline alternatives and apply selections            |
| [cognitive-clarity-refactor](skills/cognitive-clarity-refactor/SKILL.md) | Refactor text into low-cognitive-load, scannable Markdown without losing meaning |
| [claim-validator](skills/claim-validator/SKILL.md)                       | Evaluate claims against evidence                                                 |
| [commit-scribe](skills/commit-scribe/SKILL.md)                           | Write structured Git commits and push to remote                                  |
| [concept-tutor](skills/concept-tutor/SKILL.md)                           | Teach technical concepts                                                         |
| [conversation-notes](skills/conversation-notes/SKILL.md)                 | Turn conversations into standalone notes                                         |
| [email-rewrite](skills/email-rewrite/SKILL.md)                           | Rewrite professional correspondence                                              |
| [markdown-audit](skills/markdown-audit/SKILL.md)                         | Inspect documentation structure and links                                        |
| [mermaid-architect](skills/mermaid-architect/SKILL.md)                   | Create Mermaid diagrams                                                          |
| [repo-evergreen-sync](skills/repo-evergreen-sync/SKILL.md)               | Synchronize repository and resolve cascading drift                               |
| [test-strategist](skills/test-strategist/SKILL.md)                       | Strategize test coverage and adapt harnesses mid-development                     |
| [web-research](skills/web-research/SKILL.md)                             | Research external questions using primary evidence                               |
| [worth-the-squeeze](skills/worth-the-squeeze/SKILL.md)                   | Stress-test proposals against objective ROI and trade-offs                       |

---

## 8. Lifecycle Hooks and Local Settings

- **Antigravity Hooks:** Implements a destructive command gate (`safety-gate.sh` on `PreToolUse` for `run_command`), a Prettier auto-formatter (`prettier-format.sh` on `PostToolUse` for file write operations), and a Mermaid syntax validator (`mermaid-validate.sh` on `PostToolUse` for Markdown writes). See [adapters/README.md](adapters/README.md) for contract details.
- **Codex Approvals:** Codex retains its native command approval policies. Codex's hook contract does not support `force_ask`, so native prompts govern command execution.
