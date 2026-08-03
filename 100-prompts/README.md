# Prompt Library

Focused instructions and reusable workflows for AI agents.

## Audience and Design Context

These prompts are designed for one primary user: Kunal. They intentionally reflect his working and learning preferences rather than generic defaults.

- **Beginner-accessible:** Explain technical material from first principles and define unfamiliar terms.
- **Visually rich:** Use diagrams, tables, charts, plots, trees, timelines, ASCII sketches, and other appropriate visual forms extensively. Visual coverage is a comprehension requirement, not decoration.
- **Complete:** Preserve important details, qualifications, examples, and relationships. Do not replace a requested deep explanation with a shallow summary.
- **Inspectable:** Show useful analysis artifacts such as evidence, assumptions, inventories, decision criteria, plans, mappings, and verification results. Do not rely on hidden private chain-of-thought.
- **Highly structured:** Prefer clear headings, short units, bullets, tables, and explicit relationships when the active prompt calls for them.
- **Evidence-oriented:** Research current or uncertain claims and cite externally verifiable facts close to their supporting sources.
- **Autonomous:** Inspect available context and proceed under explicit reasonable assumptions. Ask questions only when the answer cannot be discovered and would materially change the result.
- **Purpose-built:** Each prompt should have one primary job and a clear stopping point. Supporting analysis and validation must serve that same job.

These preferences are intentional. Do not remove them merely because they are more detailed or visual than common prompt-writing conventions. Change them only when they directly prevent the prompt from completing its stated job accurately.

## Visible Analysis

Requests to show reasoning mean that the agent should expose reviewable work products:

- What it understood
- What evidence it inspected
- What assumptions it made
- Which meaningful options it considered
- Which decision it selected and why
- How it plans to act
- How it verified the result

This does not require disclosure of hidden private chain-of-thought or raw internal token-by-token reasoning.

## Numbering

- Use three-digit prefixes in primary increments of ten.
- Keep related prompts in the same numeric family.
- Use intermediate numbers only when inserting between established prompts.
- Prefer filenames that describe the invoked action or output.
- Treat renumbering as an architectural change; update indexes and references together.

## Current Families

- **100s — Agent operations and evidence:** Coding workflow, research, validation, and document de-identification
- **200s — Analysis and learning:** Problem framing, teaching, prompt auditing, response style, and product comparison
- **300s — Repository documentation and visualization:** Markdown repository audits and visual generation
- **400s — Document transformation:** Technical simplification, restructuring, and formatting
- **500s — Communication and code artifacts:** Email rewriting, code comments, and Git commits
- **600s–700s — Reserved:** Available for future prompt families
- **800s — German learning:** Existing German-language prompts; content currently preserved unchanged
- **900s — Chess learning:** Reserved for future chess-focused prompts

## Catalog Status

The detailed prompt-by-prompt catalog is intentionally deferred until the current improvement rounds are complete. The final catalog should document each prompt's trigger, inputs, primary output, tools, mutation permissions, related prompts, and stopping point.
