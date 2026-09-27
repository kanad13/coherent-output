---
trigger: glob
globs: "*.md"
description: "Markdown repository structural standards: 3-digit numeric prefixes, directory READMEs, and portable relative link integrity."
---

# Markdown Repository Structural Standards

These standards govern all Markdown files and documentation directories across the workspace.

---

## 1. Predictable Numbering & Naming

- **Three-Digit Prefix:** Human-maintained content files and subdirectories use a three-digit numeric prefix followed by lowercase kebab-case (e.g., `010-introduction.md`, `020-architecture.md`).
- **Configuration Exception:** System configuration rules inside `rules/` follow a standard two-digit convention (`01-`, `02-`) as a justified exception for platform configuration sorting.
- **Standard Increments:** Use primary sequence increments of ten (`010`, `020`, `030`) to reserve intermediate numbers (`015-prerequisites.md`) for future insertion without renumbering.
- **Index File Exception:** Directory index files and root documentation hubs use the exact name `README.md`. Treat `README.md` as the standard exception to the numeric-prefix convention.
- **Descriptive Names:** Document names must clearly convey their actual purpose and operational scope.

---

## 2. Directory & Root Index Standards

- **Directory README Coverage:** Every content subdirectory must contain a `README.md` serving as its local index.
- **Directory README Structure:**
  - **Purpose:** The directory's scope and intended usage.
  - **Start Here:** The primary entry point when documents have a logical reading order.
  - **Contents:** A linked list of every file and subfolder with a concise one-line summary.
  - **Navigation:** Links to parent, sibling, or downstream documents.
- **Root README:** The repository root README must provide the overall repository purpose, target audience, start-here instructions, and a linked map of top-level content directories.

---

## 3. Link Integrity & Navigation

- **Portable Relative Links:** Inside repository documentation files, use **portable relative Markdown links** exclusively (e.g., `[Auth Service](../services/020-auth.md)`). Prohibit machine-local absolute paths (`file:///Users/...`) in committed repository markdown.
- **Clickable Index Entries:** Every filename referenced in an index or guide must be a valid, clickable Markdown link.
- **Link Verification:** Ensure all relative paths, file anchors, and image references resolve to existing targets.
- **Asset Alt-Text:** Every informative image or diagram must include meaningful descriptive alt text.
