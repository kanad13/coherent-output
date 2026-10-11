# Adaptive discovery and painter framing: evaluation record

Date: 11 October 2026. Branch: `repo-audit`. Starting implementation: `b73c440`.

The [grill-me skill](skills/grill-me/SKILL.md) turns an uncertain intent into a practical decision through focused questions, investigation, and comparison. It asks about preferences the user must supply, investigates accessible facts itself, and updates its advice as the context changes. The [progressive-documentation skill](skills/progressive-documentation/SKILL.md) gains a brief painter analogy for the related writing preference: establish the whole composition, then refine its relationships and detail.

Nine fresh-agent trials and an independent review support the tested behavior. The review led to small clarifications about supporting workflows, question mechanisms, and stopping. The analogy pair showed usable results with and without the paragraph; it establishes no general performance improvement. Raw evidence is retained alongside the [earlier writing archive](evaluations/writing/README.md).

## 1. The intent and analogy decision

The discovery request calls for a thinking partner that uncovers the decision behind a proposed solution, asks progressively, brings useful evidence into the conversation, challenges weak premises, and converges. The structure must adapt to the decision rather than anticipate every domain. A restaurant choice needs less investigation than a software migration. A clear request to execute does not need an interview imposed on it.

The painter analogy works when the first pass establishes the whole composition and later passes refine it. “Faint” should mean fewer details, not vagueness or reduced accuracy. A map at increasing zoom is another plausible analogy, but zoom alone can encourage isolated detail without explaining relationships. Keeping the user's composition framing is a design choice; neither analogy was established as universally superior.

The skill includes one bounded paragraph. It explicitly preserves accuracy, essential conclusions, and the operational rules. The analogy does not request poetic language, repetition, or an analogy inside every delivered document.

Evidence about analogies needs careful scope. _Large Language Models as Analogical Reasoners_ reports gains from generating relevant worked exemplars before solving reasoning problems. That is a different intervention from adding a painter sentence to a skill. [ICLR paper](https://arxiv.org/abs/2310.01714)

_Conceptual Metaphor Theory as a Prompting Paradigm_ reports gains on its 100-task benchmark with four model families and an LLM evaluator. It does not establish improved adherence to this skill or to current Codex and Antigravity models. The practical inference is to use an analogy as compact framing, pair it with explicit instructions, and inspect real outputs. [Metaphor-prompting study](https://arxiv.org/html/2502.01901v1)

Anthropic's context guidance recommends clear instructions, useful examples, and refinement based on observed failures. Its guidance supports this evaluation method; it is not proof of the painter paragraph's benefit. [Context engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## 2. Research and workflow choices

The current upstream `grill-me` is a small entry point that calls `grilling`. That workflow models decision dependencies, asks ready questions in rounds with suggested answers, investigates accessible facts, and requires every branch to be visited before concluding with confirmation. The useful ideas are dependency order and investigating facts rather than outsourcing research to the user. [Upstream entry point](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md), [upstream interview](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)

A community Antigravity Skills listing appeared in search, but its page could not be retrieved. This investigation therefore does not establish that Google ships a first-party `grill-me` feature. The implementation uses the verified upstream concept and the user's requested behavior; it does not depend on that listing.

Selective clarification has a research basis: Zhang and Choi separate deciding when to ask, choosing the question, and answering with the new information. Their evaluated NLP tasks differ from broad real-world decision interviews, so the study motivates selective questioning rather than validating this implementation. [Clarify When Necessary](https://arxiv.org/abs/2311.09469)

The new skill owns the interview and final plan. `web-research` contributes authoritative investigation when external facts can affect the choice. `worth-the-squeeze` contributes engineering evaluation when a material proposal warrants it. Both are optional dependencies with local fallbacks, and their absence cannot be represented as completed invocation. Other decisions receive a proportionate comparison of benefit, cost, risk, reversibility, and opportunity cost.

The loop uses one focused question by default, bundles only independent prerequisites when useful, and updates a compact record of preferences, facts, assumptions, decisions, and open issues. It can suggest a labeled default when the user is unsure. It challenges conflicting constraints and weak premises without demanding a defense of settled tastes. It ends when further questions cannot materially improve the next step or the user asks to conclude. Recommendations remain distinct from choices the user actually made.

The skill is self-contained Markdown, without a tool-specific `Skill` API, a new executable helper, automatic capture files, or an exhaustive scenario catalog. It preserves prior execution authorization and does not add a blanket final approval gate. Installation uses the existing discovery and deployment routes.

## 3. Is the juice worth the squeeze?

### Proposal under review

The candidate change is a dedicated discovery skill, plus a bounded painter paragraph. The core problem is turning incomplete intentions into useful decisions while preserving the user's preference for focused questions and practical action. Extending a writing skill or an engineering-only evaluator would change its output contract; discovery instead produces a recommendation and next-step plan.

### The ledger

The benefit is a reusable interview across domains, with clear evidence and stopping rules. The cost is maintaining one new instruction file, its routing and inventory entry, and behavioral evidence. No runtime framework, new dependency, or host-specific command is introduced. Model adherence remains probabilistic.

### Trade-offs and risk

| Dimension             | Assessment                               | Evidence and consequence                                                                           |
| --------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Implementation effort | Low                                      | Existing Markdown skill format and installers suffice                                              |
| Regression scope      | Limited                                  | Added routing excludes clear execution requests; existing helpers and hook contracts are unchanged |
| Maintenance cost      | One new workflow                         | Supporting skills retain their domains; composition ownership is explicit                          |
| Opportunity cost      | Bounded                                  | Question selection and convergence avoid exhaustive interviews                                     |
| Main risk             | Excess questioning or unsupported advice | Multi-turn, stop, constraint, unavailable-tool, and live-research trials inspect these outcomes    |

### Verdict and action

**SCOPED PURSUE.** Keep the self-contained discovery loop and the short analogy paragraph. Preserve the existing writing and engineering skills as distinct jobs. Expand the instructions only when an observed failure or new requirement justifies it; do not build a domain catalog or claim universal reliability.

## 4. Acceptance criteria and independent trials

Before assessing outputs, the required behaviors were: ask a decision-relevant prerequisite rather than a questionnaire; use accessible local evidence; challenge constraints and proposals proportionately; preserve user corrections and stopping; label defaults and unavailable verification; produce an executable plan; and avoid unrequested implementation or external actions. The analogy pair must preserve every source fact and the exact warning while introducing the whole system before detail.

Producing agents received no conversation history, expected answer, or reviewer rubric. Each used an isolated installed-skill snapshot and permitted task artifacts. Simulated user replies arrived one turn at a time. The [records](evaluations/discovery/README.md) include the actual dispatch, tasks, replies, responses, and sibling snapshots where available.

| Trial                                           | Observed result                                                                                                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dining, three turns                             | Asked location first, then cuisine; incorporated a city/date correction; labeled defaults; gave a conditional plan with no invented venue or booking                                  |
| Local code, two turns                           | Reproduced case-sensitive matching, challenged hosted search against the laptop-only constraint, and proposed a local fix with checks under the user's two-hour cap                   |
| Reading club                                    | Honored settled constraints and “no more questions”; proposed a 90-minute facilitation plan with a feedback check                                                                     |
| Live research                                   | Read both supporting workflows, cited primary SQLite/Python documentation, used synthetic checks, and separated runtime evidence from unmeasured app performance                      |
| Conflicting constraints, two turns              | Exposed the impossible offline instant-sharing requirement, asked which constraint could move, then proposed a labeled offline default without product selection or further questions |
| Painter and plain, separate fresh agents        | Both retained all facts and the exact warning; both explained the full event path before detail. Neither introduced decorative prose. The pair establishes no causal improvement      |
| Eventual recommendation, final skill, two turns | Asked about the project's goal instead of prematurely recommending; after the answer and request to conclude, proposed a newsletter pilot with defaults labeled                       |
| Workflow composition, final skill               | Applied live research and engineering evaluation in a 225-word answer within the 250-word limit, with no further questions or appended reports                                        |

The independent reviewer found no demonstrated need for a redesign. It identified composition ambiguity between supporting report templates and the interview, a question-tool fallback that was too narrow, and stopping language that could confuse an eventual recommendation with “recommend now.” The skill received narrow corrections; the last two fresh trials exercised the refined contract.

The [final independent review](evaluations/discovery/composition-final/final-review.txt) recommends no further skill edits. It notes one output-level precision limit: the composition response's broad FTS5 sentence should refer specifically to the built-in trigram index and one- and two-character queries. Custom tokenizers are another extension path, so that sentence should not imply a universal impossibility. The sample's recommendation remains appropriate to the two-hour scope. The raw response is retained without retrospective correction. [SQLite custom tokenizers](https://www.sqlite.org/fts5.html#custom_tokenizers)

The saved live probe uses an in-memory database and synthetic strings. Its rerun and a separate parent rerun agree: token search does not match internal substrings; trigram `MATCH` misses one- and two-character queries; Python casefolded containment matches the tested short queries and `Straße`/`STRASSE`. The behavior agrees with the cited primary documentation. It does not establish performance or support in an uninspected app. [SQLite FTS5](https://www.sqlite.org/fts5.html#the_trigram_tokenizer), [Python strings](https://docs.python.org/3/library/stdtypes.html#str.casefold)

## 5. Lessons retained and verification limits

The broader work established several maintenance rules that apply here:

- Skill discovery, workflow invocation, executable helper calls, and native hook delivery are different claims. Each needs its own evidence.
- Preserve artifact-specific contracts. An interview, a document rewrite, an insertion-only diagram, and an engineering audit need different outputs and limits.
- Supporting workflows need explicit ownership and unavailable-step disclosure. Their default reports should not displace the requested result.
- Inspect saved outputs after post-processing. Keep raw trial bytes and the full input provenance so formatting or missing context cannot obscure what happened.
- Keep successful and unsuccessful historical evidence. Update instructions from specific findings, then use fresh agents to check the affected behavior.
- Keep canonical policy central while retaining enough local instruction for selective installations to work on their own.

The evidence is nine producing agents from one agent platform and one model configuration, plus independent review. It includes live browsing and synthetic probes but not complete tool transcripts, statistical comparisons, human learning measurements, or native Codex/Antigravity question-tool interactions. Resource limitations were declared in the dispatch prompts rather than enforced by a separate sandbox. User replies were scripted by the parent. Passing these tasks supports these samples; it does not guarantee arbitrary future adherence.

The evaluation archive remains useful as reviewable evidence and regression input. The checksum test protects its bytes rather than treating old snapshots as current instructions. The earlier archive is retained unchanged. The current [testing strategy](scripts/README.md#3-verification-strategy) adds multi-turn and composition checks to future skill maintenance.

Repository verification passes with 37 tests, formatting, and diagram checks across 27 Markdown files. All 16 skill metadata checks pass. Local navigation checks pass; inline-code link examples are excluded from active navigation. The archive test protects 45 earlier assets and 66 new assets, and controlled copies demonstrate failure on a changed user reply, a removed archive, or an unindexed trial. No earlier raw writing evidence changes and no tracked files are deleted.

The personal installer redeploys all 16 skills for Codex and Antigravity. A selective `skills@1.7.2` installation in a temporary project discovers 16 skills and installs only `grill-me` for Codex and Antigravity; its copied `SKILL.md` matches the final source byte-for-byte. Native Antigravity question and hook event delivery remain outside the claims of this evaluation.
