# Coherent Output

A curated repository of **artifacts for controlling and improving LLM output quality**.

This is your centralized toolkit for working with AI agents: system prompts, custom instructions, evaluation rubrics, and domain knowledge modules—everything you need to shape consistent, high-quality AI behavior.

---

## 🎯 The Problem & Solution

LLMs are powerful but unpredictable. Without structured guidance:

- Outputs are inconsistent across similar tasks
- Quality varies widely by prompt phrasing
- Workflows lack repeatability
- Agent behavior is hard to control

**Coherent Output solves this** by packaging tested prompts, instructions, and patterns into reusable artifacts.

---

## 📁 What's Inside

### 1. **Prompts** (`/100-prompts`)

System instructions and prompt templates that define agent behavior and workflows.

**Categories:**

- **100s:** Agent workflows & autonomous reasoning loops
- **200s:** Information synthesis, analysis, and brainstorming
- **300s:** Content formatting (Markdown, Mermaid, diagrams)
- **400s:** Text transformation (simplification, redrafting, explanation)
- **500s:** Communication & code (email, comments, product analysis)
- **600s:** Language-specific patterns (German, technical writing, etc.)

👉 **Start here:** [100-prompts/README.md](100-prompts/README.md)

### 2. **Skills** (`/skills`) — _TBD_

Reusable domain knowledge modules that teach agents specialized practices:

- Coding patterns & best practices
- Writing & communication guidelines
- Domain-specific terminology
- Process workflows

### 3. **Instructions** (`/instructions`) — _TBD_

VS Code & Copilot customization files for personal agent configuration:

- `.instructions.md` — Default behavior overrides
- `.prompt.md` — Custom prompt templates
- `.agent.md` — Multi-agent routing logic

### 4. **Hooks** (`/hooks`) — _TBD_

Conditional logic and trigger patterns for intelligent artifact selection:

- Rule-based prompt routing
- Context-aware agent selection
- Workflow branching logic

### 5. **Rubrics** (`/rubrics`) — _TBD_

Quality evaluation frameworks and scoring templates:

- Output quality checklists
- Tone & style scoring criteria
- Completeness evaluation templates

---

## 🚀 How to Use

1. **For quick guidance:** Browse [100-prompts/](100-prompts) by category number
2. **For consistency:** Apply evaluation rubrics before finalizing outputs
3. **For personalization:** Set up custom instructions in `/instructions`
4. **For scaling:** Use skills and hooks to automate artifact selection

---

## 📝 Contribution Guidelines

When adding new artifacts:

- Use category numbering for discoverability (100s, 200s, etc.)
- Write clear purpose statements at the top of each file
- Test prompts before adding them
- Keep artifacts focused and modular
- Link related files for easy navigation

---

## ✨ Design Philosophy

**Measure twice, cut once:**
Build mental models through analysis before executing changes. Every artifact here is meant to reduce guesswork and increase output consistency.

---

## 📚 Resources

- See individual folder READMEs for detailed category breakdowns
- Each prompt includes a role/persona and core workflow
- Rubrics provide explicit success criteria
- Skills contain step-by-step domain knowledge

---

_Last Updated: March 1, 2026_
