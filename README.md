# Coherent Output

A curated repository for achieving **steerable, consistent, and predictable LLM results**.

### 🧩 Why "Coherent"?

LLMs often produce fragmented or erratic outputs. "Coherence" in this context means:

- **Logical Flow:** Instructions that guide the model through a clear reasoning path.
- **Consistency:** Similar inputs yielding structurally similar, high-quality results.
- **Steerability:** The ability to precisely tune the model's behavior via modular artifacts.

This repository packages tested prompts, skills, and instructions into reusable modules to reduce guesswork and increase reliability in AI-assisted workflows.

---

## 📁 Repository Structure

Each directory contains specialized artifacts to shape AI behavior. Follow the links below for detailed documentation.

- [**100-prompts/**](100-prompts/README.md) - System instructions and prompt templates (100-600 series).
- [**200-skills/**](200-skills/README.md) - Reusable domain knowledge modules and best practices.
- [**300-instructions/**](300-instructions/README.md) - VS Code & Copilot customization (.instructions, .prompt, .agent files).
- [**400-hooks/**](400-hooks/README.md) - Logic and trigger patterns for context-aware artifact selection.
- [**500-rubrics/**](500-rubrics/README.md) - Quality evaluation frameworks and scoring templates.

---

## 🚀 Getting Started

1. **Browse Prompts:** Start with the [100-series](100-prompts/README.md#100-series-agent-workflows) for foundational agent workflows.
2. **Apply Patterns:** Use the `200-skills` to provide context for specific technical tasks.
3. **Verify Quality:** Use `500-rubrics` to evaluate and refine AI outputs.

---

## ✨ Design Philosophy

**Measure twice, cut once:** Build a strong mental model before execution. Every artifact here is designed to enforce this rigor, turning unpredictable LLM interactions into reliable, professional-grade outputs.
