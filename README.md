# Coherent Output

This repository maintains a personal library of agent instructions, skills, and hooks across Macs. Git carries the sources between devices; the installer links each Mac's applications to its local checkout.

There are two useful installation paths. The personal installer deploys the whole library, instructions, rules, and host adapters. A portable skills installer copies selected skills into a project for other agents. Skills provide model-directed workflows; hooks provide feedback on supported tool events; the verification command checks the resulting files and configuration.

## 1. Personal installation

Use Node.js 22.13.0 or later and Python 3. Provision the pinned formatter and diagram renderer, preview the mappings, then install:

```bash
npm ci
./scripts/deploy.sh --dry-run
./scripts/deploy.sh
./scripts/verify.sh
```

The dependencies include Puppeteer, which provisions the browser used by Mermaid CLI. The lockfile pins dependencies and the package manifest approves its specific install script. Hooks use provisioned tools and do not download packages while checking an edit.

For an Antigravity-only installation, use the same checkout and provisioned dependencies:

```bash
./scripts/deploy.sh --tool antigravity --dry-run
./scripts/deploy.sh --tool antigravity
./scripts/verify.sh --tool antigravity
```

This installs global instructions, rules, all skills and their bundled helpers, and the three Antigravity hook registrations. Commands resolve the recipient's checkout; generated machine-local paths are not committed. Use `--tool codex` for a Codex-only installation. Each selection generates and validates only its host artifacts, while checking shared skill metadata.

Unknown destination files cause deployment to stop before writes. Use `./scripts/deploy.sh --backup-conflicts` when adopting them: the installer preserves originals and a restore manifest under `~/.local/state/coherent-output/backups/`. Codex hook adoption also retains unrelated handlers and settings in the generated configuration.

Start a fresh chat after deployment. Codex reviews new or changed hook entries through its native trust flow; installation does not approve trust entries. Its generated checker command uses the installer's absolute Python path. Redeploy after changing the Python installation. Shell entry points and checkers add standard user and Homebrew runtime directories for GUI sessions that do not load a shell profile.

## 2. Install selected skills in a project

From the target project, use the established [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx --yes skills@1.7.2 add kanad13/coherent-output --list
npx --yes skills@1.7.2 add kanad13/coherent-output \
  --skill cognitive-clarity-refactor \
  --agent codex claude-code gemini-cli --yes
```

For unpublished changes, replace `kanad13/coherent-output` with the absolute path to this checkout. This route installs skill folders and their bundled helpers. It does not deploy this repository's global instructions, rules, hooks, or formatter dependencies. A copied skill is a snapshot; editing the source checkout does not update that copy.

The CLI's host mapping places canonical project copies in `.agents/skills` and creates host links where needed. Codex, Claude Code, and Gemini CLI project installation was exercised during the audit; full Claude/Gemini runtime execution was not tested. Antigravity IDE and Gemini CLI have different configuration conventions. See the [adapter guide](adapters/README.md).

Use the project route alongside this repository's personal installation. The personal installer owns the entire global `~/.agents/skills` symlink. A different installer writing through that global path can modify the source checkout. Do not combine global installation methods at that path.

The repository has no declared license. Choose a license before presenting it as an openly reusable public package.

## 3. How the parts work together

| Source                          | Role                                                           |
| ------------------------------- | -------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)          | Short baseline for communication, workflow, and skill routing  |
| [skills/](skills/README.md)     | Situational playbooks with discoverable name and description   |
| [rules/](rules/)                | Optional scoped policies; there are currently no written rules |
| [adapters/](adapters/README.md) | Host mappings, hook templates, and payload normalization       |
| [scripts/](scripts/README.md)   | Installation, behavior tests, and final verification           |
| [package.json](package.json)    | Pinned fallback formatter and diagram renderer                 |

A host discovers skill metadata in its supported directories. The agent reads a skill body when the task or user invocation calls for it, and invokes bundled helpers when needed. A skill's instructions do not guarantee execution of every step.

The installer composes Codex instructions from `AGENTS.md` and written rules, with natural-language conditions for glob rules. Antigravity uses its rules directory. Generated files live in ignored `.generated/`; device-owned authentication, histories, databases, and plugin caches stay local.

Codex and Antigravity use different hook payloads. Their adapters normalize edited paths into shared document checks. The checks format supported files and compile Mermaid fences, with errors returned to the host. Post-edit hooks cannot undo an edit. Shell and unsupported-tool writes need the standalone verification gate.

## 4. Writing and skill maintenance

Use [progressive-documentation](skills/progressive-documentation/SKILL.md) to introduce a substantial explanation as a coherent whole, then deepen mechanisms, relationships, consequences, and detail. Use [cognitive-clarity-refactor](skills/cognitive-clarity-refactor/SKILL.md) for dense text that needs its strict, scannable bullet hierarchy.

The [authoring contract](skills/README.md#2-skill-authoring-contract) defines the shared writing policy, artifact-specific structure, dependency rules, and validation requirements. Each writing skill includes its local writing guidance; required workflow dependencies are documented separately. Emails, procedures, reference material, and short answers keep the structures their readers need.

## 5. Working across Macs

On the source Mac, edit the library, deploy, and verify. Commit and push when that workflow is requested. On another Mac, pull the changes, run `npm ci`, deploy, verify, and start fresh chats.

After changing skills, rules, adapters, or deployment behavior:

```bash
./scripts/deploy.sh
./scripts/verify.sh
```

Behavior changes to skills also require a task trial with only the skill and input material. The [testing guide](scripts/README.md#3-verification-strategy) distinguishes automated checks, independent writing trials, and native host checks.

The [repository audit](REPO-AUDIT.md) records the original baseline and research. The [skill evaluation](SKILL-EVALUATION.md) records the implemented document guidance and independent trials.
