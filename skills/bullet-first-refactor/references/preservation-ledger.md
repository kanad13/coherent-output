# Preservation Ledger Schema & Zero-Loss Verification

When refactoring dense, highly technical, or legally sensitive documentation where information loss is prohibited, use this structured ledger before drafting.

---

## 1. Preservation Ledger Categories (`P001`, `P002`, ...)

Extract distinct source elements into categorized units:

| Category Code | Domain              | What to Extract                                                       |
| :------------ | :------------------ | :-------------------------------------------------------------------- |
| **P-CORE**    | Core Thesis         | Primary message and architectural purpose                             |
| **P-DEF**     | Definitions         | Domain terms, abbreviations, and system identities                    |
| **P-RULE**    | Invariants & Rules  | Hard constraints, operational policies, and non-negotiables           |
| **P-COND**    | Conditions & Limits | Prerequisites, branch triggers (`if A then B under C`), SLAs, metrics |
| **P-EDGE**    | Exceptions          | Edge cases, failure modes, error codes, and fallback paths            |
| **P-DATA**    | Technical Data      | Exact CLI flags, environment variables, formulas, and schema keys     |
| **P-WARN**    | Warnings & Caveats  | Risks, security advisories, and unresolved uncertainties              |

---

## 2. Line-by-Line Parity Audit

Before outputting the final refactored document, cross-check against the ledger:

- [ ] Every extracted `P-RULE` invariant appears in the final bullet hierarchy.
- [ ] Every `P-DATA` flag, key, or formula is preserved verbatim without alteration.
- [ ] Every `P-EDGE` exception is represented in its proper conceptual category.
- [ ] Modality matches source intent: hard requirements remain `must`, recommendations remain `should`.
