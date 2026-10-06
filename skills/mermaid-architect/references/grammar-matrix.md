# Mermaid Grammar Selector Matrix & Fallback Directory

Match the primary visual question to the native Mermaid grammar. Use fallback grammars when specialized or experimental grammars are unsupported by the target renderer.

---

## 1. Core & Established Grammars

| Visual Question / Domain                   | Primary Mermaid Grammar | Keyword / Declaration           | Ideal Use Case                                                | Fallback Grammar |
| :----------------------------------------- | :---------------------- | :------------------------------ | :------------------------------------------------------------ | :--------------- |
| **Process / Decision / Pipeline**          | Flowchart               | `flowchart TD` / `flowchart LR` | Algorithms, branching logic, CI/CD, execution pipelines       | `graph TD`       |
| **Actor Protocol / Time Sequence**         | Sequence Diagram        | `sequenceDiagram`               | API interactions, RPC handshakes, auth flows, event messaging | Flowchart LR     |
| **Object Lifecycle / State Transitions**   | State Diagram           | `stateDiagram-v2`               | FSMs, connection states, order status lifecycles, retries     | Flowchart TD     |
| **Database Schema / Entity Relationships** | ER Diagram              | `erDiagram`                     | SQL/NoSQL schemas, foreign keys, cardinality, data models     | Class Diagram    |
| **Class Hierarchy / Domain Types**         | Class Diagram           | `classDiagram`                  | OOP structures, interfaces, typing models, design patterns    | ER Diagram       |
| **Project Phases / Durations**             | Gantt Chart             | `gantt`                         | Project schedules, concurrent task execution, milestones      | Timeline         |
| **Category Proportions**                   | Pie Chart               | `pie`                           | Small number of non-negative parts of one whole               | Markdown Table   |

---

## 2. Specialized & Modern Grammars

| Visual Question / Domain               | Primary Mermaid Grammar | Keyword / Declaration             | Ideal Use Case                                            | Fallback Grammar              |
| :------------------------------------- | :---------------------- | :-------------------------------- | :-------------------------------------------------------- | :---------------------------- |
| **Cross-Team / Role Responsibility**   | Swimlane / Flowchart    | `flowchart TD` (with subgraphs)   | Cross-team, cross-service handoffs and ownership flows    | Flowchart LR                  |
| **Taxonomy / Concept Breakdown**       | Mindmap                 | `mindmap`                         | Category trees, feature breakdowns, mental models         | Flowchart TD                  |
| **Chronology / Milestones / Releases** | Timeline                | `timeline`                        | Release history, incident timelines, migration phases     | Gantt Chart                   |
| **User Experience / Journey**          | User Journey            | `journey`                         | User onboarding, step-by-step UX flows with satisfaction  | Flowchart LR                  |
| **Tradeoffs / 2x2 Matrix**             | Quadrant Chart          | `quadrantChart`                   | Risk vs. Value, Priority matrix, Capability evaluation    | Flowchart with Grid Subgraphs |
| **Branching / Version Control**        | Git Graph               | `gitGraph`                        | Branch/merge strategies, trunk-based development          | Flowchart LR                  |
| **System Architecture / Boundaries**   | C4 / Architecture       | `C4Context` / `architecture-beta` | Microservices topology, cloud infrastructure, trust zones | Flowchart with Subgraphs      |
| **Controlled Spatial Grid**            | Block Diagram           | `block-beta`                      | Deliberate spatial component layouts                      | Flowchart with Subgraphs      |
| **Magnitude & Flow Transfers**         | Sankey Diagram          | `sankey-beta`                     | Energy, cost allocation, conversion funnels               | Flowchart with labeled widths |
| **Quantitative Trends / Comparisons**  | XY Chart                | `xychart-beta`                    | Time series metrics, bar charts, benchmarks, throughput   | Markdown Table                |
| **Multi-Dimensional Profiles**         | Radar Diagram           | `radar-beta`                      | Competitor analysis, security posture scorecards          | Quadrant or Markdown Table    |
| **Hierarchical Proportions**           | Treemap                 | `treemap`                         | Proportional hierarchical breakdown                       | Flowchart / Pie               |
| **Set Overlaps & Intersections**       | Venn Diagram            | `venn-beta`                       | Set membership, shared features                           | Flowchart with Subgraphs      |
| **Cause & Effect / Root Cause**        | Ishikawa Diagram        | Mindmap / Flowchart               | Fishbone root cause analysis, incident post-mortems       | Flowchart LR                  |
| **Staged Workflow Status**             | Kanban Diagram          | `kanban`                          | Stage-based workflow and task progression                 | Flowchart with Subgraphs      |
| **Binary Protocol / Header Layout**    | Packet Diagram          | `packet-beta`                     | Network headers (IP/TCP), binary file structures          | Markdown Table or Flowchart   |
| **Event-Sourced Information Flow**     | Event Modeling          | `timeline` / Flowchart            | Event sourcing commands, events, read models              | Flowchart LR                  |
| **Strategic Value Chains**             | Wardley Map             | `wardley-beta`                    | Strategic evolution, dependencies, component inertia      | Flowchart TD                  |
| **Complexity Decision Domains**        | Cynefin Diagram         | `quadrantChart` / Flowchart       | Clear, complicated, complex, chaotic domains              | Flowchart Grid                |
| **Directory-Style Hierarchy**          | TreeView                | Mindmap / Flowchart               | Directory structures, nested files                        | Flowchart TD                  |
| **Requirement Traceability**           | Requirement Diagram     | `requirementDiagram`              | Verification matrix, compliance standards, risk mapping   | Flowchart TD                  |
| **Procedural Interaction Narratives**  | ZenUML                  | `zenuml`                          | Code-like procedural interaction narratives               | Sequence Diagram              |
