# Tool Adapters

This directory defines tool-specific installation blueprints and runtime bridges. Shared skills and policy source files remain strictly tool-agnostic.

---

## 1. Adapter Architecture

Each adapter folder contains a `links.json` file specifying how shared sources map into tool-specific target locations:

| Adapter                         | Target Directory            | Key Mappings                                                                                                                                                 | Runtime Mechanics                                                                                                                                                                  |
| :------------------------------ | :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Antigravity](antigravity/)** | `~/.gemini/`                | `AGENTS.md` → `~/.gemini/AGENTS.md`<br>`rules/` → `~/.gemini/config/rules`<br>`skills/` → `~/.gemini/config/skills`<br>Hooks → `~/.gemini/config/hooks.json` | Loads rules dynamically based on YAML trigger frontmatter (`always_on`, `glob`). Renders local hook commands dynamically from template.                                            |
| **[Codex](codex/)**             | `~/.codex/`<br>`~/.agents/` | `AGENTS.md` → `~/.codex/AGENTS.md`<br>`skills/` → `~/.agents/skills`                                                                                         | Merges `AGENTS.md` and all modular written rules into `.generated/codex/AGENTS.md`. Wraps any glob rules in file conditions. Leaves native Codex command approval policy in place. |

---

## 2. Antigravity Lifecycle Hooks

Antigravity lifecycle hooks are configured via `adapters/antigravity/hooks/hooks.template.json`:

- **Destructive Command Gate (`safety-gate.sh`):**
  - Event: `PreToolUse` on `run_command`.
  - Behavior: Inspects command payloads for high-risk patterns (`rm -rf /`, `git reset --hard`, `DROP DATABASE`).
  - Output: Returns `{"decision": "force_ask"}` for destructive patterns, `{"decision": "allow"}` otherwise.
- **Prettier Auto-Formatter (`prettier-format.sh`):**
  - Event: `PostToolUse` on `write_to_file` and `replace_file_content`.
  - Behavior: Sanitizes file paths (stripping quotes and expanding home paths), checks for project-level Prettier configs, falls back to the repository `.prettierrc` for unconfigured files, and automatically formats Markdown and code files.
- **Mermaid Diagram Validator (`mermaid-validate.sh`):**
  - Event: `PostToolUse` on `write_to_file` and `replace_file_content`.
  - Behavior: Fast-checks written or modified Markdown files for ` ```mermaid ` code blocks and batch-compiles them using `verify-markdown.py`. Non-zero exit on syntax error prevents broken diagram syntax from persisting unnoticed.

The installer renders local absolute script paths dynamically into `.generated/antigravity/hooks.json` via `./scripts/deploy.sh`, ensuring hook paths work on any Mac regardless of checkout location.

### Adding New Hooks: Standard Workflow

1. Place the executable shell/Python script in `adapters/antigravity/hooks/scripts/`.
2. Register the event trigger in `adapters/antigravity/hooks/hooks.template.json` using the `{{script_placeholder}}` syntax.
3. Add the template replacement in `scripts/deploy.py` under `replacements`.
4. Run `./scripts/deploy.sh` and `./scripts/verify.sh` to compile `.generated/antigravity/hooks.json` and confirm test suite passage.

---

## 3. Codex Bridge & Instruction Composition

Codex CLI does not use a directory for Markdown prompt rules (Codex's `.rules` files use a Starlark DSL specifically for command sandboxing permissions).

To ensure complete policy enforcement in Codex:

- The installer concatenates `AGENTS.md` with all modular rule bodies from `rules/*.md`.
- Any glob-triggered policies are dynamically wrapped in natural-language boundary markers (e.g., `Apply the following policy only when working on files matching <pattern>`).
- Output is written to `.generated/codex/AGENTS.md` (well under the 32 KiB instruction limit) and symlinked to `~/.codex/AGENTS.md`.

---

## 4. Skill Discovery Across Harnesses

Both Antigravity and Codex implement the [Agent Skills open standard](../skills/README.md). Neither requires the model to traverse local directories:

- **Antigravity Discovery:** Automatically scans `~/.gemini/config/skills/*/SKILL.md` (and workspace `.agents/skills/`), injects frontmatter (`name` and `description`) into an active `<skills>` system prompt block at startup, and loads the full `SKILL.md` instructions when activated.
- **Codex Discovery:** Scans `~/.agents/skills/*/SKILL.md` and repository `.agents/skills/` walking up the directory tree, catalogs skill metadata into the model prompt, and loads bodies on demand.

In both tools, Section 5 of `AGENTS.md` acts as an autonomous policy router that matches task intent to the harness-provided skill manifest.

Return to the [repository overview](../README.md).
