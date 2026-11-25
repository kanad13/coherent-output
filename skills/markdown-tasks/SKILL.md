---
name: markdown-tasks
description: Refines rough notes, existing Markdown task lists, and status updates into clean Markdown checkboxes with indented context bullets. Use when drafting, cleaning up, or updating personal Markdown task notes. Do not use for general prose refactoring, issue trackers, or documents requiring narrative paragraphs.
---

# Markdown Task Note Refiner

Transform rough task notes, existing task lists, status updates, or a mix of all three into clean, scannable Markdown task notes. Preserve every name, number, product term, constraint, and still-valid detail verbatim, and output only the refined Markdown with no preamble or commentary.

## 1. Vocabulary and Syntax Invariant

Use these terms consistently:

- **Note:** A single topic, project, or list (optionally with a title or `##` section headings) containing one or more actions.
- **Action:** One concrete, completable step written as a Markdown list item with a checkbox:
  - `- [ ]` = **open action** (still to do)
  - `- [x]` = **complete action** (finished)
  - `- [-]` = **parked action** (deferred or cancelled, kept in place for reference)
- **Context bullet:** An indented bullet (`  - ...`) directly beneath an action holding current backstory, constraints, questions, decisions, or outcomes.

**Strict syntax invariant:** Every action must be a Markdown list item starting with `- [ ] `, `- [x] `, or `- [-] `. Never emit bare checkboxes (`[ ]`, `[x]`, `[-]`) without the leading `- `. Indent every context bullet by two spaces directly beneath its parent action (`  - ...`), never at column 0.

## 2. Processing Rough Input and Meta-Instructions

- **Strip inline meta-scaffolding:** Remove framing phrases such as `"need a new task to..."`, `"add a task to..."`, `"another task in this section:"`, or `"need a new subsection for..."` and execute the intent directly as a clean heading or action.
- **Flip backstory-first notes:** When context appears before the actual ask (e.g., `"the mechanic said X - did we book Y - check with Z"`), put the concrete action on the action line and move the backstory into context bullets.
- **Respect execution order:** When input mentions a prerequisite (`"beforehand..."`, `"first..."`, `"before doing X"`), place the prerequisite action before the dependent action.
- **Bundle single meetings/calls:** Keep one meeting or call with multiple agenda topics as a single action, putting only _additional_ agenda points and key relationships in context bullets (without repeating what is already on the action line). Split genuinely unrelated tasks into separate actions.
- **Group research or preparation questions:** For research or preparation actions with multiple questions, put the high-level action on the action line and keep each question as its own short context bullet.

## 3. Handling Existing Notes, Actions, and Updates

- **Upgrade vague actions:** Rewrite poorly articulated existing actions (vague, wordy, or abstract headlines) into direct plain-English action lines while keeping their exact meaning.
- **Leave clear actions untouched:** Do not reword already-clear actions just to make edits.
- **Apply updates in place:** Write updates in active present tense so the note always reflects current truth. Never append dated patch notes or changelogs (e.g., `"Updated Nov 25:"` or `"Update:"`).
- **Preserve states unless changed:** Keep existing `- [ ]`, `- [x]`, and `- [-]` states unless the input explicitly changes them.
- **Handle completions with follow-ups:** When an action is completed (`- [x]`) and the update introduces concrete next steps, record the decision or outcome in a context bullet beneath the completed action and create separate open (`- [ ]`) actions for each next step. Never bury follow-up work inside a completed action.
- **Handle deferred or dropped items:** Mark deferred or dropped actions as parked (`- [-]`) in place and add a short context bullet explaining why.
- **Preserve valid context verbatim:** Never trim, compress, or summarize away names, numbers, constraints, or nuances in still-valid context bullets.
- **Replace superseded context in place:** When a new decision or fact contradicts an earlier one, replace the superseded context bullet in place (keeping brief rationale if it matters) instead of stacking conflicting bullets.

## 4. Organizing Sections (`##` Headings)

- **Keep simple notes flat:** Use no section headings for a few actions on one topic. Never add a generic wrapper heading such as `## Actions`.
- **Preserve fitting headings:** Keep existing `##` headings that still fit the content.
- **Route `## Active` and `## Completed`:** When a note uses `## Active` and `## Completed` sections, move newly completed (`- [x]`) actions into `## Completed`, while keeping open (`- [ ]`) and parked (`- [-]`) actions under `## Active`.
- **Group large or mixed notes:** When a note grows large (around 7+ actions) or mixes distinct phases or topics, group related actions under clear, distinct `## <Section>` headings. Never create empty or duplicate headings.

## 5. Writing Action Lines and Context Bullets

- **Three direct action forms:** Start every action line with one of:
  - Asking: `Ask <person> if/whether <exact plain-English question>`
  - Receiving: `Obtain <specific deliverable> from <person>`
  - Doing: `<Direct imperative verb> <target> to <concrete outcome>`
- **Two-second test:** A reader must know exactly what to do from the action line alone without reading any context bullets. Never write nominalized abstract headlines (e.g., `"Confirm license renewal sequence"` or `"Staging migration alignment"`).
- **Context bullets:** Put backstory, constraints, questions, decisions, or outcomes in indented context bullets (`  - ...`), with one short thought per bullet. If the action line already says everything, add no context bullets. Never repeat, echo, or paraphrase the action line beneath it.

## 6. Style, Fidelity, and Plain-Language Policy

- Use direct verbs, clear references, consistent terms, active voice, and present tense.
- Break tangled run-on sentences into short, simple sentences (one idea per sentence).
- Fix typos, spelling, and punctuation.
- Keep the author's exact names, numbers, product terms, and phrasing verbatim so the note still sounds like them.
- Use zero corporate jargon or buzzwords (no `"align stakeholders"`, `"synergize"`, `"optimize deliverables"`, `"touch base"`, or `"circle back"`).

## 7. Edge Cases

- **Brief single-task input:** Output a single `- [ ]` action line with no heading and no context bullets.
- **Bare checkboxes (`[ ]`, `[x]`, `[-]`) or unindented context bullets:** Normalize every action to `- [ ] `, `- [x] `, or `- [-] ` and indent every context bullet two spaces (`  - ...`) beneath its action.
- **Already-clean note:** Return the note unchanged without rewording clear actions or adding unnecessary structure.
- **Ambiguous status update:** Keep the current checkbox state and record the unresolved question in a short context bullet if needed.
- **Contradictory facts:** Keep the newer fact and replace the superseded context bullet in place rather than keeping both.

For worked before-and-after examples of multi-update notes and checkbox syntax, read `references/examples.md` relative to this skill directory when needed.

## 8. Output Contract

Output only the refined Markdown. Do not add any preamble, explanation, commentary, or outer code fence.
