---
name: articulation-review
description: Use when the user flags articulation problems and asks to review a document's bullets or sections for clarity or ASD-STE100 plain language. Work from comments or a stated concern, offer three inline alternatives for worthwhile changes, and finalize selected wording.
---

# Articulation Review

Help the user decide how a document should express its meaning. Preserve substantive information while improving clarity, structure, and precision.

## 1. Read the Document and Establish the Stage

- Read the full document before proposing local changes. Identify its purpose, audience, governing instructions, and relevant repository context.
- Identify the requested stage: initial review, another round of options, or finalization of selections. A request for options keeps the original text; a request to apply preferences produces final content.
- Inspect uncommitted changes before editing. When commits are part of the agreed workflow, use the [commit-scribe](../commit-scribe/SKILL.md) skill to preserve the annotated draft first. Keep recoverable copies of files outside Git.
- For a finalization request, read the earlier concerns and the new selections, then continue at Step 6. Do not generate another set of options unless requested.

## 2. Understand Feedback and Audit Related Text

- Treat annotations that start with `[LOOKOUT` as user feedback, including `[LOOKOUT: ...]` and escaped forms. Preserve Markdown links, code, and literal notation, including examples that explain the feedback format.
- Steelman each comment: explain what the user wants the reader to understand, what currently obstructs that understanding, and what a successful revision must achieve.
- If there are no annotations, use the user's stated concerns and accepted feedback from the conversation to review each bullet and section. Identify additional issues through judgment, with evidence from the text.
- Turn compound concerns into atomic, positive writing instructions. Give each issue a stable identifier and record its affected passage and acceptance criteria—the checks that show the revision meets the user's concern—in a working inventory outside the final document.
- Audit the full document for the same underlying problem before drafting. Extend a clarity principle where it applies; keep a scenario-specific preference local to that scenario.
- Read later feedback as a refinement of the earlier choice. For example, if the user selects an option and requests a shorter second sentence, apply that option with the requested sentence change.

Useful inventory instructions include:

- Explain a technical concept's practical meaning and why it matters to the reader before implementation detail. Add a short, familiar analogy or example when it makes the concept easier to understand. Keep the explanation simple and avoid introducing more unfamiliar terms.
- At first use in the file, place a short, plain-language explanation beside an unfamiliar term or acronym. Explain only what the reader needs for the passage. Use familiar words and leave secondary details for later. Explain the term once per file unless the user requests repetition.
- Write short, active sentences with one main idea. State the actor and replace a pronoun when its reference is unclear.
- Use one term for each concept. Remove filler and unnecessary jargon.
- Explain why a decision matters and state the conditions under which a mechanism or action applies.
- Preserve facts, commitments, dependencies, and genuine uncertainty. Identify missing context without inventing facts.

## 3. Decide Which Changes Add Value

- Use the [worth-the-squeeze](../worth-the-squeeze/SKILL.md) skill to assess candidate changes. For each issue, record the current defect, reader benefit, editing effort, and risk of changing meaning.
- Propose changes that resolve confusion, inconsistency, unsupported certainty, missing explanation, or obstructive structure. Retain useful text when the improvement is marginal.
- Include both pursued changes and significant decisions to leave text alone in the inventory. Keep this assessment proportionate to the document.
- If a correction depends on unfamiliar external facts, use the [web-research](../web-research/SKILL.md) skill to verify them with primary sources. A wording review alone does not establish legal, technical, or numerical facts.

## 4. Write and Insert Three Alternatives

- For each worthwhile issue, write three alternatives that differ meaningfully in structure, emphasis, or detail. Explain removal or relocation when that resolves a structural problem better than rewording.
- Preserve facts, commitments, conditions, dependencies, and the source's degree of certainty. Keep unresolved questions visible. Flag any alternative that changes substance or requires a decision beyond wording.
- Use the [bullet-first-refactor](../bullet-first-refactor/SKILL.md) skill when restructuring dense Markdown into clear bullets. Apply the user's approved changes while retaining the skill's preservation checks for unaffected information.
- Check every alternative against the shared writing principles and its passage-specific acceptance criteria. Confirm clear actors and references, consistent terms, sufficient explanation, appropriate certainty, and preserved conditions.
- Insert the alternatives beside the original passage. Retain the user's comment and label each option with its issue identifier:

```markdown
- Original passage [LOOKOUT: user concern]
  - [R01 · Option 01 — First alternative.]
  - [R01 · Option 02 — Second alternative.]
  - [R01 · Option 03 — Third alternative.]
```

- When there is no comment, add a brief `[LOOKOUT: ...]` concern before the options. Identify the exact span for a multi-bullet replacement. Follow the document's stated nesting limit; otherwise use at most three list levels. Put longer replacements in labeled blocks beside the affected span.
- Preserve tables, code blocks, diagrams, and equations in their native format. Place proposals for those elements beside them.

## 5. Save the Review and Return It to the User

- Check that every pursued issue has three options, the source and comments remain intact, and each option satisfies the inventory.
- When commits are part of the agreed workflow, use the [commit-scribe](../commit-scribe/SKILL.md) skill to commit the review before presenting it. Follow the established upstream policy.
- Link the review documents and summarize the substantive concerns. Return the options for deliberation; leave them in place until the user selects wording or delegates the choice.

## 6. Apply Selections and Further Feedback

- Match each selection and follow-up comment to its issue identifier. Apply the selected text with any requested refinement.
- If the user requests another round of alternatives, return to Steps 2–5 for those issues and retain wording already settled elsewhere.
- Reconcile linked choices, such as repeated terminology or section labels, while preserving the selected meaning. Explain a material reconciliation in the completion report.
- If the user delegates a choice, select the strongest wording against the inventory and value assessment. Ask only when conflicting instructions leave a material decision unresolved.
- Replace the affected passages with the selected wording. Remove resolved review comments, unused alternatives, issue labels, and temporary review instructions. Preserve literal examples and instructions that belong to the document.
- Capture useful new context in a separate scratch file. Mark inference separately from confirmed facts, surface deferred insights when requested, and incorporate them within the user's authorized scope.

## 7. Verify, Synchronize, and Commit Final Content

- Compare the result with the baseline and selections. Confirm that every comment is resolved, unchanged facts and constraints remain, and the final wording satisfies the inventory.
- After accepted multi-file changes, use the [repo-evergreen-sync](../repo-evergreen-sync/SKILL.md) skill to check for actual drift within the authorized scope. Apply the same value test to related edits and retain unaffected material.
- Check formatting, links, protected elements, and remaining review residue. Use [markdown-audit](../markdown-audit/SKILL.md) when navigation or link changes warrant it; run other available checks in proportion to the change.
- Use [commit-scribe](../commit-scribe/SKILL.md) when final commits are requested or required. Report the changed files, key decisions, verification results, and commit status.

## Supporting Skills and Maintenance

- Read a named supporting skill from the current available-skills catalog when its step applies. Skill names are instructions to load that workflow, not tool commands or automatic dependencies.
- If a supporting skill is unavailable, use the decision criteria in this workflow and report the missing specialist step. Do not invent a tool or modify unrelated setup.
- Keep invocation within the user's authorized task. A review request does not authorize publication, external messages, or edits across unrelated repositories.
- Maintain this skill from demonstrated failures. Check realistic annotated-review, unannotated-review, and finalization cases when changing its behavior; validate its metadata and update affected references when renaming it.
