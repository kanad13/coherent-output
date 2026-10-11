# Tool Adapters

The adapters connect one shared library to host-specific directories and hook contracts. Installation manages links and generated configuration. Native applications decide when to discover skills, trust hooks, and fire tool events.

## 1. Installed mappings

`<repo>` is the absolute local checkout. Codex uses `CODEX_HOME` or `--codex-home` when supplied; the table shows defaults.

| Host            | Destination                   | Source                                         |
| --------------- | ----------------------------- | ---------------------------------------------- |
| Codex           | `~/.agents/skills`            | `<repo>/skills`                                |
| Codex           | `~/.codex/AGENTS.md`          | `<repo>/.generated/codex/AGENTS.md`            |
| Codex           | `~/.codex/hooks.json`         | `<repo>/.generated/codex/<home-id>/hooks.json` |
| Antigravity IDE | `~/.gemini/AGENTS.md`         | `<repo>/AGENTS.md`                             |
| Antigravity IDE | `~/.gemini/config/rules`      | `<repo>/rules`                                 |
| Antigravity IDE | `~/.gemini/config/skills`     | `<repo>/skills`                                |
| Antigravity IDE | `~/.gemini/config/hooks.json` | `<repo>/.generated/antigravity/hooks.json`     |

`<home-id>` is a stable hash of the Codex home. Merged user hooks use a separate generated file per destination, so testing a second home cannot overwrite the first home's settings.

Each host's `links.json` declares these mappings. Deployment renders shell-quoted absolute commands so paths with spaces or apostrophes work.

Select a host with `./scripts/deploy.sh --tool antigravity` or `--tool codex`. Only that host's artifacts are generated and validated; shared skill metadata is still checked. Provision dependencies with `npm ci` and use the same host flag with `./scripts/verify.sh`. A selected-skill install alone does not install these hooks or their repository-wide checker.

Codex composition supports `always_on` and `glob` rules. Glob rules receive a natural-language condition, which guides the model rather than enforcing a filesystem restriction. The composed file is bounded by the default 32 KiB discovery limit. Antigravity loads rules through its own trigger mechanism, including native `manual` and `model_decision` modes that Codex composition rejects. Those modes remain usable in Antigravity-only installations. See [Antigravity rules](https://antigravity.google/docs/rules).

## 2. Hook feedback and coverage

| Host/event                                                     | Input                            | Behavior                                                             |
| -------------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------- |
| Antigravity PreToolUse, `run_command`                          | `toolCall.args.CommandLine`      | Ask for native review of common destructive forms or malformed input |
| Antigravity PostToolUse, `write_to_file\|replace_file_content` | `toolCall.args.TargetFile`       | Separate formatting and Mermaid checks                               |
| Codex PostToolUse, `apply_patch\|Edit\|Write\|Bash`            | `tool_name`, `tool_input`, `cwd` | Extract patch/write paths and run both document checks               |

The Codex matcher covers the existing supported tool names. Its command uses the installer's absolute Python executable so bootstrap does not depend on a GUI PATH containing Python. Redeploy after changing that Python installation; native review applies to changed commands. Antigravity shell launchers add standard user and Homebrew runtime directories before locating Python. Bash payloads are an explicit no-op because arbitrary shell code cannot reliably identify edited paths. Patch moves check the destination. These hooks cover configured tool events, not every way a file can change.

[document-check.py](shared/document-check.py) separates payload handling from shared checks. It resolves quoted and relative paths, prefers the target project's installed Prettier, and uses the pinned library fallback when needed. The target project's configuration takes precedence; unconfigured files use this repository's `.prettierrc`.

Mermaid checks use the helper bundled with the mermaid-architect skill. A Markdown document without Mermaid fences requires no renderer. Diagrams require a provisioned CLI at the expected version; checks do not fetch packages.

On success, document hooks return `{}` on stdout. Diagnostics go to stderr. On failure, the shared checker exits `2`; Codex also receives `decision: block` feedback. PostToolUse feedback cannot reverse the preceding edit. For exact Markdown assets, an allowed `<!-- prettier-ignore -->` comment before the protected block avoids reformatting. Inspect the saved file after hooks; a submitted edit alone does not prove preservation. Formatter errors, invalid diagrams, missing dependencies, and timeouts remain visible rather than becoming successful results.

The Antigravity safety gate is a conservative pattern check. It recognizes common Git, SQL, and recursive forced removal forms, including split flags and relative paths. It is not a shell interpreter or a security boundary. Native permissions remain necessary.

## 3. Ownership and migration

The Codex installer replaces only a recognized invocation of this checkout's `adapters/shared/document-check.py --host codex`. It preserves other PostToolUse handlers, other events, and unrelated top-level settings. Malformed JSON or invalid supported hook-container shapes stop deployment before writes. Unknown fields are preserved; this is not a full Codex schema validator.

Adopting an existing regular `hooks.json` requires `--backup-conflicts`. The original file remains recoverable in the backup directory. Later deployments read the managed file, retain unrelated additions, and update the owned entry without duplication.

Codex's native trust review still applies to new or changed entries. The installer does not edit trust state. See [Codex hooks](https://learn.chatgpt.com/docs/hooks) and [Antigravity hooks](https://antigravity.google/docs/hooks).

Antigravity's entire destination hook file remains installer-owned; conflicting originals are backed up when replacement is requested. It does not share Codex's merge schema.

## 4. Other hosts and future hooks

The portable [Skills CLI route](../README.md#2-install-selected-skills-in-a-project) distributes selected skill folders. Gemini CLI uses its own skills and `settings.json` hook conventions; this Antigravity adapter is not a Gemini CLI hook installer. Claude's native plugins can package skills and hooks, but no Claude hook adapter is maintained here.

Before adding a hook:

1. Verify the host's current event, input, output, failure, and trust contracts.
2. Keep host normalization at the adapter boundary and reuse a shared checker only where semantics match.
3. Add the template and shell-quoted render mapping.
4. Exercise real side effects, errors, missing dependencies, and bounded execution in isolated tests.
5. Document coverage and perform a native host check before claiming runtime delivery.

Return to the [repository overview](../README.md).
