"""Check the skill-trial framework itself, offline and without a model.

A grader that cannot fail proves nothing, so each grader is run against output that must
pass and against output that breaks the rule it guards. The suite checks run against the
real `evals/` folders, so editing a skill without updating its rules fails the build.
"""

import json
from pathlib import Path
import tempfile
import unittest

import skill_evals as evals
import skill_graders as graders

ORIGINAL = "# Title\n\nIntro.\n\n## Part\n\nBody.\n"
DIAGRAM = '**Diagram: A feeds B**\n\n```mermaid\nflowchart LR\nA["Alpha"] --> B["Beta"]\n```\n'
GOOD = "# Title\n\nIntro.\n\n" + DIAGRAM + "\n## Part\n\nBody.\n\n" + DIAGRAM


def make_run(directory, saved=None, response="", skills=(), original=ORIGINAL):
    """Create a run directory with a fixture and the file the agent left behind."""
    root = Path(directory)
    fixture = root / "original" / "doc.md"
    fixture.parent.mkdir(exist_ok=True)
    fixture.write_text(original, encoding="utf-8")
    work = root / "workdir"
    work.mkdir(exist_ok=True)
    if saved is not None:
        (work / "doc.md").write_text(saved, encoding="utf-8")
    return graders.Run(workdir=work, response=response, skills=set(skills), fixture=fixture)


class Graders(unittest.TestCase):
    def verdict(self, name, run, **arguments):
        return graders.GRADERS[name](run, **arguments)[0]

    def test_insertion_only_accepts_captions_and_fences_and_rejects_edits(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("insertion_only", make_run(d, GOOD), lang="mermaid"), graders.PASS)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("insertion_only", make_run(d, GOOD.replace("Intro.", "Introduction.")), lang="mermaid"), graders.FAIL)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("insertion_only", make_run(d, GOOD.replace("Body.\n", "Body.\n\nA summary sentence.\n", 1)), lang="mermaid"), graders.FAIL)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("insertion_only", make_run(d, None), lang="mermaid"), graders.FAIL)

    def test_every_heading_needs_its_own_diagram(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("every_heading_has_diagram", make_run(d, GOOD), lang="mermaid"), graders.PASS)
        with tempfile.TemporaryDirectory() as d:
            only_first = "# Title\n\nIntro.\n\n" + DIAGRAM + "\n## Part\n\nBody.\n"
            self.assertEqual(self.verdict("every_heading_has_diagram", make_run(d, only_first), lang="mermaid"), graders.FAIL)

    def test_fixture_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("fixture_unchanged", make_run(d, ORIGINAL)), graders.PASS)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("fixture_unchanged", make_run(d, ORIGINAL + "x\n")), graders.FAIL)

    def test_captions(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("captions_present", make_run(d, response=DIAGRAM), lang="mermaid"), graders.PASS)
            self.assertEqual(self.verdict("captions_present", make_run(d, response="## Heading\n\n```mermaid\nflowchart LR\nA-->B\n```\n"), lang="mermaid"), graders.FAIL)
            numbered = DIAGRAM.replace("Diagram:", "Diagram 2:")
            self.assertEqual(self.verdict("captions_present", make_run(d, response=numbered), lang="mermaid"), graders.PASS)

    def test_routing(self):
        with tempfile.TemporaryDirectory() as d:
            run = make_run(d, skills=["mermaid-architect"])
            self.assertEqual(self.verdict("skill_loaded", run, skill="mermaid-architect"), graders.PASS)
            self.assertEqual(self.verdict("skill_loaded", run, skill="d2-architect"), graders.FAIL)
            self.assertEqual(self.verdict("skill_not_loaded", run, skill="d2-architect"), graders.PASS)
            self.assertEqual(self.verdict("skill_not_loaded", run, skill="mermaid-architect"), graders.FAIL)

    def test_forbidden_and_required_text(self):
        block = "```d2\nx: X { icon: ./x.svg }\n```\n"
        with tempfile.TemporaryDirectory() as d:
            run = make_run(d, response=block)
            self.assertEqual(self.verdict("forbidden_regex", run, lang="d2", pattern=r"icon\s*:"), graders.FAIL)
            self.assertEqual(self.verdict("forbidden_regex", run, lang="d2", pattern=r"shape\s*:\s*image"), graders.PASS)
            self.assertEqual(self.verdict("required_regex", run, lang="d2", pattern=r"icon"), graders.PASS)
            self.assertEqual(self.verdict("required_regex", run, lang="d2", pattern=r"cylinder"), graders.FAIL)

    def test_unquoted_flowchart_labels_fail(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.verdict("flowchart_labels_quoted", make_run(d, response=DIAGRAM)), graders.PASS)
            bad = "```mermaid\nflowchart LR\nA[Alpha] --> B[Beta]\n```\n"
            self.assertEqual(self.verdict("flowchart_labels_quoted", make_run(d, response=bad)), graders.FAIL)
            shapes = '```mermaid\nflowchart LR\nA(["Alpha"]) --> B[("Beta")] --> C{{"Gamma"}} --> D[["Delta"]]\n```\n'
            self.assertEqual(self.verdict("flowchart_labels_quoted", make_run(d, response=shapes)), graders.PASS)

    def test_ladder_needs_a_narrow_overview_and_traceable_zooms(self):
        def doc(*pairs):
            return "\n".join(f"**Diagram: {caption}**\n\n```mermaid\n{code}\n```\n" for caption, code in pairs)
        overview = 'flowchart LR\nS["Storefront"] --> O["Order Service"] --> P["Payments"]'
        zoom = 'flowchart LR\nI["Intake"] --> F["Fulfilment"]'
        wide = "flowchart LR\n" + "\n".join(f'N{i}["Part {i}"] --> N{i + 1}["Part {i + 1}"]' for i in range(0, 16, 2))
        with tempfile.TemporaryDirectory() as d:
            good = make_run(d, response=doc(("The shop has three parts", overview), ("Order Service splits intake from fulfilment", zoom)))
            self.assertEqual(self.verdict("ladder", good, lang="mermaid"), graders.PASS)
            unrelated = make_run(d, response=doc(("The shop has three parts", overview), ("Something else entirely", zoom)))
            self.assertEqual(self.verdict("ladder", unrelated, lang="mermaid"), graders.FAIL)
            too_wide = make_run(d, response=doc(("Everything at once", wide), ("Order Service splits", zoom)))
            self.assertEqual(self.verdict("ladder", too_wide, lang="mermaid"), graders.FAIL)
            single = make_run(d, response=doc(("The shop has three parts", overview)))
            self.assertEqual(self.verdict("ladder", single, lang="mermaid"), graders.FAIL)

    def test_new_markdown_file_and_stray_images(self):
        with tempfile.TemporaryDirectory() as d:
            run = make_run(d, ORIGINAL)
            self.assertEqual(self.verdict("new_markdown_with_diagrams", run, lang="d2"), graders.FAIL)
            (run.workdir / "shop-diagrams.md").write_text("**Diagram 1: A**\n\n```d2\na -> b\n```\n", encoding="utf-8")
            self.assertEqual(self.verdict("new_markdown_with_diagrams", run, lang="d2"), graders.PASS)
            self.assertEqual(self.verdict("no_files_matching", run, pattern="*.svg"), graders.PASS)
            (run.workdir / "a.svg").write_text("<svg/>", encoding="utf-8")
            self.assertEqual(self.verdict("no_files_matching", run, pattern="*.svg"), graders.FAIL)


class DeadRuns(unittest.TestCase):
    """A run that never reached the model must be blocked, never a pass."""

    def test_login_failure_is_blocked_even_for_a_should_not_case(self):
        case = {"id": "x", "prompt": "p", "graders": [["skill_not_loaded", {"skill": "d2-architect"}]]}
        with tempfile.TemporaryDirectory() as d:
            run_dir = Path(d) / "run-1"
            (run_dir / "workdir").mkdir(parents=True)
            (run_dir / "response.md").write_text("Not logged in · Please run /login", encoding="utf-8")
            verdicts = evals.grade_run("d2-architect", case, run_dir)
        self.assertEqual([v[1] for v in verdicts], [graders.BLOCKED])
        self.assertEqual(evals.case_outcome([verdicts, verdicts, verdicts], 2)[0], "blocked")

    def test_empty_run_is_blocked(self):
        case = {"id": "x", "prompt": "p", "graders": [["skill_not_loaded", {"skill": "d2-architect"}]]}
        with tempfile.TemporaryDirectory() as d:
            run_dir = Path(d) / "run-1"
            (run_dir / "workdir").mkdir(parents=True)
            self.assertEqual(evals.grade_run("d2-architect", case, run_dir)[0][1], graders.BLOCKED)


class Transcripts(unittest.TestCase):
    def test_skill_loads_and_final_response_are_read_back(self):
        events = [
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "mermaid-architect"}}]}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "/h/.claude/skills/d2-architect/SKILL.md"}}]}},
            {"type": "result", "result": "Done."},
        ]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in events) + "\nnot json\n", encoding="utf-8")
            response, skills = evals.parse_transcript(path)
        self.assertEqual(response, "Done.")
        self.assertEqual(skills, {"mermaid-architect", "d2-architect"})

    def test_case_outcome_needs_two_of_three_and_never_counts_blocked_as_pass(self):
        ok = [("g", graders.PASS, "")]
        bad = [("g", graders.FAIL, "")]
        blocked = [("g", graders.BLOCKED, "")]
        self.assertEqual(evals.case_outcome([ok, ok, bad], 2)[0], "pass")
        self.assertEqual(evals.case_outcome([ok, bad, bad], 2)[0], "fail")
        self.assertEqual(evals.case_outcome([ok, blocked, bad], 2)[0], "blocked")


class SuiteChecks(unittest.TestCase):
    """Run the static checks on the real suites, then on deliberately broken copies."""

    def test_every_real_suite_is_consistent(self):
        self.assertTrue(evals.suites(), "no suites found")
        for skill in evals.suites():
            with self.subTest(skill=skill):
                self.assertEqual(evals.static_problems(skill)[0], [])

    def test_broken_suites_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "skills/demo").mkdir(parents=True)
            (root / "evals/demo/fixtures").mkdir(parents=True)
            (root / "skills/demo/SKILL.md").write_text("# Demo\n\n## 1. Rules\n\nAlways say yes. You should see Section 4.\n", encoding="utf-8")
            rules = [{"id": "R1", "quote": "Always say yes."}, {"id": "R2", "quote": "Never say no."}, {"id": "R3", "quote": "Always say yes."}]
            cases = [{"id": "c1", "prompt": "p", "rules": ["R1", "R9"], "graders": [["skill_loaded", {"skill": "demo"}], "no_such_grader"]}]
            (root / "evals/demo/rules.json").write_text(json.dumps(rules), encoding="utf-8")
            (root / "evals/demo/cases.json").write_text(json.dumps(cases), encoding="utf-8")
            saved = evals.SKILLS, evals.EVALS
            evals.SKILLS, evals.EVALS = root / "skills", root / "evals"
            try:
                errors, warnings = evals.static_problems("demo")
            finally:
                evals.SKILLS, evals.EVALS = saved
        text = "\n".join(errors)
        self.assertIn("R2: quoted text not found", text)
        self.assertIn("R3: no case pressures", text)
        self.assertIn("unknown rule R9", text)
        self.assertIn("unknown grader no_such_grader", text)
        self.assertIn("Section 4, which does not exist", text)
        self.assertTrue(any("should" in w for w in warnings))

    def test_digest_changes_when_the_skill_changes(self):
        skill = evals.suites()[0]
        path = evals.SKILLS / skill / "SKILL.md"
        original = path.read_bytes()
        before = evals.skill_digest(skill)
        try:
            path.write_bytes(original + b"\n")
            self.assertNotEqual(before, evals.skill_digest(skill))
        finally:
            path.write_bytes(original)
        self.assertEqual(before, evals.skill_digest(skill))


if __name__ == "__main__":
    unittest.main()
