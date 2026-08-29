---
title: "How-To: Generate LLM Context XML & Sitemaps"
description: "Practical guide for executing parse_llms_txt.py script to build XML context and sitemap files."
type: "guide"
id: "docs/how-to/generate-llms-context.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L2-Operational"
tags:
  - "dsom-protocol"
  - "how-to"
  - "llm-context"
related_links:
  - "docs/how-to/run-tool.md"
  - "docs/reference/cli-and-tools.md"
nav_order: 2
layout: "default"
---

# How-To Guide: Generating LLM Context XML & Sitemaps

This guide details how to execute `parse_llms_txt.py` to maintain updated context files and sitemaps.

---

## ⚡ Step-by-Step Procedure

### 1. Rebuilding All Documentation Artefacts

Execute the script with `--generate-all`:

```bash
python3 parse_llms_txt.py --generate-all
```

### 2. Generating Custom XML Context Payload

To convert a specific `llms.txt` file into `llm_context.xml`:

```bash
python3 parse_llms_txt.py --input llms.txt --output llm_context.xml --root .
```

### 3. Validating Results

Verify the output payload syntax:

```bash
head -n 20 llm_context.xml
```
