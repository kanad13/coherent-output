# Discovery trial records

Nine producing agents started without the parent conversation. Each received an isolated skill snapshot, a task, and permitted raw artifacts. A separate reviewer inspected the instructions and actual results. The [dated report](../../DISCOVERY-EVALUATION.md) defines the criteria and records the conclusions.

Each case retains `skill.txt`, `task.txt`, `protocol.txt`, and `output.txt`. The protocol records the actual dispatch and resource limits. For interactive cases, `followup-*.txt` contains the exact simulated user replies and turn instructions; `response-*.txt` preserves the responses. `output.txt` is the final response. Additional files retain sibling snapshots, local fixtures, research completion reports, and a reproducible synthetic probe. All trial assets are hashed in the [manifest](manifest.json).

| Case                    | Input                                    | Result                                               | Scope                                                                                 |
| ----------------------- | ---------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Dining                  | [Task](dining/task.txt)                  | [Final response](dining/output.txt)                  | Three turns; changes of city and date; unavailable browsing                           |
| Local code              | [Task](code/task.txt)                    | [Final response](code/output.txt)                    | Two turns; reproduce a local failure; challenge a migration; preserve scope           |
| Reading club            | [Task](boundaries/task.txt)              | [Response](boundaries/output.txt)                    | Settled constraints and an explicit end to questioning                                |
| Live research           | [Task](live-research/task.txt)           | [Response](live-research/output.txt)                 | Primary documentation, engineering evaluation, and synthetic search checks            |
| Conflicting constraints | [Task](constraints/task.txt)             | [Final response](constraints/output.txt)             | Two turns; impossible requirement; uncertainty; unavailable named workflows           |
| Painter framing         | [Task](painter/task.txt)                 | [Guide](painter/output.txt)                          | Whole-picture writing with the bounded analogy                                        |
| Plain framing           | [Task](plain/task.txt)                   | [Guide](plain/output.txt)                            | Identical writing task with the analogy paragraph removed                             |
| Eventual recommendation | [Task](eventual-recommendation/task.txt) | [Final response](eventual-recommendation/output.txt) | Final skill; ask before an eventual recommendation, then stop when requested          |
| Workflow composition    | [Task](composition-final/task.txt)       | [Response](composition-final/output.txt)             | Final skill; live research and evaluation within 250 words, without further questions |

The first seven cases use the initial interview draft or the paired writing snapshots. The last two interview cases use the final skill after independent review. Historical snapshots remain unchanged when instructions evolve.

The [initial review](composition-final/initial-review.txt) and [final review](composition-final/final-review.txt) retain the reviewer's findings and evidence limits. Their dispatch protocols are also hashed with that case; the reviewer was separate from all producing agents.

The live research [completion record](live-research/completion.txt) distinguishes original execution from its saved rerun. Run its synthetic probe with `python3 evaluations/discovery/live-research/probe.txt` from the repository root. It uses an in-memory database and invented strings, without real notes or network calls. The [recorded output](live-research/probe-output.txt) is specific to the recorded Python/SQLite runtime.

Question tools were bypassed to keep the simulated interview away from the human. These trials assess produced dialogue and decisions; they do not establish native question-tool behavior in Codex or Antigravity. Tool-use completion records are agent reports, supported by primary sources and the independently reproduced probe, rather than complete tool transcripts.

Return to the [evidence index](../README.md) or [testing strategy](../../scripts/README.md#3-verification-strategy).
