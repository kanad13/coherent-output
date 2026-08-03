# Document De-identification and Anonymization

## Purpose

Create a shareable version of a document by removing or consistently replacing information that could identify people, organizations, projects, systems, or confidential business context. Preserve structure, meaning, tone, and formatting as closely as possible.

## Safety Boundary

De-identification reduces disclosure risk; it cannot guarantee that re-identification is impossible. Report residual risk honestly.

Do not overwrite the source document. Do not commit or publish the anonymized output or restoration key unless the user explicitly requests it.

## Sensitive Information Categories

Inspect for both direct and indirect identifiers:

- **People:** Names, usernames, signatures, pronouns tied to identity, job titles, reporting relationships, biographies
- **Contact details:** Email addresses, phone numbers, postal addresses, account handles
- **Organizations:** Company, customer, vendor, department, office, and team names
- **Projects and systems:** Product names, codenames, repositories, domains, hostnames, internal tools, ticket identifiers
- **Locations and dates:** Precise locations, travel details, exact dates, rare event combinations
- **Identifiers:** Employee, customer, device, IP, account, contract, and transaction identifiers
- **Business-sensitive facts:** Budgets, headcount, revenue, pricing, incidents, unpublished metrics, roadmaps
- **Embedded data:** Filenames, paths, URLs, image text, comments, document properties, revision history, EXIF or other metadata
- **Quasi-identifiers:** Combinations of otherwise ordinary facts that could reveal an identity

## Workflow

### 1. Establish Scope

- Identify the source and requested output.
- Determine the intended sharing audience and acceptable residual risk.
- Record any categories the user explicitly wants preserved or removed.
- Inventory file formats, attachments, images, tables, links, and metadata that need inspection.

**Visible output — Scope Note:** Intended audience, protected categories, preservation requirements, and known limitations.

### 2. Build the Sensitive-Entity Inventory

- Read the complete source before replacing anything.
- Record each unique sensitive entity and all known variants:
  - Capitalization variants
  - Abbreviations and aliases
  - Possessive or inflected forms
  - Usernames, email fragments, and initials
  - References embedded in paths, URLs, or filenames
- Identify indirect clues and sensitive relationships.
- Group the inventory by category.

### 3. Choose a Treatment

Assign one treatment to each inventory item:

- **Replace:** Use a consistent pseudonym or typed placeholder.
- **Generalize:** Replace precision with a broader value, such as an exact date with a month or an exact amount with a range.
- **Redact:** Remove information when no meaningful safe substitute exists.
- **Preserve:** Retain only when the sharing purpose requires it and the risk is acceptable.

Default to typed placeholders such as `PERSON_01`, `ORG_01`, and `PROJECT_01` for maximum auditability. Use readable pseudonyms when narrative readability matters. Every replacement must be unique and consistent.

### 4. Present the Replacement Manifest

Create a manifest containing:

| Original or Pattern | Variants | Category | Treatment | Replacement | Reason |
| --- | --- | --- | --- | --- | --- |

- Order literal replacements from longest to shortest.
- Flag uncertain entities and indirect identifiers separately.
- Pause for approval before applying replacements unless the user explicitly requested autonomous execution.

### 5. Apply Deterministic Changes

- Create a new output file; preserve the source.
- Prefer deterministic editing or transformation tools over generative rewriting.
- Apply approved literal replacements longest-first.
- Handle pattern-based data such as emails, phone numbers, IDs, and URLs.
- Inspect and sanitize filenames, links, images, comments, tracked changes, and metadata when the format supports them.
- Preserve formatting and document structure wherever possible.

### 6. Audit the Result

Perform all relevant checks:

- Search for every original term and known variant.
- Re-run pattern scans for contact data and identifiers.
- Read the output for contextual or relational clues.
- Verify replacement consistency and uniqueness.
- Confirm numbers, dates, and names were generalized as approved.
- Inspect document metadata and embedded assets.
- Compare structure and non-sensitive content against the source.

If new sensitive information is found, add it to the inventory, update the manifest, and repeat the necessary steps.

### 7. Handle the Restoration Key Safely

If reversibility is required:

- Create a separate restoration key only with the user's approval.
- Store it outside the shareable output location.
- Use a user-approved path and restrictive access controls when available.
- Never include the key in the anonymized document, repository, archive, or final shared package.

If reversibility is not required, do not create a key.

## Handoff

Report:

- Output location
- Categories treated
- Verification performed
- Whether a restoration key exists and where it was stored
- Any uncertain matches, unsupported file features, or residual re-identification risks

Never claim that the result is risk-free.
