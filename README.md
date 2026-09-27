# Coherent Output

A curated, version-controlled repository of **universal agent behaviors, capabilities, and invariants** — engineered for steerable, predictable, and high-integrity LLM outcomes.

---

## 1. Architectural Philosophy: Universal & Tool-Agnostic

This repository serves as a **Single Source of Truth (SSOT)** for AI agent customization. The artifacts here are authored according to open standards and first principles rather than tied to any proprietary tool:

- **Open Standard Agent Skills:** All procedural capabilities in `skills/` conform to the [Agent Skills standard](https://agentskills.io) (`SKILL.md` format), making them portable across modern agentic runtime environments.
- **Universal Operating Rules:** Invariants in `rules/` and `AGENTS.md` enforce timeless engineering discipline: ASD-STE100 technical language, cognitive chunking, closed-world evidence grounding, and code documentation that explains *Why, not What*.
- **Deterministic Lifecycle Hooks:** Automated event interception in `hooks/` providing safety gates and formatting without depending on model compliance.

---

## 2. Repository Layout

```
coherent-output/
├── AGENTS.md                  # Global persona, learner profile & baseline invariants
├── .prettierrc                # Formatting standards (proseWrap: preserve, 120 print width)
│
├── rules/                     # Continuous operational rules & constraints
│   ├── 01-autonomous-workflow.md      # trigger: always_on (Core mandate & 5-step loop)
│   ├── 02-repo-integrity-drift.md     # trigger: always_on (Logic immunity & drift prevention)
│   ├── 03-code-comment-invariants.md  # trigger: always_on (Intent imperative: "Why, not What")
│   ├── 04-bullet-first-asd100.md      # trigger: always_on (ASD-STE100 & Bullet-First format)
│   └── 05-markdown-standards.md       # trigger: glob (*.md) (Numbering & relative links)
│
├── skills/                    # Modular on-demand capabilities (Agent Skills open standard)
│   ├── commit-scribe/         # /commit-scribe (Structured conventional commits)
│   ├── markdown-audit/        # /markdown-audit (Doc numbering, READMEs & link audit)
│   ├── repo-evergreen-sync/   # /repo-evergreen-sync (Delta-anchored repo reconciliation)
│   ├── mermaid-architect/     # /mermaid-architect (Native Mermaid visual modeling)
│   ├── bullet-first-refactor/ # /bullet-first-refactor (5-phase zero-loss text refactoring)
│   ├── concise-answer/        # /concise-answer (Hyper-dense direct answer overlay)
│   ├── web-research/          # /web-research (4-step research & primary source citation)
│   ├── claim-validator/       # /claim-validator (Hypothesis stress-testing & 5 verdicts)
│   ├── deidentify-document/   # /deidentify-document (PII & sensitive entity anonymization)
│   ├── discovery-advisor/     # /discovery-advisor (Socratic sparring & hand-off brief)
│   ├── concept-tutor/         # /concept-tutor (Scaffolded guides & interactive tutoring)
│   ├── code-beginner-comments/# /code-beginner-comments (Educational line-by-line comments)
│   ├── email-rewrite/         # /email-rewrite (Communication brief & professional email draft)
│   ├── conversation-notes/    # /conversation-notes (Book-like synthesis of session history)
│   ├── product-comparison/    # /product-comparison (Candidate normalization & TCO matrix)
│   └── german-tutor/          # /german-tutor (German learning, B1 reader & gender analysis)
│
├── hooks/                     # Deterministic lifecycle gates & automated scripts
│   ├── hooks.json             # Hook event configuration
│   └── scripts/
│       ├── safety-gate.sh     # PreToolUse gate for destructive bash commands
│       └── prettier-format.sh # PostToolUse deterministic Prettier auto-formatter
│
├── tools/                     # Practical utilities and standalone applications
│   ├── notepad.html           # Minimalist local notepad
│   └── devcontainer/          # Universal and Node.js container environments
│
└── scripts/
    └── deploy.sh              # Idempotent symlink deployment script
```

---

## 3. Tool Deployment & Symlink Mapping

While this repository is tool-agnostic, deployment adapters link artifacts into tool-specific configuration directories:

### Antigravity 2.0 Deployment
Run the deployment script to establish symlinks into `~/.gemini/`:
```bash
./scripts/deploy.sh
```
Target mapping:
- `AGENTS.md` → `~/.gemini/AGENTS.md`
- `rules/` → `~/.gemini/config/rules/`
- `skills/` → `~/.gemini/config/skills/`
- `hooks/hooks.json` → `~/.gemini/config/hooks.json`

### Multi-Tool Portability (Claude Code, Cursor, Copilot)
- **Claude Code:** Symlink `skills/` to `~/.claude/skills/` and link or reference `AGENTS.md` in `~/.claude/CLAUDE.md`.
- **Cursor / VS Code:** Point project settings or rules to `rules/` and `AGENTS.md`.
