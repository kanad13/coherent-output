# Scripts

The installer deploys this checkout without copying device-owned state. Verification checks both configuration and observable behavior. Independent skill trials are separate evidence for workflows whose output depends on model judgment.

## 1. Commands and prerequisites

Install Node.js 22.13.0 or later, npm, Python 3, and the pinned dependencies:

```bash
npm ci
./scripts/deploy.sh --dry-run
./scripts/deploy.sh
./scripts/verify.sh
```

Puppeteer supplies the browser used by Mermaid CLI. The manifest approves its pinned install script. If browser provisioning is unavailable, report Mermaid verification as unavailable.

| Script                                     | Responsibility                                                                |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| [deploy.sh](deploy.sh)                     | Shell entry point for the Python installer                                    |
| [deploy.py](deploy.py)                     | Preflight, generated files, links, recoverable backups, Codex hook merge      |
| [test_deploy.py](test_deploy.py)           | Isolated installations, conflicts, migration, identity validation             |
| [test_hooks.py](test_hooks.py)             | Actual formatting, diagram compilation, payload contracts, visible failures   |
| [test_evaluations.py](test_evaluations.py) | Raw trial assets retain their recorded hashes and every trial remains indexed |
| [check_diagrams.py](check_diagrams.py)     | Repository-wide Mermaid gate using the bundled skill checker                  |
| [verify.sh](verify.sh)                     | Installed-state check, all tests, repository formatting, diagram validation   |

Use `--tool codex` or `--tool antigravity` for one host. Unselected host configuration does not participate in generation or validation. Use `--target-home <temporary-home>` to exercise installation without changing the real home. Codex also accepts `--codex-home` and `CODEX_HOME`. The verification runner forwards these installer selection and target flags to its installed-state check; the source behavior suite, formatting, and diagram checks still run.

For example, install and verify Antigravity without requiring a Codex installation:

```bash
./scripts/deploy.sh --tool antigravity
./scripts/verify.sh --tool antigravity
```

## 2. Focused checks

```bash
./scripts/deploy.sh --check
npm test
npm run format:check
python3 skills/mermaid-architect/scripts/verify-markdown.py README.md
```

The Mermaid helper returns `0` for verified diagrams or no fences, `1` for invalid syntax, and `2` when verification cannot run. The hook translates checker failures into host feedback. No checker downloads dependencies while running.

## 3. Verification strategy

| Workflow                             | Required observable result                                                                   | Evidence                                                                                                        |
| ------------------------------------ | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Install on another Mac               | Correct links and generated files; recoverable unknown files                                 | Isolated homes and checkouts with spaces/apostrophes                                                            |
| Install only one host                | Unselected host templates and rule restrictions do not block deployment                      | Native Antigravity manual/model rules and unrelated invalid template cases                                      |
| Start hooks from a GUI environment   | Provisioned Python and Node are found before checks run                                      | Generated Codex command and all three installed Antigravity commands under a restricted PATH                    |
| Adopt Codex hook configuration       | Owned handler updates once; unrelated handlers/settings survive                              | Merge, backup, malformed-schema, and repeat tests                                                               |
| Edit through a supported host tool   | Actual resulting file is formatted                                                           | Real Prettier calls through both payload adapters                                                               |
| Project-specific formatting          | Project configuration governs output                                                         | Isolated project configuration test                                                                             |
| Write invalid Markdown diagrams      | Host receives a failure                                                                      | Real Mermaid compilation with valid and invalid sources                                                         |
| Missing tooling or malformed payload | Failed check with diagnostics                                                                | Controlled unavailable dependencies and malformed input                                                         |
| Invoke bundled helper elsewhere      | Works outside repository cwd; no temporary files remain                                      | Raw diagram compilation from an isolated directory                                                              |
| Use a writing skill alone            | Requested structure and content survive                                                      | Fresh agents with only the skill and fixture; [evaluation record](../SKILL-EVALUATION.md)                       |
| Use an interview skill across turns  | Questions adapt to answers; research, corrections, constraints, and stopping govern the plan | Fresh agents, controlled user replies, and a live research case; [discovery record](../DISCOVERY-EVALUATION.md) |
| Preserve trial evidence              | Historical snapshots, inputs, and outputs retain recorded bytes                              | Archive manifest completeness and checksum test                                                                 |
| Native event delivery                | Host actually fires and surfaces the configured hook                                         | Manual native tool event; JSON contract tests alone are insufficient                                            |

Run `verify.sh` after deployment, hook, helper, or metadata changes. Run independent skill trials after changing a skill's output contract, structure, preservation rules, or routing boundary. Pure wording fixes need proportionate inspection.

Trials use isolated skill copies and task fixtures. Do not provide the desired answer or reviewer rubric to the producing agent. Inspect outputs for facts, uncertainty, protected assets, task format, and the behavior being changed. Keep input, skill snapshot, raw output, and verdict so the result is reviewable.

For interactive workflows, supply one user answer per turn and retain every prompt and response. Test a correction and a request to stop, and distinguish live tool execution from offline simulation. Register new archive folders in `test_evaluations.py`; each folder's manifest hashes the original skill, task, output, and additional evidence. The archive check preserves historical bytes; it does not rerun model behavior or require old snapshots to match current skills.

The automated suite does not prove all hosts fire hooks or all model runs follow a skill. Codex native shell delivery was observed after the missing checker was repaired. Native Codex patch delivery was also exercised with an actually formatted valid document and feedback from an invalid diagram. Antigravity event delivery remains unverified; Gemini and Claude hook execution is outside the maintained adapter scope.

## 4. Maintaining the checks

Retain installation tests that establish preflight and backup behavior. Extend tests when a host schema or supported tool changes. Fix source defects before changing expectations. Use real tooling for critical effects; use controlled failures to establish error reporting.

Record unresolved runtime gaps explicitly. Repository formatting and generated-state checks do not substitute for native trust review or independent skill-output inspection.

Return to the [repository overview](../README.md).
