#!/usr/bin/env python3
"""Check whether agents follow a skill's instructions, not only whether the skill parses.

A skill is a set of instructions that a model may ignore, misread, or never load. This tool
tests that, and it is meant for the moments a skill is added or edited, not for every use.

Commands:
  check   Static: rules, cases, and wording lint. Cheap; runs inside verify.sh.
  images  Render every diagram of every run to its own PNG; each must be viewed alone and
          recorded in <run>/visual.json before the case can pass.
  prepare Create run folders and prompts, so the harness that is editing the skill can
          run each case with its own fresh agents (subagents or its CLI).
  run     Same, but drive Claude Code's print mode for you.
  grade   Grade what the agents left behind.
  status  Report which skills changed since their last passing trial.

Each skill with a suite has `evals/<skill>/rules.json` (the instructions under test, each
quoted verbatim from SKILL.md), `cases.json` (tasks, each naming the rules it pressures and
the deterministic graders that judge it), and `fixtures/`. See evals/README.md.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_graders as graders  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
EVALS = REPO / "evals"
APP_BINARY = Path.home() / "Library/Application Support/Claude/claude-code"
WEAK = re.compile(r"\b(should|try to|consider|ideally|maybe|might|generally|usually|where possible|if possible|feel free)\b", re.I)
SECTION_REF = re.compile(r"\bSections? (\d+)(?:-(\d+))?")
MAX_SKILL_LINES = 240
MAX_BULLET_WORDS = 70
DEFAULT_RUNS = 3


def suites():
    """Return the names of skills that have an eval suite."""
    return sorted(p.parent.name for p in EVALS.glob("*/cases.json")) if EVALS.exists() else []


def load_suite(skill):
    """Load rules and cases for a skill. Raises ValueError on malformed files."""
    directory = EVALS / skill
    try:
        rules = json.loads((directory / "rules.json").read_text(encoding="utf-8"))
        cases = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{skill}: cannot load suite: {error}")
    return rules, cases


def skill_digest(skill):
    """Hash the skill folder and its suite, so an edit to either makes the last trial stale."""
    digest = hashlib.sha256()
    for root in (SKILLS / skill, EVALS / skill):
        for path in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "last-run.json"):
            digest.update(str(path.relative_to(REPO)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


# --- static checks -------------------------------------------------------------------

def static_problems(skill):
    """Return (errors, warnings) for one skill's suite and wording.

    Errors mean the suite no longer describes the skill (a quoted rule vanished, a rule has
    no pressure case, a Section reference points nowhere). Warnings flag wording that
    agents follow poorly; they do not fail a build.
    """
    errors, warnings = [], []
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    try:
        rules, cases = load_suite(skill)
    except ValueError as error:
        return [str(error)], warnings
    flat = re.sub(r"\s+", " ", text)
    ids = set()
    for rule in rules:
        if rule["id"] in ids:
            errors.append(f"duplicate rule id {rule['id']}")
        ids.add(rule["id"])
        if re.sub(r"\s+", " ", rule["quote"]) not in flat:
            errors.append(f"{rule['id']}: quoted text not found in SKILL.md (skill edited; update the rule or the quote): {rule['quote'][:70]!r}")
    covered = set()
    for case in cases:
        covered.update(case.get("rules", []))
        for rule_id in case.get("rules", []):
            if rule_id not in ids:
                errors.append(f"case {case['id']} names unknown rule {rule_id}")
        for name, _ in (g if isinstance(g, list) else [g, {}] for g in case["graders"]):
            if name not in graders.GRADERS:
                errors.append(f"case {case['id']} uses unknown grader {name}")
        fixture = case.get("fixture")
        if fixture and not (EVALS / skill / "fixtures" / fixture).exists():
            errors.append(f"case {case['id']} fixture {fixture} is missing")
    for rule_id in sorted(ids - covered):
        errors.append(f"{rule_id}: no case pressures this rule, so nothing would notice it being ignored")
    sections = {int(m) for m in re.findall(r"^#{2,3} (\d+)\.", text, re.M)}
    for number, end in SECTION_REF.findall(text):
        for n in range(int(number), int(end or number) + 1):
            if n not in sections:
                errors.append(f"reference to Section {n}, which does not exist (headings: {sorted(sections)})")
    lines = text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        warnings.append(f"SKILL.md has {len(lines)} lines (budget {MAX_SKILL_LINES}): long skills lose rules in the middle")
    in_code = False
    for number, line in enumerate(lines, 1):
        if line.startswith("```"):
            in_code = not in_code
        if in_code or line.startswith(("|", "#", "---")):
            continue
        for match in WEAK.finditer(line):
            warnings.append(f"line {number}: weak wording {match.group(0)!r}; state a rule, a condition, or a default")
        if re.match(r"\s*[-*\d]", line) and len(line.split()) > MAX_BULLET_WORDS:
            warnings.append(f"line {number}: {len(line.split())}-word bullet; split it so each rule can be followed alone")
    return errors, warnings


# --- running agents ------------------------------------------------------------------

def agent_command(prompt_file, workdir):
    """Build the command that runs one fresh headless agent, or raise RuntimeError.

    `COHERENT_AGENT_CMD` overrides it; the template may use {prompt_file} and {workdir}.
    The default drives Claude Code in print mode with stream-json so skill loads can be read
    back from the transcript.
    """
    template = os.environ.get("COHERENT_AGENT_CMD")
    if template:
        return shlex.split(template.format(prompt_file=prompt_file, workdir=workdir))
    binary = os.environ.get("COHERENT_CLAUDE_BIN") or shutil.which("claude")
    if not binary and APP_BINARY.exists():
        found = sorted(APP_BINARY.glob("*/*/claude.app/Contents/MacOS/claude"))
        binary = str(found[-1]) if found else None
    if not binary:
        raise RuntimeError("no agent CLI: install Claude Code, or set COHERENT_CLAUDE_BIN or COHERENT_AGENT_CMD")
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    return [binary, "-p", prompt, "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
            "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep,Skill,WebFetch"]


def parse_transcript(path):
    """Return (final response, set of skills loaded) from a stream-json transcript."""
    response, skills = "", set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result" and isinstance(event.get("result"), str):
            response = event["result"]
        for block in (event.get("message") or {}).get("content", []) if isinstance(event.get("message"), dict) else []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            args = block.get("input") or {}
            if block.get("name") == "Skill" and args.get("skill"):
                skills.add(str(args["skill"]).split(":")[-1])
            found = re.search(r"/skills/([\w-]+)/SKILL\.md", str(args.get("file_path", "")))
            if found:
                skills.add(found.group(1))
    return response, skills


def run_case(skill, case, run_dir, timeout):
    """Run one fresh agent on one case, leaving workdir/, transcript.jsonl and response.md."""
    workdir = run_dir / "workdir"
    workdir.mkdir(parents=True)
    fixture = case.get("fixture")
    if fixture:
        shutil.copy(EVALS / skill / "fixtures" / fixture, workdir / fixture)
    prompt_file = run_dir / "prompt.txt"
    prompt_file.write_text(case["prompt"], encoding="utf-8")
    command = agent_command(prompt_file, workdir)
    with (run_dir / "transcript.jsonl").open("w", encoding="utf-8") as sink:
        try:
            subprocess.run(command, cwd=workdir, stdout=sink, stderr=subprocess.STDOUT, timeout=timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            sink.write('\n{"type":"timeout"}\n')
    response, _ = parse_transcript(run_dir / "transcript.jsonl")
    (run_dir / "response.md").write_text(response, encoding="utf-8")


# --- grading -------------------------------------------------------------------------

def load_run(skill, case, run_dir):
    """Rebuild a graders.Run from a run directory."""
    transcript = run_dir / "transcript.jsonl"
    response, skills = parse_transcript(transcript) if transcript.exists() else ("", set())
    saved = run_dir / "response.md"
    if saved.exists() and saved.read_text(encoding="utf-8").strip():
        response = saved.read_text(encoding="utf-8")
    loaded = run_dir / "skills.txt"
    if loaded.exists():
        skills |= set(loaded.read_text(encoding="utf-8").split())
    fixture = EVALS / skill / "fixtures" / case["fixture"] if case.get("fixture") else None
    return graders.Run(workdir=run_dir / "workdir", response=response, skills=skills, fixture=fixture)


DEAD_RUN = re.compile(r"not logged in|please run /login|invalid api key|credit balance|rate limit|usage limit|authentication", re.I)


def run_problem(run, run_dir):
    """Return why a run did not happen, or None.

    A run that never reached the model would otherwise pass every "should not" check, which
    is how a negative case turns into a false pass.
    """
    transcript = run_dir / "transcript.jsonl"
    if transcript.exists() and '"type":"timeout"' in transcript.read_text(encoding="utf-8", errors="replace"):
        return "the agent timed out"
    head = run.response.strip()[:300]
    if DEAD_RUN.search(head) and len(run.response) < 400:
        return f"the agent never ran: {head!r}"
    if not head and not any(run.workdir.rglob("*.md")):
        return "the agent left no response and no files"
    return None


def visual_verdict(case, run_dir):
    """Judge the recorded visual review of a run's diagram images, or None when not required.

    Compilation and structure checks cannot see overlap, clipping, or a crowded picture, so a
    diagram case is not done until every rendered image has been viewed on its own and
    recorded in visual.json as "pass" or "fail: reason". A missing image, a missing record, or
    an unlisted image is blocked, never a pass.
    """
    if case.get("visual") is False:
        return None
    folder = run_dir / "images"
    images = sorted(path.relative_to(folder).as_posix() for path in folder.rglob("diagram-*.png")) if folder.exists() else []
    if not images:
        return ("visual_review", graders.BLOCKED, "no images: run `skill_evals.py images`, then view each image alone and record it in visual.json")
    try:
        review = json.loads((run_dir / "visual.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        review = {}
    missing = [name for name in images if name not in review]
    if missing:
        return ("visual_review", graders.BLOCKED, f"{len(missing)} of {len(images)} image(s) not reviewed, for example {missing[0]}")
    failed = {name: note for name, note in review.items() if name in images and not str(note).strip().lower().startswith("pass")}
    if failed:
        name, note = next(iter(failed.items()))
        return ("visual_review", graders.FAIL, f"{len(failed)} image(s) failed review, for example {name}: {note}")
    return ("visual_review", graders.PASS, f"{len(images)} image(s) viewed")


def grade_run(skill, case, run_dir):
    """Return a list of (grader, status, detail) for one run."""
    run = load_run(skill, case, run_dir)
    problem = run_problem(run, run_dir)
    if problem:
        return [("agent_ran", graders.BLOCKED, problem)]
    verdicts = []
    for spec in case["graders"]:
        name, arguments = (spec[0], spec[1]) if isinstance(spec, list) else (spec, {})
        try:
            status, detail = graders.GRADERS[name](run, **arguments)
        except Exception as error:  # a crashing grader is a blocked check, never a pass
            status, detail = graders.BLOCKED, f"grader crashed: {error}"
        verdicts.append((name, status, detail))
    visual = visual_verdict(case, run_dir)
    if visual:
        verdicts.append(visual)
    return verdicts


def case_outcome(runs, needed):
    """Combine run verdicts: pass when enough runs pass every grader, blocked if any grader was blocked and not enough passed."""
    passed = sum(all(s == graders.PASS for _, s, _ in verdicts) for verdicts in runs)
    if passed >= needed:
        return "pass", passed
    blocked = any(s == graders.BLOCKED for verdicts in runs for _, s, _ in verdicts)
    return ("blocked" if blocked else "fail"), passed


def grade_skill(skill, out, selected=None):
    """Grade every case directory under out/skill. Returns (report text, all_passed, results)."""
    rules, cases = load_suite(skill)
    results, lines = {}, [f"# Skill trial: {skill}", ""]
    lines += ["| Case | Runs | Passed | Outcome |", "| :-- | --: | --: | :-- |"]
    details = []
    for case in cases:
        if selected and case["id"] not in selected:
            continue
        case_dir = out / skill / case["id"]
        run_dirs = sorted(p for p in case_dir.glob("run-*") if p.is_dir()) if case_dir.exists() else []
        if not run_dirs:
            continue
        graded = [grade_run(skill, case, d) for d in run_dirs]
        needed = math.ceil(len(graded) * 2 / 3)
        outcome, passed = case_outcome(graded, needed)
        results[case["id"]] = (outcome, passed, len(graded))
        lines.append(f"| {case['id']} | {len(graded)} | {passed} | {outcome} |")
        for number, verdicts in enumerate(graded, 1):
            for name, status, detail in verdicts:
                if status != graders.PASS:
                    details.append(f"- `{case['id']}` run {number}: **{status}** {name}: {detail}")
    lines += ["", "## Failures and blocked checks", ""] + (details or ["None."])
    lines += ["", "## Rules", "", "| Rule | Line in SKILL.md | Cases | Result |", "| :-- | --: | :-- | :-- |"]
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    for rule in rules:
        line = next((i for i, l in enumerate(text.splitlines(), 1) if rule["quote"][:40] in l), 0)
        mine = [(c["id"], results[c["id"]][0]) for c in cases if rule["id"] in c.get("rules", []) and c["id"] in results]
        verdict = "not run" if not mine else ("pass" if all(o == "pass" for _, o in mine) else "FAIL: " + ", ".join(c for c, o in mine if o != "pass"))
        lines.append(f"| {rule['id']} | {line} | {', '.join(c for c, _ in mine) or '-'} | {verdict} |")
    ran = [r for r in results.values()]
    return "\n".join(lines), bool(ran) and all(outcome == "pass" for outcome, _, _ in ran), results


def write_stamp(skill, results, out):
    """Record a passing trial against the skill's current digest."""
    stamp = {"digest": skill_digest(skill), "cases": {k: {"outcome": o, "passed": p, "runs": n} for k, (o, p, n) in results.items()}}
    (EVALS / skill / "last-run.json").write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8")


# --- commands ------------------------------------------------------------------------

def command_check(args):
    status = 0
    for skill in args.skills or suites():
        errors, warnings = static_problems(skill)
        for message in errors:
            print(f"{skill}: ERROR {message}", file=sys.stderr)
        for message in warnings:
            print(f"{skill}: warning {message}")
        status = status or int(bool(errors))
        if not errors:
            print(f"{skill}: suite consistent ({len(warnings)} wording warning(s))")
    return status


def command_images(args):
    """Render every diagram of every graded run to its own PNG, and list them for review."""
    out = Path(args.out)
    _, cases = load_suite(args.skill)
    by_id = {c["id"]: c for c in cases}
    listed = 0
    for run_dir in sorted((out / args.skill).glob("*/run-*")):
        case = by_id.get(run_dir.parent.name)
        if not case or case.get("visual") is False:
            continue
        run = load_run(args.skill, case, run_dir)
        folder = run_dir / "images"
        shutil.rmtree(folder, ignore_errors=True)
        index = [f"# Images for {run_dir.parent.name} {run_dir.name}", ""]
        for lang in ("mermaid", "d2"):
            text = graders.primary_text(run, lang)
            found = graders.fences(text, lang)
            if not found:
                continue
            with tempfile.TemporaryDirectory() as scratch:
                document = Path(scratch) / "doc.md"
                document.write_text(text, encoding="utf-8")
                verifier = str(graders.VERIFIERS[lang])
                if lang == "mermaid":
                    command = [sys.executable, "-I", verifier, str(document), "--png", str(folder / lang)]
                else:
                    palette = str(SKILLS / "d2-architect/assets/house-palette.d2")
                    command = [sys.executable, "-I", verifier, str(document), "--sheet", str(folder / lang), "--palette", palette]
                subprocess.run(command, capture_output=True, text=True, timeout=900, env=os.environ.copy())
            for number, (caption, _) in enumerate(found, 1):
                image = folder / lang / f"diagram-{number}.png"
                if image.exists():
                    index.append(f"- `{lang}/diagram-{number}.png`: {caption}")
                    print(image)
                    listed += 1
        (run_dir / "images").mkdir(exist_ok=True)
        (run_dir / "images" / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\n{listed} image(s). View each one alone, then write <run>/visual.json as {{\"<lang>/diagram-N.png\": \"pass\" or \"fail: reason\"}} for every image.")
    return 0 if listed else 2


def command_prepare(args):
    """Create run folders for the selected cases and print each prompt with its folder."""
    out = Path(args.out or tempfile.mkdtemp(prefix="skill-trials-"))
    _, cases = load_suite(args.skill)
    chosen = [c for c in cases if (not args.case or c["id"] in args.case) and (args.all or args.case or c.get("tier") == "smoke")]
    manifest = []
    for case in chosen:
        for number in range(1, (args.runs or 1) + 1):
            run_dir = out / args.skill / case["id"] / f"run-{number}"
            (run_dir / "workdir").mkdir(parents=True, exist_ok=True)
            if case.get("fixture"):
                shutil.copy(EVALS / args.skill / "fixtures" / case["fixture"], run_dir / "workdir" / case["fixture"])
            (run_dir / "prompt.txt").write_text(case["prompt"], encoding="utf-8")
            manifest.append({"case": case["id"], "run": str(run_dir), "prompt": case["prompt"]})
    (out / args.skill / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"\nFor each run: start a fresh agent with the prompt, working only in <run>/workdir. It writes its final reply to <run>/response.md and the skills it loaded to <run>/skills.txt. Then: python3 scripts/skill_evals.py grade {args.skill} --out {out}")
    return 0


def command_run(args):
    out = Path(args.out or tempfile.mkdtemp(prefix="skill-trials-"))
    rules, cases = load_suite(args.skill)
    chosen = [c for c in cases if (not args.case or c["id"] in args.case) and (args.all or args.case or c.get("tier") == "smoke")]
    if not chosen:
        print("No cases selected; use --all or --case.", file=sys.stderr)
        return 1
    try:
        agent_command(Path("/dev/null"), Path("."))
    except RuntimeError as error:
        print(f"Trials unavailable: {error}", file=sys.stderr)
        return 2
    for case in chosen:
        for number in range(1, (args.runs or DEFAULT_RUNS) + 1):
            run_dir = out / args.skill / case["id"] / f"run-{number}"
            if run_dir.exists():
                continue
            print(f"running {case['id']} #{number} ...", flush=True)
            run_case(args.skill, case, run_dir, args.timeout)
    print(f"Results in {out}")
    return finish_grade(args.skill, out, {c["id"] for c in chosen}, args.stamp, partial=not args.all)


def finish_grade(skill, out, selected, stamp, partial):
    report, ok, results = grade_skill(skill, out, selected)
    print(report)
    if stamp and ok and not partial:
        write_stamp(skill, results, out)
        print(f"\nStamped {skill} at digest {skill_digest(skill)}.")
    elif stamp:
        print("\nNot stamped: a stamp needs every case to pass in a full run (--all).")
    if any(o == "blocked" for o, _, _ in results.values()):
        return 2
    return 0 if ok else 1


def command_grade(args):
    return finish_grade(args.skill, Path(args.out), None, args.stamp, partial=False)


def command_status(args):
    stale = 0
    for skill in suites():
        path = EVALS / skill / "last-run.json"
        try:
            recorded = json.loads(path.read_text(encoding="utf-8"))["digest"]
        except (OSError, KeyError, json.JSONDecodeError):
            recorded = None
        if recorded == skill_digest(skill):
            print(f"{skill}: trial current")
        else:
            stale += 1
            reason = "never trialled" if recorded is None else "changed since the last passing trial"
            print(f"{skill}: STALE ({reason}); run `python3 scripts/skill_evals.py prepare {skill} --all`, start an agent per folder, view each image, then `grade --stamp` (see evals/README.md)")
    return 1 if (stale and args.require_fresh) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="static suite and wording checks")
    check.add_argument("skills", nargs="*")
    prepare = sub.add_parser("prepare", help="create run folders for the harness to run with its own agents")
    prepare.add_argument("skill")
    prepare.add_argument("--case", action="append")
    prepare.add_argument("--all", action="store_true")
    prepare.add_argument("--runs", type=int, help="runs per case (default 1)")
    prepare.add_argument("--out")
    images = sub.add_parser("images", help="render each graded diagram to its own PNG for review")
    images.add_argument("skill")
    images.add_argument("--out", required=True)
    run = sub.add_parser("run", help="run fresh agents on the cases, then grade")
    run.add_argument("skill")
    run.add_argument("--case", action="append", help="run only this case (repeatable)")
    run.add_argument("--all", action="store_true", help="every case, not just the smoke tier")
    run.add_argument("--runs", type=int, help=f"runs per case (default {DEFAULT_RUNS})")
    run.add_argument("--out", help="results directory (default: a new temporary one outside the checkout)")
    run.add_argument("--timeout", type=int, default=1200, help="seconds per run")
    run.add_argument("--stamp", action="store_true", help="record the digest when a full run passes")
    grade = sub.add_parser("grade", help="grade results produced elsewhere")
    grade.add_argument("skill")
    grade.add_argument("--out", required=True)
    grade.add_argument("--stamp", action="store_true")
    status = sub.add_parser("status", help="which skills changed since their last passing trial")
    status.add_argument("--require-fresh", action="store_true")
    args = parser.parse_args()
    return {"check": command_check, "prepare": command_prepare, "images": command_images, "run": command_run, "grade": command_grade, "status": command_status}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
