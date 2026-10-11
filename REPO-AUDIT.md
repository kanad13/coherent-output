# Coherent Output: repository audit and recommendations

Audit date: 11 October 2026. Baseline: local `main` at `7216341`. Working branch: `repo-audit`.

This is the original investigation and decision record, captured before implementation. Its findings describe the baseline at `7216341`. The [repository overview](README.md) and [testing guide](scripts/README.md) describe the current implementation and verification requirements.

## 1. Direct answer

Keep the personal deployment script. Add a separate, documented route for people who want individual skills. The existing repository already works with the Vercel Skills installer; rebuilding that installer would add little value.

Repair hook ownership and verification before expanding automation. The existing verification command passes while an installed Codex hook points to a missing file. The Mermaid hook also converts checker failures into successful hook results.

Use a shared, short writing policy with task-specific instructions inside each writing skill. Invoke cognitive-clarity-refactor when the task needs its structural refactoring workflow. Making every writing task invoke that workflow would impose its Markdown layout on emails, explanations, and other formats.

## 2. What the repository does

Coherent Output is a personal agent configuration library. Git carries the source between Macs; each Mac runs a Python installer to connect local applications to its own checkout. The repository also contains 14 reusable instruction-based skills.

There are four distinct mechanisms:

| Mechanism               | Source                                                         | What happens                                                                                                                 |
| ----------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Persistent instructions | [AGENTS.md](AGENTS.md)                                         | Establish communication, workflow, autonomy, and skill-routing policies.                                                     |
| On-demand procedures    | [skills/](skills/README.md)                                    | The host discovers skill metadata; the agent activates a relevant procedure.                                                 |
| Conditional policies    | `rules/`                                                       | Antigravity can load rules by trigger. Codex receives composed prose conditions. There are currently **zero written rules**. |
| Executable automation   | [adapters/](adapters/README.md), [scripts/](scripts/README.md) | Deployment renders configuration; supported host events run hook commands. Skill helpers run when an agent calls them.       |

These mechanisms have different guarantees. A file on disk can be discoverable without its instructions being followed. A configured hook can run reliably without its checker reporting failures correctly.

### Deployment data flow

```text
Git checkout
  AGENTS.md + rules/*.md
    -> compose .generated/codex/AGENTS.md
    -> link ~/.codex/AGENTS.md

  skills/
    -> link ~/.agents/skills
    -> link ~/.gemini/config/skills

  AGENTS.md + rules/
    -> link ~/.gemini/AGENTS.md
    -> link ~/.gemini/config/rules

  Antigravity hook template + local checkout paths
    -> render .generated/antigravity/hooks.json
    -> link ~/.gemini/config/hooks.json
    -> host event -> shell wrapper -> checker
```

[deploy.sh](scripts/deploy.sh) resolves the checkout from its own location and invokes [deploy.py](scripts/deploy.py). The Python installer:

1. Reads the adapter manifests and selects `all`, `codex`, or `antigravity`.
2. Composes Codex instructions and renders shell-quoted Antigravity commands.
3. Checks source availability, nonempty skill names/descriptions, duplicate names, and destination conflicts.
4. Supports read-only previews and installation checks.
5. Writes generated files atomically and replaces managed links.
6. Preserves unknown conflicting destinations when `--backup-conflicts` is selected.
7. Removes a redundant repository discovery link when the same library is already installed globally.

Useful existing safeguards include conflict preflight, recoverable backups, custom target homes, support for checkout paths with spaces/apostrophes, and repeat-install stability.

The installer owns six application links and two generated files. It **does not own or inspect Codex hooks**. Neither deployment nor verification is a background synchronization service; the user or agent must run the scripts.

### Skill inventory and relationships

| Skill                      | Intended outcome                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| commit-scribe              | Verify, stage, create a structured commit, and push upstream.                                                      |
| repo-evergreen-sync        | Reconcile code, documentation, contracts, and tests after coding. Calls test-strategist and commit-scribe.         |
| markdown-audit             | Inspect documentation structure, indexes, names, and links.                                                        |
| project-scaffolding        | Establish working project foundations and records that support later sessions.                                     |
| test-strategist            | Map user workflows to appropriate verification and maintain the testing strategy.                                  |
| claim-validator            | Test factual claims and expose assumptions and contradictory evidence.                                             |
| worth-the-squeeze          | Compare engineering value with implementation and maintenance cost.                                                |
| web-research               | Research external facts and contracts with source attribution.                                                     |
| articulation-review        | Propose alternatives for confusing passages and apply selected wording. Calls writing and value-assessment skills. |
| cognitive-clarity-refactor | Preserve meaning while converting dense prose to its specified Markdown hierarchy.                                 |
| conversation-notes         | Produce comprehensive, standalone notes from a conversation.                                                       |
| email-rewrite              | Preserve facts and commitments while producing three correspondence drafts.                                        |
| concept-tutor              | Explain technical concepts in a learning sequence. Refers to cognitive-clarity-refactor.                           |
| mermaid-architect          | Insert diagrams while protecting existing content and verify diagrams with bundled helpers.                        |

Only mermaid-architect currently bundles skill helper code: [verify-markdown.py](skills/mermaid-architect/scripts/verify-markdown.py) and [verify-mmdc.sh](skills/mermaid-architect/scripts/verify-mmdc.sh). The remaining skills primarily instruct the model.

Skill references are procedure dependencies, not automatic software dependencies. For example, installing only repo-evergreen-sync does not automatically install its named sibling skills. Its Git-finalization instructions also need to remain within the user's authorized task; a reference to commit-scribe does not authorize an otherwise unrequested push.

## 3. Investigation 1: how other repositories install across agents

### The common mechanisms

A skill is a folder containing `SKILL.md` with metadata and instructions, plus optional resources. Installing usually puts that folder where the target host discovers it. The agent then loads the procedure when relevant. The open format defines packaging and progressive loading; it does not provide a universal execution engine. [Agent Skills specification](https://agentskills.io/specification)

The installation commands in popular repositories fall into several categories:

| Example                                                                                                                                 | Documented route                                                 | What to learn from the example                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) and [vercel-labs/skills](https://github.com/vercel-labs/skills) | `npx skills add <owner/repo>`                                    | One installer discovers folders and places selected skills in host discovery locations.                                                                |
| [anthropics/skills](https://github.com/anthropics/skills)                                                                               | Claude plugin marketplace registration, then plugin installation | A native package groups selected skills. A bare skills folder and a plugin package are different distribution units.                                   |
| [obra/superpowers](https://github.com/obra/superpowers)                                                                                 | Host-specific plugin/extension installation                      | One source library can have several native packaging adapters. The repository documents a Gemini extension and native Codex/Claude/Antigravity routes. |
| [affaan-m/ECC](https://github.com/affaan-m/ECC)                                                                                         | Installer targets, profiles, and optional hook runtime           | Repositories containing rules, agents, and hooks often retain a custom installer. Skill-only installation is insufficient for their full setup.        |

These are documented publisher workflows, not claims that every advertised integration was exercised during this audit.

### Discovery and hooks are host-specific

| Host                  | Relevant local skill discovery                                                            | Hook/configuration distinction                                                        |
| --------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Codex                 | User `~/.agents/skills`; project `.agents/skills`. Symlinked skill folders are supported. | Uses its own hook schema and trust flow.                                              |
| Claude Code           | User `~/.claude/skills`; project `.claude/skills`; plugin skill folders.                  | Native plugin packaging can carry additional components.                              |
| Gemini CLI            | User/workspace `.gemini/skills` and `.agents/skills` aliases.                             | Hooks use `BeforeTool`/`AfterTool` in `settings.json`, with `tool_input` payloads.    |
| Antigravity 2.0 / IDE | Global `~/.gemini/config/skills`; workspace `.agents/skills`.                             | Hooks use `PreToolUse`/`PostToolUse`, named hook configurations, and `toolCall.args`. |
| Antigravity CLI       | Global `~/.gemini/antigravity-cli/skills`, workspace `.agents/skills`, and plugin skills. | A distinct product from Gemini CLI and from the Antigravity IDE.                      |

Sources: [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills), [Gemini skills](https://geminicli.com/docs/cli/skills/), [Gemini hooks](https://geminicli.com/docs/hooks/reference/), [Antigravity skills](https://antigravity.google/docs/skills), [Antigravity hooks](https://antigravity.google/docs/hooks).

The repo's existing Antigravity paths match the documented 2.0/IDE locations. Calling that adapter a Gemini CLI adapter would be inaccurate. The existing `~/.agents/skills` installation can independently make skills available to Gemini CLI, but it does not install Gemini CLI's global instructions or hooks.

### What was tested

Using **Skills CLI 1.7.2**, in temporary directories:

- Listing the local checkout discovered all 14 skills.
- Listing `kanad13/coherent-output` from GitHub discovered all 14 skills.
- Installing cognitive-clarity-refactor and mermaid-architect for Codex, Claude Code, and Gemini CLI succeeded.
- The installer created real skill copies in the consumer's `.agents/skills`.
- Claude's entries were relative symlinks to those copies.
- The Mermaid helper was bundled.
- A `skills-lock.json` file recorded source information and hashes.
- The installer did not install the root `AGENTS.md`, adapters, or hooks.
- The canonical installed folder was a copy, not a live link to this checkout.

Representative command executed from a temporary consumer project:

```bash
npx --yes skills@1.7.2 add /path/to/coherent-output \
  --skill cognitive-clarity-refactor mermaid-architect \
  --agent codex claude-code gemini-cli --yes
```

The actual probe supplied the checkout's absolute path. No global skill installation was performed.

A proposed public-facing command can therefore be documented without a new installer:

```bash
# Inspect the catalog.
npx skills@1.7.2 add kanad13/coherent-output --list

# Install selected skills into the current project.
npx skills@1.7.2 add kanad13/coherent-output \
  --skill cognitive-clarity-refactor \
  --agent codex claude-code gemini-cli
```

Pinning the CLI makes these examples reproducible. Revalidate the documented version when updating it.

### Is the existing method better?

| Dimension             | Existing deploy.sh                                                              | Common Skills CLI route                                                                |
| --------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Personal editing loop | Live links expose checkout edits immediately.                                   | Copies provide a separate consumer snapshot.                                           |
| Components            | Installs the personal instructions, rules, skills, and Antigravity hook config. | Installs skill folders and their bundled resources.                                    |
| Selection             | Installs the whole library for a selected adapter.                              | Selects individual skills and agents.                                                  |
| Supported hosts       | Two explicitly maintained adapters.                                             | Broad installer-supported host mapping.                                                |
| Conflict behavior     | Preflight and recoverable backups.                                              | Installer-specific behavior; evaluate in isolation before mixing installation schemes. |
| Dependency scope      | Python deployment; Node tooling for formatting/diagrams.                        | Node/npm to run the installer; helper runtime dependencies remain separate.            |
| Update model          | Git pull updates linked source; deploy refreshes generated files.               | Explicit installer updates refresh copied skills.                                      |

**Opinion:** retain both routes. The personal installer fits your multi-Mac workflow. The portable route fits other users and projects. Neither dominates the other because they install different scopes.

The whole-directory link `~/.agents/skills -> <repo>/skills` gives this checkout ownership of that entire catalog. Another global installer writing through that path can alter the source checkout. This is a filesystem consequence, not a tested global mutation. Avoid mixing global schemes until coexistence is explicitly supported; project-local consumer installs are the safer comparison surface.

For public reuse, document skill dependencies and add a chosen repository license. A license decision belongs to the owner. Native plugins become worthwhile when you need to distribute hooks or other host features with the skills. Building several plugin adapters immediately would expand maintenance before repairing current runtime gaps.

## 4. Investigation 2: scripts and hooks

### What existing verification actually proves

[verify.sh](scripts/verify.sh) runs:

1. `deploy.py --check`: registered link and generated-content health.
2. `test_deploy.py`: nine isolated deployment tests.
3. `npx prettier --check`: source formatting.

The full command returned **exit 0**, with **9 tests passing** and formatting passing. It does not prove hook invocation inside either app, complete skill metadata validity, Mermaid compilation across the library, or adherence to a skill's semantic procedure.

### Findings and reproductions

| ID  | Finding                                                           | Evidence and impact                                                                                                                                                                                                                                                 | Priority |
| --- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| H01 | Installed Codex hook points to a missing checker.                 | `~/.codex/hooks.json` has a PostToolUse handler for Bash/apply_patch/Edit/Write invoking `adapters/shared/document-check.py --host codex`. That file is absent, and the Codex adapter does not manage hooks. Shell-tool calls surfaced this error during the audit. | First    |
| H02 | Mermaid wrapper discards checker failure.                         | [mermaid-validate.sh](adapters/antigravity/hooks/scripts/mermaid-validate.sh), line 36 in the baseline, ignores checker errors and then emits `{}`. A controlled verifier exiting 7 produced wrapper exit 0.                                                        | First    |
| H03 | Missing Mermaid dependency reports success.                       | [verify-markdown.py](skills/mermaid-architect/scripts/verify-markdown.py) returns 0 when npx is unavailable. An isolated probe reproduced the skip-success result.                                                                                                  | First    |
| H04 | Formatter test asserts the response, not the formatted file.      | [test_deploy.py](scripts/test_deploy.py), lines 126–139, checks exit code and `{}`. A formatter that does nothing can satisfy those assertions.                                                                                                                     | High     |
| H05 | File hooks cover only two tool names.                             | The template matches write_to_file and replace_file_content. Shell-created changes are outside those matchers. Hook coverage does not mean every filesystem write is covered.                                                                                       | High     |
| H06 | Command detector has a narrow pattern set.                        | It asks for `git reset --hard` and `rm -rf /example`, but returns allow for relative paths, split flags, long flags, and malformed JSON.                                                                                                                            | High     |
| H07 | Host payloads cannot be reused directly.                          | A valid Antigravity payload formatted a sample file. A Codex-shaped payload left the same file unchanged and still returned success. This is expected for the current host-specific wrapper, but prevents direct reuse.                                             | High     |
| H08 | Dependencies are floating and failures are hidden.                | npx invocations do not pin Prettier/Mermaid CLI in tracked package metadata. Formatting discards errors; diagram wrappers hide failure status. Cold-start downloads may exceed hook timeouts; that timing risk was not measured.                                    | Medium   |
| H09 | Installer metadata checks are weaker than the authoring contract. | In an isolated copy, `name: INVALID_NAME` plus a 1,100-character description passed deployment dry-run. The installer checks presence/uniqueness, not all format constraints.                                                                                       | Medium   |
| H10 | Diagram preview helper leaves an extra temporary file.            | `OUTPUT_FILE="$(mktemp).svg"` creates a base file, then cleans only the suffixed SVG. Early exits also bypass cleanup.                                                                                                                                              | Low      |

The dangerous command samples in H06 were passed as JSON data to the detector. They were never executed.

| Input to safety-gate.sh           | Observed decision |
| --------------------------------- | ----------------- |
| `pwd`                             | allow             |
| `git reset --hard`                | force_ask         |
| `git push origin --force`         | force_ask         |
| `rm -rf /example`                 | force_ask         |
| `rm -rf ./example`                | allow             |
| `rm -r -f /example`               | allow             |
| `rm --recursive --force /example` | allow             |
| Malformed JSON                    | allow             |

This detector is a limited warning mechanism. Expanding a regex does not create complete shell-command enforcement. Keep native approval and sandbox policy as the primary boundary.

### Documented contracts versus observed behavior

The Antigravity template's location, named configuration shape, payload fields, and force_ask response match the current documentation. The problem is not an unsupported hook format. It is incomplete coverage and suppressed failures.

Codex currently supports lifecycle hooks, user/project hook files, and trust review. Shell calls match Bash; patch calls can match apply_patch/Edit/Write. Its contract differs from Antigravity's. [Codex hooks](https://learn.chatgpt.com/docs/hooks)

A PostToolUse checker operates after the write. Detecting an error cannot retroactively prevent the file from being written. The [adapter documentation](adapters/README.md) currently overstates both failure propagation and prevention. Describe detection, feedback, and repair separately.

The [skill authoring guide](skills/README.md) also says explicit invocation deterministically forces playbook execution. Invocation can select/load a procedure; it does not guarantee that every model-directed step or helper call occurs. Reliable checks need executable assertions on the resulting behavior.

### Recommended implementation boundary

1. Make Codex hook ownership explicit. Either replace the orphan entry with an installer-managed checker, or remove that specific obsolete entry if the behavior is no longer required. Preserve unrelated user hooks. Establish the entry's origin before migration; this audit did not determine who created it.
2. Separate each host's input/output adapter from the document-checking logic. Normalize the path and requested checks, then run shared checks. Reuse logic, not host-specific JSON.
3. Return a distinct failed/skipped result when a required checker cannot run. Keep stdout compliant with each host's contract and send diagnostics to stderr or the supported feedback field.
4. Assert observable effects: resulting file content, invalid-diagram detection, dependency failure, and bounded runtime.
5. Pin formatting/diagram dependencies. Prefer project tooling where appropriate; make fallback tooling explicit.
6. Use hooks for timely feedback and a standalone check/continuous integration gate for completion requirements.
7. Keep skill helpers in their own bundles and resolve paths from the loaded skill directory.

A shared checker plus thin adapters is a bounded consolidation. A generic hook framework or a full shell parser would impose disproportionate maintenance.

### Verification strategy to carry into implementation

The canonical command remains `scripts/verify.sh`, documented in the root README and scripts README. Extend those instructions with this workflow map when repairs are implemented:

| Workflow                 | Required evidence                                                      | Appropriate check                                                               |
| ------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| New Mac deployment       | Correct links, generated files, and preserved unknown settings         | Existing isolated installer tests plus Codex hook migration cases               |
| Formatter on an edit     | File contents become the expected format                               | File assertion with a controlled executable and one real formatter smoke test   |
| Invalid Mermaid document | Error is observable and never reported as verified                     | Valid/invalid fixtures, dependency-unavailable case, wrapper propagation test   |
| Supported app event      | Intended hook actually fires with the app's payload                    | One disposable-file workflow per supported host, recording event/result         |
| Skill-only installation  | Selected folder and resources load without repo-global files           | Isolated installer smoke test and a fresh host-session invocation               |
| Skill metadata           | Invalid names, lengths, or required dependencies are rejected/reported | Specification-aware validation                                                  |
| Hook coverage            | Known bypass surfaces are documented                                   | Matchers, tool paths, and shell-based writes reviewed against host capabilities |

Keep passed unit/integration checks separate from pending host-runtime checks. An actual Antigravity event was not triggered during this audit.

## 5. Investigation 3: writing-standard drift

### What has drifted

The updated [cognitive-clarity-refactor](skills/cognitive-clarity-refactor/SKILL.md) combines selected STE100 structural principles, Google developer-documentation guidance, and a Fog ~10 readability aim.

| Location                                                               | Current policy                                                           | Recommended treatment                                                                              |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md), communication section                          | Names STE100 alone                                                       | State a short shared plain-language baseline and define when structural refactoring applies.       |
| [skills/README.md](skills/README.md), authoring guidance and inventory | Requires STE100-compliant instructions; repeats STE100-only descriptions | Make this the canonical authoring/style contract; update descriptions where their promise changes. |
| [conversation-notes](skills/conversation-notes/SKILL.md)               | STE100-only drafting and completeness checks                             | Use the shared policy while preserving comprehensive-note requirements.                            |
| [email-rewrite](skills/email-rewrite/SKILL.md)                         | STE100-only candidate drafts                                             | Use the shared policy; retain recipient tone, diplomatic hedging, and three distinct approaches.   |
| [concept-tutor](skills/concept-tutor/SKILL.md)                         | STE100-only prose mandate plus a structural skill reference              | Use the shared policy; choose structure that supports learning.                                    |
| [repo-evergreen-sync](skills/repo-evergreen-sync/SKILL.md)             | STE100-only documentation rules and mandatory bullet hierarchy           | Align prose policy. Preserve language-specific code/docstring conventions.                         |
| [articulation-review](skills/articulation-review/SKILL.md)             | Refers to cognitive-clarity-refactor mainly for layout                   | Clarify whether the dependency means the full workflow or only writing principles.                 |
| [README.md](README.md), architecture explanation                       | Presents STE100 as the universal communication standard                  | Align the explanation with the chosen baseline.                                                    |

This is primarily **policy-description drift**. Many existing instructions already agree with active voice, clear terms, and low complexity. Missing the words Google or Fog does not by itself prove worse output. Replace conflicting or overstated requirements; avoid a mechanical name substitution across every file.

Google-style Python docstrings in repo-evergreen-sync are a separate code-documentation convention. They are not stale references to the Google prose style guide.

### Why cognitive-clarity-refactor should not become every writer's parent workflow

That skill performs a specific transformation: strict two-tier Markdown, bold category anchors, one-assertion child bullets, decision tables, protected assets, and chunked assembly. An email, tutorial, skill instruction, or concise chat answer may need another structure.

There is also a packaging issue. The selective installation probe carried only the requested skill folders. Sibling skill references do not make their content available automatically. A bare instruction to use cognitive-clarity-refactor can become an unresolved dependency for someone who installed only email-rewrite.

**Recommended split:**

- **Shared policy:** clarity, accuracy, voice, vocabulary, readability, and preservation.
- **Task workflow:** the skill's own procedure and output contract.
- **Optional structural transformation:** cognitive-clarity-refactor when dense Markdown requires that transformation.

For this 14-skill library, a compact local baseline in affected writing skills is proportionate. Keep the canonical policy in skills/README.md and require maintainers to review all its consumers when it changes. The duplication is limited and intentional; the full refactoring workflow stays centralized.

If the library grows enough that this maintenance step repeatedly fails, generate bundled local reference files from one canonical policy. Defer that build system until there is evidence that the smaller approach is insufficient. A cross-skill filesystem link would fail selective packaging.

### Calibrate the standards before propagating them

**STE100:** Describe the repository's policy as STE100-inspired plain language unless full conformance is actually assessed. The full standard includes controlled vocabulary and writing rules, not just active voice and short sentences. The primary site's indexed description establishes that distinction; its full PDF could not be fetched during this audit. [ASD explanation](https://www.asd-ste100.org/about.html)

**Google guidance:** Clear pronouns are acceptable; repeating the entity on every mention is unnecessary. The current cognitive skill's “explicitly name ... on every mention” sentence is stronger than its useful “avoid unanchored pronouns” rule. Google also advises against choppy writing and supports natural, approachable prose. Adopt selected principles and label project-specific constraints as such. [Google pronouns](https://developers.google.com/style/pronouns), [Google tone](https://developers.google.com/style/tone)

**Fog ~10:** The skill names a target but provides no calculator, sampling procedure, or measured acceptance check. Treat the value as an informal readability aim. If measuring it, define how prose is sampled and how code, identifiers, tables, and fragments are handled. Use the score as a diagnostic, not proof of comprehension or a mandatory hook threshold. Readability formulas do not assess audience, purpose, or all factors in effective communication. [CDC on readability formulas](https://www.cdc.gov/ccindex/tool/index-different.html)

**Formatting:** The two-tier bullet layout is this repository's chosen transformation format. It is not a requirement imposed by all three external standards. Choose paragraphs, steps, lists, and tables according to the artifact. [Google lists](https://developers.google.com/style/lists)

### Proposed lightweight policy

This is proposed wording, not an applied edit:

> Write for the intended reader. Use direct verbs, active voice, familiar words, and short sentences with clear references. Define unfamiliar terms on first use and use consistent names. Preserve facts, conditions, uncertainty, and necessary technical vocabulary. Apply selected STE100 and Google developer-documentation principles without imposing a single layout on every artifact. Aim for readable technical prose; use Fog scores only as a diagnostic when measured. Use cognitive-clarity-refactor when dense Markdown needs its structural transformation.

Each writing skill should add only its necessary local constraints. Email-rewrite needs recipient tone and commitment preservation. Conversation-notes needs completeness. Concept-tutor needs explanatory sequencing. The shared policy should not erase those differences.

## 6. Proposed central authoring and maintenance contract

Update the existing authoring guide rather than adding another skill solely to govern this small library. Keep a short pointer in AGENTS.md so maintainers can discover it.

The revised contract should require:

1. **Outcome and boundaries:** Define the artifact, preservation rules, success criteria, and exclusions.
2. **Accurate metadata:** Validate naming, directory match, description length, and routing language. The open format allows optional fields; “exactly name and description” is a local restriction, not the full specification.
3. **Portable bundles:** Keep necessary resources inside the skill folder. Test installation of one skill without the repository's global instructions.
4. **Explicit dependencies:** Classify sibling procedures as required or optional. State what to do if they are unavailable. A name reference is not automatic installation or execution.
5. **Shared writing policy:** Identify prose-policy consumers and update affected metadata, instructions, and examples together.
6. **Artifact-appropriate structure:** Keep layout requirements inside the skills that need them.
7. **Executable contracts:** Document helper arguments, dependencies, output, exit status, cleanup, and timeout. Resolve helpers from the skill directory.
8. **Host compatibility:** Record supported hosts, tested versions, hook locations, payload schemas, tool matchers, and native limitations.
9. **Evidence appropriate to the claim:** Metadata validation proves format; installer tests prove placement; app events prove hook firing; output review establishes procedure quality.
10. **Maintenance sequence:** Inspect the change and consumers, update authoring records and relevant catalogs, run deployment/verification where appropriate, then report remaining gaps. Commit/push only within the authorized workflow.

Include a small evaluation set for writing changes:

| Fixture                          | Acceptance criteria                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Dense technical passage          | Preserve entities, conditions, warnings, and uncertainty; improve navigation.                          |
| Business email                   | Preserve dates and commitments; keep exploratory options tentative; retain usable correspondence tone. |
| Technical explanation            | Explain prerequisites before abstractions; retain correct terminology; use suitable prose structure.   |
| Document with code/table/diagram | Preserve protected assets and substantive assertions.                                                  |
| Standalone skill install         | Instructions remain usable without an implicit global policy or missing sibling.                       |

These are proposed behavioral checks. No model-quality benchmark or numerical readability assessment was run in this audit.

## 7. “Is the juice worth the squeeze?” decision ledger

The underlying problem is reliable, portable agent behavior with a manageable maintenance burden. The proposed changes should address demonstrated failures and concrete distribution friction.

Effort estimates below are planning judgments, not measured implementation times.

| Candidate change                                              | Juice: concrete benefit                                        | Squeeze and risk                                                   | Verdict                | Bounded action                                                    |
| ------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------- | ----------------------------------------------------------------- |
| Document the existing portable install route                  | Verified compatibility; selective installation for three hosts | Low: examples, prerequisites, dependency/compatibility notes       | **STRONG PURSUE**      | Retain deploy.sh and add a skill-only route.                      |
| Replace deploy.sh with a custom universal installer           | Limited additional benefit over existing tools                 | High: host mapping, updates, conflicts, platform support           | **REJECT / SKIP**      | Use the established CLI for skill consumers.                      |
| Repair hook ownership and failure reporting                   | Removes a live missing-file failure and false-success results  | Moderate: schema adapters, migration, meaningful tests             | **SCOPED PURSUE**      | Manage the Codex entry and share only document-checking logic.    |
| Treat the command regex as complete enforcement               | No defensible completeness guarantee                           | High continuing maintenance; shell syntax bypasses                 | **REJECT / SKIP**      | Retain native controls and describe the detector's limited scope. |
| Make every writer invoke cognitive-clarity-refactor           | Centralizes some style wording                                 | Cross-skill dependency and inappropriate layout changes            | **COUNTER-PROPOSAL**   | Shared short policy plus task-local acceptance criteria.          |
| Align current writing consumers and authoring rules           | Resolves actual declared-policy drift                          | Low/moderate: bounded prose edits and representative output review | **STRONG PURSUE**      | Update affected consumers, preserving their artifact contracts.   |
| Introduce generated policy bundles or many native plugins now | Potential future consistency/distribution benefit              | Adds build artifacts, manifests, and host-specific maintenance     | **DEFER / ACCUMULATE** | Revisit after runtime repair and demonstrated consumer demand.    |

The supported scope is a small compatibility/documentation pass and a bounded hook repair. A new distribution framework is unnecessary.

### Sequenced action plan

1. **Runtime reliability:** Resolve the orphan Codex hook, preserve user settings, propagate checker failures, strengthen formatter assertions, and distinguish missing dependencies from successful checks.
2. **Portable distribution:** Document the tested CLI commands, standalone limitations, sibling dependencies, and chosen license. Decide later whether per-skill links are needed for global coexistence.
3. **Writing policy:** Revise AGENTS.md and skills/README.md, then update the identified writing consumers. Correct the cognitive skill's overly strong entity-repetition and unmeasured readability promises.
4. **Maintenance verification:** Add metadata and selected-install checks; document one real event workflow per supported hook host; optionally add continuous integration for the standalone completion checks.

## 8. Evidence and remaining uncertainty

| Claim/topic                                        | Evidence category            | Source                                                         | Confidence and limit                                              |
| -------------------------------------------------- | ---------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------- |
| 14 skills, zero written rules, six installed links | Verified local fact          | Source inventory, manifests, deployment check                  | High                                                              |
| Existing verification passes                       | Verified local fact          | verify.sh exit 0; nine tests; formatting result                | High for those checks only                                        |
| Portable packaging works                           | Verified local fact          | Skills 1.7.2 local install; GitHub listing                     | High for discovery/placement; host execution pending              |
| Codex checker is missing                           | Verified local fact          | Installed hooks.json, absent source, surfaced shell-tool error | High; origin of entry unknown                                     |
| Mermaid failure is suppressed                      | Verified local fact          | Controlled checker exit 7; wrapper exit 0 and empty JSON       | High for failure propagation                                      |
| Command detector misses listed inputs              | Verified local fact          | JSON-only safety-gate probes                                   | High; no destructive commands executed                            |
| Metadata validation is incomplete                  | Verified local fact          | Invalid-name/oversized-description isolated dry-run            | High                                                              |
| Shared format and progressive loading              | Documented primary contract  | [Agent Skills](https://agentskills.io/specification)           | High; not an execution guarantee                                  |
| Host discovery and hook dialects differ            | Documented primary contracts | Official host documentation linked in Section 3                | High for documentation; version-specific runtime proof incomplete |
| Other repositories' native distribution choices    | Publisher documentation      | Repository READMEs linked in Section 3                         | High for advertised workflows; integrations not audited           |
| Small policy plus local constraints is preferable  | Engineering inference        | Packaging probe and local output contracts                     | Moderate/high; validate through representative output review      |
| Fog scores alone do not establish clarity          | Primary-source guidance      | [CDC](https://www.cdc.gov/ccindex/tool/index-different.html)   | High for the general limitation                                   |

Local versions observed: Codex CLI 0.160.0, Antigravity CLI 1.2.14, Antigravity app 2.22.0, Antigravity IDE 2.5.5, and local Prettier 3.6.2. Gemini CLI and Claude runtime workflows were not executed.

All hook fixtures and consumer installations were isolated from the user's application configuration. No live Antigravity hook event, full Mermaid browser compilation, cross-Mac deployment, plugin installation, skill-quality benchmark, or full STE100 conformance audit was performed.

The initial shell-tool errors surfaced a missing **PostToolUse** handler. The installed configuration establishes the event type; those errors do not establish that the requested shell commands never ran. Subsequent audit commands used an independent process API and did not disable or change the configured hook.

Completion criteria met: branch created from local main; repository behavior mapped; all three investigations addressed with local probes and primary sources; alternatives evaluated; implementation boundaries and unresolved evidence stated.
