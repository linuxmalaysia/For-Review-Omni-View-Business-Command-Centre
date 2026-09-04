---
title: "Tutorial: LLMs.txt & XML Context Setup Pipeline"
description: "Step-by-step tutorial on generating, validating, and consuming llms.txt and XML context payloads."
type: "tutorial"
id: "docs/tutorials/llms-txt-setup.md"
dsom_governance:
  domain: "AI"
  context_tier: "L2-Operational"
tags:
  - "dsom-protocol"
  - "llms-txt"
  - "context-pipeline"
related_links:
  - "docs/how-to/generate-llms-context.md"
  - "docs/reference/cli-and-tools.md"
nav_order: 2
layout: "default"
---

# Tutorial: LLMs.txt & XML Context Setup Pipeline

This tutorial guides software engineers and autonomous AI agents through initializing, generating, and validating machine-parseable context files.

---

## 🎯 Learning Objectives

By completing this tutorial, you will:

- Understand the role of `llms.txt` and `llm_context.xml` in DSOM context management.
- Run `parse_llms_txt.py` to regenerate all index and sitemap files.
- Validate generated XML context for consumption by Large Language Models.

---

## 📋 Step 1: Execute Context Generator

Run the generator utility from the repository root:

```bash
python3 parse_llms_txt.py --generate-all
```

---

## 📋 Step 2: Verify Created Artifacts

Confirm that the following files have been created or updated:

- `llms.txt` and `docs/llms.txt`
- `llms-full.txt` and `docs/llms-full.txt`
- `sitemap.txt` and `docs/sitemap.txt`
- `sitemap.xml` and `docs/sitemap.xml`
- `llm_context.xml`

---

## 📋 Step 3: Parse Context in AI Pipelines

To ingest and validate documentation programmatically in Python:

```python
import xml.etree.ElementTree as ET
from parse_llms_txt import parse_llms_txt, generate_xml_context

parsed = parse_llms_txt("llms.txt")
xml_context = generate_xml_context(parsed, root_dir=".")
root = ET.fromstring(xml_context)
byte_count = len(xml_context.encode("utf-8"))
print(f"Validated XML context element <{root.tag}> containing {byte_count} bytes.")
```
