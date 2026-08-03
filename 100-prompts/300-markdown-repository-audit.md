# Markdown Repository Audit

## Purpose

Audit a Markdown-focused repository or documentation folder against the user's preferred structure, naming, navigation, formatting, asset, and linking standards. Produce a detailed correction plan. Apply the plan after the user explicitly requests implementation.

## Scope

Apply these standards to human-maintained documentation content. Treat source code, generated files, dependency folders, build artifacts, and tool-owned directories as outside the audit scope until the user explicitly includes them.

Repository-specific instructions take precedence. Report each conflict and the resulting applied rule.

## Standards

### 1. Predictable Numbering and Naming

- Human-maintained content files and content folders use a three-digit numeric prefix and a lowercase kebab-case name.
- Required root and directory index files use the exact name `README.md`. Treat this as the standard index-file exception to numeric-prefix and kebab-case rules.
- Use primary sequence numbers in increments of ten:
  - `010-introduction.md`
  - `020-architecture.md`
  - `030-operations.md`
- Reserve an intermediate number such as `015-prerequisites.md` for insertion between established items.
- Treat existing numeric identities as stable. Close harmless gaps during a user-approved reorganization.
- Rename an existing numbered item when:
  - Its current name misrepresents its content.
  - Its position is materially misleading.
  - The user approves a deliberate reorganization.
- Use descriptive names that state the document's actual purpose.

### 2. Directory README Files

Every in-scope content directory contains a `README.md` that serves as its local index.

Each directory README contains:

- **Purpose:** The directory's scope and intended use
- **Start here:** The correct entry point when sequence matters
- **Contents:** A linked list of every in-scope file and subfolder with a one-line description
- **Navigation:** Related parent, sibling, or next-step links when useful

Keep substantive guide content in dedicated documents. The README provides orientation and navigation.

### 3. Root README

The repository root README contains:

- Repository purpose
- Intended audience
- Start-here instructions
- A linked map of top-level content folders
- Essential usage or contribution information

### 4. Document Structure

Use this default skeleton for substantive documents:

```markdown
# [Document Title]

## Purpose

[Why this document exists, who uses it, and what it covers.]

## In This Document

- [Section](#section)

---

## [Body Sections]

---

## Related / Next Steps

- [Related document](path/to/document.md) - Why it is relevant.
```

- Use the table of contents when a document has more than five headings or is difficult to scan.
- Keep each section focused on one primary question.
- Allow short reference pages to use a slimmed-down skeleton and record the justified exception.

### 5. Assets

- Store human-maintained non-Markdown assets in a stable root-level `assets/` directory, with repository tooling requirements determining any alternative location.
- Use descriptive, sequentially numbered, lowercase kebab-case asset names.
- Keep generated assets in an explicitly identified generated location when applicable.
- Use the repository's supported link form and verify rendered links. Prefer repo-root-relative paths when they render correctly on the target platform.
- Every informative image requires useful alt text.

### 6. Links and Navigation

- Every filename mentioned in an index is a clickable link.
- Sequential guides link to the preceding and next step.
- Substantive documents end with related or next-step links.
- Use stable heading anchors.
- Ensure every document is reachable from an appropriate index or related-content path.
- Verify internal links, anchors, image paths, and case-sensitive paths.

## Audit Workflow

### 1. Establish Scope

- Read repository instructions and relevant README files.
- Inventory in-scope directories, documents, and assets.
- Identify excluded code, generated, vendor, or tool-owned paths.
- State the audit scope and any conflicting conventions.

### 2. Build the Repository Map

Produce a visual tree showing:

- Current numbering and hierarchy
- README coverage
- Assets
- Orphans or misplaced content
- Broken or missing navigation relationships

### 3. Audit Each Standard

Evaluate:

- Naming and ordering
- Directory and root README coverage
- Document skeletons and navigation aids
- Asset placement and naming
- Internal links, anchors, and image paths
- Orphans, duplicates, and sequence gaps

For every finding, record:

- Path
- Current state
- Violated or intentionally excepted standard
- User impact
- Exact proposed change
- Dependencies on other changes

### 4. Present the Audit and Plan

Use this output structure:

```markdown
# Markdown Repository Audit

## Scope and Repository Map

## Summary

- **Compliant:**
- **Needs attention:**
- **Conflicts or justified exceptions:**

## Findings

| Priority | Path | Finding | Standard | Proposed change |
| --- | --- | --- | --- | --- |

## Rename and Move Map

| Current path | Proposed path | Reason | Links affected |
| --- | --- | --- | --- |

## Sequenced Correction Plan

1. [Dependency-aware action]

## Verification Plan

- [Checks to run after implementation]
```

An audit-only request concludes with the audit and correction plan.

## Implementation Mode

When the user explicitly approves implementation:

1. Re-read the current repository state.
2. Reconcile any changes made since the audit.
3. Apply approved moves and renames in dependency order.
4. Update all affected links and indexes in the same change.
5. Preserve unrelated user work.
6. Run link, structure, and naming checks.
7. Present a final compliance audit and any remaining exceptions.
