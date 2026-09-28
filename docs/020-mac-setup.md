# Setup on each Mac

## Install

1. Install the desired apps and sign in separately on the Mac.
2. Ensure `python3` runs in the terminal and is available to Antigravity's hook process.
3. Ensure `prettier` is available to the hook process if automatic formatting is required.
4. Clone this repository to a stable local directory of your choice.
5. Run the commands below from that checkout.
6. Start fresh Codex and Antigravity chats.
7. Inspect Antigravity's Customizations panel and run the [verification prompt](030-antigravity-verification.md).

```bash
./scripts/deploy.sh --dry-run
./scripts/deploy.sh
./scripts/deploy.sh --check
```

All six application-facing links are global user customizations. The generated files contain paths for this Mac and are excluded from Git. The generated Codex instructions include all shared rule bodies. Skills and Antigravity rules remain directly linked to their sources.

Use `--tool codex` or `--tool antigravity` when only one app is wanted. The Antigravity target covers Antigravity 2.0 and the IDE, which share these configuration paths. It does not install Antigravity CLI skills in the CLI's separate directory.

The installer uses `CODEX_HOME` when it is set. Use `--codex-home /absolute/path` to choose it explicitly. `--target-home /temporary/path` redirects installation destinations for isolated checks; it also ignores the current `CODEX_HOME` unless `--codex-home` is supplied. Generated artifacts always belong to the checkout running the installer.

## Update across devices

1. Edit the source files on one Mac.
2. Run deployment and `--check` on that Mac.
3. Commit and push the source changes through your normal Git workflow.
4. Pull those changes in the existing checkout on each other Mac.
5. Rerun deployment and `--check` on each Mac.
6. Start fresh chats to refresh active instructions.

Git synchronization is manual. There is no background syncing service. This task does not commit or push changes automatically. Existing uncommitted source changes must be published before another Mac can pull them.

Both Macs must use the same Git revision to share the same source setup. Compare `git rev-parse HEAD` and `git status --short` when diagnosing differences. Compare app, Python, and Prettier versions when runtime behavior differs. Model selection and app feature availability can still affect behavior.

A dedicated local checkout is preferable to a checkout in a live cloud-synced folder because it gives each Mac its own Git state and generated files. Keep the checkout available while using the apps. If you move it, rerun deployment; old absolute links may be reported as conflicts.

## Conflicts and backups

Preview and check modes do not write files. A normal deployment recognizes this checkout's current mappings and the previous instruction and hook links. Unknown existing files, directories, and symlinks cause it to stop before writing installation artifacts.

To deliberately replace conflicting destinations while preserving their content:

```bash
./scripts/deploy.sh --backup-conflicts
./scripts/deploy.sh --check
```

Backups are stored under `~/.local/state/coherent-output/backups/<timestamp>/`. The installer prints the original path and backup path. A `manifest.json` in that directory records the mapping for recovery. Backup names include an index to avoid collisions. Existing directories are preserved as directories; their contents are not merged into this library automatically. Review those backups if a Mac already has additional skills or custom hooks you want to retain.

To restore a destination, inspect the printed mapping, remove only the symlink created by this installer at that destination, and move its backup back to the original path. If no conflicting content existed, uninstalling consists of removing the six installer-owned symlinks from the [mapping table](../README.md#installed-mapping). Preserve their source targets. The installer does not alter model settings, authentication files, app databases, or unrelated configuration.

## Inspect a problem

```bash
./scripts/deploy.sh --check
python3 scripts/test_deploy.py
```

`--check` verifies link destinations and generated content against the sources. It does not prove that a running application has loaded them. For Codex, inspect a fresh chat's available skills and active instructions. For Antigravity, inspect its Customizations panel and run the [runtime verification](030-antigravity-verification.md).

A nonempty `AGENTS.override.md` in Codex home takes precedence over the installed global `AGENTS.md`. More specific project instructions can also override global guidance. These independent overrides remain under your control.

Return to the [documentation index](README.md).
