# Zero-Tolerance Anti-Pattern Catalog

Enforce zero tolerance for these 24 specific documentation, code, and architectural drift modes during evergreen synchronization passes:

---

## 1. Documentation Drift Anti-Patterns (Eliminate Completely)

1. **Patch-Note Infiltration (Delta Ingestion):**
   - **Ban:** Appending inline changelog notes or version deltas into living documentation (e.g., `*Note: Updated in v2 to use DuckDB*`, `*Recently patched to fix bug where...*`).
   - **Rule:** Write exclusively in the active present tense describing current operational reality.
2. **Backward-Looking Code Archaeology:**
   - **Ban:** Explaining superseded architectures, decommissioned frameworks, or abandoned implementation choices in living reference docs.
   - **Rule:** Route historical narratives exclusively to Git commit messages.
3. **Enterprise & Multi-Tenant Bureaucracy:**
   - **Ban:** Introducing multi-stage release tiers (`staging/prod`), PR contributor guidelines, SLA disclaimers, SOC2 compliance checklists, or multi-tenant permission schemes into personal or single-developer tools.
4. **Hedging, Sycophancy & Conversational Padding:**
   - **Ban:** Weak modals (`You might want to consider...`, `It is recommended to maybe...`), conversational filler, apologies, and closing pleasantries (`Hopefully this helps!`).
   - **Rule:** Use direct operational modality (`must`, `should`, `may`).
5. **Structural & Formatting Inconsistency:**
   - **Ban:** Mixing arbitrary prose paragraphs with unmanaged heading depths (`#### 1.2.3.1`).
   - **Rule:** Enforce shallow contiguous headings ($H_2 / H_3$) and scannable bullet hierarchies.
6. **Echoing & Redundant Stating:**
   - **Ban:** Restating the heading title in the first sentence immediately beneath it (e.g., `## Configuration` followed by `This section contains configuration parameters`).
   - **Ban:** Prose paragraphs before or after a code fence that merely narrate what the code fence displays.
7. **Ghost & Orphan References:**
   - **Ban:** Markdown links, CLI flag documentation, environment variables, or import statements referencing deleted files, removed flags, or dead functions.
8. **Handoff Faking & Phantom Capability Claims:**
   - **Ban:** Claiming multi-platform or OS support (e.g., `Works on Linux, macOS, and Windows`) unless the underlying codebase implements explicit cross-platform handlers.
9. **Attention Thinning & "Middle-Loss":**
   - **Ban:** Delivering polished opening and closing sections while allowing intermediate reference sections to collapse into vague summaries or drop nested parameters.
   - **Rule:** Maintain identical rigor, tabular detail, and constraint completeness across every section.
10. **Semantic Duplication across Files (DRY Violation):**
    - **Ban:** Copying identical multi-line setup, configuration, or architectural explanations across multiple documentation files.
    - **Rule:** Establish a Single Source of Truth in one canonical file and reference it via portable relative links.
11. **Asymmetric Contract Drift:**
    - **Ban:** Hallucinated CLI flags, obsolete parameters, inverted types, and inaccurate default values in documentation.

---

## 2. Code & Comment Drift Anti-Patterns (Purge & Cleanse)

12. **Trivial Echo Comments:**
    - **Purge:** Comments that merely restate visible syntax mechanics (e.g., `i += 1  # increment i`, `# return result`, `// assign variable`).
13. **Tutorial & Exploratory Narrative Comments:**
    - **Purge:** Stream-of-consciousness narrative comments (e.g., `# Here we loop over items to check if...`, `// Now we need to handle...`).
14. **Session & Attribution Tags:**
    - **Purge:** Assistant attribution markers, turn tags, author stamps, and bugfix tickets (e.g., `# Fixed by Assistant on Turn 4`, `# Sprint 12 bugfix`).
15. **Dead Code Graveyards:**
    - **Purge:** Commented-out legacy code blocks (`# def old_impl(): ...`). Rely entirely on Git for version history.
16. **Pseudocode & Reasoning Scratchpad Residue:**
    - **Purge:** Leftover scratchpad notes and planning checklists (e.g., `# Step 1: parse input`, `# Check edge case`).
17. **Inconsistent Docstring Standards:**
    - **Rule:** Enforce uniform docstrings matching the host language: Google style (Python), JSDoc/TSDoc (JS/TS), Rustdoc (Rust), Go doc (Go).
18. **Lying & Inverted Docstrings:**
    - **Rule:** Parameter types, return types, exceptions raised, and defaults must match actual runtime code with 100% precision.
19. **Rule of Intent ("Why, not What"):**
    - **Preserve:** Comments explaining non-obvious algorithms, OS quirks, kernel anomalies, hardware constraints, regex logic, or crash-prevention rationale.

---

## 3. Code Smells & Architectural Anti-Patterns (Flag as Technical Debt)

Record these in the **Technical Debt & Architectural Findings** catalog without altering runtime code:

20. **Defensive Over-Engineering for Local Tools:** Unnecessary abstract factory hierarchies, complex dependency injection containers, or multi-tiered exceptions in simple scripts.
21. **Dependency & Utility Fragmentation:** Third-party library imports used where standard library primitives or existing sibling utilities suffice.
22. **Shadow Logic & Wrapper Proliferation:** Duplicate wrapper layers or shadow functions created to bypass edge cases (`_v2`, `_safe_execute`, `clean_text_custom`).
23. **Hardcoded Machine-Specific Paths:** Local machine paths (`/Users/...`, `C:\...`) that should be dynamic or configurable.
24. **Prior Collapse & Modal Defaulting:** Bypassing repository-native schemas or conventions in favor of generic web patterns.
