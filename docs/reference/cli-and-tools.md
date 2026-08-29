---
title: "Technical Reference: CLI, Tools & Utilities Specifications"
description: "Factual CLI and Python API parameter specifications for parse_llms_txt.py and CI automation tools."
nav_order: 2
layout: default
---

# Technical Reference: CLI Tools & Utilities Specification

This document provides factual specifications for command-line tools, Python APIs, and automation utilities in Omni-View.

---

## 🛠 `parse_llms_txt.py` Specification

Command line utility and Python library for parsing `llms.txt` files, generating XML context payloads, and maintaining site map files.

### Command Line Interface

```bash
python3 parse_llms_txt.py [OPTIONS]
```

#### CLI Parameters

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--input`, `-i` | String | `llms.txt` | Path to input `llms.txt` file. |
| `--output`, `-o` | String | `llm_context.xml` | Path for generated XML context file. |
| `--root`, `-r` | String | `.` | Repository root path for relative file resolution. |
| `--generate-all` | Flag | `False` | Regenerates `llms.txt`, `llms-full.txt`, `sitemap.txt`, `sitemap.xml`. |

### Python API Interface

#### `parse_llms_txt(content_or_path: str) -> Dict[str, Any]`
Parses an `llms.txt` file path or raw text string into a structured dictionary.

- **Parameters**: `content_or_path` (`str`)
- **Returns**: `Dict[str, Any]` with keys `"title"`, `"summary"`, `"sections"`.

#### `generate_xml_context(llms_data: Dict[str, Any], root_dir: str = ".") -> str`
Converts parsed dictionary into formatted XML string.

- **Parameters**:
  - `llms_data` (`Dict[str, Any]`): Output from `parse_llms_txt()`.
  - `root_dir` (`str`): Base path for reading document files.
- **Returns**: Pretty-printed XML string (`str`).

#### `generate_llms_txt(docs_dir: str = "docs") -> str`
Generates canonical `llms.txt` string adhering to llmstxt.org format.

#### `generate_llms_full(docs_dir: str = "docs", root_dir: str = ".") -> str`
Generates consolidated `llms-full.txt` string containing all documentation.

#### `generate_sitemaps(docs_dir: str = "docs", base_url: str = "https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre") -> Tuple[str, str]`
Generates `sitemap.txt` and `sitemap.xml` strings.

---

## 🧪 Testing Utilities

Executed via `uv run pytest`:

- **`tests/test_docs_and_structure.py`**: Verifies Diátaxis folder tree, YAML frontmatter, `SUMMARY.md`, `llms.txt`, and sitemap files.
- **`tests/test_llms_parser.py`**: Unit tests for `parse_llms_txt.py` CLI and API functions.
- **`tests/test_html_files.py`**: DOM and layout assertions for HTML views in `Web Ui/`.
- **`tests/test_js_files.py`**: JavaScript code syntax and logic assertions.
- **`tests/test_css_files.py`**: CSS syntax and class assertions.
