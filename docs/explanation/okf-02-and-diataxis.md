---
title: "Explanation: Google OKF 0.2 & DSOM Integration Rationale"
description: "Conceptual explanation of Google Ontological Knowledge Frame 0.2 and Domain-Specific Operational Model for AI agents."
nav_order: 2
layout: default
---

# Explanation: Google OKF 0.2 & DSOM Integration Rationale

This document explains the integration of **Google OKF 0.2 (Ontological Knowledge Frame)** and **DSOM (Domain-Specific Operational Model)** within the Omni-View repository documentation system.

---

## 💡 Conceptual Background

As LLM-driven autonomous AI agents (such as Google Jules, Antigravity, and CI sub-agents) assume active roles in software engineering tasks, standard unstructured documentation causes context window overflow, redundant file reads, and degraded code generation accuracy.

To address this, Omni-View integrates **Google OKF 0.2** and **DSOM** standards alongside the **Diátaxis Framework**.

---

## 🎯 Google OKF 0.2 (Ontological Knowledge Frame)

Google OKF 0.2 establishes a structured ontological schema for machine-readable context discovery:

1. **Explicit Entity Mapping**: Every file, utility, script, and database table has an unambiguous canonical path and type declaration in `docs/reference/file-structure-and-api.md` and `docs/reference/cli-and-tools.md`.
2. **Standardized Context Discovery (`llms.txt`)**: Following [llmstxt.org](https://llmstxt.org/), `llms.txt` maps all published documentation nodes with concise summaries. AI agents can parse this file to construct an XML context graph (`llm_context.xml`) without reading unneeded binary assets.
3. **Structured Frontmatter Metadata**: Every Markdown file in `docs/` contains standard Jekyll YAML frontmatter (`title`, `description`, `nav_order`), ensuring compatibility with both GitHub Pages and GitBook parser engines.

---

## ⚡ Domain-Specific Operational Model (DSOM)

DSOM defines operational boundaries and execution constraints for autonomous agents operating in this repository:

- **Minimal Sufficient Context**: AI agents must ingest only files directly pertinent to assigned tasks.
- **Reference Anchoring**: `docs/reference/file-structure-and-api.md` serves as the single source of truth for file paths and backend schemas.
- **Deterministic Verification Contract**: Every code change must be validated by running automated unit tests (`uv run pytest`) prior to PR submission.
