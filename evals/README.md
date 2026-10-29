# Skill trials

These suites test whether agents follow a skill's instructions. A skill can parse, install, and still be ignored: the model may never load it, may skip a rule, or may misread a rule that is badly placed or worded. Run these checks when a skill is added or edited. They do not run each time a skill is used.

## 0. When to run

Every time a skill is added or edited, activate `test-strategist` for that skill. It reviews the skill's existing tests, finds the instructions that no case pressures, and adds cases and graders. Then run `check` (free), the trial (`run <skill> --all --stamp`), and `python3 scripts/sabotage_check.py` if graders or helpers changed. `verify.sh` marks a skill `STALE` until its trial has passed against the current text. A trial that cannot run because no agent CLI is logged in is reported as blocked, not as a pass.

## 1. What is tested

| Question                                 | Check                                                                                                                                                                                                                                                       | Cost                      |
| :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------ |
| Does the suite still describe the skill? | Every rule is a verbatim quote of `SKILL.md`; every rule has a case that pressures it; every `Section N` reference resolves.                                                                                                                                | Free, in `verify.sh`      |
| Is the wording easy to follow?           | Warnings for weak modals ("should", "consider"), bullets over 70 words, and files over 240 lines.                                                                                                                                                           | Free, in `verify.sh`      |
| Does the right skill load?               | Routing cases check which skills the agent loaded: automatic, explicit-only, and handoff.                                                                                                                                                                   | Model runs                |
| Does the output obey the rules?          | Deterministic graders run the skill's own verifier and check bytes, captions, counts, ladder shape, and forbidden text.                                                                                                                                     | Model runs                |
| Is a rule ignored, or just badly placed? | The report lists each rule with its line in `SKILL.md` and its result. Failures that cluster late in the file or in long bullets point at wording, not at the model.                                                                                        | Model runs                |
| Does each picture look right?            | `images` renders every diagram of every run to its own PNG. The reviewer views each PNG alone (never a long page of diagrams) and records `pass` or `fail: reason` per image in `<run>/visual.json`. A case with unreviewed or failed images does not pass. | Model runs and a reviewer |
| Is a failure luck?                       | Each case runs three times; it passes when at least two runs pass every grader.                                                                                                                                                                             | Model runs                |

A run where the agent never ran (login failure, timeout, empty output) is reported as **blocked**, never as a pass. Without this, every "should not" case passes on a dead agent.

## 2. Commands

```bash
python3 scripts/skill_evals.py check                 # static; also runs in verify.sh
python3 scripts/skill_evals.py status                # which skills changed since their last passing trial
python3 scripts/skill_evals.py prepare mermaid-architect --all --runs 3 # then run an agent per folder
python3 scripts/skill_evals.py images mermaid-architect --out <dir>      # one PNG per diagram; view each, write visual.json
python3 scripts/skill_evals.py grade mermaid-architect --out <dir> --stamp
python3 scripts/skill_evals.py grade d2-architect --out <results-dir>
```

- **Who runs trials:** the harness that is adding or editing the skill. Skills must work in every harness; testing them does not. `prepare` creates one folder per run (fixture copied into `workdir/`, prompt in `prompt.txt`). The harness starts a fresh agent per folder with only the prompt, using its own agent facility (subagents, or its CLI). Each agent writes its final reply to `response.md` and the skills it loaded to `skills.txt`. Then `images` renders each diagram to its own PNG, and the reviewer views them one at a time and records the verdicts in `visual.json` (a case that produces no diagrams is marked `"visual": false`). `grade` then judges the folders. `run` is optional automation that drives Claude Code's print mode (it needs a logged-in `claude`; `COHERENT_AGENT_CMD` replaces the command).
- **Renderers:** graders call each skill's own verifier. Set `COHERENT_D2_RENDERER_URL` to a running d2-renderer service (`http://localhost:8080`) or provision D2 as the skill describes. An unavailable renderer blocks the check; it does not pass it.
- **Results:** `run` writes `<out>/<skill>/<case>/run-<n>/` with `workdir/`, `transcript.jsonl`, and `response.md`. The default location is a new temporary folder outside the checkout. `grade` accepts results made by another host: add `response.md`, a `workdir/`, and a `skills.txt` that lists the skills loaded.
- **Stamp:** a full passing run writes `evals/<skill>/last-run.json` with a digest of the skill folder and its suite. `status` compares digests, so any later edit marks the trial stale. Commit the stamp with the skill change it covers.
- **Smoke tier:** cases marked `"tier": "smoke"` run by default. Use `--all` before a stamp.

## 3. Adding a skill suite

1. Create `evals/<skill>/rules.json`: one entry per instruction worth testing, `{"id": "...", "quote": "..."}`, where `quote` is copied exactly from `SKILL.md`. Pick instructions where a model's habit pulls the other way, such as limits, handoffs, preservation, and forbidden content.
2. Create `evals/<skill>/cases.json`. Each case has an `id`, a `prompt` that gives the agent no hint about the rule, the `rules` it pressures, and `graders`: `[name, {arguments}]` pairs from `scripts/skill_graders.py`. Add a `fixture` file under `evals/<skill>/fixtures/` when the task edits or reads a document.
3. Include at least one routing case that must not load the skill, and one case that pushes against a rule (a request for icons for the D2 skill; a concept of 18 parts for the 10-node limit).
4. Add a grader to `skill_graders.py` only for a check no existing grader covers, and add a passing and a failing example to `scripts/test_skill_evals.py`. A grader that cannot fail proves nothing.
5. Run `check`, then `run --all`, and read the output files of at least one run. A passing grader shows that its rule held in that run; it does not show that every output is good.

## 4. Known weaknesses found by trials

- **d2-architect, boundary views:** a container holding many boxes, with labelled edges leaving it, repeatedly produced labels that collide with the container border or a ragged stack of boxes (`source-not-target`, two of three runs). Candidate fix: draw the container with only the parts that touch the outside, and give edges that leave it one word or no label.
- **d2-architect, zoom captions:** the caption sometimes still omits the opened part's label (`concept-set`, one of three runs), even with an example in the skill.
- **mermaid-architect, overviews:** one run drew a tangled overview with a line through a label (`ladder-big`, one of three runs).
- **Visual review is a judgment:** verdicts follow one standard (fail: clipped or overlapped text, a line or border through a label, sprawl, a backwards flow; pass with a note: cramped but legible). Another reviewer may draw the line differently, so keep the `visual.json` notes.

## 5. Limits

- Graders judge structure and rules. They do not judge whether a diagram explains its subject well; read a sample of the outputs.
- Three runs per case show instability, not a rate. Raise `--runs` for a rule that fails intermittently.
- Rule-effect testing (running the same case with one rule removed) is not built. To do it by hand, copy the skill under another name without the rule, deny the original skill, and compare pass rates.
- Trials run the agent with the user's own settings and instructions, in a temporary working folder, with an allowlist of tools. They do not sandbox the machine.
