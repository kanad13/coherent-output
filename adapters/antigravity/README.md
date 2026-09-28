# Antigravity adapter

[links.json](links.json) maps shared instructions, skills, and rules into the Antigravity 2.0 / IDE global configuration locations. Antigravity CLI has a separate global skills location and is outside this installation target.

The installer renders [hooks.template.json](hooks/hooks.template.json) into `.generated/antigravity/hooks.json`. It quotes the actual checkout path in each shell command, including paths containing spaces or apostrophes.

- [safety-gate.sh](hooks/scripts/safety-gate.sh) examines the proposed `run_command` payload. Its existing pattern check returns `force_ask` for recognized destructive commands and `allow` otherwise. This pattern check is not a complete shell security parser.
- [prettier-format.sh](hooks/scripts/prettier-format.sh) formats supported files after `write_to_file` or `replace_file_content`. It skips failed tool calls and does nothing when Prettier is unavailable on its `PATH`.

Both scripts require Bash and Python 3. Formatting uses the Prettier executable found by the hook process. The scripts retain their previous input and output contracts. The installer relocates their paths without changing those contracts.

Inspect the application's Customizations panel to confirm loaded skills, rules, and enabled hooks. Use the [verification prompt](../../docs/030-antigravity-verification.md) for an evidence-based runtime check.

Sources: [skill locations](https://www.antigravity.google/docs/skills/), [rule discovery](https://www.antigravity.google/docs/rules/), [hook configuration](https://www.antigravity.google/docs/hooks/).

Return to [adapters](../README.md).
