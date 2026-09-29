# Tool Adapters

This directory defines tool-specific installation blueprints and runtime bridges. Shared skills and policy source files remain strictly tool-agnostic.

---

## 1. Adapter Architecture

Each adapter folder contains a `links.json` file specifying how shared sources map into tool-specific target locations:

| Adapter                         | Target Directory            | Key Mappings                                                                                                                                                 | Runtime Mechanics                                                                                                                                                                      |
| :------------------------------ | :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Antigravity](antigravity/)** | `~/.gemini/`                | `AGENTS.md` → `~/.gemini/AGENTS.md`<br>`rules/` → `~/.gemini/config/rules`<br>`skills/` → `~/.gemini/config/skills`<br>Hooks → `~/.gemini/config/hooks.json` | Loads rules dynamically based on YAML trigger frontmatter (`always_on`, `glob`). Renders local hook commands dynamically from template.                                                |
| **[Codex](codex/)**             | `~/.codex/`<br>`~/.agents/` | `AGENTS.md` → `~/.codex/AGENTS.md`<br>`skills/` → `~/.agents/skills`                                                                                         | Merges `AGENTS.md` and all modular written rules into `.generated/codex/AGENTS.md`. Preserves file condition around `*.md` rule. Leaves native Codex command approval policy in place. |

---

## 2. Antigravity Lifecycle Hooks

Antigravity lifecycle hooks are configured via `adapters/antigravity/hooks/hooks.template.json`:

- **Destructive Command Gate (`safety-gate.sh`):**
  - Event: `PreToolUse` on `run_command`.
  - Behavior: Inspects command payloads for high-risk patterns (`rm -rf /`, `git reset --hard`, `DROP DATABASE`).
  - Output: Returns `{"decision": "force_ask"}` for destructive patterns, `{"decision": "allow"}` otherwise.
- **Prettier Auto-Formatter (`prettier-format.sh`):**
  - Event: `PostToolUse` on `write_to_file` and `replace_file_content`.
  - Behavior: Automatically runs Prettier on formatted code and Markdown files if `prettier` is available on `PATH`.

The installer renders local absolute script paths dynamically into `.generated/antigravity/hooks.json`, ensuring hook paths work on any Mac regardless of checkout location.

---

## 3. Codex Bridge & Instruction Composition

Codex CLI does not use a directory for Markdown prompt rules (Codex's `.rules` files use a Starlark DSL specifically for command sandboxing permissions).

To ensure complete policy enforcement in Codex:

- The installer concatenates `AGENTS.md` with all modular rule bodies from `rules/*.md`.
- Glob-triggered policies (`04-markdown-standards.md`) are wrapped in natural-language boundary markers (`Apply the following policy only when working on files matching *.md`).
- Output is written to `.generated/codex/AGENTS.md` (well under the 32 KiB instruction limit) and symlinked to `~/.codex/AGENTS.md`.

Return to the [repository overview](../README.md).
