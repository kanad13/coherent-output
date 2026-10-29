"""Deterministic graders for skill trials.

A grader inspects what an agent left behind (its final response, the files in its working
directory, and which skills it loaded) and answers pass, fail, or blocked. Graders never
call a model: a skill trial is only evidence when the verdict does not depend on another
model's mood. "Blocked" means the check could not run (missing renderer), which is an
unverified result and never counts as a pass.

Each grader takes a `Run` and keyword arguments from the case file, and returns
(status, detail).
"""

from dataclasses import dataclass, field
import difflib
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parent.parent
PASS, FAIL, BLOCKED = "pass", "fail", "blocked"
OPENING = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w-]*)\s*$")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+\S")
CAPTION = re.compile(r"^\*\*Diagram( \d+)?: .+\*\*$")
VERIFIERS = {
    "mermaid": REPO / "skills/mermaid-architect/scripts/verify-markdown.py",
    "d2": REPO / "skills/d2-architect/scripts/verify-d2.py",
}


@dataclass
class Run:
    """What one trial left behind."""

    workdir: Path
    response: str = ""
    skills: set = field(default_factory=set)
    fixture: Path | None = None


def fences(text, lang):
    """Return (caption, code) for each fence of `lang`, in order.

    The caption is the nearest non-blank line above the fence, or None.
    """
    found, fence, language, lines, last = [], None, None, [], None
    for line in text.splitlines():
        if fence is None:
            opening = OPENING.match(line)
            if opening:
                fence, language, lines = opening.group(1), opening.group(2).lower(), []
            elif line.strip():
                last = line.strip()
        elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
            if language == lang:
                found.append((last, "\n".join(lines)))
            fence, last = None, None
        else:
            lines.append(line)
    return found


def markdown_texts(run):
    """Return {name: text} for the response and every Markdown file the run holds."""
    texts = {"<response>": run.response}
    for path in sorted(run.workdir.rglob("*.md")):
        if ".claude" in path.parts:
            continue
        texts[str(path.relative_to(run.workdir))] = path.read_text(encoding="utf-8", errors="replace")
    return texts


def primary_text(run, lang):
    """Pick the single text that holds the most diagrams of `lang`.

    Diagrams usually appear twice (printed and saved), so grading both would double count.
    """
    texts = markdown_texts(run)
    return max(texts.values(), key=lambda text: len(fences(text, lang)), default="")


def all_fences(run, lang):
    """Return the deduplicated diagrams of `lang` across every text, by code."""
    seen, result = set(), []
    for text in markdown_texts(run).values():
        for caption, code in fences(text, lang):
            if code not in seen:
                seen.add(code)
                result.append((caption, code))
    return result


def load_module(path, name):
    """Import a script with a hyphenated file name."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- routing -------------------------------------------------------------------------

def skill_loaded(run, skill):
    return (PASS, "") if skill in run.skills else (FAIL, f"{skill} was not loaded; loaded: {sorted(run.skills) or 'none'}")


def skill_not_loaded(run, skill):
    return (FAIL, f"{skill} was loaded but should not be") if skill in run.skills else (PASS, "")


# --- counting ------------------------------------------------------------------------

def diagram_count(run, lang, minimum=0, maximum=None):
    count = len(all_fences(run, lang))
    if count < minimum:
        return FAIL, f"{count} {lang} diagram(s); need at least {minimum}"
    if maximum is not None and count > maximum:
        return FAIL, f"{count} {lang} diagram(s); need at most {maximum}"
    return PASS, f"{count} {lang} diagram(s)"


def captions_present(run, lang):
    """Every diagram carries a bold `**Diagram: ...**` caption directly above its fence."""
    bad = [i for i, (caption, _) in enumerate(all_fences(run, lang), 1) if not (caption and CAPTION.match(caption))]
    return (FAIL, f"diagram(s) {bad} lack a `**Diagram: <insight>**` caption") if bad else (PASS, "")


# --- verification through the skill's own helper -------------------------------------

def diagrams_verify(run, lang, strict=True):
    """Run the skill's verifier over the text with the most diagrams.

    Exit 1 means a defect the skill forbids; exit 2 means the check could not run.
    """
    text = primary_text(run, lang)
    if not fences(text, lang):
        return FAIL, f"no {lang} diagrams to verify"
    with tempfile.TemporaryDirectory() as directory:
        document = Path(directory) / "trial.md"
        document.write_text(text, encoding="utf-8")
        command = [sys.executable, "-I", str(VERIFIERS[lang]), str(document)] + (["--strict"] if strict else [])
        result = subprocess.run(command, capture_output=True, text=True, timeout=600, env=os.environ.copy())
    detail = (result.stderr or result.stdout).strip()[-600:]
    if result.returncode == 0:
        return PASS, ""
    return (BLOCKED if result.returncode == 2 else FAIL), detail


# --- forbidden and required text -----------------------------------------------------

def forbidden_regex(run, lang, pattern):
    """No diagram of `lang` matches `pattern` (multiline)."""
    for number, (_, code) in enumerate(all_fences(run, lang), 1):
        if re.search(pattern, code, re.M):
            return FAIL, f"diagram {number} matches /{pattern}/"
    return PASS, ""


def required_regex(run, lang, pattern):
    """At least one diagram of `lang` matches `pattern` (multiline)."""
    if any(re.search(pattern, code, re.M) for _, code in all_fences(run, lang)):
        return PASS, ""
    return FAIL, f"no {lang} diagram matches /{pattern}/"


def response_matches(run, pattern):
    return (PASS, "") if re.search(pattern, run.response, re.I | re.S) else (FAIL, f"response does not match /{pattern}/")


def flowchart_labels_quoted(run):
    """Every flowchart node label is double-quoted (the skill's syntax rule)."""
    unquoted = re.compile(r"\w(\[(?![\"(\[/\\])|\((?![\"(\[])|\{(?![\"{]))[^\"\n]*[\]\)\}]")
    for number, (_, code) in enumerate(all_fences(run, "mermaid"), 1):
        if re.match(r"\s*(flowchart|graph)\b", code):
            for line in code.splitlines():
                if line.strip().startswith(("classDef", "style", "subgraph", "direction", "class ")):
                    continue
                if unquoted.search(line):
                    return FAIL, f"diagram {number} has an unquoted label: {line.strip()[:80]}"
    return PASS, ""


# --- ascii art ---------------------------------------------------------------------

ASCII_ART = re.compile(r"[┌┐└┘│─├┤┬┴┼╔╗╚╝║═▲▼◄►]|\+[-=]{2,}\+|^\s*\+[-=]{3,}|^\s*\|\s+\S.*\s\|\s*$", re.M)


def no_ascii_art(run):
    """Neither the response nor any Markdown file draws with ASCII or box-drawing characters.

    Mermaid fences and Markdown tables are skipped; any other fence, including `text`, is checked.
    """
    for name, text in markdown_texts(run).items():
        kept, fence, language = [], None, None
        for line in text.splitlines():
            if fence is None:
                opening = OPENING.match(line)
                if opening:
                    fence, language = opening.group(1), opening.group(2).lower()
                elif not re.match(r"^\s*\|.*\|\s*$", line):
                    kept.append(line)
            elif re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            elif language != "mermaid":
                kept.append(line)
        match = ASCII_ART.search("\n".join(kept))
        if match:
            return FAIL, f"{name} draws with ASCII art near {match.group(0)!r}"
    return PASS, ""


# --- files ---------------------------------------------------------------------------

def no_files_matching(run, pattern):
    """No file in the working directory matches the glob `pattern` (for example `*.svg`)."""
    hits = [str(p.relative_to(run.workdir)) for p in run.workdir.rglob(pattern) if ".claude" not in p.parts]
    return (FAIL, f"unexpected files: {hits}") if hits else (PASS, "")


def new_markdown_with_diagrams(run, lang, minimum=1):
    """A Markdown file that did not exist before holds at least `minimum` diagrams."""
    original = run.fixture.name if run.fixture else None
    for path in sorted(run.workdir.rglob("*.md")):
        if ".claude" in path.parts or path.name == original:
            continue
        if len(fences(path.read_text(encoding="utf-8", errors="replace"), lang)) >= minimum:
            return PASS, str(path.relative_to(run.workdir))
    return FAIL, f"no new Markdown file holds {minimum} {lang} diagram(s)"


def fixture_unchanged(run):
    """The fixture file is byte-identical to the original."""
    saved = run.workdir / run.fixture.name
    if not saved.exists():
        return FAIL, f"{run.fixture.name} is missing"
    return (PASS, "") if saved.read_bytes() == run.fixture.read_bytes() else (FAIL, f"{run.fixture.name} was modified")


def insertion_only(run, lang):
    """Existing bytes survive and the only additions are captions and `lang` fences.

    Compares line by line with the original: a replaced or deleted line fails, and every
    inserted run must consist of blank lines, `**Diagram...**` captions, and whole fences.
    """
    saved = run.workdir / run.fixture.name
    if not saved.exists():
        return FAIL, f"{run.fixture.name} is missing"
    before = run.fixture.read_bytes().decode("utf-8").splitlines(keepends=True)
    after = saved.read_bytes().decode("utf-8").splitlines(keepends=True)
    for tag, a1, a2, b1, b2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if tag in ("replace", "delete"):
            return FAIL, f"original line(s) {a1 + 1}-{a2} were changed or removed"
        if tag == "insert":
            problem = inserted_run_problem(after[b1:b2], lang)
            if problem:
                return FAIL, f"insertion at line {b1 + 1}: {problem}"
    return PASS, ""


def inserted_run_problem(lines, lang):
    """Return why an inserted run is not caption-plus-fence material, or None."""
    inside = False
    for line in lines:
        text = line.rstrip("\r\n")
        if inside:
            inside = not re.match(r"^ {0,3}`{3,}\s*$", text)
        elif not text.strip() or CAPTION.match(text.strip()):
            continue
        elif OPENING.match(text) and OPENING.match(text).group(2).lower() == lang:
            inside = True
        else:
            return f"unexpected text {text.strip()[:60]!r}"
    return "an unclosed fence" if inside else None


def every_heading_has_diagram(run, lang):
    """Each heading's section (up to the next heading) holds a `lang` diagram."""
    saved = run.workdir / run.fixture.name
    if not saved.exists():
        return FAIL, f"{run.fixture.name} is missing"
    sections, current, inside = [], None, None
    for line in saved.read_text(encoding="utf-8").splitlines():
        if inside:
            inside = None if re.match(r"^ {0,3}" + re.escape(inside) + r"{3,}\s*$", line) else inside
            continue
        opening = OPENING.match(line)
        if opening:
            if current is not None and opening.group(2).lower() == lang:
                current["diagrams"] += 1
            inside = opening.group(1)[0]
        elif HEADING.match(line):
            current = {"heading": line.strip(), "diagrams": 0}
            sections.append(current)
    missing = [s["heading"] for s in sections if not s["diagrams"]]
    return (FAIL, f"headings without a diagram: {missing}") if missing else (PASS, f"{len(sections)} headings covered")


# --- ladder --------------------------------------------------------------------------

D2_KEYWORDS = {"vars", "classes", "direction", "near", "style", "shape", "label", "class", "d2", "config"}


def top_level_count(lang, code):
    """Count the parts a diagram shows at its outermost level (a heuristic, no renderer)."""
    if lang == "mermaid":
        verifier = load_module(VERIFIERS["mermaid"], "mermaid_verifier")
        return len(verifier.parse_flowchart(code)["nodes"])
    depth, names = 0, set()
    for line in code.splitlines():
        if depth == 0:
            for name in re.findall(r"(?:^|->|<-|--)\s*([A-Za-z_][\w-]*)", line):
                if name not in D2_KEYWORDS:
                    names.add(name)
        depth += line.count("{") - line.count("}")
    return len(names)


def labels(lang, code):
    """Return the display labels a diagram defines."""
    if lang == "mermaid":
        return {part.strip().lower() for text in re.findall(r'"([^"]+)"', code) for part in text.split("<br/>") if part.strip(" ━")}
    return {m.strip().strip("\"'").lower() for m in re.findall(r"^\s*[\w.-]+\s*:\s*([^{\n]+)", code, re.M) if m.strip()}


def ladder(run, lang, first_max=7, continuity=0.6):
    """The set opens wide and later captions name a part drawn earlier.

    The first diagram has at most `first_max` top-level parts. At least `continuity` of
    the later captions mention a label from an earlier diagram, which is how the zoom
    stays traceable.
    """
    diagrams = fences(primary_text(run, lang), lang)
    if len(diagrams) < 2:
        return FAIL, f"{len(diagrams)} diagram(s): a ladder needs an overview and at least one zoom"
    count = top_level_count(lang, diagrams[0][1])
    if count > first_max:
        return FAIL, f"the first diagram shows {count} parts; an overview shows at most {first_max}"
    earlier, linked = labels(lang, diagrams[0][1]), 0
    for caption, code in diagrams[1:]:
        text = (caption or "").lower()
        if any(len(label) >= 3 and label in text for label in earlier):
            linked += 1
        earlier |= labels(lang, code)
    share = linked / (len(diagrams) - 1)
    if share < continuity:
        return FAIL, f"only {linked} of {len(diagrams) - 1} later captions name a part drawn earlier"
    return PASS, f"overview of {count} parts; {linked}/{len(diagrams) - 1} zooms traceable"


GRADERS = {
    "skill_loaded": skill_loaded,
    "skill_not_loaded": skill_not_loaded,
    "diagram_count": diagram_count,
    "captions_present": captions_present,
    "diagrams_verify": diagrams_verify,
    "forbidden_regex": forbidden_regex,
    "required_regex": required_regex,
    "response_matches": response_matches,
    "flowchart_labels_quoted": flowchart_labels_quoted,
    "no_ascii_art": no_ascii_art,
    "no_files_matching": no_files_matching,
    "new_markdown_with_diagrams": new_markdown_with_diagrams,
    "fixture_unchanged": fixture_unchanged,
    "insertion_only": insertion_only,
    "every_heading_has_diagram": every_heading_has_diagram,
    "ladder": ladder,
}
