---
title: "SOP: Knowledge-First Discovery & Context Preservation Protocol"
description: "SOP detailing how AI agents and human operators leverage OKF YAML frontmatter (topics, description) in .agents/brain/ and docs/ before external search or remote execution."
type: "standard_operating_procedure"
id: "docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md"
dsom_governance:
  domain: "AI"
  context_tier: "L1-Overview"
tags:
  - "okf"
  - "discovery"
  - "context-management"
  - "brain"
  - "dsom"
  - "sop"
topics:
  - "okf"
  - "discovery"
  - "context-management"
  - "brain"
  - "dsom"
  - "sop"
related_links:
  - "docs/explanation/dsom-governance.md"
  - "docs/explanation/okf-02-and-diataxis.md"
  - ".agents/AGENTS.md"
  - ".agents/brain/palace_registry.md"
nav_order: 3
layout: "default"
---

# 📚 SOP: Local Knowledge-First Discovery & OKF Context Protocol

## 1. Executive Intent

To prevent unnecessary SSH probes, remote server executions, token context window exhaustion, and context loss during agentic sessions, AI agents and human operators must adhere strictly to the **Local Knowledge-First Protocol**.

All project facts, architectural specifications, UI components, data structures, and operational rules are indexed via **Google OKF v0.2 YAML Frontmatter** in `.agents/brain/`, `.agents/skills/`, and `docs/`.

---

## 2. Standard Operating Procedure (Step-by-Step Discovery Flow)

```text
[ Step 1: User Request / Task Assignment ]
         │
         ▼
[ Step 2: Local OKF Frontmatter & Metadata Search ] ──▶ grep / inspect .agents/brain/ & docs/ (topics: / description:)
         │
         ▼
[ Step 3: Targeted File Reading & Line Inspection ] ──▶ read closet.md or targeted line ranges on matched .md files
         │
         ▼
[ Step 4: Local Code / Unit Test Execution ] ──▶ verify behavior using local scripts & uv run pytest
         │
         ▼
[ Step 5: Remote Execution / External Search ] ──▶ ONLY if information is absent locally and required for task completion
```

---

### Step 1: Local Frontmatter & Metadata Search
Before issuing any remote SSH/Ansible probe or performing external search (e.g. Google):
1. **Query OKF Frontmatter**: Search local `.md` files in `docs/` and `.agents/brain/` for relevant `topics:`, `description:`, or `title:` fields.
2. **Consult Spatial Registry**: Inspect `.agents/brain/palace_registry.md` to identify the designated Wing, Hall, and Room for the domain.

### Step 2: Targeted File Inspection
Once the relevant document or spatial anchor is located:
- Read specific closet files (`closet.md`) or targeted line ranges to preserve token efficiency.
- Avoid ingesting unreferenced binary files or entire full-repository dumps.

### Step 3: Verified Execution
- Run localized unit tests (`uv run pytest`) and validation scripts (`parse_llms_txt.py`) to confirm workspace integrity.

---

## 3. Mandatory Rules Reference

- **Rule (OKF Frontmatter)**: All documentation and governance `.md` files must open on line 1 with `---` and contain valid OKF v0.2 YAML metadata.
- **Rule (Metadata-First Discovery)**: Always search `topics:` and `description:` metadata before reading full file bodies.
- **Rule (Local Knowledge-First Mandate)**: Search `.agents/brain/` and `docs/` locally before searching Google or reaching out to remote servers/nodes.
