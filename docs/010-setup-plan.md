# Personal setup across Macs

- **Objective:**
  - Use this Git repository as the source for one person's agent customizations on multiple Macs.
  - Install shared skills globally in each tool.
  - Keep authentication, sessions, app databases, plugin caches, machine trust, and unrelated app settings local to each Mac.

## Implementation plan

1. Inspect the current links, skill inventory, rules, and hook contracts.
2. Keep shared instructions in `AGENTS.md`, portable workflows in `skills/`, and written policies in `rules/`.
3. Move Antigravity hook configuration and scripts into its adapter.
4. Define each tool's installation mapping in its own adapter.
5. Compose Codex global instructions from the shared instructions and written rules.
6. Preserve the Markdown rule's conditional scope in the composed instructions.
7. Generate local hook commands from the actual checkout location.
8. Implement one repeatable installer with preview, inspection, and conflict handling.
9. Remove the redundant repository skill link while retaining personal global discovery.
10. Exercise installation, repeated installation, conflicts, and paths containing spaces in temporary directories.
11. Deploy to this Mac and inspect the resulting links and generated content.
12. Document installation and updates on other Macs.
13. Provide an Antigravity prompt that distinguishes file availability from actual runtime discovery and execution.

- **Compatibility decisions:**
  - Antigravity loads the shared Markdown rules with their activation metadata.
  - Codex receives those rules through a generated `AGENTS.md`.
  - Codex's `.rules` files express command approval policy and do not represent these written rules.
  - Antigravity retains its command approval and formatting hooks.
  - Codex retains its existing native approval settings.
  - Codex's documented `PreToolUse` contract does not support the equivalent of Antigravity's `force_ask`; the installer does not install a misleading equivalent.

- **Acceptance evidence:**
  - Both tool mappings resolve to this checkout or its locally generated files.
  - Each tool's global skills directory exposes all 16 source skills.
  - No skill is installed through an additional repository discovery link.
  - Generated Codex instructions preserve all five rule bodies and the Markdown condition.
  - Hook commands reference this Mac's checkout path.
  - Unknown destination content causes a conflict before installation writes anything.
  - Repeating installation produces no further changes.
  - Antigravity runtime discovery remains a separate check using the supplied prompt.

## Execution evidence

- **Completed on the current Mac:**
  - The shared-source layout and both adapter mappings are installed.
  - The installer reports all six application-facing links as correct.
  - Both global skill paths expose 16 skills.
  - The generated Codex instructions contain all five policy bodies in 17,404 bytes.
  - This Codex chat receives the composed policies in its active instructions.
  - The redundant repository skill link is removed.
  - Seven isolated installation checks pass.
  - The installed formatter command formats disposable JSON while preserving its data.
  - Shell syntax checks and Git whitespace checks pass.
  - Relative file links in all nine updated documentation files resolve.
  - The verification environment provides Python 3.14.7 and Prettier 3.9.9.

- **Checks performed by the application or another Mac:**
  - A fresh Antigravity chat uses the supplied prompt to verify its runtime catalog and automatic hook activation.
  - Other Macs receive committed source changes through Git and run their own deployment.
  - The source changes in this task remain uncommitted until the normal Git publishing workflow is performed.
