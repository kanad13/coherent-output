#!/usr/bin/env python3
"""Break each guarded behavior of the diagram skills and confirm a test notices.

A check that cannot fail proves nothing. Each mutation edits one source file, runs the test
module that should guard it, expects a failure, and restores the file. Run it after changing
a diagram skill's helper, a grader, or their tests; it is too slow for every commit.

Exit codes: 0 every mutation was caught, 1 a mutation survived or did not apply.
"""

from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent

MUTATIONS = [
    ("d2: forbidden-content rule removed", "skills/d2-architect/scripts/verify-d2.py", "    errors.extend(message for pattern, message in FORBIDDEN if pattern.search(code))\n", "", "test_d2_verifier.py"),
    ("d2: non-box shapes allowed", "skills/d2-architect/scripts/verify-d2.py", "(?!(?:sql_table|class|sequence_diagram|rectangle)\\b)\\w", "(?:NEVERMATCH)\\w", "test_d2_verifier.py"),
    ("d2: ladder node limit 15 -> 99", "skills/d2-architect/scripts/verify-d2.py", "LADDER_NODE_LIMIT = 15", "LADDER_NODE_LIMIT = 99", "test_d2_verifier.py"),
    ("d2: service 400 no longer invalid", "skills/d2-architect/scripts/verify-d2.py", 'return ("invalid" if error.code == 400 else "unavailable")', 'return ("invalid" if error.code == 999 else "unavailable")', "test_d2_verifier.py"),
    ("d2: source violations need a renderer to be reported", "skills/d2-architect/scripts/verify-d2.py", "    if early:\n        return 1\n", "", "test_d2_verifier.py"),
    ("d2: width cap ignored", "skills/d2-architect/scripts/verify-d2.py", "    if width > max_width or height > max_height:", "    if False:", "test_d2_verifier.py"),
    ("d2: strip ratio ignored", "skills/d2-architect/scripts/verify-d2.py", "    elif not full and max(width / height, height / width) > MAX_RATIO:", "    elif False:", "test_d2_verifier.py"),
    ("mermaid: strip ratio ignored", "skills/mermaid-architect/scripts/verify-markdown.py", "    if max(width / height, height / width) > MAX_RATIO:", "    if False:", "test_diagram_structure.py"),
    ("mermaid: size warning removed", "skills/mermaid-architect/scripts/verify-markdown.py", "    if width > MAX_WIDTH or height > MAX_HEIGHT:", "    if False:", "test_diagram_structure.py"),
    ("evals: unreviewed images pass", "scripts/skill_evals.py", '    missing = [name for name in images if name not in review]\n    if missing:', '    missing = [name for name in images if name not in review]\n    if False:', "test_skill_evals.py"),
    ("evals: failed image review ignored", "scripts/skill_evals.py", "    if failed:\n        name, note = next", "    if False:\n        name, note = next", "test_skill_evals.py"),
    ("mermaid: shape check disabled", "skills/mermaid-architect/scripts/verify-markdown.py", "        if ODD_SHAPE.search(text):", "        if False:", "test_diagram_structure.py"),
    ("mermaid: node limit 10 -> 99", "skills/mermaid-architect/scripts/verify-markdown.py", "MAX_NODES = 10", "MAX_NODES = 99", "test_diagram_structure.py"),
    ("graders: insertion_only always passes", "scripts/skill_graders.py", '    saved = run.workdir / run.fixture.name\n    if not saved.exists():\n        return FAIL, f"{run.fixture.name} is missing"\n    before =', '    return PASS, ""\n    saved = run.workdir / run.fixture.name\n    if not saved.exists():\n        return FAIL, f"{run.fixture.name} is missing"\n    before =', "test_skill_evals.py"),
    ("graders: ladder ignores overview width", "scripts/skill_graders.py", "    if count > first_max:", "    if False:", "test_skill_evals.py"),
    ("graders: ascii check never matches", "scripts/skill_graders.py", '        if match:\n            return FAIL, f"{name} draws with ASCII', '        if False:\n            return FAIL, f"{name} draws with ASCII', "test_skill_evals.py"),
    ("evals: dead runs not blocked", "scripts/skill_evals.py", '    if problem:\n        return [("agent_ran"', '    if False:\n        return [("agent_ran"', "test_skill_evals.py"),
    ("evals: vanished rule quote not reported", "scripts/skill_evals.py", 'if re.sub(r"\\s+", " ", rule["quote"]) not in flat:', "if False:", "test_skill_evals.py"),
]


def main():
    bad = 0
    for name, path, old, new, test in MUTATIONS:
        target = REPO / path
        original = target.read_text(encoding="utf-8")
        if original.count(old) != 1:
            print(f"NOT APPLIED  {name}: the mutated text is gone; update this list")
            bad += 1
            continue
        try:
            target.write_text(original.replace(old, new), encoding="utf-8")
            result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(REPO / "scripts"), "-p", test], capture_output=True, text=True, timeout=300)
        finally:
            target.write_text(original, encoding="utf-8")
        caught = result.returncode != 0
        bad += not caught
        print(f"{'caught  ' if caught else 'SURVIVED'}  {name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
