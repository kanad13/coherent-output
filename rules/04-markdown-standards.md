---
trigger: glob
globs: "*.md"
description: "Markdown repository structural standards: curated guide numbering, directory README indexes, and portable relative link integrity."
---

# Markdown Repository Structural Standards

These standards govern Markdown files, directory indexes, and link structures across the repository.

---

## 1. Predictable Numbering & Naming

- **Curated Documentation Guides:**
  - Use a three-digit numeric prefix followed by lowercase kebab-case for curated sequential documentation guides and chapter files (e.g., `010-introduction.md`, `020-architecture.md`).
- **Standard Increments:**
  - Use primary sequence increments of ten (`010`, `020`, `030`) to reserve intermediate numbers (`015-prerequisites.md`) for future insertions without renumbering.
- **System and Component Exceptions:**
  - System configuration rules inside `rules/` follow a standard two-digit convention (`01-`, `02-`) for platform sorting.
  - Standard development directories, code packages, tools, adapters, and skill bundles follow standard unnumbered naming conventions.
- **Index File Naming:**
  - Directory index files and root documentation hubs use the exact name `README.md` as the standard exception to numeric prefixes.
- **Descriptive Names:**
  - Document names must clearly convey their actual purpose and operational scope.

---

## 2. Directory & Root Index Standards

- **Directory README Coverage:**
  - Every content subdirectory must contain a `README.md` serving as its local index.
- **Directory README Structure:**
  - Purpose: declare the directory scope and intended usage.
  - Start Here: identify the primary entry point when documents have a logical reading order.
  - Contents: provide a linked list of every file and subfolder with a concise one-line summary.
  - Navigation: provide links to parent, sibling, or downstream documents.
- **Root README Requirements:**
  - Provide overall repository purpose, target audience, onboarding instructions, and a linked map of top-level content directories.

---

## 3. Link Integrity & Navigation

- **Portable Relative Links:**
  - Use portable relative Markdown links exclusively inside repository documentation files (e.g., `[Auth Service](../services/020-auth.md)`).
  - Prohibit machine-local absolute paths (`file:///Users/...`) in committed repository markdown.
- **Clickable Index Entries:**
  - Ensure every filename referenced in an index or guide is a valid, clickable Markdown link.
- **Link Verification:**
  - Verify that all relative paths, file anchors, and image references resolve to existing targets before completing tasks.
- **Asset Alt-Text:**
  - Include meaningful descriptive alt text for every informative image or diagram.
