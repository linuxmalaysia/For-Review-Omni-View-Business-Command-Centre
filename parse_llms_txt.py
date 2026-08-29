#!/usr/bin/env python3
"""
parse_llms_txt.py - Parser, XML Context Generator, and Site Map Utility for llms.txt

Adheres to https://llmstxt.org/ specification and Google OKF 0.2 / DSOM principles.
Provides both CLI and Python API interfaces.
"""

import argparse
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Tuple, Optional


def parse_llms_txt(content_or_path: str) -> Dict[str, Any]:
    """
    Parses an llms.txt file or string content into a structured dictionary representation.

    Args:
        content_or_path: File path to llms.txt or raw text content of llms.txt.

    Returns:
        Dict containing project title, description, and categorized sections.
    """
    if os.path.exists(content_or_path):
        with open(content_or_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = content_or_path

    lines = text.splitlines()
    data: Dict[str, Any] = {
        "title": "",
        "summary": "",
        "sections": []
    }

    current_section: Optional[Dict[str, Any]] = None

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        if line_str.startswith("# ") and not data["title"]:
            data["title"] = line_str[2:].strip()
        elif line_str.startswith("> ") and not data["summary"]:
            data["summary"] = line_str[2:].strip()
        elif line_str.startswith("## "):
            sec_title = line_str[3:].strip()
            current_section = {"title": sec_title, "items": []}
            data["sections"].append(current_section)
        elif line_str.startswith("- ") or line_str.startswith("* "):
            item_text = line_str[2:].strip()
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)(?::\s*(.*))?", item_text)
            if match:
                title = match.group(1).strip()
                url = match.group(2).strip()
                desc = match.group(3).strip() if match.group(3) else ""
                item = {"title": title, "url": url, "description": desc}
                if current_section is None:
                    current_section = {"title": "General", "items": []}
                    data["sections"].append(current_section)
                current_section["items"].append(item)

    return data


def generate_xml_context(llms_data: Dict[str, Any], root_dir: str = ".") -> str:
    """
    Generates an XML context payload from parsed llms.txt data and local document contents.

    Args:
        llms_data: Structured output from parse_llms_txt.
        root_dir: Root directory of repository to resolve relative doc paths.

    Returns:
        Formatted XML string containing documentation context.
    """
    root = ET.Element("llm_context", title=llms_data.get("title", "Documentation Context"))

    if llms_data.get("summary"):
        summary_elem = ET.SubElement(root, "summary")
        summary_elem.text = llms_data["summary"]

    sections_elem = ET.SubElement(root, "sections")

    for sec in llms_data.get("sections", []):
        sec_elem = ET.SubElement(sections_elem, "section", name=sec.get("title", ""))
        for item in sec.get("items", []):
            doc_elem = ET.SubElement(sec_elem, "document", href=item.get("url", ""))

            title_elem = ET.SubElement(doc_elem, "title")
            title_elem.text = item.get("title", "")

            if item.get("description"):
                desc_elem = ET.SubElement(doc_elem, "description")
                desc_elem.text = item.get("description", "")

            # Attempt to embed local document content if file exists
            rel_path = item.get("url", "").lstrip("/")
            file_path = os.path.join(root_dir, rel_path)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    content_elem = ET.SubElement(doc_elem, "content")
                    content_elem.text = file_content
                except Exception:
                    pass

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent="  ")


def generate_llms_txt(docs_dir: str = "docs") -> str:
    """
    Generates the standard llms.txt index content from docs directory tree.
    """
    content = [
        "# Omni-View Business Command Centre",
        "",
        "> Integrated Operations Management System documentation system adhering to Diátaxis and Google OKF 0.2 specifications.",
        "",
        "## Core Documentation Quadrants",
        "",
        "- [Getting Started Tutorial](docs/tutorials/getting-started.md): Guided onboarding tutorial for system usage.",
        "- [LLMs.txt Setup Tutorial](docs/tutorials/llms-txt-setup.md): Step-by-step tutorial on generating and consuming LLM context files.",
        "- [Manage Inventory and Payouts](docs/how-to/manage-inventory-and-payouts.md): How-to guide for stock management and employee payout procedures.",
        "- [Generate LLMs Context Guide](docs/how-to/generate-llms-context.md): How-to guide for utilizing parse_llms_txt.py script.",
        "- [File Structure and API Reference](docs/reference/file-structure-and-api.md): Technical reference for frontend and database schema.",
        "- [CLI and Tools Reference](docs/reference/cli-and-tools.md): Command line parameters, environment specs, and Python utility documentation.",
        "- [Architecture and Diátaxis Explanation](docs/explanation/architecture-and-diataxis.md): System architecture and Diátaxis framework implementation.",
        "- [OKF 0.2 and DSOM Integration](docs/explanation/okf-02-and-diataxis.md): Conceptual overview of Ontological Knowledge Frame 0.2 and Domain-Specific Operational Model.",
        "",
        "## Optional & System Documents",
        "",
        "- [Documentation Index](docs/README.md): Primary documentation home page.",
        "- [SUMMARY Table of Contents](docs/SUMMARY.md): GitBook-compatible navigation summary.",
        "- [START-HERE Onboarding Index](START-HERE.md): Dual-audience developer and AI agent onboarding entry point."
    ]
    return "\n".join(content) + "\n"


def generate_llms_full(docs_dir: str = "docs", root_dir: str = ".") -> str:
    """
    Generates full documentation text (llms-full.txt) incorporating all files.
    """
    doc_paths = [
        "README.md",
        "START-HERE.md",
        os.path.join(docs_dir, "README.md"),
        os.path.join(docs_dir, "SUMMARY.md"),
        os.path.join(docs_dir, "tutorials", "getting-started.md"),
        os.path.join(docs_dir, "tutorials", "llms-txt-setup.md"),
        os.path.join(docs_dir, "how-to", "manage-inventory-and-payouts.md"),
        os.path.join(docs_dir, "how-to", "generate-llms-context.md"),
        os.path.join(docs_dir, "reference", "file-structure-and-api.md"),
        os.path.join(docs_dir, "reference", "cli-and-tools.md"),
        os.path.join(docs_dir, "explanation", "architecture-and-diataxis.md"),
        os.path.join(docs_dir, "explanation", "okf-02-and-diataxis.md"),
    ]

    full_text = ["# Omni-View Complete Documentation (llms-full.txt)", ""]
    for path in doc_paths:
        full_path = os.path.join(root_dir, path)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            full_text.append(f"--- FILE: {path} ---")
            full_text.append(content)
            full_text.append("")

    return "\n".join(full_text)


def generate_sitemaps(docs_dir: str = "docs", base_url: str = "https://linuxmalaysia.github.io/openwiki") -> Tuple[str, str]:
    """
    Generates sitemap.txt and sitemap.xml for documentation site.
    """
    urls = [
        f"{base_url}/",
        f"{base_url}/START-HERE",
        f"{base_url}/docs/",
        f"{base_url}/docs/tutorials/getting-started",
        f"{base_url}/docs/tutorials/llms-txt-setup",
        f"{base_url}/docs/how-to/manage-inventory-and-payouts",
        f"{base_url}/docs/how-to/generate-llms-context",
        f"{base_url}/docs/reference/file-structure-and-api",
        f"{base_url}/docs/reference/cli-and-tools",
        f"{base_url}/docs/explanation/architecture-and-diataxis",
        f"{base_url}/docs/explanation/okf-02-and-diataxis"
    ]

    sitemap_txt = "\n".join(urls) + "\n"

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{url}</loc>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>\n")

    sitemap_xml = "\n".join(xml_lines)
    return sitemap_txt, sitemap_xml


def main():
    parser = argparse.ArgumentParser(description="Parse llms.txt and generate XML context and site metadata.")
    parser.add_argument("--input", "-i", default="llms.txt", help="Path to input llms.txt file")
    parser.add_argument("--output", "-o", default="llm_context.xml", help="Path to output XML context file")
    parser.add_argument("--root", "-r", default=".", help="Root directory of repository")
    parser.add_argument("--generate-all", action="store_true", help="Generate llms.txt, llms-full.txt, sitemap.txt, sitemap.xml")

    args = parser.parse_args()

    if args.generate_all:
        print("Generating documentation indexes and sitemaps...")

        # llms.txt
        llms_content = generate_llms_txt()
        with open("llms.txt", "w", encoding="utf-8") as f:
            f.write(llms_content)
        with open("docs/llms.txt", "w", encoding="utf-8") as f:
            f.write(llms_content)

        # llms-full.txt
        llms_full_content = generate_llms_full(root_dir=args.root)
        with open("llms-full.txt", "w", encoding="utf-8") as f:
            f.write(llms_full_content)
        with open("docs/llms-full.txt", "w", encoding="utf-8") as f:
            f.write(llms_full_content)

        # Sitemaps
        stxt, sxml = generate_sitemaps()
        with open("sitemap.txt", "w", encoding="utf-8") as f:
            f.write(stxt)
        with open("docs/sitemap.txt", "w", encoding="utf-8") as f:
            f.write(stxt)
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sxml)
        with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sxml)

        print("Index generation complete.")

    if os.path.exists(args.input):
        parsed = parse_llms_txt(args.input)
        xml_output = generate_xml_context(parsed, root_dir=args.root)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(xml_output)
        print(f"XML context written to {args.output}")
    else:
        if not args.generate_all:
            print(f"Input file '{args.input}' not found. Use --generate-all to initialize index files.")


if __name__ == "__main__":
    main()
