#!/usr/bin/env python3
"""Install the personal agent library without copying machine-owned app state."""

import argparse
import datetime
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile


REPO = Path(__file__).resolve().parent.parent


def frontmatter(path):
    text = path.read_text()
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Missing frontmatter: {path}")
    metadata = {}
    for line in parts[1].strip().splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"Unsupported frontmatter line in {path}: {line}")
        metadata[key.strip()] = value.strip().strip('\"').strip("'")
    return metadata, parts[2].lstrip("\n")


def generated_files():
    instructions = REPO.joinpath("AGENTS.md").read_text().rstrip() + "\n"
    for rule in sorted(REPO.joinpath("rules").glob("*.md")):
        metadata, body = frontmatter(rule)
        trigger = metadata.get("trigger")
        if trigger not in ("always_on", "glob"):
            raise ValueError(f"Codex composition does not support trigger {trigger!r}: {rule}")
        instructions += f"\n---\n\n## Shared policy: {rule.name}\n\n"
        if trigger == "glob":
            pattern = metadata.get("globs") or metadata.get("glob")
            if not pattern:
                raise ValueError(f"Missing file pattern: {rule}")
            instructions += (
                f"Apply the following policy only when working on files matching `{pattern}`. "
                "This condition governs the entire policy through the END CONDITIONAL POLICY marker.\n\n"
            )
        instructions += body.rstrip() + "\n"
        if trigger == "glob":
            instructions += "\n<!-- END CONDITIONAL POLICY -->\n"
    if len(instructions.encode()) > 32768:
        raise ValueError("Generated Codex instructions exceed the default 32 KiB discovery limit.")

    hooks = json.loads(REPO.joinpath("adapters/antigravity/hooks/hooks.template.json").read_text())
    scripts = REPO / "adapters/antigravity/hooks/scripts"
    replacements = {
        "{{safety_gate}}": shlex.quote(str(scripts / "safety-gate.sh")),
        "{{prettier_format}}": shlex.quote(str(scripts / "prettier-format.sh")),
    }
    for config in hooks.values():
        for event, groups in config.items():
            if event == "enabled":
                continue
            for group in groups:
                for handler in group["hooks"]:
                    for token, replacement in replacements.items():
                        handler["command"] = handler["command"].replace(token, replacement)
                    if "{{" in handler["command"]:
                        raise ValueError("Unresolved hook command template")
    return {
        REPO / ".generated/codex/AGENTS.md": instructions,
        REPO / ".generated/antigravity/hooks.json": json.dumps(hooks, indent=2) + "\n",
    }


def present(path):
    return os.path.lexists(path)


def link_target(path):
    if not path.is_symlink():
        return None
    # macOS exposes /var through /private/var; normalize aliases even for dangling targets.
    return (path.parent / os.readlink(path)).resolve()


def write_atomic(path, content):
    if path.is_file() and path.read_text() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".coherent-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("all", "codex", "antigravity"), default="all")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    modes.add_argument("--check", action="store_true", help="Inspect installed links and generated content")
    parser.add_argument("--backup-conflicts", action="store_true", help="Preserve conflicting destinations before replacing them")
    parser.add_argument("--target-home", type=Path, help="Use a separate installation home, including for verification")
    parser.add_argument("--codex-home", type=Path, help="Override the Codex home; otherwise use CODEX_HOME or ~/.codex")
    args = parser.parse_args()
    target_home = (args.target_home or Path.home()).expanduser().resolve()
    configured_codex = None if args.target_home else os.environ.get("CODEX_HOME")
    codex_home = (args.codex_home or Path(configured_codex or target_home / ".codex")).expanduser().resolve()
    scopes = {"home": target_home, "codex": codex_home}
    selected = ("codex", "antigravity") if args.tool == "all" else (args.tool,)
    generated = generated_files()
    links = []
    for tool in selected:
        for spec in json.loads(REPO.joinpath(f"adapters/{tool}/links.json").read_text()):
            destination = scopes[spec["scope"]] / spec["destination"]
            source = REPO / spec["source"]
            previous = [REPO / item for item in spec.get("previous_sources", [])]
            if source not in generated and not source.exists():
                raise ValueError(f"Source is missing: {source}")
            links.append((destination, source, previous))

    skill_files = sorted(REPO.joinpath("skills").glob("*/SKILL.md"))
    if not skill_files:
        raise ValueError("No source skills found")
    names = []
    for skill in skill_files:
        metadata, _ = frontmatter(skill)
        if not metadata.get("name") or not metadata.get("description"):
            raise ValueError(f"Skill requires name and description: {skill}")
        names.append(metadata["name"])
    if len(names) != len(set(names)):
        raise ValueError("Duplicate names in source skill library")

    conflicts = []
    for destination, source, previous in links:
        target = link_target(destination)
        if present(destination) and target not in [source, *previous]:
            conflicts.append(destination)
    for destination in conflicts:
        print(f"CONFLICT {destination}")
    if conflicts and not args.backup_conflicts and not args.check:
        raise ValueError("Nothing installed. Inspect conflicts; use --backup-conflicts to preserve and replace them.")

    local_skills = REPO / ".agents/skills"
    redundant = link_target(local_skills) == REPO / "skills"
    relevant_generated = {source: generated[source] for _, source, _ in links if source in generated}
    problems = 0
    for destination, source, _ in links:
        correct = link_target(destination) == source and source.exists()
        print(f"{'OK' if correct else 'LINK'} {destination} -> {source}")
        if args.check and not correct:
            problems += 1
    for path, content in relevant_generated.items():
        current = path.is_file() and path.read_text() == content
        print(f"{'OK' if current else 'GENERATE'} {path}")
        if args.check and not current:
            problems += 1
    if redundant:
        print(f"REMOVE redundant repo discovery link: {local_skills}")
        if args.check:
            problems += 1
    if args.check or args.dry_run:
        print(f"Source inventory: {len(skill_files)} skills, {len(list(REPO.joinpath('rules').glob('*.md')))} written rules.")
        return 1 if problems else 0

    # Preflight makes unknown existing content an explicit, recoverable choice.
    backup_root = target_home / ".local/state/coherent-output/backups" / datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
    backup_records = []
    for path, content in relevant_generated.items():
        write_atomic(path, content)
    for index, (destination, source, _) in enumerate(links):
        if link_target(destination) == source:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination in conflicts:
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / f"{index}-{destination.name}"
            backup_records.append({"original": str(destination), "backup": str(backup)})
            write_atomic(backup_root / "manifest.json", json.dumps(backup_records, indent=2) + "\n")
            os.rename(destination, backup)
            print(f"BACKUP {destination} -> {backup}")
        descriptor, temporary = tempfile.mkstemp(prefix=".coherent-link-", dir=destination.parent)
        os.close(descriptor)
        os.unlink(temporary)
        try:
            os.symlink(source, temporary)
            os.replace(temporary, destination)
        finally:
            if os.path.lexists(temporary):
                os.unlink(temporary)
    if redundant:
        local_skills.unlink()
    print(f"Installed {', '.join(selected)}: {len(skill_files)} shared skills. Start fresh app chats after deployment.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
