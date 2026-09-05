#!/usr/bin/env python3
"""
tools/build_project_book.py

Universal Technical Handbook Assembler & Multi-Format Compiler
Standard: Terminal & Cloud Standard (DSOM Rule 11 & Rule 22)
"""

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT_DIR / "build" / "book"
BUILD_DIR.mkdir(parents=True, exist_ok=True)

MASTER_MD = BUILD_DIR / "master_book.md"
COVER_HTML = BUILD_DIR / "cover.html"
THEME_CSS = BUILD_DIR / "terminal-theme.css"

WARNING_KEYWORDS = re.compile(
    r"\b(BUG|FIX|Confirmed|live|vendor|NEVER|destroy|destructive|ORA-\d+|crash|escalation|hard way|WARNING|CAUTION|CRITICAL)\b",
    re.IGNORECASE
)


def extract_frontmatter_metadata(raw_content: str) -> tuple[dict, str]:
    """Extracts title and description from frontmatter and returns (metadata, content_without_frontmatter)."""
    metadata = {}
    content = raw_content
    lines = raw_content.splitlines()
    if lines and lines[0].strip() == "---":
        end_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx != -1:
            frontmatter_lines = lines[1:end_idx]
            content = "\n".join(lines[end_idx + 1:])
            for line in frontmatter_lines:
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    metadata[k] = v
    return metadata, content.strip()


def strip_frontmatter_and_footer(content: str) -> tuple[dict, str]:
    """Strips leading YAML frontmatter and document signature footers from markdown content."""
    metadata, content = extract_frontmatter_metadata(content)

    # Strip terminal signature block through end-of-file (\Z)
    content = re.sub(
        r"\n\n---\s*\n\*[^*]+(?:\(DSOM\)|All Rights Reserved|GNU General|Deep State of Mind).*\Z",
        "",
        content,
        flags=re.DOTALL
    )

    # Convert horizontal rules --- to *** ONLY outside fenced code blocks
    lines = content.splitlines()
    new_lines = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
        if not in_code_block and re.match(r"^---\s*$", stripped):
            new_lines.append("***")
        else:
            new_lines.append(line)

    return metadata, "\n".join(new_lines).strip()


def convert_github_alerts(text: str) -> str:
    """Transforms GitHub Markdown alerts into styled HTML callout cards."""
    pattern = re.compile(
        r"^>\s*(?:\*\*)?\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION|SUCCESS)\](?:\*\*)?(?:[ \t]*(.*))?\n((?:^>.*$\n?)*)",
        re.MULTILINE
    )

    def replacer(match):
        alert_type = match.group(1).upper()
        first_line = match.group(2) or ""
        raw_body = match.group(3) or ""
        lines = []
        if first_line.strip():
            lines.append(first_line.strip())
        for line in raw_body.splitlines():
            lines.append(re.sub(r"^>\s?", "", line))
        body = "\n".join(lines).strip()

        if alert_type in ("WARNING", "CAUTION", "IMPORTANT"):
            css_class = "callout callout-warning"
            icon = "⚠️" if alert_type != "CAUTION" else "🛑"
            title = alert_type.capitalize()
        elif alert_type in ("TIP", "SUCCESS"):
            css_class = "callout callout-tip"
            icon = "💡" if alert_type == "TIP" else "✅"
            title = alert_type.capitalize()
        else:
            css_class = "callout callout-note"
            icon = "💡"
            title = "Note"

        return f'\n<div class="{css_class}">\n<strong>{icon} {title}</strong>\n\n{body}\n</div>\n\n'

    return pattern.sub(replacer, text)


def scale_backticks(code_text: str) -> tuple[str, str]:
    """Dynamically scales outer code fences based on inner backtick counts."""
    max_ticks = 0
    matches = re.findall(r"(`{3,})", code_text)
    for m in matches:
        if len(m) > max_ticks:
            max_ticks = len(m)
    fence = "`" * max(3, max_ticks + 1)
    return fence, fence


def extract_commentary(code_text: str, lang: str = "yaml") -> str | None:
    """Extracts leading comment blocks (excluding shebangs) into operational commentary callouts."""
    lines = code_text.splitlines()
    comment_lines = []
    start_idx = 1 if lines and lines[0].strip() == "---" else 0
    for i in range(start_idx, len(lines)):
        l = lines[i]
        stripped = l.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            if stripped.startswith("#!"):
                continue  # Skip shebang line in commentary extraction
            comment_lines.append(stripped.lstrip("#").strip())
        else:
            break
    if not comment_lines:
        return None
    comment_text = " ".join(comment_lines)
    is_warning = bool(WARNING_KEYWORDS.search(comment_text))
    callout_class = "callout callout-warning" if is_warning else "callout callout-note"
    callout_title = "Developer Commentary — Read Before Executing" if is_warning else "Developer Operational Context"
    callout_icon = "⚠️" if is_warning else "💡"
    body = "\n".join(f"> {cl}" for cl in comment_lines[:15])
    return f'<div class="{callout_class}">\n<strong>{callout_icon} {callout_title}</strong>\n\n{body}\n</div>\n'


def ingest_code_file(file_path: Path, lang: str, title: str, anchor: str) -> str:
    """Ingests a source code file into a markdown chapter with commentary callouts."""
    if not file_path.exists():
        return f"\n*File not found: {file_path}*\n"
    content = file_path.read_text(encoding="utf-8", errors="replace")
    callout = extract_commentary(content, lang)
    fence_start, fence_end = scale_backticks(content)
    rel_path = file_path.relative_to(ROOT_DIR).as_posix()
    md_parts = [f'\n<a id="{anchor}"></a>\n### {title}\n']
    md_parts.append(f"**Source File:** `{rel_path}`\n")
    if callout:
        md_parts.append(callout)
    md_parts.append(f"{fence_start}{lang}\n{content.strip()}\n{fence_end}\n")
    return "\n".join(md_parts)


def ingest_doc_file(rel_path: str, heading_offset: int = 1, show_provenance: bool = True) -> str:
    """Ingests a documentation markdown file into the master handbook."""
    file_path = ROOT_DIR / rel_path
    if not file_path.exists():
        return f"\n*Documentation file not found: {rel_path}*\n"
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    metadata, clean = strip_frontmatter_and_footer(raw)
    clean = convert_github_alerts(clean)

    out = []
    if show_provenance:
        out.append(f'<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>{rel_path}</code></div>\n')

    if "description" in metadata and metadata["description"]:
        desc = metadata["description"]
        out.append(f'<div class="callout callout-note">\n<strong>📌 Executive Summary</strong>\n\n{desc}\n</div>\n')

    in_code_block = False
    for line in clean.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            out.append(line)
            continue

        if not in_code_block:
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                lvl = min(len(m.group(1)) + heading_offset, 6)
                hashes = "#" * lvl
                out.append(f"{hashes} {m.group(2)}")
                continue

        out.append(line)

    return "\n".join(out) + "\n"


def build_master_book():
    """Assembles the complete repository documentation and source code into master_book.md."""
    print("Assembling master book markdown...")
    parts = []

    # Book Executive Overview
    parts.append("""# Executive Overview {.unnumbered}
> **Classification:** PRIVATE AND CONFIDENTIAL (P&C)
> **Compiled By:** Antigravity Cognitive Twin
> **Standard:** Terminal & Cloud Technical Handbook Standard
""")

    # Part 1: Governance & Master Prompts
    parts.append("# Part 1: Governance & Compilation Master Prompts {.part}")
    parts.append(ingest_doc_file("docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md", heading_offset=1))

    # Part 2: How-To Guides & Skill Adoption
    parts.append("# Part 2: Operational How-To Guides {.part}")
    parts.append(ingest_doc_file("docs/how-to/HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK.md", heading_offset=1))
    parts.append(ingest_doc_file("docs/how-to/deploy-omni-view-on-render.md", heading_offset=1))
    parts.append(ingest_doc_file("docs/how-to/manage-inventory-and-payouts.md", heading_offset=1))

    # Part 3: Architecture & System Philosophy
    parts.append("# Part 3: Architecture & System Philosophy {.part}")
    parts.append(ingest_doc_file("docs/explanation/architecture-and-diataxis.md", heading_offset=1))
    parts.append(ingest_doc_file("docs/explanation/okf-02-and-diataxis.md", heading_offset=1))

    # Part 4: Core Implementation Source Code
    parts.append("# Part 4: Core Implementation Source Code {.part}")
    parts.append(ingest_code_file(ROOT_DIR / "parse_llms_txt.py", "python", "LLM Parser & Sitemap Utility", "code-parse-llms-txt"))
    parts.append(ingest_code_file(ROOT_DIR / "tools" / "generate_summary.py", "python", "Summary Table of Contents Generator", "code-generate-summary"))

    full_text = "\n\n".join(parts)
    MASTER_MD.write_text(full_text, encoding="utf-8")
    print(f"Master markdown written: {MASTER_MD} ({len(full_text):,} bytes)")


if __name__ == "__main__":
    build_master_book()
