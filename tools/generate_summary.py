#!/usr/bin/env python3
"""
tools/generate_summary.py

Auto-discovers all Markdown (.md) files across root and docs/ directory recursively,
parsing their YAML frontmatter title (or H1 title if no frontmatter),
and writes an updated SUMMARY.md at the repository root and docs/SUMMARY.md.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_title_from_md(filepath: str) -> str:
    """Extracts title from YAML frontmatter or first H1 header in a Markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
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
    except (IndexError, ValueError, KeyError) as e:
        print(f"Warning: Parse issue in {filepath}: {e}")

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

    docs_dir = os.path.join(ROOT_DIR, 'docs')
    if os.path.isdir(docs_dir):
        # Recursively find all .md files under docs/ excluding SUMMARY.md
        discovered_files = []
        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') and file != 'SUMMARY.md':
                    full_path = os.path.join(root, file)
                    rel_from_docs = os.path.relpath(full_path, docs_dir)
                    discovered_files.append((rel_from_docs, full_path))

        # Group by category (first subdirectory component)
        categories = {}
        uncategorized = []

        for rel_path, full_path in sorted(discovered_files):
            parts = rel_path.split(os.sep)
            title = get_title_from_md(full_path)
            link_target = f"{doc_prefix}{rel_path.replace(os.sep, '/')}"

            if len(parts) > 1:
                cat_slug = parts[0]
                if cat_slug not in categories:
                    categories[cat_slug] = []
                categories[cat_slug].append((title, link_target))
            else:
                uncategorized.append((title, link_target))

        for cat_slug in sorted(categories.keys()):
            cat_title = cat_slug.replace('-', ' ').title()
            lines.append(f"## {cat_title}")
            lines.append("")
            for title, link_target in sorted(categories[cat_slug]):
                lines.append(f"* [{title}]({link_target})")
            lines.append("")

        if uncategorized:
            lines.append("## Additional Documentation")
            lines.append("")
            for title, link_target in sorted(uncategorized):
                lines.append(f"* [{title}]({link_target})")
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
