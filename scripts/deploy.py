#!/usr/bin/env python3
"""Install the agent library without copying machine-owned application state.

Preflight the selected host artifacts and shared skill metadata before writes.
Generated commands resolve this checkout and its local runtime; conflicts stay
recoverable through explicit backups rather than destructive replacement.
"""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import sys
import tempfile


REPO = Path(__file__).resolve().parent.parent


def frontmatter(path):
    """Read this library's flat metadata profile without claiming full YAML support.

    Args:
        path: Path to a skill or rule with single-line frontmatter fields.

    Returns:
        A metadata dictionary and the remaining document body.

    Raises:
        ValueError: Frontmatter is absent, nested, duplicate, or empty.
        OSError: The source cannot be read.
    """
    text = path.read_text()
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Missing frontmatter: {path}")
    metadata = {}
    for line in parts[1].strip().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line[0].isspace():
            raise ValueError(f"Only flat single-line frontmatter is supported: {path}")
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"Unsupported frontmatter line in {path}: {line}")
        if key in metadata or not value.strip():
            raise ValueError(f"Duplicate or empty frontmatter field in {path}: {key}")
        metadata[key.strip()] = value.strip().strip('\"').strip("'")
    return metadata, parts[2].lstrip("\n")


def merge_post_tool_hooks(template_path, host, destination):
    """Replace only this checkout's handler while preserving unrelated user state.

    Args:
        template_path: Repository-relative hook template for the host.
        host: Value of the owned checker's ``--host`` argument.
        destination: Existing host configuration file to merge into, or None.

    Returns:
        Serialized configuration using the installer's absolute Python executable.

    Raises:
        ValueError: Existing JSON or supported hook-container shapes are invalid.
        OSError: An existing configuration or source template cannot be read.
    """
    template = json.loads(REPO.joinpath(template_path).read_text())
    checker = str(REPO / "adapters/shared/document-check.py")
    for group in template["hooks"]["PostToolUse"]:
        for handler in group["hooks"]:
            handler["command"] = handler["command"].replace("{{python_executable}}", shlex.quote(sys.executable))
            handler["command"] = handler["command"].replace("{{document_check}}", shlex.quote(checker))
    label = host.capitalize()
    try:
        current = json.loads(destination.read_text()) if destination and destination.is_file() else {}
    except json.JSONDecodeError as error:
        raise ValueError(f"{label} configuration is not valid JSON ({error}); nothing installed.") from error
    if not isinstance(current, dict) or not isinstance(current.get("hooks", {}), dict):
        raise ValueError(f"{label} configuration must contain a hooks object; nothing installed.")
    events = current.setdefault("hooks", {})
    groups = events.get("PostToolUse", [])
    if not isinstance(groups, list):
        raise ValueError(f"{label} PostToolUse must be an array; nothing installed.")
    preserved = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError(f"Invalid {label} PostToolUse group; nothing installed.")
        handlers = []
        for handler in group["hooks"]:
            if not isinstance(handler, dict):
                raise ValueError(f"Invalid {label} hook handler; nothing installed.")
            try:
                tokens = shlex.split(handler.get("command", ""))
            except ValueError:
                tokens = []
            owned = len(tokens) == 4 and tokens[1:] == [checker, "--host", host]
            if not owned:
                handlers.append(handler)
        if handlers:
            preserved.append({**group, "hooks": handlers})
    events["PostToolUse"] = preserved + template["hooks"]["PostToolUse"]
    return json.dumps(current, indent=2) + "\n"


def codex_hooks(codex_home):
    """Merge the Codex handler into the destination's existing hooks."""
    destination = codex_home / "hooks.json" if codex_home else None
    return merge_post_tool_hooks("adapters/codex/hooks.template.json", "codex", destination)


def claude_settings(claude_home):
    """Merge the Claude Code handler into the user's settings, which the app also writes."""
    destination = claude_home / "settings.json" if claude_home else None
    return merge_post_tool_hooks("adapters/claude/settings.template.json", "claude", destination)


def composed_instructions():
    """Compose supported policies without silently activating native-only triggers.

    Codex and Claude Code have no native trigger modes, so both receive this text.

    Returns:
        Instruction text within its default discovery size limit.

    Raises:
        ValueError: A rule cannot be composed or the result exceeds 32 KiB.
        OSError: An instruction source cannot be read.
    """
    instructions = REPO.joinpath("instructions/global.md").read_text().rstrip() + "\n"
    for rule in sorted(REPO.joinpath("rules").glob("*.md")):
        metadata, body = frontmatter(rule)
        trigger = metadata.get("trigger")
        if trigger not in ("always_on", "glob"):
            raise ValueError(f"Composed instructions do not support trigger {trigger!r}: {rule}")
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
        raise ValueError("Composed instructions exceed the 32 KiB discovery limit.")
    return instructions


def antigravity_hooks():
    """Resolve local commands without importing another host's configuration.

    Returns:
        Serialized Antigravity hooks with shell-quoted checkout paths.

    Raises:
        ValueError: Source JSON or command placeholders are invalid.
        OSError: The source template cannot be read.
    """
    hooks = json.loads(REPO.joinpath("adapters/antigravity/hooks/hooks.template.json").read_text())
    scripts = REPO / "adapters/antigravity/hooks/scripts"
    replacements = {
        "{{safety_gate}}": shlex.quote(str(scripts / "safety-gate.sh")),
        "{{prettier_format}}": shlex.quote(str(scripts / "prettier-format.sh")),
        "{{mermaid_validate}}": shlex.quote(str(scripts / "mermaid-validate.sh")),
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
    return json.dumps(hooks, indent=2) + "\n"


TOOLS = ("codex", "claude", "antigravity")


def generated_files(codex_home=None, selected=TOOLS, claude_home=None):
    """Scope preflight to selected hosts while leaving unselected state untouched.

    Args:
        codex_home: Optional destination for merging existing Codex hooks.
        selected: Host names whose generated artifacts are required.

    Returns:
        A mapping from generated file paths to their intended text contents.
    """
    generated = {}
    if "codex" in selected:
        generated[REPO / ".generated/codex/AGENTS.md"] = composed_instructions()
        generated[REPO / f".generated/codex/{codex_home_id(codex_home)}/hooks.json"] = codex_hooks(codex_home)
    if "claude" in selected:
        generated[REPO / ".generated/claude/CLAUDE.md"] = composed_instructions()
    if "antigravity" in selected:
        generated[REPO / ".generated/antigravity/hooks.json"] = antigravity_hooks()
    return generated


def merged_files(claude_home, selected):
    """Name host files the application also writes, so they are merged, not linked.

    Returns:
        A mapping from destination paths to their intended merged contents.
    """
    return {claude_home / "settings.json": claude_settings(claude_home)} if "claude" in selected else {}


def present(path):
    """Treat dangling links as existing destinations that require ownership checks.

    Args:
        path: Destination path to inspect.

    Returns:
        Whether a filesystem entry exists, including a dangling symlink.
    """
    return os.path.lexists(path)


def codex_home_id(codex_home):
    """Keep merged user hooks isolated by installation destination.

    Args:
        codex_home: Resolved Codex destination home, or None for no destination.

    Returns:
        A stable 16-character hash used to namespace generated hook files.
    """
    return hashlib.sha256(str(codex_home).encode()).hexdigest()[:16]


def link_target(path):
    """Normalize filesystem aliases before deciding whether a link is owned.

    Args:
        path: Possible installation symlink.

    Returns:
        Its resolved target, including dangling targets, or None for other files.
    """
    if not path.is_symlink():
        return None
    # macOS exposes /var through /private/var; normalize aliases even for dangling targets.
    return (path.parent / os.readlink(path)).resolve()


def write_atomic(path, content, keep_mode=False):
    """Avoid partial generated files and unnecessary writes on repeat deployment.

    Args:
        path: Generated output path.
        content: Desired text contents.
        keep_mode: Retain an existing file's permissions, as settings files may be private.

    Raises:
        OSError: The source, temporary file, or replacement cannot be accessed.
    """
    if path.is_file() and path.read_text() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".coherent-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(content)
        if keep_mode and path.is_file():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def main():
    """Preflight ownership before installing the selected host mappings.

    Returns:
        Zero for installation, preview, or a correct installed state; one for
        installed-state drift. Entry-point error handling also reports one.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("all", *TOOLS), default="all")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    modes.add_argument("--check", action="store_true", help="Inspect installed links and generated content")
    parser.add_argument("--backup-conflicts", action="store_true", help="Preserve conflicting destinations before replacing them")
    parser.add_argument("--target-home", type=Path, help="Use a separate installation home, including for verification")
    parser.add_argument("--claude-home", type=Path, help="Override the Claude Code home; otherwise use CLAUDE_CONFIG_DIR or ~/.claude")
    parser.add_argument("--codex-home", type=Path, help="Override the Codex home; otherwise use CODEX_HOME or ~/.codex")
    args = parser.parse_args()
    target_home = (args.target_home or Path.home()).expanduser().resolve()
    configured_codex = None if args.target_home else os.environ.get("CODEX_HOME")
    codex_home = (args.codex_home or Path(configured_codex or target_home / ".codex")).expanduser().resolve()
    configured_claude = None if args.target_home else os.environ.get("CLAUDE_CONFIG_DIR")
    claude_home = (args.claude_home or Path(configured_claude or target_home / ".claude")).expanduser().resolve()
    scopes = {"home": target_home, "codex": codex_home, "claude": claude_home}
    selected = TOOLS if args.tool == "all" else (args.tool,)
    generated = generated_files(codex_home, selected, claude_home)
    merged = merged_files(claude_home, selected)
    links = []
    for tool in selected:
        for spec in json.loads(REPO.joinpath(f"adapters/{tool}/links.json").read_text()):
            destination = scopes[spec["scope"]] / spec["destination"]
            source = REPO / spec["source"].replace("{codex_home_id}", codex_home_id(codex_home))
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
        name = metadata["name"]
        if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {skill}")
        if name != skill.parent.name:
            raise ValueError(f"Skill name must match its directory: {skill}")
        if len(metadata["description"]) > 1024:
            raise ValueError(f"Skill description exceeds 1024 characters: {skill}")
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
    for path, content in merged.items():
        current = path.is_file() and path.read_text() == content
        print(f"{'OK' if current else 'MERGE'} {path}")
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
    for path, content in merged.items():
        if path.is_file() and path.read_text() != content:
            backup_root.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup_root / f"merged-{path.name}")
            print(f"BACKUP {path} -> {backup_root / ('merged-' + path.name)}")
        write_atomic(path, content, keep_mode=True)
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
