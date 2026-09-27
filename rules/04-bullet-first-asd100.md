---
trigger: always_on
description: "ASD-STE100 Controlled Technical Language, Cognitive Chunking, Bullet-First formatting, Zero-Loss invariant, and Protected Elements."
---

# Bullet-First & Controlled Technical Language (ASD-STE100)

These formatting and linguistic invariants apply across all agent responses, technical documents, and repository content.

---

## 1. Controlled Technical Language (ASD-STE100)

- **One Idea Per Sentence:** Restrict each sentence to a single controlling idea, action, or causal relationship. Split compound multi-clause thoughts into nested child bullets.
- **Natural Syntactic Flow:** Write direct, affirmative sentences. Preserve natural articles (`a`, `the`), verbs, and logical connectives (`because`, `if`, `when`) without artificial truncation.
- **Active Voice & Explicit Actors:** Ensure every sentence names a clear actor performing the action (_"The authentication gateway validates the JWT"_, not _"The JWT is validated"_).
- **Direct Affirmative Phrasing:** State what an item is, has, or does directly using ordinary verbs (`use`, `build`, `run`, `check`, `store`).
- **Noun Cluster Restriction:** Limit consecutive nouns to a maximum of three.
- **Terminological Determinism:** Use one canonical term for each system concept consistently throughout. Define unfamiliar or specialized terms in plain language at first use.

---

## 2. Bullet-First Micro-Formatting Standard

Format all non-protected body text using structured bullet trees:

- **Bullet-First Hierarchy:** Every ordinary body line must reside within an unordered bullet tree (`- `). Paragraph walls of text are strictly prohibited.
- **Top-Level Bold Category Anchors:**
  - Top-level bullets serve strictly as conceptual anchors formatted as `- **Category Label:**` with **no** trailing sentence on the same line.
- **Un-bolded Child Bullets:**
  - All substantive assertions, conditions, metrics, and explanations reside in nested child bullets (` -`) with **zero** bold labels.
- **Nesting Depth Cap:** Restrict list hierarchies to a maximum of three levels (`- `, `  -`, `    -`).
- **Ordered Lists for Steps:** Restrict numbered lists (`1.`, `2.`) strictly to sequential workflows, chronological phases, or execution algorithms.

---

## 3. Zero-Loss Invariant & Protected Elements

- **Zero-Loss Invariant:** Preserve 100% of substantive facts, numbers, units, dates, formulas, parameters, and exact modal certainty (`must`, `should`, `may` — never weaken or strengthen modal force).
- **Protected Elements (Never Convert to Bullets):**
  - **Tables:** Comparison matrices and structured tabular data retain native GFM table syntax.
  - **Code Blocks:** Fenced code blocks (```) retain executable syntax and indentation.
  - **Mermaid Diagrams & Math:** Diagrams and LaTeX blocks retain native delimiters.
  - **Frontmatter & Blockquotes:** YAML/TOML frontmatter and blockquotes (`>`) retain native formatting.

---

## 4. Medium-Specific Format Exceptions

- **General Technical Text:** Bullet-First formatting is the mandatory default for specifications, architectural guides, notes, explanations, and audit reports.
- **Targeted Medium Exceptions:** Natural correspondence (emails, chat messages) and language learning reading texts follow their native prose layout rather than bullet trees.
