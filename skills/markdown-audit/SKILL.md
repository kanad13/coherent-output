---
name: markdown-audit
description: Audits Markdown repositories and documentation folders against numbering, naming, README coverage, navigation, and link integrity standards. Use when reviewing documentation structure or organizing repo docs. Do not use for evaluating prose wording (use articulation-review) or refactoring text content (use cognitive-clarity-refactor).
---

# Markdown Repository Audit

Follow this protocol to audit documentation folders, verify structural standards, and produce sequenced correction plans. Execute a non-destructive audit of file hierarchies, broken links, and navigation indexes, categorizing all defects into prioritized remediation batches.

---

## 1. Audit Scope & Exclusions

- **Target Scope:** Human-maintained documentation, knowledge bases, and notes folders (`*.md`).
- **Excluded Paths:** Source code files, generated artifacts, dependency directories (`node_modules`), vendor folders, and tool-owned directories (`.git`).
- **Precedence:** Repository-specific instructions in project documentation take precedence over defaults.

---

## 2. Structural Standards Reference

Evaluate target repositories against these structural standards:

### 1. Predictable Numbering & Naming

- **Curated Documentation Guides:**
  - Content files in curated documentation libraries use a three-digit numeric prefix followed by lowercase kebab-case (e.g., `010-introduction.md`, `020-architecture.md`).
- **Standard Increments:**
  - Use primary sequence increments of ten (`010`, `020`, `030`) to reserve intermediate numbers (`015-prerequisites.md`) for future insertions without renumbering.
- **Index File Naming:**
  - Directory index files and root documentation hubs use the exact name `README.md` as the standard exception to numeric prefixes.
- **Justified Exceptions:**
  - Standard development directories, code packages, tools, adapters, and skill bundles follow standard unnumbered naming conventions.
  - System configuration rules inside `rules/` follow a standard two-digit convention (`01-`, `02-`).

### 2. Directory & Root Index Standards

- **Directory README Coverage:**
  - Every content subdirectory must contain a `README.md` serving as its local index.
- **Directory README Structure:**
  - Purpose: declare the directory scope and intended usage.
  - Start Here: identify the primary entry point when documents have a logical reading order.
  - Contents: provide a linked list of every file and subfolder with a concise one-line summary.
  - Navigation: provide links to parent, sibling, or downstream documents.
- **Root README Requirements:**
  - Provide overall repository purpose, target audience, onboarding instructions, and a linked map of top-level content directories.

### 3. Link Integrity & Navigation

- **Portable Relative Links:**
  - Use portable relative Markdown links exclusively inside repository documentation files (e.g., `[Auth Service](../services/auth.md)`).
  - Prohibit machine-local absolute paths (`file:///Users/...`) in committed repository markdown.
- **Clickable Index Entries:**
  - Ensure every filename referenced in an index or guide is a valid, clickable Markdown link.
- **Target Verification:**
  - Ensure all relative paths, file anchors, and image references resolve to existing targets.
- **Asset Alt-Text:**
  - Include meaningful descriptive alt text for every informative image or diagram.

---

## 3. Four-Phase Audit Protocol

### Phase 1: Establish Scope & Inventory

- Discover all Markdown files and subdirectories within the target scope.
- Inventory assets, images, and embedded resources.
- Note any local conventions declared in existing READMEs.

### Phase 2: Build the Repository Map

- Construct a visual tree representation showing:
  - Numeric sequence and file hierarchy.
  - Directory `README.md` coverage.
  - Orphaned or misplaced files.
  - Broken or missing navigational relationships.

### Phase 3: Audit Against Standards

- Audit discovered files against the three Structural Standards (Numbering, README Coverage, Link Integrity).
- Document non-compliant paths, missing index files, broken links, and unjustified naming patterns.

### Phase 4: Present Audit & Correction Plan

Use this structured deliverable:

```markdown
# Markdown Repository Audit

## Scope & Repository Map

[Visual tree of current files]

## Compliance Summary

- **Compliant:** [List compliant areas]
- **Needs Attention:** [List areas with violations]
- **Justified Exceptions:** [List documented exceptions]

## Findings

| Priority | Path | Finding | Standard | Proposed Change |
| -------- | ---- | ------- | -------- | --------------- |

## Rename & Move Map (if applicable)

| Current Path | Proposed Path | Reason | Affected Links |
| ------------ | ------------- | ------ | -------------- |

## Sequenced Correction Plan

1. [Dependency-aware action step]

## Verification Plan

- [Checks to run after implementation]
```

---

## 4. Two-Phase Execution Gate

- **Phase 1 Output:** Conclude with the audit report and correction plan.
- **Phase 2 Implementation:** Perform actual file moves, renames, and link updates **only after the user explicitly approves** the correction plan.
- When applying changes:
  1. Apply renames and moves in dependency order.
  2. Update all affected internal links in the same atomic operation.
  3. Verify that all updated paths resolve.
