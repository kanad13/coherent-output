---
name: progressive-documentation
description: Creates or restructures explanatory documents so readers understand the whole subject before exploring mechanisms, relationships, and detail. Use for multi-topic guides, system overviews, proposals, and documents that exhaust one topic before introducing the next. Do not expand brief answers or impose layers on procedure-only runbooks, chronological narratives, or lookup references.
---

# Progressive Documentation

Structure explanatory documents in breadth-first layers of depth. Establish the complete subject and its primary relationships before adding detailed mechanisms, trade-offs, and specifics.

---

## 1. Operating Invariants

1. **Breadth Before Depth:**
   - Introduce every major topic, component, or pillar at a high level before descending into the details of any single one.
   - Prohibit topic siloing: never exhaust Topic A before introducing Topic B.
2. **Verbatim Asset Preservation:**
   - Preserve all code blocks, data tables, numerical values, formulas, and quoted text byte-for-byte.
   - Do not mutate or truncate reference assets during restructuring.
3. **Scope Guard:**
   - Apply to multi-topic explanations, system overviews, proposals, strategy memos, and policies.
   - Do not apply to chronological runbooks, linear step-by-step procedures, or brief direct answers. Keep procedures in executable sequence.

---

## 2. The 4 Depth Strata

Organize content into four progressive layers:

| Layer                | Focus               | Contents                                                                                                                               |
| :------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Orientation**   | The Whole Subject   | Purpose, core problem or objective, all major topics/actors defined, unifying flow or lifecycle, and immediate bottom-line conclusion. |
| **2. Relationships** | Interconnections    | How the topics/actors interact, depend on each other, or collaborate across a shared workflow.                                         |
| **3. Dynamics**      | Nuance & Trade-offs | Constraints, trade-offs, decision rationale, risks, edge cases, and failure modes.                                                     |
| **4. Reference**     | Granular Specifics  | Exact specifications, implementation steps, configurations, formulas, tables, and verbatim data.                                       |

---

## 3. Execution Protocol

### Step 1: Inventory & Asset Isolation

1. Identify all primary topics, components, or pillars in the source material.
2. Extract and protect literal assets (tables, code, data points) to prevent mutation.

### Step 2: Stratum Allocation

1. Assign every fact, assertion, and section in the source to its appropriate layer (1–4).
2. Validate that every primary topic has a definition in Layer 1 before any topic appears in Layers 2–4.
3. Formulate a single unifying workflow or narrative that connects all topics.

### Step 3: Layered Drafting

1. **Draft Layer 1 (Orientation):** State the overarching goal or context. Introduce all topics briefly. Trace the unifying end-to-end flow. State the main takeaway.
2. **Draft Layer 2 (Relationships):** Detail how the topics interact. Ground explanations in the unifying workflow.
3. **Draft Layer 3 (Dynamics):** Explain why the system or policy is designed this way. Address constraints, risks, and alternatives.
4. **Draft Layer 4 (Reference):** Provide granular parameters, exact data, procedures, and literal assets.

### Step 4: Verification Gate

Confirm completion against these criteria:

- [ ] Every major topic is introduced in Layer 1.
- [ ] No topic's deep details appear before other topics are introduced.
- [ ] Each layer adds a distinct tier of depth across all topics.
- [ ] All code, tables, numbers, and quoted assets match the source byte-for-byte.
