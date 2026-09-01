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
import xml.sax.saxutils
from xml.dom import minidom
from typing import Dict, List, Any, Tuple, Optional


def parse_llms_txt(content_or_path: str) -> Dict[str, Any]:
    """
    Parse llms.txt content or a file into structured metadata and document sections.
    
    Parameters:
        content_or_path (str): Path to an llms.txt file or raw llms.txt content.
    
    Returns:
        Dict[str, Any]: Parsed title, summary, and sections containing document titles,
            URLs, and optional descriptions.
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
    Generate XML context from parsed `llms.txt` data, including metadata and available local document contents.
    
    Parameters:
    	llms_data (Dict[str, Any]): Parsed `llms.txt` data containing the title, summary, sections, and documents.
    	root_dir (str): Root directory used to resolve relative document paths.
    
    Returns:
    	str: Formatted XML context document.
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

            # Embed local document content if file exists
            rel_path = item.get("url", "").lstrip("/")
            file_path = os.path.join(root_dir, rel_path)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    content_elem = ET.SubElement(doc_elem, "content")
                    content_elem.text = file_content
                except (OSError, UnicodeDecodeError) as err:
                    raise RuntimeError(f"Failed to read indexed document '{file_path}': {err}") from err

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent="  ")


def generate_llms_txt(docs_dir: str = "docs", relative_to_docs: bool = False) -> str:
    """
    Generate the standard Markdown index for the project's documentation.
    
    Parameters:
    	docs_dir (str): Documentation directory name retained for API compatibility.
    
    Returns:
    	str: Markdown content containing the project title, summary, and documentation links.
    """
    p = "" if relative_to_docs else "docs/"
    root_p = "" if relative_to_docs else ""

    content = [
        "# Omni-View Business Command Centre - DSOM AI Knowledge Base",
        "",
        "> DSOM-governed, OKF v0.2-compliant documentation index for AI Agents and LLMs.",
        "",
        "## Core Governance & Architecture",
        "",
        f"- [Knowledge-First Discovery SOP]({p}SOP-KNOWLEDGE-FIRST-DISCOVERY.md): Protocol detailing local metadata search prior to remote probes.",
        f"- [DSOM Governance]({p}explanation/dsom-governance.md): Metacognitive context management and protocol standards.",
        f"- [Diátaxis Framework]({p}explanation/diataxis.md): Quadrant layout and documentation structure.",
        f"- [System Architecture]({p}explanation/system-architecture.md): Subsystem topologies and integration points.",
        f"- [Architecture and Diátaxis Explanation]({p}explanation/architecture-and-diataxis.md): Decoupled system architecture and framework adoption.",
        f"- [OKF 0.2 and DSOM Integration]({p}explanation/okf-02-and-diataxis.md): Conceptual overview of Open Knowledge Format 0.2 and Domain-Specific Operational Model.",
        "",
        "## Tools & Component References",
        "",
        f"- [Tool Index]({p}reference/index.md): Exhaustive list of scripts, modules, and API signatures.",
        f"- [File Structure and API Reference]({p}reference/file-structure-and-api.md): Technical reference for frontend and database schema.",
        f"- [CLI and Tools Reference]({p}reference/cli-and-tools.md): Command line parameters, environment specs, and Python utility documentation.",
        f"- [OpenWiki Engine Specification]({p}reference/openwiki-emulator.md): Specifications for OpenWiki Python tools and batch operations.",
        "",
        "## Practical Operational Guides",
        "",
        f"- [Operational Recipes Index]({p}how-to/index.md): Operational recipes index.",
        f"- [Manage Inventory and Payouts]({p}how-to/manage-inventory-and-payouts.md): How-to guide for stock management and employee payout procedures.",
        f"- [Generate LLMs Context Guide]({p}how-to/generate-llms-context.md): How-to guide for utilizing parse_llms_txt.py script.",
        f"- [Execute Tool Workflows]({p}how-to/run-tool.md): Task-oriented execution recipes for tools and pipelines.",
        "",
        "## Tutorials & Onboarding",
        "",
        f"- [Quickstart Onboarding Guide]({p}tutorials/01-getting-started.md): Beginner step-by-step onboarding walkthrough.",
        f"- [Getting Started Tutorial]({p}tutorials/getting-started.md): Guided onboarding tutorial for system usage.",
        f"- [LLMs.txt Setup Tutorial]({p}tutorials/llms-txt-setup.md): Step-by-step tutorial on generating and consuming LLM context files.",
        "",
        "## Optional & System Documents",
        "",
        f"- [Documentation Hub]({p}index.md): Central entry hub for documentation.",
        f"- [Documentation Index]({p}README.md): Primary documentation home page.",
        f"- [SUMMARY Table of Contents]({p}SUMMARY.md): GitBook-compatible navigation summary.",
        f"- [START-HERE Onboarding Index]({root_p}START-HERE.md): Dual-audience developer and AI agent onboarding entry point.",
        f"- [Project Changelog]({root_p}CHANGELOG.md): Version release history and updates log.",
        f"- [Project History]({root_p}HISTORY.md): Historical milestone background."
    ]
    return "\n".join(content) + "\n"


def generate_llms_full(docs_dir: str = "docs", root_dir: str = ".") -> str:
    """
    Build a complete documentation index from available repository and documentation files.
    
    Parameters:
    	docs_dir (str): Directory containing the documentation files.
    	root_dir (str): Repository root used to resolve file paths.
    
    Returns:
    	str: Formatted documentation text containing the contents of each available file.
    """
    doc_paths = [
        "README.md",
        "START-HERE.md",
        "CHANGELOG.md",
        "HISTORY.md",
        os.path.join(docs_dir, "README.md"),
        os.path.join(docs_dir, "index.md"),
        os.path.join(docs_dir, "SUMMARY.md"),
        os.path.join(docs_dir, "START-HERE.md"),
        os.path.join(docs_dir, "CHANGELOG.md"),
        os.path.join(docs_dir, "HISTORY.md"),
        os.path.join(docs_dir, "SOP-KNOWLEDGE-FIRST-DISCOVERY.md"),
        os.path.join(docs_dir, "explanation", "dsom-governance.md"),
        os.path.join(docs_dir, "explanation", "diataxis.md"),
        os.path.join(docs_dir, "explanation", "system-architecture.md"),
        os.path.join(docs_dir, "explanation", "architecture-and-diataxis.md"),
        os.path.join(docs_dir, "explanation", "okf-02-and-diataxis.md"),
        os.path.join(docs_dir, "tutorials", "01-getting-started.md"),
        os.path.join(docs_dir, "tutorials", "getting-started.md"),
        os.path.join(docs_dir, "tutorials", "llms-txt-setup.md"),
        os.path.join(docs_dir, "how-to", "index.md"),
        os.path.join(docs_dir, "how-to", "manage-inventory-and-payouts.md"),
        os.path.join(docs_dir, "how-to", "generate-llms-context.md"),
        os.path.join(docs_dir, "how-to", "run-tool.md"),
        os.path.join(docs_dir, "reference", "index.md"),
        os.path.join(docs_dir, "reference", "file-structure-and-api.md"),
        os.path.join(docs_dir, "reference", "cli-and-tools.md"),
        os.path.join(docs_dir, "reference", "openwiki-emulator.md"),
    ]

    full_text = ["# Omni-View Complete Documentation (llms-full.txt)", ""]
    for path in doc_paths:
        full_path = os.path.join(root_dir, path)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            cleaned_content = "\n".join(line.rstrip() for line in content.splitlines())
            full_text.append(f"--- FILE: {path} ---")
            full_text.append(cleaned_content)
            full_text.append("")

    return "\n".join(full_text).rstrip() + "\n"


def generate_sitemaps(docs_dir: str = "docs", base_url: str = "https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre") -> Tuple[str, str]:
    """
    Generate text and XML sitemaps for the documentation site.
    
    Parameters:
        base_url (str): Base URL used to construct sitemap entries.
    
    Returns:
        Tuple[str, str]: Text sitemap content and XML sitemap content.
    """
    urls = [
        f"{base_url}/",
        f"{base_url}/START-HERE",
        f"{base_url}/SOP-KNOWLEDGE-FIRST-DISCOVERY",
        f"{base_url}/CHANGELOG",
        f"{base_url}/HISTORY",
        f"{base_url}/explanation/dsom-governance",
        f"{base_url}/explanation/diataxis",
        f"{base_url}/explanation/system-architecture",
        f"{base_url}/explanation/architecture-and-diataxis",
        f"{base_url}/explanation/okf-02-and-diataxis",
        f"{base_url}/tutorials/01-getting-started",
        f"{base_url}/tutorials/getting-started",
        f"{base_url}/tutorials/llms-txt-setup",
        f"{base_url}/how-to/index",
        f"{base_url}/how-to/manage-inventory-and-payouts",
        f"{base_url}/how-to/generate-llms-context",
        f"{base_url}/how-to/run-tool",
        f"{base_url}/reference/index",
        f"{base_url}/reference/file-structure-and-api",
        f"{base_url}/reference/cli-and-tools",
        f"{base_url}/reference/openwiki-emulator"
    ]

    sitemap_txt = "\n".join(urls) + "\n"

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        escaped_url = xml.sax.saxutils.escape(url)
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{escaped_url}</loc>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>\n")

    sitemap_xml = "\n".join(xml_lines)
    return sitemap_txt, sitemap_xml


def main():
    """Run the command-line interface for parsing llms.txt and generating documentation metadata."""
    parser = argparse.ArgumentParser(description="Parse llms.txt and generate XML context and site metadata.")
    parser.add_argument("--input", "-i", default="llms.txt", help="Path to input llms.txt file")
    parser.add_argument("--output", "-o", default="llm_context.xml", help="Path to output XML context file")
    parser.add_argument("--root", "-r", default=".", help="Root directory of repository")
    parser.add_argument("--generate-all", action="store_true", help="Generate llms.txt, llms-full.txt, sitemap.txt, sitemap.xml")

    args = parser.parse_args()

    root_dir = getattr(args, "root", ".")
    target_docs_dir = os.path.join(root_dir, "docs")

    if getattr(args, "generate_all", False):
        print("Generating documentation indexes and sitemaps...")

        # Sync root docs to docs/ relative to root_dir
        import shutil
        os.makedirs(target_docs_dir, exist_ok=True)

        for root_doc in ["CHANGELOG.md", "HISTORY.md"]:
            src = os.path.join(root_dir, root_doc)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(target_docs_dir, root_doc))

        start_here_src = os.path.join(root_dir, "START-HERE.md")
        if os.path.exists(start_here_src):
            with open(start_here_src, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                frontmatter = (
                    "---\n"
                    "layout: default\n"
                    'title: "Onboarding Standard & Operational Index"\n'
                    'description: "Dual-audience onboarding standard and operational entry point for developers and AI agents."\n'
                    "---\n\n"
                )
                content = frontmatter + content

            content = content.replace("docs/tutorials/", "tutorials/")
            content = content.replace("docs/how-to/", "how-to/")
            content = content.replace("docs/reference/", "reference/")
            content = content.replace("docs/explanation/", "explanation/")

            with open(os.path.join(target_docs_dir, "START-HERE.md"), "w", encoding="utf-8") as f:
                f.write(content)

        # llms.txt
        root_llms = generate_llms_txt(relative_to_docs=False)
        docs_llms = generate_llms_txt(relative_to_docs=True)

        with open(os.path.join(root_dir, "llms.txt"), "w", encoding="utf-8") as f:
            f.write(root_llms)
        with open(os.path.join(target_docs_dir, "llms.txt"), "w", encoding="utf-8") as f:
            f.write(docs_llms)

        # llms-full.txt
        llms_full_content = generate_llms_full(root_dir=root_dir)
        with open(os.path.join(root_dir, "llms-full.txt"), "w", encoding="utf-8") as f:
            f.write(llms_full_content)
        with open(os.path.join(target_docs_dir, "llms-full.txt"), "w", encoding="utf-8") as f:
            f.write(llms_full_content)

        # Sitemaps
        stxt, sxml = generate_sitemaps()
        with open(os.path.join(root_dir, "sitemap.txt"), "w", encoding="utf-8") as f:
            f.write(stxt)
        with open(os.path.join(target_docs_dir, "sitemap.txt"), "w", encoding="utf-8") as f:
            f.write(stxt)
        with open(os.path.join(root_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sxml)
        with open(os.path.join(target_docs_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sxml)

        print("Index generation complete.")

    input_path = os.path.join(root_dir, args.input) if not os.path.isabs(args.input) else args.input
    output_path = os.path.join(root_dir, args.output) if not os.path.isabs(args.output) else args.output

    if os.path.exists(input_path):
        parsed = parse_llms_txt(input_path)
        xml_output = generate_xml_context(parsed, root_dir=root_dir)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_output)
        print(f"XML context written to {output_path}")
    else:
        if not args.generate_all:
            print(f"Input file '{args.input}' not found. Use --generate-all to initialize index files.")


if __name__ == "__main__":
    main()
