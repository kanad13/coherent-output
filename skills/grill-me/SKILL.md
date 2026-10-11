---
name: grill-me
description: Runs an adaptive discovery interview that turns an uncertain goal, choice, or proposed change into an evidence-informed recommendation and next-step plan. Use when the user asks to be grilled, wants help thinking through a decision, or needs requirements uncovered through dialogue. Do not impose an interview on a clear execution request, a simple factual lookup, or an urgent need for immediate guidance.
---

# Grill Me: Adaptive Discovery & Decision Protocol

Follow this protocol to conduct an adaptive discovery interview. Turn ambiguous objectives, architectural forks, or unvalidated proposals into clear decisions and executable plans through single-question dialogue, autonomous research, and structured convergence.

---

## 1. Non-Negotiable Operational Invariants

1. **Single-Question Invariant:**
   - Ask exactly **one** focused question per turn.
   - Never output questionnaires, surveys, or multi-question lists.
   - _Exception:_ Bundling is permitted only when 2–3 options are strictly co-dependent and unlock the exact same immediate choice.
2. **Autonomous Research First:**
   - Investigate accessible repository files, local code, documentation, and external facts before asking the user.
   - Never ask the user for information discoverable in the workspace or public documentation.
3. **Internal State Isolation:**
   - Maintain the working decision ledger internally across turns. Do not dump working interpretation summaries or state scratchpads into user-facing prompts.
4. **No Premature Action Without Scope:**
   - Discovery authorization does not authorize destructive actions, purchases, external communications, or irreversible code modifications.
   - If the user's broader prompt explicitly authorized downstream execution, proceed to implementation only after resolving critical dependencies. Otherwise, terminate at the synthesis plan.
5. **Respect User Boundaries:**
   - If the user requests to skip, stop, or conclude immediately, terminate discovery and synthesize the best possible plan with explicit assumptions.
   - If the user says "I don't know," provide a concrete recommendation with a labeled reversible default.

---

## 2. Four-Phase Discovery Protocol

```
┌─────────────────┐     ┌───────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│ Phase 1:        │ ──► │ Phase 2:          │ ──► │ Phase 3:            │ ──► │ Phase 4:        │
│ Frame & Ground  │     │ Formulate & Ask   │     │ Research & Evaluate │     │ Converge & Plan │
└─────────────────┘     └───────────────────┘     └─────────────────────┘     └─────────────────┘
```

### Phase 1: Frame & Ground

1. **Ingest Context:**
   - Inspect user prompt, active workspace, files, and recent conversation history.
   - Separate the **underlying problem** (core need) from the **proposed solution** (mechanism).
2. **Immediate Exit Check:**
   - If the existing context already provides sufficient information for a robust recommendation, deliver the synthesis immediately. Do not invent questions to satisfy an arbitrary interview quota.
3. **Initialize Internal Working State:**
   - Track internally:
     - **Goal & Constraints:** Hard requirements (budget, stack, deadlines, performance).
     - **Verified Facts:** Confirmed workspace facts vs. unverified assumptions.
     - **Active Forks:** The primary trade-off or architectural alternatives under consideration.

### Phase 2: Formulate & Ask

1. **Identify the Highest-Leverage Unknown:**
   - Determine the single unresolved parameter most likely to shift the recommendation or eliminate options.
   - Sequence prerequisites first: settle architecture before discussing configuration details.
2. **Format and Dispatch Question:**
   - State the decision context in 1–2 direct sentences.
   - Offer 2–4 distinct, viable options with a brief trade-off rationale.
   - State a recommended option when evidence supports one, clearly labeled as `(Recommended)`.
   - Tool selection:
     - If the host provides an interactive question tool (e.g., `ask_question`), use it with structured options and write-in support.
     - Otherwise, output direct conversational Markdown with clear bullet options.
3. **Wait for User Response:**
   - Never simulate or assume the user's answer in the same turn. Wait for the user to reply.

### Phase 3: Research & Evaluate

1. **Evaluate User Input:**
   - Update internal working state with confirmed decisions and constraints.
   - Replace earlier assumptions when the user provides contradictory facts.
2. **Autonomous Unknown Resolution:**
   - If the user's answer surfaces technical, pricing, or library questions, activate `web-research` (or search tools) autonomously before responding.
   - Cite authoritative primary sources for verified facts.
3. **Challenge Anti-Patterns Proportionately:**
   - If the user's chosen direction contradicts known constraints or introduces disproportionate maintenance burden, activate `worth-the-squeeze` principles.
   - Highlight the specific trade-off or failure mode and provide a lightweight counter-proposal.
   - Stop challenging once the user affirms a deliberate trade-off.

### Phase 4: Converge & Plan

1. **Convergence Gate:**
   - Terminate questioning when:
     - All critical dependencies for selecting a path are resolved.
     - Remaining uncertainties are low-risk and reversible.
     - The user requests a recommendation or plan.
2. **Deliver Structured Synthesis Report:**

```markdown
# Discovery Synthesis & Decision Plan

## 1. Frame & Governing Constraints

- **Core Objective:** [Single-sentence statement of the true underlying goal]
- **Hard Constraints:** [Budget, stack, deadlines, performance, or team requirements]

## 2. Recommendation & Trade-Offs

- **Selected Direction:** [Direct recommendation]
- **Key Trade-Off:** [What is gained vs. what is sacrificed compared to alternatives]
- **Rejected Alternatives:** [Why other candidate options were discarded]

## 3. Decision Ledger

- **Confirmed User Decisions:** [Decisions explicitly chosen by the user]
- **Assumed Defaults:** [Reversible defaults suggested by the agent for open non-blockers]

## 4. Execution Plan

1. [Ordered action step 1 with completion criteria]
2. [Ordered action step 2 with completion criteria]
3. [Ordered action step 3 with completion criteria]
```

---

## 3. Edge-Case Handling

| Situation                                                      | Action                                                                                             |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **Conflicting constraints** (e.g., zero cost + enterprise SLA) | Surface the conflict directly. Ask which constraint has priority; do not silently drop one.        |
| **User says "I don't know" or skips**                          | Supply a reasonable, reversible default. Explain why it is safe, note the assumption, and advance. |
| **User changes earlier premise**                               | Invalidate downstream deductions. Re-evaluate affected options and confirm the revised branch.     |
| **Tool / search unavailable**                                  | State unverified assumptions clearly. Provide a conditional plan branching on the unverified fact. |
