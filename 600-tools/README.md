# 600-tools: Practical Utilities & Standalone Applications

- **Overview:**
  - This directory contains ready-to-use, production-grade tools designed for real-world workflows.
  - These are self-contained applications with minimal or zero dependencies, optimized for immediate use.

---

## Tools Catalog

### [notepad.html](notepad.html) — Mobile Find & Replace Editor

**Purpose:** A lightweight, mobile-optimized plain-text editor with built-in find & replace functionality.

**Key Features:**

- **Always-visible Find & Replace bar** — Quick text search and replacement without UI clutter
- **Case-sensitive/insensitive toggle** — Aa button or Alt+C shortcut for flexible matching
- **Auto-save to browser localStorage** — 500ms debounce ensures content persistence across sessions
- **Touch-friendly UI** — Optimized for iPad and iPhone interfaces
- **Word wrap enabled** — Readable text on any screen size
- **Zero external dependencies** — Pure HTML/CSS/JavaScript, self-contained file
- **Responsive design** — Works on desktop, tablet, and mobile

**Usage:**

- Type in the Find field to search in real-time
- Press Enter in Find to jump to the next match
- Click "Next" to navigate through matches
- Use "Replace" for single replacements or "Replace All" for bulk replacements
- Press Escape to return focus to the editor

**Browser Compatibility:**

- Modern browsers with ES6 support (Safari, Chrome, Firefox, Edge)
- Tested on iPad and iPhone
- Storage limit: ~5–10 MB (browser localStorage limit)

**Common Customizations:**

- **Auto-save delay:** Edit `SAVE_DELAY` constant (currently 500ms)
- **Font family:** Modify textarea CSS `font-family` property
- **Button/input sizes:** Adjust `.fr-buttons` and `.fr-row` padding values
- **Breakpoint for responsive design:** Update `@media (max-width: 768px)` rule

**Known Limitations:**

- Plain-text find/replace only (no regex mode)
- Undo history limited to browser's native textarea undo (Cmd/Ctrl+Z)
- localStorage has browser-imposed size limits (~5–10 MB)

**License:** MIT — Feel free to use, modify, and distribute.

---

## Using These Tools

1. **Standalone:** Each tool is a standalone file and can be used independently.
2. **Self-contained:** No setup, installation, or build process required.
3. **Distribution:** Copy the file to your server or open directly in a browser.
4. **Customization:** Modify CSS, JavaScript variables, or HTML structure to suit your needs.
