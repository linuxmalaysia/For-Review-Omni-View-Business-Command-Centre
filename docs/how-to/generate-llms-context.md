---
title: "How-To: Generate XML Context with parse_llms_txt.py"
description: "Practical guide for parsing llms.txt and generating XML context payloads for LLMs."
nav_order: 2
layout: default
---

# How-To Guide: Generating XML Context with parse_llms_txt.py

This guide explains how to run `parse_llms_txt.py` to convert `llms.txt` files into XML context structures and maintain site sitemaps.

---

## 🛠 How to Parse llms.txt into XML Context

Run `parse_llms_txt.py` specifying input file and output XML destination:

```bash
python3 parse_llms_txt.py --input llms.txt --output llm_context.xml --root .
```

- `--input`: Path to input `llms.txt` file.
- `--output`: Destination path for XML output file.
- `--root`: Root path used to locate referenced documentation files.

---

## 🔄 How to Synchronize All LLM Indexes and Sitemaps

Run the `--generate-all` command to update `llms.txt`, `llms-full.txt`, `sitemap.txt`, and `sitemap.xml`:

```bash
python3 parse_llms_txt.py --generate-all
```

This updates files in both the repository root and `docs/` directory.

---

## 🐍 How to Use Python API in Custom Scripts

Integrate `parse_llms_txt` into Python workflows:

```python
import parse_llms_txt

# 1. Parse llms.txt file into dictionary
data = parse_llms_txt.parse_llms_txt("llms.txt")
print(f"Title: {data['title']}")
print(f"Sections count: {len(data['sections'])}")

# 2. Generate XML context string
xml_output = parse_llms_txt.generate_xml_context(data, root_dir=".")

# 3. Write XML context to disk
with open("llm_context.xml", "w", encoding="utf-8") as f:
    f.write(xml_output)
```
