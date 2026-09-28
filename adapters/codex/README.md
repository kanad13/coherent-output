# Codex adapter

[links.json](links.json) maps personal skills and global instructions into Codex. The installer respects `CODEX_HOME`, with `~/.codex` as its default. `--codex-home` provides an explicit override.

The installer composes `AGENTS.md` and the bodies of the five shared Markdown rules into `.generated/codex/AGENTS.md`. Always-on rules apply throughout the session. The `*.md` rule carries an explicit condition around its complete body. Codex interprets this condition as an instruction; it does not provide Antigravity's native activation mechanism.

Run deployment again after editing instructions or rules. `--check` reports stale generated content. Skill edits use direct symlinks and do not require regeneration, though the app may need a fresh chat or restart to refresh discovery.

The adapter does not install `.rules` command policies or lifecycle hooks. Codex's existing runtime approval settings continue to apply. In particular, the documented `PreToolUse` output does not support `permissionDecision: "ask"`, so it cannot faithfully implement Antigravity's `force_ask` gate. Automatic formatting is available through the Antigravity adapter only.

Sources: [instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skill discovery](https://learn.chatgpt.com/docs/build-skills), [command rules](https://learn.chatgpt.com/docs/agent-configuration/rules), [hook decisions](https://learn.chatgpt.com/docs/hooks).

Return to [adapters](../README.md).
