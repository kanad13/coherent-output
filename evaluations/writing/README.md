# Writing trial records

Each directory contains `skill.txt`, `task.txt`, and `output.txt`. These are the isolated skill snapshot, supplied task, and actual saved result. The [evaluation record](../../SKILL-EVALUATION.md) explains criteria, outcomes, and limitations.

To repeat a trial, copy `skill.txt` to `SKILL.md` in a disposable directory and provide that file plus `task.txt` to a fresh agent with no conversation history. Allow it to save and inspect its output. Do not provide the desired answer or reviewer rubric. Compare the saved result with the task after any active hooks or formatters.

The native-probe directory records valid and invalid Codex patch results. The invalid edit produced failure feedback after its side effect. These records do not substitute for exercising another native host.

The mermaid-final trial also retains its original source, inserted block, diagram, helper snapshots, and completion report. To repeat it, copy `baseline.txt` to `source.md`, restore the two helper snapshots under `scripts/` with their original filenames, and make `verify-mmdc.sh` executable. Provision the skill's pinned renderer before starting the fresh agent. Its task requires native patch application so post-edit formatting participates in the preservation check.

The files use a plain-text extension to preserve observed formatting exactly. Keep the initially failed cognitive trial alongside the successful rerun.

Git attributes disable line-ending conversion for these raw `.txt` files and permit intentional blank insertion separators at end of file. Other whitespace checks remain enabled. See [Git attributes](https://git-scm.com/docs/gitattributes).

Retain these records as regression evidence, not installed skill resources. The suite checks the manifest's recorded hashes and requires every writing trial to remain indexed. When behavior changes, add a new trial rather than rewriting an earlier result. Installers distribute `skills/`; this archive stays in the source repository.
