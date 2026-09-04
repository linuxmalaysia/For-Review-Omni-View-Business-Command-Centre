---
okf_version: "0.2"
type: "skill"
title: "Project Technical Book & Handbook Compiler"
timestamp: "2026-09-05T00:00:00Z"
description: "Autonomously synthesizes repository code, Diataxis documentation, and system telemetry into publication-grade print-ready PDF, standalone HTML, and EPUB handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework."
topics: ["pandoc", "pdf", "html", "epub", "print-optimized", "diataxis", "handbook"]
status: "stable"
stale_after: "2027-09-05"
name: "project-technical-book-compiler"
---

# Project Technical Book & Handbook Compiler

## Purpose
Standardizes the automated assembly, styling, and multi-format compilation of entire project repositories into unified, publication-grade engineering handbooks.

## Execution Commands

### 1. Build Master Markdown
```bash
uv run python tools/build_project_book.py
```

### 2. Compile Standalone Interactive HTML (Pandoc 3.x)
```bash
pandoc build/book/master_book.md -o build/book/handbook.html \
  --standalone --toc --toc-depth=3 --number-sections \
  --include-before-body=build/book/cover.html \
  --css=terminal-theme.css \
  --syntax-highlighting=tango \
  --metadata title="Project Technical Handbook" \
  --metadata author="Lead Architect" \
  --metadata date="September 2026" -V lang=en
```

### 3. Bake Native Vector SVGs & Inline Theme CSS
```bash
uv run python tools/bake_native_svg.py
```

### 4. Compile Publication-Grade PDF (Headless Chromium / Edge)
```powershell
$tmpProfile = "$env:TEMP\edge-pdf-profile-$(Get-Random)"
Start-Process -FilePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" \
  -ArgumentList "--headless=new", "--disable-gpu", "--run-all-compositor-stages-before-draw", \
  "--user-data-dir=$tmpProfile", "--no-pdf-header-footer", "--print-to-pdf=build/book/handbook.pdf", \
  "file:///path/to/build/book/handbook.html" -Wait
Remove-Item -Recurse -Force $tmpProfile -ErrorAction SilentlyContinue
```

### 5. Compile EPUB 3 Ebook
```bash
pandoc build/book/master_book.md -o build/book/handbook.epub \
  -t epub3 --toc --toc-depth=3 \
  --css=build/book/terminal-theme.css \
  --metadata title="Project Technical Handbook"
```
