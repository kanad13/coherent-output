# Document De-identification and Anonymization

## Purpose

Use this methodology when creating shareable versions of documents by removing or replacing identifying information about people, organizations, projects, systems, or confidential business context. Preserve structure, meaning, tone, and formatting.

## Safety Boundary

De-identification reduces disclosure risk. Report the remaining re-identification risk and the limits of the completed checks.

Preserve the source document and create a separate anonymized output. Commit or publish the anonymized output after the user explicitly requests that action. Keep every restoration key in its approved private location.

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
- **Quasi-identifiers:** Combinations of individually ordinary facts that could reveal an identity

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
- **Redact:** Remove information when deletion provides the safest treatment.
- **Preserve:** Retain information required by the sharing purpose when the risk is acceptable.

Default to typed placeholders such as `PERSON_01`, `ORG_01`, and `PROJECT_01` for maximum auditability. Use readable pseudonyms when narrative readability matters. Every replacement must be unique and consistent.

### 4. Present the Replacement Manifest

Create a manifest containing:

| Original or Pattern | Variants | Category | Treatment | Replacement | Reason |
| ------------------- | -------- | -------- | --------- | ----------- | ------ |

- Order literal replacements from longest to shortest.
- Flag uncertain entities and indirect identifiers separately.
- Present the manifest and pause for approval by default. Proceed autonomously when the user explicitly requests that mode.
- Treat the manifest and restoration key as sensitive material.
- Display or store original values in a user-approved private context.
- Use masked values when approval can be completed with a partial identifier.
- Keep both artifacts separate from public issues, commits, shared packages, and publications.

### 5. Apply Deterministic Changes

- Create a new output file; preserve the source.
- Prefer deterministic editing or transformation tools over generative rewriting.
- Apply approved literal replacements longest-first.
- Handle pattern-based data such as emails, phone numbers, IDs, and URLs.
- Inspect and sanitize filenames, links, images, comments, tracked changes, and metadata when the format supports them.
- Preserve formatting and document structure wherever possible.
- When an available tool lacks access to an embedded feature, report the feature and the resulting residual risk. Release proceeds after capable tooling verifies it or the user explicitly accepts the documented residual risk.

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
- Keep the key exclusively in its approved secure location, separate from the anonymized document, repository, archive, and final shared package.

Create a restoration key for reversible workflows.

## Handoff

Report:

- Output location
- Categories treated
- Verification performed
- Whether a restoration key exists and where it was stored
- Any uncertain matches, unsupported file features, or residual re-identification risks

Describe the result as risk-reduced and include the residual risks.
