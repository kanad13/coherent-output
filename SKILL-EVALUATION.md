# Document progression and reliability: evaluation record

Date: 11 October 2026. Branch: `repo-audit`, created from local `main` at `7216341`.

This record describes the writing and host-check implementation committed as `b73c440`. Subsequent interview and painter-analogy work is recorded in the [discovery evaluation](DISCOVERY-EVALUATION.md); the counts and raw trial snapshots below remain historical evidence.

The new [progressive-documentation skill](skills/progressive-documentation/SKILL.md) builds a reader's understanding in successive passes. The opening explains the whole subject and the roles of its main parts. Later sections connect those parts through mechanisms, consequences, choices, and exact detail. The implementation also repairs hook failures and aligns writing guidance across the library.

The independent trials support this approach on the tested tasks. They also exposed an integration failure: an exact table changed after a native file write. Fresh cognitive and Mermaid trials pass after their skills gained saved-file verification and concrete preservation paths. Automated checks pass, and native Codex patch delivery has been exercised. Live Antigravity event delivery and another Mac remain unverified.

## 1. The writing intent and skill decision

The reader should have a coherent, useful understanding at every depth. An early pass establishes the main picture; each return adds a mechanism, relationship, consequence, or decision. This gives readers context for details and lets them stop early with an accurate model. The introduction must explain relationships rather than list future headings.

The skill also keeps important limits early, introduces terms before reasoning depends on them, uses examples when helpful, and preserves facts and uncertainty. Procedures retain executable order. Chronology, lookup references, required templates, and short answers retain their appropriate structures. These safeguards prevent a preferred explanatory style from distorting other artifacts.

A separate skill is worthwhile because it changes document-wide sequencing. Cognitive-clarity-refactor has a different contract: dense prose becomes a strict two-tier bullet hierarchy. That contract remains useful. The two skills can cooperate when both transformations apply. This recommendation agrees with Google's guidance to outline large documents and progressively introduce detail; it is a design judgment, not a measured claim that one structure suits every reader. [Google technical writing](https://developers.google.com/tech-writing/two/large-docs)

## 2. Policy and installation choices

The canonical [authoring contract](skills/README.md#2-skill-authoring-contract) now specifies:

- Selected STE100 and Google developer-documentation principles as plain-language guidance.
- A Gunning Fog aim near 10 as an informal diagnostic, with no unsupported score or compliance claim.
- Artifact-specific structure and short local guidance inside independently installed writing skills.
- Explicit required and optional sibling dependencies, with unavailable steps reported.
- Behavior trials using fresh agents, isolated skill snapshots, task fixtures, and inspected outputs.

Notes and tutorials gain whole-picture sequencing. Emails retain three candidate drafts, recipient tone, and firm versus tentative commitments. Articulation reviews retain their alternatives and source passages. Repository synchronization uses appropriate document structure and respects the authorized Git scope.

The personal installer remains the right route for this library's multi-Mac setup. The documented Skills CLI route serves selective project consumers without duplicating a universal installer. Skills installation does not install global instructions or hooks. The [original audit](REPO-AUDIT.md) contains the repository comparisons and primary sources; its findings describe the pre-repair baseline.

## 3. Independent writing trials

Each producing agent started with `fork_turns: none` and received only a skill snapshot, task material, an output path, and isolation constraints. It was not given the intended answer or reviewer rubric. Agents shared the available model/runtime; this is not a cross-model benchmark. Source facts, numerical limits, uncertainty, protected assets, output shape, and progression were checked after writing.

The [retained fixtures](evaluations/writing/README.md) contain the actual skill snapshots, task text, and saved outputs as plain text. These raw records are not reformatted by repository tooling.

| Case                                                                          | Skill                           | Observed result                                                                                                                                       |
| ----------------------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [System guide](evaluations/writing/system-guide/output.txt)                   | Progressive documentation       | Pass: 813-word explanation introduces the complete event path, then interactions and operational limits                                               |
| [Archive rewrite](evaluations/writing/restructure/output.txt)                 | Progressive documentation       | Pass: 657 words; source facts, exact command, and exact table retained                                                                                |
| [Boundaries](evaluations/writing/boundaries/output.txt)                       | Progressive documentation       | Pass: warning and ordered procedure retained; short answer stays below 60 words; lookup categories retained                                           |
| [Conversation notes](evaluations/writing/conversation/output.txt)             | Conversation notes              | Pass: comprehensive notes retain decisions, rejected options, local evidence, unknowns, and release conditions                                        |
| [Email](evaluations/writing/email/output.txt)                                 | Email rewrite                   | Pass: each of three drafts retains every substantive fact, commitment, condition, owner, and uncertainty                                              |
| [Tutorial](evaluations/writing/tutor/output.txt)                              | Concept tutor                   | Pass: 507 words; whole path precedes mechanisms; hypothesis is assessed without an invented timing claim                                              |
| [Initial cognitive rewrite](evaluations/writing/cognitive/output.txt)         | Cognitive clarity refactor      | Failed exact-table preservation; command and substantive facts retained                                                                               |
| [Corrective cognitive trial](evaluations/writing/cognitive-rerun/output.txt)  | Cognitive clarity refactor      | Pass: saved command and ownership table match byte-for-byte; required hierarchy and facts retained                                                    |
| [Articulation review](evaluations/writing/articulation/output.txt)            | Articulation review             | Drafting passes; unavailable evaluator disclosed only in commentary. Final disclosure was clarified and retested                                      |
| [Final progressive rewrite](evaluations/writing/progressive-final/output.txt) | Final progressive documentation | Pass: 676 words; increasing depth and all facts retained; saved command and table match byte-for-byte                                                 |
| [Dependency boundary](evaluations/writing/evergreen/output.txt)               | Repository evergreen sync       | Pass: scoped correction and meaningful test recommendation; unavailable test-strategist, unrun checks, and Git scope reported                         |
| [Final articulation trial](evaluations/writing/articulation-final/output.txt) | Final articulation review       | Pass: three unresolved alternatives per concern; source preserved; completion report names the unavailable evaluator and unperformed workflow         |
| [Final Mermaid insertion](evaluations/writing/mermaid-final/output.txt)       | Mermaid architect               | Pass: detected native formatting drift, restored and verified the baseline, then delivered one compiled diagram with all 675 original bytes preserved |

### What the failure established

The initial cognitive agent submitted the original table in its successful `apply_patch` call. The saved table had expanded padding and separators. It did not invoke a formatter and initially checked its submitted edit rather than the saved file.

The shared hook's real formatter reproduces that change. The structural skills now require comparison after hooks or other post-processing. Where extra comments are allowed, a Prettier block-ignore comment protects an exact Markdown asset. A non-mutating delivery path or an explicit conflict report is required when the artifact prohibits such comments. The automated hook test verifies actual block protection, and the fresh cognitive trial verifies exact saved content.

The failed output remains in the record. A successful corrective sample does not guarantee every future agent run will follow the skill.

The independent reviewer found the same gap in Mermaid's insertion-only contract. Its revised workflow now checks the saved document with recorded insertions removed. Unlike the structural writing skills, Mermaid permits only a caption and diagram fence, so ignore comments would violate its payload contract. In the fresh trial, native patch application changed existing headings and a table. The agent detected that drift, verified restoration of the baseline, and delivered the candidate through a byte-preserving write. Removing its one insertion reproduces all 675 original bytes. Both the agent and an independent rerun compiled the final diagram successfully; the [completion report](evaluations/writing/mermaid-final/completion.txt) records the actual checks.

## 4. Hook and installer repairs

Host input schemas remain separate. Shared document checking formats supported paths, respects project configuration and ignore files, validates diagrams, and returns visible failures. Runtime checks use provisioned dependencies rather than downloading packages during an edit.

The installer owns the previously orphaned Codex checker registration while preserving unrelated hooks and settings. Merged hook files are isolated by Codex home so an installation test cannot overwrite another home's personal hooks. Conflicting originals receive recoverable backups. Native hook trust state is untouched.

Generated commands can start with restricted GUI runtime paths: Codex uses the installer's absolute Python executable, and shell launchers add standard user and Homebrew directories before finding Python. Antigravity-only deployment accepts native manual/model rules without applying Codex composition restrictions. Codex-only deployment does not parse Antigravity templates. The verification runner accepts the same host selection as deployment.

Prettier and Mermaid CLI are pinned with a lockfile. Browser provisioning is explicit. Invalid diagrams differ from unavailable renderers or browsers. Helpers work outside the source checkout and remove temporary files. The Antigravity command gate covers additional common destructive forms and malformed input, while remaining a pattern check rather than a security boundary.

An independent reviewer reproduced configuration loss, ignored project formatting, ignore-file failures, mutation after failed tool events, incorrect missing-browser status, restricted-PATH failures, and coupling between host selections. The fixes have regression coverage. The final bootstrap and host-selection repairs pass direct checks; an additional independent follow-up could not complete because of a usage limit.

## 5. Verification and practical limits

| Check                                                            | Result                                                                                                                                                    |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clean dependency provisioning with `npm ci --no-audit --no-fund` | Passed from the tracked manifest and lockfile                                                                                                             |
| Isolated deployment, real checker, and retained-evidence suite   | 37 tests pass                                                                                                                                             |
| Installed Antigravity commands                                   | Isolated Antigravity-only deployment: safety feedback, actual formatting, and valid/invalid diagram feedback pass under a restricted GUI PATH             |
| Staged-source Antigravity installation                           | Materialized staged files into a separate checkout, provisioned with npm ci, installed to an isolated home, and passed the full 37-test verification gate |
| Codex bootstrap and host selection                               | Generated Codex command starts without Python on PATH; each host ignores unselected configuration constraints                                             |
| Native Codex valid patch                                         | Saved heading actually formatted; Mermaid compiled successfully                                                                                           |
| Native Codex bootstrap patch                                     | After deployment of the absolute Python command, a native patch actually formats its heading and accepts a valid diagram                                  |
| Native Codex invalid patch                                       | PostToolUse returned parse-error feedback; nested tool promise rejected after the file was written                                                        |
| Codex migration                                                  | Installed mapping and repeat check pass; unrelated-state preservation and recoverable backups pass in isolated tests                                      |
| Metadata, links, formatting, repository diagrams                 | Passed: 15 skill metadata checks, 88 active local links, formatting, and diagram scanning across 23 Markdown files                                        |

The native invalid-patch result demonstrates feedback delivery, not rollback: the edit had already occurred. That behavior matches the [Codex PostToolUse contract](https://learn.chatgpt.com/docs/hooks).

Antigravity payload contracts are exercised through real scripts and tooling, but live Antigravity event delivery has not been observed. A second Mac has not been exercised. The selected-skill route was tested for project installation, not full Claude or Gemini skill execution. New or changed native hook entries still require the host's trust review.

No full ASD-STE100 assessment, measured Fog score, or universal skill-adherence claim is made.
