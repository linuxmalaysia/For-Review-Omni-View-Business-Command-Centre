---
title: "OpenWiki Engine & Data Parsing Specification"
description: "Technical reference and API specification for OpenWiki parsing utilities and batch operations."
type: "reference"
id: "docs/reference/openwiki-emulator.md"
dsom_governance:
  domain: "DataEngineering"
  context_tier: "L3-TechnicalReference"
tags:
  - "dsom-protocol"
  - "reference"
  - "openwiki"
related_links:
  - "docs/reference/cli-and-tools.md"
  - "docs/reference/file-structure-and-api.md"
nav_order: 3
layout: "default"
---

# OpenWiki Engine Specification

This specification documents data extraction, Markdown parsing, and batch document processing engines within the repository's tooling environment.

---

## 🛠 `parse_llms_txt` Integration Engine

`parse_llms_txt.py` acts as the primary parser and context builder for DSOM/OKF knowledge graphs.

### Function Signatures

```python
def parse_llms_txt(content_or_path: str) -> Dict[str, Any]:
    """Parse llms.txt content or file path into structured metadata dictionary."""

def generate_xml_context(llms_data: Dict[str, Any], root_dir: str = ".") -> str:
    """Generate XML context tree containing document metadata and embedded content."""

def generate_llms_txt(docs_dir: str = "docs", relative_to_docs: bool = False) -> str:
    """Generate Markdown llms.txt index content."""

def generate_llms_full(docs_dir: str = "docs", root_dir: str = ".") -> str:
    """Build consolidated documentation text for all indexed Markdown files."""

def generate_sitemaps(docs_dir: str = "docs", base_url: str = "https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre") -> Tuple[str, str]:
    """Generate text and XML sitemap strings."""
```

### Exit Codes & Exception Behavior

- Exit `0`: Successful execution and output generation.
- Exception `RuntimeError`: Raised when an indexed file path in `llms.txt` cannot be read during XML generation.
