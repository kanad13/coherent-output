# Coherent Output

This repository holds one person's shared agent instructions and skills across multiple Macs. Git carries the source files between devices. Each Mac runs the installer to connect its local applications to its own checkout.

## Start here

Run these commands from this checkout with Python 3 available:

```bash
./scripts/deploy.sh --dry-run
./scripts/deploy.sh
./scripts/deploy.sh --check
```

The installer defaults to Codex and Antigravity 2.0 / IDE. Use `--tool codex` or `--tool antigravity` to select one. Start fresh chats after deployment. The installer checks filesystem configuration; the [Antigravity verification prompt](docs/030-antigravity-verification.md) checks what the application actually discovers.

## Source layout

| Location | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Shared persona, communication standards, and operating discipline |
| [skills/](skills/) | Portable workflows in the Agent Skills format |
| [rules/](rules/) | Shared written policies with Antigravity activation metadata |
| [adapters/](adapters/README.md) | Tool-specific installation mappings and hook formats |
| [scripts/](scripts/README.md) | Installer and isolated installation checks |
| [docs/](docs/README.md) | Implementation plan, Mac setup guide, and verification prompt |
| [tools/](tools/README.md) | Notepad and development containers |
| [.prettierrc](.prettierrc) | Formatting defaults for this repository |

The installer creates `.generated/` locally for composed Codex instructions and Antigravity hook commands containing this Mac's checkout path. Git ignores those generated files. Edit their sources and rerun deployment.

## Installed mapping

`<repo>` means the actual checkout on that Mac. `~` means that Mac's user home.

| Tool reads | Source or generated target |
| --- | --- |
| `~/.agents/skills` | `<repo>/skills` |
| `~/.codex/AGENTS.md` | `<repo>/.generated/codex/AGENTS.md` |
| `~/.gemini/config/skills` | `<repo>/skills` |
| `~/.gemini/AGENTS.md` | `<repo>/AGENTS.md` |
| `~/.gemini/config/rules` | `<repo>/rules` |
| `~/.gemini/config/hooks.json` | `<repo>/.generated/antigravity/hooks.json` |

Codex instructions combine the shared `AGENTS.md` and all five written rules. The Markdown policy retains an explicit file condition in the instructions. Codex evaluates that condition as model guidance; Antigravity evaluates its native `glob` activation metadata. Codex's `.rules` files serve a different purpose: command approval policy.

The skills are installed globally. This repository does not also install them through `.agents/skills`. App-owned system skills and plugin caches remain separate from this library.

## Skills

| Skill | Purpose |
| --- | --- |
| [bullet-first-refactor](skills/bullet-first-refactor/SKILL.md) | Refactor text into structured bullets without losing meaning |
| [claim-validator](skills/claim-validator/SKILL.md) | Evaluate claims against evidence |
| [code-beginner-comments](skills/code-beginner-comments/SKILL.md) | Explain code for learners |
| [commit-scribe](skills/commit-scribe/SKILL.md) | Write structured Git commits |
| [concept-tutor](skills/concept-tutor/SKILL.md) | Teach technical concepts |
| [concise-answer](skills/concise-answer/SKILL.md) | Give concise technical answers |
| [conversation-notes](skills/conversation-notes/SKILL.md) | Turn conversations into standalone notes |
| [deidentify-document](skills/deidentify-document/SKILL.md) | Remove identifying information |
| [discovery-advisor](skills/discovery-advisor/SKILL.md) | Clarify requirements and architecture choices |
| [email-rewrite](skills/email-rewrite/SKILL.md) | Rewrite professional correspondence |
| [german-tutor](skills/german-tutor/SKILL.md) | Support German language learning |
| [markdown-audit](skills/markdown-audit/SKILL.md) | Inspect documentation structure and links |
| [mermaid-architect](skills/mermaid-architect/SKILL.md) | Create Mermaid diagrams |
| [product-comparison](skills/product-comparison/SKILL.md) | Compare products and ownership costs |
| [repo-evergreen-sync](skills/repo-evergreen-sync/SKILL.md) | Reconcile repository documentation |
| [web-research](skills/web-research/SKILL.md) | Research external questions using primary evidence |

## Hooks and local settings

Antigravity receives the [destructive-command gate and Prettier hook](adapters/antigravity/README.md). Their scripts retain their existing behavior. Prettier must be available on the hook process's `PATH` for formatting to occur.

The [Codex adapter](adapters/codex/README.md) installs instructions and skills. It leaves the existing Codex approval policy in place. It does not install an equivalent of Antigravity's `force_ask` hook because the documented Codex hook contract does not support that decision. It does not enable automatic formatting in Codex.

Authentication, histories, app databases, plugins, permissions, and app-specific model settings remain local to each Mac. Whole app configuration directories are not synchronized.
