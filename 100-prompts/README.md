# Prompts (100-600 series)

System instructions and prompt templates organized by function. Each prompt defines a specific LLM behavior or workflow.

---

## 📋 Category Breakdown

### **100 Series: Agent Workflows & Autonomous Reasoning**

Foundational workflows for independent problem-solving and decision-making.

| Prompt                                               | Purpose                                                                                |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [100-agent-workflow.md](100-agent-workflow.md)       | Core 4-step cycle (Understand → Plan → Execute → Review) for autonomous task execution |
| [105-search-agent.md](105-search-agent.md)           | Fast information retrieval with intent parsing and citation management                 |
| [110-pii-anonymization.md](110-pii-anonymization.md) | Detect and remove personally identifiable information while preserving content         |
| [115-doc-updater.md](115-doc-updater.md)             | Intelligent document modification with conflict detection and approval workflows       |

**When to use:** Start every complex task with 100 or 105. Use 110/115 for data handling tasks.

---

### **200 Series: Information Synthesis & Analysis**

Prompts for integrating, analyzing, and brainstorming with information.

| Prompt                                                 | Purpose                                                                 |
| ------------------------------------------------------ | ----------------------------------------------------------------------- |
| [200-info-synthesize.md](200-info-synthesize.md)       | Merge new information into existing knowledge bases without data loss   |
| [205-tech-brainstorm.md](205-tech-brainstorm.md)       | Generate technical solutions through structured ideation                |
| [210-adaptive-pedagogue.md](210-adaptive-pedagogue.md) | Teach complex concepts by adapting to learner's level and pace          |
| [215-prompt-craft.md](215-prompt-craft.md)             | Engineer high-quality prompts through iterative refinement              |
| [220-skeptic-ai.md](220-skeptic-ai.md)                 | Challenge assumptions and identify weaknesses (adversarial review mode) |
| [225-precision-laconian.md](225-precision-laconian.md) | Communicate maximum information with minimum words                      |

**When to use:** 200 for knowledge management, 215 for prompt engineering, 220 for quality review.

---

### **300 Series: Content Formatting & Visualization**

Prompts for restructuring content into specific formats.

| Prompt                                             | Purpose                                                                |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| [300-markdown-files.md](300-markdown-files.md)     | Convert any text into well-structured, bullet-driven Markdown          |
| [305-markdown-repos.md](305-markdown-repos.md)     | Create comprehensive Markdown documentation for code repositories      |
| [310-mermaid-diagrams.md](310-mermaid-diagrams.md) | Generate flowcharts, architecture diagrams, and visual representations |
| [315-mermaid-slides.md](315-mermaid-slides.md)     | Build presentation slides using Mermaid syntax                         |

**When to use:** 300 for document structure, 310-315 for visual communication.

---

### **400 Series: Text Transformation**

Prompts for rewriting and adapting text for different purposes.

| Prompt                                               | Purpose                                                   |
| ---------------------------------------------------- | --------------------------------------------------------- |
| [400-text-simplify.md](400-text-simplify.md)         | Reduce complex language to everyday vocabulary            |
| [405-eli5-explain.md](405-eli5-explain.md)           | Explain technical concepts to children or novices         |
| [410-doc-redraft.md](410-doc-redraft.md)             | Rewrite documentation with improved clarity and structure |
| [415-info-consolidator.md](415-info-consolidator.md) | Merge multiple documents into a single cohesive summary   |

**When to use:** Chain these for multi-pass refinement (410 → 400 → 225).

---

### **500 Series: Communication & Code**

Prompts for professional communication and code documentation.

| Prompt                                           | Purpose                                                                  |
| ------------------------------------------------ | ------------------------------------------------------------------------ |
| [500-email-compose.md](500-email-compose.md)     | Draft professional emails with tone and audience control                 |
| [505-code-comments.md](505-code-comments.md)     | Generate clear, maintainable code comments and documentation strings     |
| [510-product-analyst.md](510-product-analyst.md) | Analyze products/features from user perspective with actionable insights |

**When to use:** 500 for external communication, 505 for code quality.

---

### **600 Series: Language-Specific Patterns**

Specialized prompts for specific languages or writing conventions.

| Prompt                                             | Purpose                                              |
| -------------------------------------------------- | ---------------------------------------------------- |
| [600-german-sentences.md](600-german-sentences.md) | Generate grammatically correct German sentences      |
| [605-german-articles.md](605-german-articles.md)   | Determine correct article (der/die/das) usage        |
| [610-german-word2word.md](610-german-word2word.md) | Translate technical terminology word-by-word         |
| [615-german-gender.md](615-german-gender.md)       | Predict gender and grammatical case for German words |

**When to use:** For language-specific tasks; can be adapted for other languages.

---

## 🔗 Usage Patterns

**Single-task workflows:**

- Information retrieval → `105-search-agent.md`
- Format document → `300-markdown-files.md`
- Simplify text → `400-text-simplify.md`

**Multi-step workflows:**

- Complex analysis → `100-agent-workflow.md` + `200-info-synthesize.md`
- Create documentation → `305-markdown-repos.md` + `505-code-comments.md`
- Quality refinement → `410-doc-redraft.md` → `400-text-simplify.md` → `225-precision-laconian.md`

**Specialized chains:**

- Prompt engineering → `215-prompt-craft.md` + `220-skeptic-ai.md`
- Teaching → `210-adaptive-pedagogue.md` + `405-eli5-explain.md`
- Product work → `510-product-analyst.md` + `500-email-compose.md`

---

## ✨ Design Notes

- **Numbering:** Categories increase by 100, items by 5, for future expansion
- **Scope:** Each prompt is focused on one task or workflow
- **Structure:** Role → Principles → Core Workflow (consistent format)
- **Modularity:** Prompts can be chained or used independently

---

_For main repo overview, see [../README.md](../README.md)_
