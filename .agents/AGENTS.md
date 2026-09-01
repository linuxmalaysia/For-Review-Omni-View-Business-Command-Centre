---
type: governance_constitution
title: "Omni View Sovereign AI Constitution & Agent Rulebook"
description: "Core constitutional AI rules, Local Knowledge-First discovery mandate, and Palace onboarding laws for Omni View Business Command Centre."
topics: [agents, dsom, okf, governance, rules, palace, discovery]
---

# 🤖 Sovereign AI Constitution & Agent Rulebook

Welcome to **Omni View Business Command Centre**. This repository operates under the **Deep State of Mind (DSOM)** framework and **Google OKF v0.2** standards. All AI agents (including Google Jules, Antigravity, Claude, and subagents) and human developers must adhere strictly to the rules codified below.

---

## 📜 Core Operational Mandates

### 1. Local Knowledge-First & Metadata Discovery Mandate
- **Rule**: Before attempting any external network access, searching Google, or executing probes on remote servers/nodes (e.g. Ansible hosts, cloud targets), the AI agent **MUST FIRST** search local project knowledge in `.agents/brain/` and `docs/`.
- **Metadata Search**: Use frontmatter metadata search (`topics:`, `description:`, `title:`) in OKF YAML headers or targeted directory inspection (`list_files`, `read_file`).
- **Scope**: External tools or remote execution are strictly reserved for applying approved changes or retrieving live runtime state that cannot be determined locally.

### 2. Spatial Memory & Palace Onboarding Law
- **Rule**: The repository uses the **Sovereign Markdown Palace** spatial memory system (`.agents/brain/`).
- **Start of Session / SOD Protocol**:
  1. Inspect `.agents/brain/palace_registry.md` to load the spatial map of Wings, Halls, and Rooms.
  2. Walk to the relevant Room and inspect its `closet.md` or targeted anchor file before reading long walkthrough logs.
  3. Update active session state in `.agents/brain/task.md` and `.agents/brain/implementation_plan.md`.

### 3. Open Knowledge Format (OKF v0.2) Standard
- **Rule**: Every documentation Markdown file under `docs/` and governance files under `.agents/` MUST open on line 1 with `---` containing OKF v0.2 YAML frontmatter.
- **Required Metadata**: `title`, `description`, `type`, `id`, `dsom_governance` (domain and context_tier), `tags` / `topics`, `related_links`, `nav_order`, and `layout`.

### 4. Minimal Context Window & Token Efficiency
- **Rule**: Bypassing unnecessary context window loading saves tokens and prevents context degradation.
- Read targeted line ranges or closet summaries rather than full repository snapshots.

### 5. Deterministic Verification & Testing
- **Rule**: Every state modification (file creation, edit, rename, deletion) MUST be verified using read-only tools.
- All code and documentation changes must pass the test suite (`uv run pytest`) and maintain documentation indexes (`python3 parse_llms_txt.py --generate-all`).

---

## 🧭 Document Routing Entry Points

- **Palace Registry**: `.agents/brain/palace_registry.md`
- **Knowledge-First Discovery SOP**: `docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md`
- **Onboarding Standard**: `START-HERE.md`
- **Documentation Index**: `docs/README.md` & `llms.txt`
