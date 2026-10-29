# Coherent Output: Repository Instructions

This repository is the source for the user's global agent setup. It is not an application. Its output is the set of files that the installer links into Claude Code, Codex, and Antigravity. The global baseline lives in [instructions/global.md](instructions/global.md) and is already loaded; do not repeat it here.

## Where things live

| Path                                             | Role                                                                    |
| ------------------------------------------------ | ----------------------------------------------------------------------- |
| [instructions/global.md](instructions/global.md) | Template for the user's global `AGENTS.md` and `CLAUDE.md`.             |
| [skills/](skills/)                               | One folder per skill. Each holds a `SKILL.md` and optional helpers.     |
| [adapters/](adapters/README.md)                  | Per-application link maps, hook templates, and the shared edit checker. |
| [scripts/](scripts/README.md)                    | Installer (`deploy.py`), tests, and `verify.sh`.                        |
| [docs/skills.md](docs/skills.md)                 | Skill authoring contract, maintenance steps, and the skill inventory.   |

## Rules for changes

- **Editing a skill:** read the authoring contract in [docs/skills.md](docs/skills.md#2-skill-authoring-contract) first. Keep frontmatter to flat `name` and `description`; the installer rejects anything else. Add new skills to the inventory table in the same change.
- **After every skill edit or new skill:** activate `test-strategist` on that skill before the commit. It audits the skill's tests, then you add or update `evals/<skill>/` (rules quoted verbatim from `SKILL.md`, cases that push against each rule, graders in `scripts/skill_graders.py`). Run the trial with your own fresh agents: `python3 scripts/skill_evals.py prepare <skill> --all`, start one agent per run folder, then `grade <skill> --out <dir> --stamp`. The harness that edits the skill runs its trials; do not ask other harnesses to. Never call the skill verified on static checks alone. Details: [evals/README.md](evals/README.md).
- **Adding or removing a reference between skills:** update the call-graph table in [docs/skills.md](docs/skills.md#4-routing-and-call-graph) in the same change. The installer refuses a table that disagrees with the skill texts.
- **Editing `instructions/global.md`:** this changes every application on every machine. Codex and Claude Code receive a generated copy, so the change takes effect only after `./scripts/deploy.sh`. Antigravity links to the file directly.
- **Editing an adapter or `deploy.py`:** add or update a test in `scripts/` that runs against an isolated home. Use `--target-home` for manual trials. Never test against the real home without `--dry-run` first.
- **Adding an application or hook:** follow [adapters/README.md](adapters/README.md#4-adding-an-application-or-a-hook).
- **Hand-edited generated files:** never edit anything in `.generated/`. Change the source and redeploy.

## Required checks

After any change to a skill, instruction, adapter, or script:

```bash
./scripts/deploy.sh      # regenerate and relink
./scripts/verify.sh      # drift check, tests, Prettier, Mermaid
```

`verify.sh` must pass before a commit. It reports each skill with a suite as `STALE` when the skill changed after its last passing trial. After a change to a helper, a grader, or their tests, also run `python3 scripts/sabotage_check.py` (breaks each guarded behavior and confirms a test fails). A pre-commit hook in `.githooks/` runs the fast subset (`deploy.sh` enables it for the clone), and CI repeats the checks on push. None of these can judge whether a changed skill still produces good output; for that, run a fresh-agent trial as described in [scripts/README.md](scripts/README.md#3-verification-strategy).

## Writing style

Docs in this repository follow the plain-language policy in [docs/skills.md](docs/skills.md#shared-writing-policy). Describe current behavior in the present tense; history belongs in commit messages. Put one fact in one place and link to it.
