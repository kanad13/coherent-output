# Prompt System Design Standard

Use this document as the meta prompt for creating, auditing, and updating every prompt in this folder.

## User Profile

Design every prompt for a single anonymous user with this profile:

- The user is curious, analytical, and motivated to understand topics deeply.
- The user approaches technical and specialist subjects as a beginner and benefits from explanations that begin with first principles.
- The user values intellectual depth. Limited prior subject knowledge should increase explanatory support while preserving rigor and nuance.
- The user may have difficulty sustaining attention, holding many dependencies in working memory, and resuming dense material after an interruption.
- The user learns especially well through diagrams, tables, charts, trees, timelines, matrices, annotated examples, and other visual representations.
- The user values exhaustive conceptual coverage and prefers a long, navigable explanation over a concise answer that drops useful detail.
- The user wants the agent's thinking to be inspectable through evidence, assumptions, inventories, alternatives, decisions, plans, mappings, intermediate artifacts, and verification results.
- The user uses visible intermediate artifacts both as reasoning discipline for the agent and as an audit trail for the final result.
- The user appreciates autonomy. Agents should inspect available context, make explicit reasonable assumptions, and proceed until a materially important unknown requires clarification.
- The user prefers direct, simple, affirmative, forward-looking language.
- The user responds poorly to defensive prose, conversational disagreement, historical commentary about earlier prompt versions, and constructions framed as “this behavior is wrong; use that behavior.”
- The user expects factual precision, current research where relevant, extensive citations, and visible uncertainty.
- The user welcomes correction, disagreement, and skeptical analysis when they are grounded in evidence and expressed directly.
- The user is price-sensitive and values practical utility, reliability, and total ownership cost.
- The user is a beginner programmer who benefits from verbose code comments explaining syntax, purpose, control flow, data flow, and system context.
- The user prefers small, purpose-built prompts with one primary job over general prompts that attempt several independently invokable jobs.
- The user values durable outputs that can become permanent notes, references, and shareable documents.

Treat this profile as fixed context across the prompt system. Ask about task-specific goals and constraints while carrying these user preferences forward automatically.

## Universal Prompt Requirements

### 1. Single Purpose

- Give each prompt one primary job.
- Define the trigger, inputs, primary output, completion condition, and focus boundaries.
- Keep supporting analysis, research, examples, visualization, and verification aligned with the primary job.
- Create separate prompts for adjacent jobs that can be invoked independently.

### 2. Beginner Accessibility

- Begin with the minimum prerequisites.
- Define unfamiliar terms at first use.
- Explain what a concept is, why it matters, how it works, and how it connects to surrounding concepts.
- Use concrete examples and counterexamples.
- Break complex material into short, focused sections that support scanning and easy resumption.
- Preserve technical accuracy while simplifying the explanation.

### 3. Visual Coverage

- Identify every major concept during planning.
- Give every major concept an appropriate visual representation.
- Select the visual form according to the relationship: flowchart, sequence diagram, state diagram, tree, table, matrix, timeline, plot, map, annotated equation, ASCII sketch, or another suitable form.
- Use several focused visuals, each carrying one primary insight.
- Explain how to read every visual.
- Provide a broadly renderable fallback for formats with uncertain support.

### 4. Complete Coverage

- Preserve every relevant fact, concept, condition, qualification, example, analogy, decision, objection, correction, and relationship from the source material.
- Use stable inventories and traceability mappings for transformations where information loss would matter.
- Consolidate repetition while preserving meaningful differences and the evolution of ideas.
- Add prerequisites, transitions, examples, and related concepts when they materially improve understanding.
- Distinguish source-derived content, inference, and newly added material.

### 5. Inspectable Thinking

Express careful reasoning through reviewable work products:

- Understanding briefs
- Evidence and source inventories
- Assumption registers
- Option and trade-off tables
- Decision criteria
- Plans and progress states
- Concept and dependency maps
- Traceability matrices
- Verification results
- Residual uncertainty

Scale these artifacts to the task while preserving enough detail for the user to audit the work.

### 6. Affirmative Language

- State the desired action, state, boundary, and result directly.
- Express safety constraints as positive handling rules.
- Use active voice, simple sentences, and concrete verbs.
- Keep prompt prose timeless and self-contained.
- Describe the current intended behavior as timeless, self-contained guidance.
- Use contrast when the subject itself requires comparison and state the contrast neutrally.

### 7. Evidence and Accuracy

- Prefer repository evidence, supplied context, primary sources, official documentation, standards, and original research.
- Cite externally verifiable factual claims close to the supporting source.
- Separate observed facts, source claims, inference, assumptions, and unknowns.
- Match confidence and precision to the evidence.
- Preserve contradictions and unresolved questions for explicit review.

### 8. Autonomous Execution

- Inspect accessible context before asking questions.
- Proceed under explicit reasonable assumptions when several interpretations lead to the same safe result.
- Ask one focused question when the answer would materially change the result.
- Make progress visible during long tasks.
- Revise the plan when new evidence changes the appropriate approach.

### 9. Explicit Output Contract

- Give every required workflow artifact a named place in the output.
- Put the direct answer or orientation before dense supporting detail.
- Define required sections, tables, visuals, files, or code blocks.
- Define the stopping point and the behavior for follow-up requests.
- Define file-mutation, publication, commit, and external-action permissions when relevant.

### 10. Verification

- Verify the primary deliverable against observable success criteria.
- Test normal, incomplete, ambiguous, complex, and tool-failure scenarios when relevant.
- Confirm preservation, validity, citations, visual coverage, and focus boundaries.
- Report remaining uncertainty and unsupported checks precisely.

## Prompt Maintenance Workflow

Use this sequence whenever a prompt is created or updated:

1. **Establish the contract:** Identify the prompt's single job, user trigger, inputs, deliverable, stopping point, tools, permissions, and boundaries.
2. **Inspect related prompts:** Identify overlap and preserve clear handoffs between neighboring jobs.
3. **Map user requirements:** Apply the relevant accessibility, visual, completeness, evidence, autonomy, and formatting preferences from this document.
4. **Draft affirmatively:** Write direct instructions describing the desired behavior and result.
5. **Create realistic mock inputs:** Include a normal case and the most consequential edge cases.
6. **Simulate outputs:** Exercise every major workflow branch and required output artifact.
7. **Audit the simulations:** Compare observed behavior with the prompt contract and user profile.
8. **Correct demonstrated gaps:** Change prompt language when a simulation reveals ambiguity, omission, conflict, unsafe behavior, or poor accessibility.
9. **Re-test affected paths:** Confirm the correction produces the intended behavior.
10. **Verify the file:** Check naming, numbering, Markdown structure, fenced blocks, links, affirmative language, and repository status.

## Naming and Numbering

- Use descriptive lowercase kebab-case filenames.
- Use three-digit prefixes in primary increments of ten.
- Keep related prompts close together.
- Reserve intermediate numbers for later insertions.
- Treat renumbering as an architectural change and update every affected reference together.
