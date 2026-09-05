#!/usr/bin/env python3
"""
tools/build_project_book.py

Universal Technical Handbook Assembler & Multi-Format Compiler
Standard: Terminal & Cloud Standard (DSOM Rule 11 & Rule 22)
"""

from __future__ import annotations

import re
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


def parse_fence_delimiter(line: str) -> tuple[str, int, bool] | None:
    """Parses fence delimiter character, length, and whether it's a standalone closing fence (no info string).
    Returns (char, length, is_standalone_closing).
    """
    stripped = line.strip()
    m = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
    if m:
        delim = m.group(1)
        info_string = m.group(2).strip()
        is_closing = (info_string == "")
        return delim[0], len(delim), is_closing
    return None


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
    active_fence: tuple[str, int] | None = None

    for line in lines:
        fence = parse_fence_delimiter(line)
        if fence:
            f_char, f_len, f_is_closing = fence
            if active_fence is None:
                active_fence = (f_char, f_len)
            elif f_char == active_fence[0] and f_len >= active_fence[1] and f_is_closing:
                active_fence = None
            new_lines.append(line)
            continue

        if active_fence is None and re.match(r"^---\s*$", line.strip()):
            new_lines.append("***")
        else:
            new_lines.append(line)

    return metadata, "\n".join(new_lines).strip()


def convert_github_alerts(text: str) -> str:
    """Transforms GitHub Markdown alerts into styled HTML callout cards while preserving literal blocks in fences."""
    lines = text.splitlines()
    processed_lines = []
    active_fence: tuple[str, int] | None = None
    buffer = []

    def process_buffer(buf_lines: list[str]) -> list[str]:
        buf_text = "\n".join(buf_lines)
        if not buf_text:
            return []
        pattern = re.compile(
            r"^>\s*(?:\*\*)?\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION|SUCCESS)\](?:\*\*)?(?:[ \t]*(.*))?\n((?:^>.*$\n?)*)",
            re.MULTILINE
        )

        def replacer(match):
            alert_type = match.group(1).upper()
            first_line = match.group(2) or ""
            raw_body = match.group(3) or ""
            alines = []
            if first_line.strip():
                alines.append(first_line.strip())
            for line in raw_body.splitlines():
                alines.append(re.sub(r"^>\s?", "", line))
            body = "\n".join(alines).strip()

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

        res = pattern.sub(replacer, buf_text)
        return res.splitlines()

    for line in lines:
        fence = parse_fence_delimiter(line)
        if fence:
            f_char, f_len, f_is_closing = fence
            if active_fence is None:
                # Flush prose buffer through alert converter
                if buffer:
                    processed_lines.extend(process_buffer(buffer))
                    buffer = []
                active_fence = (f_char, f_len)
                processed_lines.append(line)
            elif f_char == active_fence[0] and f_len >= active_fence[1] and f_is_closing:
                active_fence = None
                processed_lines.append(line)
            else:
                processed_lines.append(line)
            continue

        if active_fence is not None:
            processed_lines.append(line)
        else:
            buffer.append(line)

    if buffer:
        processed_lines.extend(process_buffer(buffer))

    return "\n".join(processed_lines)


def scale_backticks(code_text: str) -> tuple[str, str]:
    """Dynamically scales outer code fences based on inner backtick counts."""
    max_ticks = 0
    matches = re.findall(r"(`{3,})", code_text)
    for m in matches:
        max_ticks = max(max_ticks, len(m))
    fence = "`" * max(3, max_ticks + 1)
    return fence, fence


def extract_commentary(code_text: str, lang: str = "yaml") -> str | None:
    """Extracts leading comment blocks (excluding shebangs and YAML frontmatter) into operational commentary callouts."""
    lines = code_text.splitlines()
    start_idx = 0

    # Advance past YAML frontmatter if present
    if lines and lines[0].strip() == "---":
        end_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx != -1:
            start_idx = end_idx + 1

    comment_lines = []
    for i in range(start_idx, len(lines)):
        line_str = lines[i]
        stripped = line_str.strip()
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

    if metadata.get("description"):
        desc = metadata["description"]
        out.append(f'<div class="callout callout-note">\n<strong>📌 Executive Summary</strong>\n\n{desc}\n</div>\n')

    active_fence: tuple[str, int] | None = None
    for line in clean.splitlines():
        fence = parse_fence_delimiter(line)
        if fence:
            f_char, f_len, f_is_closing = fence
            if active_fence is None:
                active_fence = (f_char, f_len)
            elif f_char == active_fence[0] and f_len >= active_fence[1] and f_is_closing:
                active_fence = None
            out.append(line)
            continue

        if active_fence is None:
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
