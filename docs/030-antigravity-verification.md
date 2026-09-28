# Antigravity verification prompt

Start a fresh Antigravity chat in this checkout after deployment. Paste the following prompt. Repeat the discovery portion from another project to establish that installation is global.

```text
Verify my personal coherent-output setup on this Mac. I use the same Git repository on several Macs, with a separate local installation on each one.

First, before reading any SKILL.md files or searching the skills directory, report which coherent-output skills are already present in your runtime's available-skills catalog. Keep this initial discovery evidence separate from files you find afterward. Do not claim that a skill was automatically discovered merely because you can read its file.

Then read README.md, docs/020-mac-setup.md, and the Antigravity adapter documentation in this repository. Run ./scripts/deploy.sh --tool antigravity --check. This command is read-only. Inspect and resolve the Antigravity installation links.

Verify these expectations:
- ~/.gemini/AGENTS.md points to the shared AGENTS.md.
- ~/.gemini/config/skills points to the shared skills directory containing 16 SKILL.md files.
- ~/.gemini/config/rules points to the five shared Markdown rules.
- ~/.gemini/config/hooks.json points to the locally generated Antigravity configuration.
- Hook commands resolve to the scripts under adapters/antigravity/hooks/scripts in this Mac's checkout.
- The same skills are not also installed through this repo's .agents/skills.
- The Markdown rule has its *.md condition; the other four rules are always_on.

Inspect the Customizations panel or another runtime-provided inventory if you can access it. Distinguish configured files, discovered capabilities, enabled hooks, and demonstrated execution. If an app state is inaccessible, report it as unverified.

Demonstrate actual skill use:
1. Explicitly load and apply concise-answer to explain why the source repository can live at a different path on each Mac.
2. Explicitly load and apply email-rewrite to this sample: "Please send the revised draft by Friday so I can review it before Monday's meeting." Return the rewritten email in this chat; do not send it.
Report the skill paths you used.

Check hooks safely. You may feed harmless synthetic JSON payloads to their scripts. Dangerous command strings must remain input data and must never be executed. Test the formatter only on a disposable file in a temporary directory. If your native write tool can safely edit that temporary file, use it to check whether the PostToolUse formatter actually fires; direct script execution alone does not prove automatic hook activation. Verify whether Python 3 and Prettier are available to the hook process. Do not trigger a destructive command to test the approval gate.

Finish with PASS, FAIL, or UNVERIFIED for instructions, skill discovery, skill use, rule activation, hook configuration, and automatic hook execution. Explain the shared sources, the two tool adapters, generated local files, and the Git pull + deploy workflow in your own words. Identify discrepancies with exact paths and suggested corrections. Keep the installation unchanged during this audit.
```

Return to the [documentation index](README.md).
