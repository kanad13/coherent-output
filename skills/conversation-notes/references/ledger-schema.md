# Atomic Conversation Ledger Schema

When synthesizing extensive multi-turn conversations into standalone reference documentation, use this schema to capture all contributions before drafting.

---

## 1. Ledger Schema

Assign stable identifiers (`A001`, `A002`, `A003`, ...) to every atomic contribution:

| Field              | Description                            | Allowed Values / Examples                                                                                                                                                              |
| :----------------- | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Atomic ID**      | Stable unique identifier               | `A001`, `A002`, `A003`                                                                                                                                                                 |
| **Turn**           | Message number or origin index         | `Turn 1`, `Turn 3`                                                                                                                                                                     |
| **Source**         | Originating speaker or tool            | `User`, `Assistant`, `Tool: run_command`, `File`                                                                                                                                       |
| **Type**           | Conceptual classification              | `Question`, `Objective`, `Fact`, `Claim`, `Definition`, `Explanation`, `Example`, `Analogy`, `Constraint`, `Objection`, `Correction`, `Decision`, `Action`, `Failure`, `Open Question` |
| **Atomic Content** | Exact substantive statement or finding | Concise statement of the contribution                                                                                                                                                  |
| **Topic Thread**   | Conceptual category                    | `Architecture`, `Testing`, `Configuration`, `Debugging`                                                                                                                                |
| **Status**         | Resolution state                       | `Introduced`, `Accepted`, `Revised`, `Rejected`, `Resolved`, `Unresolved`                                                                                                              |
| **Relationships**  | Dependencies and causal links          | `Depends on A001`, `Contradicts A004`, `Alternative to A010`                                                                                                                           |

---

## 2. Extraction & Preservation Rules

1. **Split Compound Statements:** Break multi-part arguments into independently traceable atomic units.
2. **Preserve Rejected Approaches:** Record discarded alternatives and dead ends; they explain why the final architecture was selected.
3. **Capture Tool Findings:** Record exact command flags, error messages, and output summaries from tool invocations.
4. **Traceability Guarantee:** Map 100% of `A001...` entries to their canonical destination in the final notes.
