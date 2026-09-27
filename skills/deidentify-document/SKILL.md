---
name: deidentify-document
description: Removes or replaces direct and indirect identifying information (PII, credentials, company codenames, internal IPs) from documents while preserving structure, formatting, and technical meaning. Use when anonymizing logs, sanitizing documents for sharing, or redacting sensitive data.
---

# Document De-identification & Anonymization

Follow this deterministic protocol to sanitize documents and datasets for safe external sharing.

---

## 1. Safety Boundary & Invariants

- **Source Preservation:** Never overwrite the original document. Write sanitized text to a separate output file (e.g., `<filename>.anonymized.md`).
- **Restoration Key Isolation:** Keep all translation tables and replacement keys in a secure, isolated artifact; never embed the key inside the shared deliverable.
- **Residual Risk Disclosure:** Explicitly report remaining quasi-identifier or re-identification risks at the conclusion of the audit.

---

## 2. Sensitive Information Categories

Audit the source document across eight distinct categories:

1. **People:** Names, usernames, signatures, job titles, and biographies.
2. **Contact Details:** Email addresses, phone numbers, postal addresses, Slack handles.
3. **Organizations:** Company names, client names, vendors, partners, and internal team labels.
4. **Projects & Systems:** Codenames, repository names, internal domains, hostnames, tickets (`PROJ-1234`).
5. **Locations & Timestamps:** Exact coordinates, internal conference rooms, travel itineraries, precise timestamps.
6. **Technical Identifiers:** IP addresses, MAC addresses, employee IDs, customer UUIDs, tokens, and database primary keys.
7. **Business Metrics:** Budgets, revenue, pricing tables, headcount, incident severity reports.
8. **Quasi-Identifiers:** Combinations of non-sensitive facts that collectively identify a subject.

---

## 3. Seven-Step Execution Pipeline

### Step 1: Establish Scope & Risk Posture

- Determine the target audience and acceptable residual risk.
- Identify specific entities the user explicitly wants preserved or masked.

### Step 2: Build Sensitive-Entity Inventory

- Read the entire document before applying modifications.
- Record every unique entity along with all lexical variants (capitalizations, abbreviations, possessives).

### Step 3: Assign Deterministic Treatments

Assign one of four treatments to each item:

- **`Replace`:** Substitute with typed, deterministic placeholders (`PERSON_01`, `ORG_01`, `HOST_01`).
- **`Generalize`:** Replace exact precision with broader ranges (e.g., replace `June 14, 2024` with `Q2 2024`).
- **`Redact`:** Omit completely where deletion is safest.
- **`Preserve`:** Retain standard public technologies or library names.

### Step 4: Present Replacement Manifest

Display the proposed mapping table for inspection before applying changes.

### Step 5: Apply Deterministic Substitutions

- Apply replacements consistently across text, code snippets, headers, and image alt-texts.
- Guarantee that `PERSON_01` maps to the exact same individual across all occurrences.

### Step 6: Post-Sanitization Audit

- Scan the output for leaked substrings, email domain fragments, or leftover identifiers.

### Step 7: Store Deliverables Safely

- Output the clean, anonymized document.
- Store the translation key in an isolated, private file.
