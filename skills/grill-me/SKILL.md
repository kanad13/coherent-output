---
name: grill-me
description: Runs an adaptive discovery interview that turns an uncertain goal, choice, or proposed change into an evidence-informed recommendation and next-step plan. Use when the user asks to be grilled, wants help thinking through a decision, or needs requirements uncovered through dialogue. Do not impose an interview on a clear execution request, a simple factual lookup, or an urgent need for immediate guidance.
---

# Grill Me: Adaptive Discovery & Decision Protocol

Conduct an adaptive discovery interview that turns an ambiguous objective, architectural fork, or unvalidated proposal into a clear decision and an executable plan. Use single-question dialogue, research before asking, steelmanning, and structured convergence.

---

## 1. Operational Invariants

1. **One question per turn.**
   - Ask one focused question.
   - Exception: bundle 2–3 options only when they are strictly co-dependent and unlock the same immediate choice.
2. **Research before asking.**
   - Inspect accessible files, code, documentation, and public facts first. Ask the user only what the workspace and public sources cannot answer.
3. **Steelman, then challenge.**
   - Interpret the user's intent at its highest standard of rigor before evaluating it.
   - Weigh each proposed mechanism's real utility ("juice") against its lifetime friction, maintenance tax, lock-in, and blast radius ("squeeze"). Surface non-obvious trade-offs and name anti-patterns before accepting a direction.
4. **Durable tracker in the repository.**
   - Keep the working ledger in `.grill-me-tracker.md` at the workspace root, updated each turn with the objective, constraints, confirmed decisions, verified facts, assumptions, and open forks.
   - Keep chat turns for the question and its options; keep raw notes in the file.
   - The tracker is a deliberate workspace file. At convergence, tell the user it exists and ask whether to keep it, commit it, or delete it.
5. **Respect the user's boundaries.**
   - If the user asks to skip, stop, or conclude, end discovery and synthesize the best plan with explicit assumptions.
   - If the user says "I don't know," give a concrete recommendation with a labeled, reversible default and record the assumption.
   - Discovery authorizes no execution. Proceed to implementation only when the user's request explicitly asked for it and critical dependencies are resolved; otherwise end at the plan.

---

## 2. Four-Phase Protocol

Frame and ground, then formulate and ask, then research and squeeze, then converge and plan. Phases 2 and 3 repeat until the convergence gate opens.

### Phase 1: Frame & Ground

1. **Ingest context:** read the prompt, workspace, and recent conversation. Separate the underlying problem from the proposed solution.
2. **Immediate exit check:** if existing context already supports a robust recommendation, deliver the synthesis now.
3. **Initialize the tracker** with four headings: **Core Objective**, **Hard Constraints** (budget, stack, deadline, performance), **Verified Facts** (confirmed versus assumed), **Active Forks**.

### Phase 2: Formulate & Ask

1. **Find the highest-leverage unknown:** the one unresolved parameter most likely to change the recommendation or eliminate options. Settle prerequisites first. When several unknowns compete, take them in this order: goal, hard constraints, success measure, reversibility, who decides, then details.
2. **Dispatch the question:**
   - State the decision context in 1–2 sentences.
   - Offer 2–4 distinct, viable options with a one-line trade-off each. Mark one `(Recommended)` when evidence supports it.
   - Use the host's interactive question tool when one exists, with structured options and a write-in choice. Otherwise ask in plain Markdown with bulleted options.
3. **Wait for the reply.** Never simulate or assume the user's answer.

### Phase 3: Research, Steelman & Squeeze

1. **Ingest the answer:** record it in the tracker. If the user changes an earlier premise, invalidate every downstream deduction, re-evaluate the affected options, and confirm the revised branch.
2. **Resolve unknowns autonomously:** when pricing, limits, compatibility, or other external facts matter, activate `web-research` before replying. Without it, search directly, prefer primary sources, and label anything unverified.
3. **Squeeze the choice:**
   - Does the mechanism deliver value proportional to its build and operating burden?
   - If it adds high friction, fragility, or needless complexity, challenge it: explain the failure mode and offer a lighter alternative.
   - Once the user affirms an informed trade-off, stop challenging it.
   - When a concrete proposal survives to the plan, activate `worth-the-squeeze` for a final verdict. Without it, state the strongest reason against and the cheapest way to test it.
4. **Pre-mortem:** before converging, ask or answer one question: "If this choice turned out badly in six months, what is the most likely reason?" Fold the answer into the plan.

### Phase 4: Converge & Plan

1. **Convergence gate:** stop questioning when all path-selecting dependencies are resolved, the remaining uncertainties are low-risk and reversible, or the user asks for a plan. Interviews usually settle within about seven questions; past that, offer to converge with labeled defaults.
2. **Finalize the tracker** and deliver the synthesis:

```markdown
# Discovery Synthesis & Decision Plan

## 1. Frame & Governing Constraints

- **Core Objective:** [Single-sentence statement of the true underlying goal]
- **Hard Constraints:** [Budget, stack, deadlines, performance, or team requirements]

## 2. Recommendation & Trade-Offs

- **Selected Direction:** [Direct recommendation]
- **Key Trade-Off:** [What is gained versus sacrificed compared to alternatives]
- **Rejected Alternatives:** [Why other candidate options were discarded]
- **Main Risk:** [Result of the pre-mortem]

## 3. Decision Ledger

- **Confirmed User Decisions:** [Decisions explicitly chosen by the user]
- **Assumed Defaults:** [Reversible defaults suggested by the agent for open non-blockers]
- **Revisit When:** [Observable conditions that would change this recommendation]

## 4. Execution Plan

1. [First reversible step, with completion criteria]
2. [Ordered action step 2 with completion criteria]
3. [Ordered action step 3 with completion criteria]
```

---

## 3. Edge Cases

| Situation                                                      | Action                                                                                                      |
| :------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| **Conflicting constraints** (e.g., zero cost + enterprise SLA) | Surface the conflict. Ask which constraint has priority; never silently drop one.                           |
| **Tool or search unavailable**                                 | Record unverified assumptions in the tracker. Give a conditional plan that branches on the unverified fact. |
| **User asks you to just decide**                               | Choose the reversible default, state the assumption and the revisit condition, and deliver the synthesis.   |
