# Markdown Task Note Examples (Shape Reference Only)

## Checkbox and Indentation Syntax

Good:

```markdown
- [ ] task 01
  - context
- [x] task 02
  - context
  - more context
- [-] task 03
  - other context
```

Bad:

```text
[ ] task 01
- context
[x] task 02
- context
- more context
[-] task 03
- other context
```

## Self-Sufficient Action (No Context Bullets Needed)

- Input: `"check with elena if the annual software license has to be renewed before march 1 or if we can run month to month while legal reviews the new terms"`
- Bad: `- [ ] Confirm software license renewal timing and interim month-to-month legal eligibility with Elena`
- Good: `- [ ] Ask Elena if the annual software license must be renewed before March 1, or if we can run month-to-month while legal reviews the new terms`

## Backstory-First Input and Agenda-Bundled Meeting

- Input:
  - `"the vet said leo's booster shot is due - did we order it - check with maya"`
  - `"another task: arrange a meeting with daniel and priya from legal to review the partner agreement and give an update on the api launch. priya reports to daniel. also ask daniel to speak at the Q1 kickoff on Jan 15"`
- Good:

```markdown
- [ ] Ask Maya whether Leo's booster shot was ordered
  - The vet said Leo's booster shot is due.
- [ ] Arrange a meeting with Daniel and Priya from legal to review the partner agreement and share an API launch update
  - Ask Daniel to speak at the Q1 kickoff on January 15.
  - Priya reports to Daniel.
```

## Prerequisite Reordering and Research Questions

- Input:

```markdown
## need a new subsection

- this subsection is for hiring a summer intern for the frontend team
- hr already posted the role and sent 5 resumes, i need to review them
- beforehand i need to check how our intern program works, how many weeks they stay, whether they can convert to full time, what budget covers their laptop
```

- Good:

```markdown
## Frontend Intern Hiring

- [ ] Research how our intern program works before reviewing the resumes
  - How many weeks do interns stay?
  - Can they convert to full-time?
  - Which budget covers their laptop?
- [ ] Review the 5 resumes from HR for the frontend summer intern role
  - HR has already posted the role and shared the resumes.
```

## Existing Note with Mixed Updates

- Input:

```markdown
## Product & Operations

- [ ] Confirm staging server migration readiness with Priya
  - Current server runs Ubuntu 20.04.
  - Deploy to EU-West region. (changed: use EU-Central instead because of latency)
- [ ] Talk to Daniela about the new SaaS product design (done - we agreed to build a clickable prototype first and ask legal to review the free-tier terms)
- [ ] Add SSO login for enterprise customers (park this for now, waiting on Q3 budget approval)
- [ ] Email Sam the Q3 budget spreadsheet
```

- Good:

```markdown
## Product & Operations

- [ ] Ask Priya if the staging server is ready to migrate
  - Current server runs Ubuntu 20.04.
  - Deploy to EU-Central instead of EU-West due to latency.
- [x] Talk to Daniela about the new SaaS product design
  - Agreed to build a clickable prototype before full development.
- [ ] Build a clickable prototype for the new SaaS product
- [ ] Ask legal to review the free-tier terms for the new SaaS product
- [-] Add SSO login for enterprise customers
  - Parked until Q3 budget is approved.
- [ ] Email Sam the Q3 budget spreadsheet
```
