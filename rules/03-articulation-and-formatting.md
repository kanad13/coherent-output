---
trigger: always_on
description: "ASD-STE100 Controlled Technical Language, Cognitive Chunking, Bullet-First micro-formatting, Zero-Loss invariant, Protected Elements, and relative link integrity."
---

# Articulation, Controlled Language & Formatting Standards

These formatting and linguistic invariants apply across all agent responses, technical documents, and repository content.

---

## 1. Controlled Technical Language (ASD-STE100)

- **Cognitive Chunking:**
  - Restrict each sentence to a single controlling idea, action, or causal relationship.
  - Split compound multi-clause thoughts into nested child bullets.
- **Natural Syntactic Flow:**
  - Write direct, affirmative sentences.
  - Preserve natural articles, verbs, and logical connectives without artificial truncation or run-on sprawl.
- **Active Voice & Explicit Actors:**
  - Ensure every sentence names a clear actor performing the action.
- **Direct Affirmative Phrasing:**
  - State what an item is, has, or does directly using ordinary verbs such as use, build, run, check, or store.
- **Noun Cluster Restriction:**
  - Limit consecutive nouns to a maximum of three.
- **Terminological Determinism:**
  - Use one canonical term for each system concept consistently throughout.
  - Define unfamiliar or specialized terms in plain language upon first use.

---

## 2. Bullet-First Micro-Formatting Standard

Format all non-protected body text using structured bullet trees:

- **Bullet-First Hierarchy:**
  - Place every ordinary body line within an unordered bullet tree.
  - Prohibit paragraph walls of text.
- **Top-Level Bold Category Anchors:**
  - Restrict top-level bullets strictly to conceptual category anchors formatted as `- **Anchor:**` with no trailing sentence on the same line.
- **Un-bolded Child Bullets:**
  - Place all substantive assertions, conditions, metrics, and explanations inside nested child bullets with zero bold labels.
- **Nesting Depth Cap:**
  - Restrict list hierarchies to a maximum of three levels.
- **Sequential Ordered Lists:**
  - Restrict numbered lists strictly to sequential workflows, chronological phases, or execution algorithms.

---

## 3. Zero-Loss Invariant & Protected Elements

- **Zero-Loss Invariant:**
  - Preserve 100% of substantive facts, numbers, units, dates, formulas, parameters, and configuration settings.
  - Preserve exact modal certainty without weakening or strengthening modal force.
- **Protected Elements:**
  - Retain native syntax and formatting for tables, fenced code blocks, Mermaid diagrams, LaTeX math blocks, frontmatter, and blockquotes.
  - Never convert protected elements into bullet items.

---

## 4. Medium-Specific Format Scoping

- **Mandatory Technical Contexts:**
  - Apply Bullet-First micro-formatting as the mandatory default for all agent session turns, explanations, technical responses, specifications, architectural guides, notes, and audit reports.
- **Human Correspondence Exception:**
  - Apply native prose layout exclusively when drafting external human correspondence on behalf of the user, such as emails or chat messages to colleagues.
  - Apply native prose layout to language learning reading texts.

---

## 5. Link Integrity & Markdown Navigation

- **Portable Relative Links:**
  - Use portable relative Markdown links exclusively inside repository documentation files (e.g., `[Auth Service](../services/auth.md)`).
  - Prohibit machine-local absolute paths (`file:///Users/...`) in committed repository markdown.
- **Clickable File References:**
  - Ensure every document filename referenced in an index or guide is a valid, clickable Markdown link.
- **Target Verification:**
  - Verify that all relative paths, file anchors, and image references resolve to existing targets before completing tasks.
- **Asset Alt-Text:**
  - Include meaningful descriptive alt text for every informative image or diagram.
