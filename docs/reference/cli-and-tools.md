---
title: "Technical Reference: CLI, Tools & Utilities Specifications"
description: "Factual CLI parameters for parse_llms_txt.py and CI automation tools."
type: "reference"
id: "docs/reference/cli-and-tools.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L3-TechnicalReference"
tags:
  - "dsom-protocol"
  - "reference"
  - "cli"
related_links:
  - "docs/reference/index.md"
  - "docs/reference/openwiki-emulator.md"
nav_order: 2
layout: "default"
---

# Technical Reference: CLI Tools & Utilities Specification

This document provides factual specifications for command-line options and parameters for utilities in Omni-View. For Python API function signatures, see [OpenWiki Engine Specification](openwiki-emulator.md).

---

## 🛠 `parse_llms_txt.py` Specification

Command line utility for parsing `llms.txt` files, generating XML context payloads, and maintaining site map files.

### Command Line Interface

```bash
python3 parse_llms_txt.py [OPTIONS]
```

#### CLI Parameters

| Flag | Short | Default | Description |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | `llms.txt` | Path to source `llms.txt` document. |
| `--output` | `-o` | `llm_context.xml` | Target output path for XML context payload. |
| `--root` | `-r` | `.` | Root directory of repository to resolve relative paths. |
| `--generate-all` | N/A | `False` | Trigger generation of `llms.txt`, `llms-full.txt`, `sitemap.txt`, and `sitemap.xml`. |
