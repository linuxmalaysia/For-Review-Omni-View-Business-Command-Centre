---
title: "Tutorial: Setting Up LLMs.txt and Context Pipelines"
description: "Step-by-step tutorial on generating llms.txt, llms-full.txt, and XML context files for AI agents."
nav_order: 2
layout: default
---

# Tutorial: Setting Up LLMs.txt and Context Pipelines

This tutorial teaches you how to construct, generate, and consume `llms.txt` and XML context files for autonomous AI agents using `parse_llms_txt.py`.

---

## 🎯 Learning Objectives

By completing this tutorial, you will:
- Understand the `llms.txt` format specification.
- Generate `llms.txt`, `llms-full.txt`, and XML context files automatically.
- Pass XML context payloads to AI agent runtimes (e.g., Jules, LLM prompts).

---

## 📋 Prerequisites

- Python 3.9+ installed.
- Terminal / Command line access.
- Repository cloned locally.

---

## 🚀 Step 1: Generate Standard LLMs.txt and Sitemaps

Execute `parse_llms_txt.py` with the `--generate-all` flag to produce site indexes:

```bash
python3 parse_llms_txt.py --generate-all
```

Expected output:
```text
Generating documentation indexes and sitemaps...
Index generation complete.
XML context written to llm_context.xml
```

This creates `llms.txt`, `llms-full.txt`, `sitemap.txt`, and `sitemap.xml` in both the root directory and `docs/`.

---

## 📄 Step 2: Inspect the Output XML Context File

View `llm_context.xml` to examine the structured XML representation:

```bash
head -n 25 llm_context.xml
```

Sample output snippet:
```xml
<?xml version="1.0" ?>
<llm_context title="Omni-View Business Command Centre">
  <summary>Integrated Operations Management System documentation system...</summary>
  <sections>
    <section name="Core Documentation Quadrants">
      <document href="docs/tutorials/getting-started.md">
        <title>Getting Started Tutorial</title>
        <description>Guided onboarding tutorial for system usage.</description>
        <content>---
title: "Tutorial: Getting Started with Omni-View"...
        </content>
      </document>
    </section>
  </sections>
</llm_context>
```

---

## 🤖 Step 3: Provide XML Context to AI Agent Pipelines

Pass `llm_context.xml` or `llms-full.txt` directly to LLM context ingestion pipelines or system prompts:

```python
import parse_llms_txt

# Programmatically load XML context payload
with open("llm_context.xml", "r", encoding="utf-8") as f:
    xml_payload = f.read()

print(f"Loaded XML Context payload ({len(xml_payload)} bytes) for AI agent runtime.")
```

---

## 🎓 Next Steps

- Consult [How-To: Generate LLMs Context](../how-to/generate-llms-context.md) for custom parameter configurations.
- Review technical API details in [CLI & Tools Reference](../reference/cli-and-tools.md).
