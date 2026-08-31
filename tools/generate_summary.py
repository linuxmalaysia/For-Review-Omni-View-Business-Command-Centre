#!/usr/bin/env python3
"""
tools/generate_summary.py

Auto-discovers all Markdown (.md) files in root and docs/ directory,
parsing their YAML frontmatter title (or H1 title if no frontmatter),
and writes an updated SUMMARY.md at the repository root and docs/SUMMARY.md.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_title_from_md(filepath: str) -> str:
    """Extracts title from YAML frontmatter or first H1 header in a Markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].splitlines():
                    if line.strip().startswith('title:'):
                        title_val = line.split('title:', 1)[1].strip()
                        return title_val.strip('"').strip("'")

        # Check H1 header
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
    except Exception:
        pass

    filename = os.path.basename(filepath)
    return filename.replace('.md', '').replace('-', ' ').title()


def generate_summary_lines(is_docs_folder: bool = False):
    prefix = "" if not is_docs_folder else "../"
    doc_prefix = "docs/" if not is_docs_folder else ""

    lines = [
        "---",
        "layout: default",
        'title: "SUMMARY"',
        'description: "Table of Contents and Navigation Index"',
        "---",
        "",
        "# Summary",
        "",
        f"* [Home]({prefix}README.md)",
        f"* [Getting Started]({prefix}START-HERE.md)",
        f"* [Changelog]({prefix}CHANGELOG.md)",
        f"* [History]({prefix}HISTORY.md)",
        ""
    ]

    categories = {
        "tutorials": "Tutorials",
        "how-to": "How-To Guides",
        "reference": "Reference",
        "explanation": "Explanation"
    }

    docs_dir = os.path.join(ROOT_DIR, 'docs')

    for cat_slug, cat_title in categories.items():
        cat_dir = os.path.join(docs_dir, cat_slug)
        lines.append(f"## {cat_title}")

        if os.path.isdir(cat_dir):
            for filename in sorted(os.listdir(cat_dir)):
                if filename.endswith('.md'):
                    rel_path = f"{doc_prefix}{cat_slug}/{filename}"
                    full_path = os.path.join(cat_dir, filename)
                    title = get_title_from_md(full_path)
                    lines.append(f"* [{title}]({rel_path})")

        lines.append("")

    other_docs = []
    if os.path.isdir(docs_dir):
        for item in sorted(os.listdir(docs_dir)):
            full_path = os.path.join(docs_dir, item)
            if os.path.isfile(full_path) and item.endswith('.md') and item != 'SUMMARY.md':
                rel_path = f"{doc_prefix}{item}"
                title = get_title_from_md(full_path)
                other_docs.append(f"* [{title}]({rel_path})")

    if other_docs:
        lines.append("## Additional Documentation")
        lines.extend(other_docs)
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_summary():
    """Scans repository and builds structured SUMMARY.md."""
    # Write root SUMMARY.md
    root_summary_content = generate_summary_lines(is_docs_folder=False)
    root_summary_path = os.path.join(ROOT_DIR, 'SUMMARY.md')
    with open(root_summary_path, 'w', encoding='utf-8') as f:
        f.write(root_summary_content)

    # Write docs/SUMMARY.md
    docs_summary_content = generate_summary_lines(is_docs_folder=True)
    docs_dir = os.path.join(ROOT_DIR, 'docs')
    docs_summary_path = os.path.join(docs_dir, 'SUMMARY.md')
    os.makedirs(docs_dir, exist_ok=True)
    with open(docs_summary_path, 'w', encoding='utf-8') as f:
        f.write(docs_summary_content)

    print(f"Successfully generated {root_summary_path} and {docs_summary_path}")


if __name__ == '__main__':
    build_summary()
