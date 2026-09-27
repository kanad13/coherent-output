---
name: markdown-audit
description: Audits Markdown repositories and documentation folders against numbering, naming, README coverage, navigation, and link integrity standards. Use when reviewing documentation structure or organizing repo docs.
---

# Markdown Repository Audit

Follow this protocol to audit documentation folders and produce sequenced correction plans.

---

## 1. Audit Scope & Exclusions

- **Target Scope:** Human-maintained documentation and notes folders (`*.md`).
- **Excluded Paths:** Source code files, generated artifacts, dependency directories (`node_modules`), vendor folders, and tool-owned directories (`.git`).
- **Precedence:** Repository-specific instructions in project documentation take precedence over defaults.

---

## 2. Four-Phase Audit Protocol

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

Evaluate every item against five core standards:

1. **Predictable 3-Digit Numbering:** Are content files prefixed with `010-`, `020-`? Are standard sequence increments of 10 used? Is `README.md` used for index files?
2. **Directory README Coverage:** Does every subfolder contain a local index `README.md` containing Purpose, Start Here, and Contents?
3. **Document Skeletons:** Do substantive guides provide Title, Purpose, Table of Contents, Body, and Next Steps?
4. **Asset Placement:** Are non-markdown assets stored in an `assets/` directory with clean naming and alt text?
5. **Link & Anchor Health:** Are all internal links relative, clickable, and verified against real targets?

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

## 3. Two-Phase Execution Gate

- **Phase 1 Output:** Conclude with the audit report and correction plan.
- **Phase 2 Implementation:** Perform actual file moves, renames, and link updates **only after the user explicitly approves** the correction plan.
- When applying changes:
  1. Apply renames and moves in dependency order.
  2. Update all affected internal links in the same atomic operation.
  3. Verify that all updated paths resolve.
