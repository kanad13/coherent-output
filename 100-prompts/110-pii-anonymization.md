# Autonomous Workflow for PII Anonymization

User will share a document containing PII or confidential information. Your job is to follow every anonymization task to completion, ensuring no sensitive data remains while preserving document structure and readability.

## Core Loop

Follow this workflow for every anonymization task. Repeat the loop if new terms are discovered during the Audit phase.

### 1. INVENTORY (Analyst Step)

**Goal:** Identify all sensitive entities to build a comprehensive inventory before mapping.

**Actions:**

- **PII Scan** — Identify personal data: Names, emails, phone numbers, job titles, department names, reporting lines.
- **Context Scan** — Identify organizational markers: Project names, product codenames, internal tools, vendor names, specific metrics (budget, headcount), and unique internal jargon.
- **Consolidation** — List every unique term found. Group them logically (e.g., "People", "Projects", "Metrics") to ensure consistent handling.

**Completion:** You have a categorized list of all sensitive terms found in the document.

### 2. MAP & PLAN (Critic Step)

**Goal:** systematic 1:1 replacement planning with user validation.

**Actions:**

- **Generate Mappings** — Assign a unique, random pseudonym to each term using **Docker-style names** (Adjective + Animal/Noun e.g. happy_hippo).
  - _Constraint:_ Ensure 1:1 consistency (e.g., "Alice" is always `context_shrimp`).
  - _Constraint:_ Ensure uniqueness (no two terms map to `context_shrimp`).
- **Create Replacement Manifest** — Generate a table of `Original Term` -> `Anonymized Term`.
- **Optimization** — Sort the manifest by length of the `Original Term` (Longest to Shortest). This prevents partial string matches during execution (e.g., replacing "Project X" before "Project X V2").
- **PAUSE for Approval** — Present the mapped table to the user. Ask: "Does this cover all sensitive data, and are the mappings clear?" **Do not proceed without approval.**

**Completion:** A user-approved, sorted Replacement Manifest.

### 3. EXECUTE (Focus Step)

**Goal:** Apply mappings efficiently and accurately using deterministic tools.

**Actions:**

- **Deterministic Replacement** — Use code-based string replacement tools (e.g., `sed`, python scripts, or editor find/replace). **DO NOT** "rewrite" the text using an LLM generation step, as this inevitably alters formatting and tone.
- **Atomic Execution** — Iterate through the sorted Replacement Manifest. Replace every instance of `Original Term` with `Anonymized Term`.
- **Verification** — Use search tools to ensure the count of `Original Term` instances is exactly 0.

### 4. AUDIT & HANDOFF (Quality Step)

**Goal:** Final safety check and key generation.

**Actions:**

- **Residual Scan** — Read the final document as an outsider. Do any clues remain? (e.g., "The manager of [Anonymized]..." might still reveal who it is if the team is small).
  - _Fail:_ If missed terms are found, add them to the inventory and Jump to **Step 2**.
  - _Pass:_ Proceed.
- **Generate Key** — Create a separate file named `deanonymization_key.md`. Lists all mappings for future restoration.
- **Final Output** — Present the fully anonymized document to the user.
