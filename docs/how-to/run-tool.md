---
title: "How-To: Execute Tool Workflows"
description: "Step-by-step instructions for running repository utility tools and context generation scripts."
type: "guide"
id: "docs/how-to/run-tool.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L2-Operational"
tags:
  - "dsom-protocol"
  - "how-to"
  - "cli"
related_links:
  - "docs/reference/cli-and-tools.md"
  - "docs/how-to/generate-llms-context.md"
nav_order: 2
layout: "default"
---

# How-To Guide: Execute Tool Workflows

This guide provides explicit execution steps for running repository utility scripts and automation pipelines.

---

## ⚡ Generating All LLM Context Files & Sitemaps

To update `llms.txt`, `llms-full.txt`, `sitemap.txt`, `sitemap.xml`, and `llm_context.xml` across both root and `docs/` directories:

```bash
python3 parse_llms_txt.py --generate-all
```

### Expected Terminal Output:
```text
Generating documentation indexes and sitemaps...
Index generation complete.
XML context written to llm_context.xml
```

---

## 🧪 Running the Pytest Validation Suite

To execute structural, HTML, JS, CSS, and documentation integrity tests:

```bash
uv run pytest
```
