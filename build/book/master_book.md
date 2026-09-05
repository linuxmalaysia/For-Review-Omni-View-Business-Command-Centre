# Executive Overview {.unnumbered}
> **Classification:** PRIVATE AND CONFIDENTIAL (P&C)
> **Compiled By:** Antigravity Cognitive Twin
> **Standard:** Terminal & Cloud Technical Handbook Standard


# Part 1: Governance & Compilation Master Prompts {.part}

<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Master operational prompt and technical blueprint for compiling multi-file Markdown documentation suites into publication-grade, print-optimized PDF, HTML, EPUB, and ODT handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework.
</div>

## Technical Book Design & PDF Compilation Master Prompt Guide

> **Document Type:** Governance Blueprint & Reusable AI Master Prompt
> **Classification:** Private And Confidential (P&C)
> **Attribution:** Compile by: Harisfazillah Jamel
> **Standard:** Terminal & Cloud Technical Ebook & Handbook Standard (DSOM Rule 11 & Rule 22)

***

### 1. Executive Overview & Dual Purpose

This document serves two complementary functions:
1. **The Reusable AI Master Prompt (Section 2):** A complete, drop-in system prompt that can be provided to any advanced AI coding assistant (Google Antigravity, Google Jules, Claude, Cursor, ChatGPT) to autonomously orchestrate, style, and compile an entire repository of multi-file Markdown (`.md`) documentation and source code into a publication-grade PDF handbook.
2. **The Architectural Blueprint & Engineering Field Manual (Sections 3–7):** An exhaustive technical record documenting the formatting standards, color palettes, typography pairings, CSS `@page` rules, and the **ten critical engineering hurdles** solved to eliminate syntax crashes, blank pages, link leaks, and ink waste during multi-format compilation (PDF, standalone HTML, EPUB 3, and styled ODT).
3. **The Embedded Skill SOP (Section 6):** The full operational specification of the `dsom-technical-book-compiler` skill, ensuring complete self-containment.

***

### 2. The Reusable AI Master Prompt

*Copy and paste the entire block below into your AI prompt window or agent instruction set:*

```markdown
You are a Principal Publication Systems Architect and Pandoc Book Engineering Specialist.
Your task is to take an entire repository of Markdown (.md) documents and source code trees, assemble them into a cohesive, publication-grade technical handbook, and compile them into a print-optimized PDF, standalone interactive HTML, EPUB 3, and styled OpenDocument Text (ODT).

### MANDATORY DESIGN & STYLING SPECIFICATIONS (TERMINAL & CLOUD STANDARD)

1. PRINT-OPTIMIZED PURE WHITE STANDARD (ZERO TONER WASTE):
   - For all PDF and print compilations, dark or black container backgrounds are STRICTLY FORBIDDEN.
   - Base Body Background: Pure White (#FFFFFF !important).
   - Code Blocks (Preformatted): Light Alabaster/Gray (#F8FAFC) with a subtle slate border (1px solid #CBD5E1), dark charcoal text (#0F172A), and high-contrast dark syntax highlighting (Pandoc 'tango' style: Keywords #1E40AF bold, Strings #047857, Comments #64748B italic, Numbers #B45309, Functions #6D28D9).
   - Callout & Alert Boxes: Light pastel containers with high-contrast colored left borders:
     * Critical Warnings & Cautions: Background #FEF2F2, Left Border 5px solid #DC2626, Border 1px solid #FCA5A5, Text #991B1B.
     * Operational Notes & Information: Background #F0F9FF, Left Border 5px solid #0284C7, Border 1px solid #BAE6FD, Text #075985.
     * Pro-Tips: Background #F0FDF4, Left Border 5px solid #16A34A, Border 1px solid #BBF7D0, Text #166534.
     * Chapter Executive Summaries: Background #F8FAFC, Border 1px solid #CBD5E1, Text #334155.

2. TYPOGRAPHY & VISUAL HIERARCHY:
   - Body Text: Clean sans-serif ('Inter', 'Plus Jakarta Sans', or system-ui fallback), 10pt, line-height 1.55, color #0F172A.
   - Code & Terminal Elements: Monospace font ('JetBrains Mono', 'Fira Code', or 'Consolas'), 8.5pt, line-height 1.4.
   - Headings:
     * Book Title (Cover): 22pt bold, Linux Blue (#1E3A8A).
     * Part Headers (H1 .part): 22pt bold, Linux Blue (#1E3A8A), shaded banner #F8FAFC with 8px solid #1E3A8A left bar, page-break-before: always.
     * Chapter Headers (H2): 16pt bold, Linux Blue (#1E3A8A), bottom border 1px solid #E2E8F0.
     * Section Headers (H3): 13pt bold, Deep Ubuntu (#77216F).
     * Sub-section Headers (H4): 11pt semibold, Deep Teal (#0D9488).

3. PAGE LAYOUT & RUNNING HEADERS/FOOTERS:
   - Page Size: A4 (margin: 20mm 15mm 20mm 15mm).
   - Running Header Top-Left: "<Book Title>" (Inter 8pt, #64748B).
   - Running Header Top-Right: "PRIVATE AND CONFIDENTIAL (P&C)" (Inter 8pt bold, #DC2626).
   - Running Footer Bottom-Left: "Compile by: Harisfazillah Jamel" (Inter 8pt, #64748B).
   - Running Footer Bottom-Right: "Page " counter(page) (Inter 8pt bold, #0F172A).

4. STANDALONE COVER PAGE (SINGLE PAGE FIT):
   - Passed to Pandoc via '--include-before-body=cover.html'.
   - Must fit entirely on Page 1 without spilling over.
   - Contain badges: Private And Confidential (P&C) (#FEE2E2), Technology badges (#EFF6FF), Tooling badges (#F0FDF4).
   - Metadata grid: 2-column key-value grid (Architect, Compiler, Audience, Classification, Covenant, Edition).
   - CSS Guard: Hide duplicate Pandoc title header (#title-block-header { display: none !important; }) and prevent cover title page break (.cover-title { break-before: avoid !important; }).

### NON-NEGOTIABLE ENGINEERING PIPELINE CONSTRAINTS

1. FRONTMATTER & FOOTER STRIPPING:
   - Systematically strip individual YAML frontmatter (lines between leading '---' fences) and individual document signature footers from every ingested .md file to prevent Pandoc YAML parser crashes ('Unknown alias').
   - Extract 'title' and 'description' from frontmatter: convert description into an executive summary callout box above the chapter body.

2. DYNAMIC BACKTICK SCALING:
   - When ingesting code files containing triple backticks (```), dynamically scale the outer markdown fence to 4 or 5 backticks (```` or `````) to prevent premature block closure.

3. ANTI-BLANK PAGE DISCIPLINE:
   - Never combine manual HTML page break tags ('<div class="page-break"></div>') with CSS 'page-break-before: always;'. Use CSS classes exclusively on H1/Part elements.

4. MERMAID MULTI-DIAGRAM ISOLATION PROTOCOL:
   - Diagram-Scoped Namespaces: Reusing identical node IDs (e.g. NODE1, DB, GATEWAY) across diagrams is strictly prohibited. Prefix all node IDs within each diagram with a unique diagram namespace (e.g. TB_, PA_, PB_, PC_) to eliminate global SVG node collisions.
   - Sequential DOM Replacement: Never rely on 'mermaid.run()' which causes millisecond timestamp collisions in headless Chromium. Render diagrams sequentially via 'mermaid.render("diagram_svg_" + i, code)' into unique containers.
   - Entity Unescaping Pipeline: Unescape '&quot;', '&lt;', '&gt;', '&amp;' inside '<pre class="mermaid">' blocks before rendering, and extract 'innerHTML' (not 'textContent') to preserve stacked card line breaks.
   - Balanced Flowchart Architecture: Prevent tall vertical flowchart towers (height > 600px) that cause blank page overflows. Split complex diagrams into balanced 2-column or orthogonal grid layouts.

5. SOFT-PATH INTERNAL LINK RESOLUTION MANDATE (3-TIER NORMALISATION):
   - Pre-index all chapters ('#chap-{slug}') and ingested code blocks ('#code-{slug}') into an internal anchor dictionary.
   - Rewrite all markdown links using a 3-tier normalisation lookup:
     * Tier 1 (Exact Match): Check raw relative path against dictionary.
     * Tier 2 (Normalised Match): Strip 'file:///', Windows drive letters ('C:/', 'D:/'), project root prefix, and 'build/' prefix, then check dictionary.
     * Tier 3 (Basename-Only Match): Strip all parent directories and check dictionary by filename only.
     * Preserve '#fragment' anchor jumps across all three tiers.
   - Post-Compile Audit: Assert zero absolute path leaks ('D:/', 'C:/', 'file:///') survive in compiled PDF/HTML links.

6. DEVELOPER COMMENTARY EXTRACTION PROTOCOL:
   - For every ingested Ansible playbook, shell script, or configuration file, parse the leading '#' comment block (contiguous comments before the first active code key).
   - Regex Keyword Scan: If comments contain keywords ('BUG', 'FIX', 'Confirmed', 'live', 'vendor', 'NEVER', 'destroy', 'destructive', 'ORA-\d+', 'crash', 'escalation', 'hard way'), render a ⚠️ orange warning callout ('callout-warning', 'Developer Commentary — Read Before Executing') ABOVE the code fence. Otherwise, render a 💡 blue note callout ('callout-note', 'Developer Commentary').
   - Keep the original '#' comments inside the code block intact.

7. MULTI-FORMAT COMPILATION SUITE:
   - Step 1: Standalone HTML with embedded Mermaid.js ESM and print CSS.
   - Step 2: Print-to-PDF via Headless Chromium/Edge with '--headless=new --run-all-compositor-stages-before-draw --virtual-time-budget=8000'.
   - Step 3: EPUB 3 with clean table of contents metadata.
   - Step 4: OpenDocument Text (ODT) with custom reference styles for Google Docs/LibreOffice collaboration.
```

***

### 3. Visual Design System: The "Terminal & Cloud" Framework

#### 3.1 Color Palette & Contrast Economics

| Role | HEX Code | Print Rationale | CSS Class / Property |
| :--- | :--- | :--- | :--- |
| **Page Background** | `#FFFFFF` | Pure white. Eliminates background shading and toner waste. | `body { background-color: #FFFFFF !important; }` |
| **Body Text** | `#0F172A` | Deep charcoal slate. Maximum contrast against white without harsh black glare. | `color: #0F172A !important;` |
| **Primary Headings** | `#1E3A8A` | Linux Blue. Professional, authoritative enterprise header branding. | `h1, h2 { color: #1E3A8A; }` |
| **Secondary Headings**| `#77216F` | Deep Ubuntu Purple. High-visibility distinction for major subsections. | `h3 { color: #77216F; }` |
| **Tertiary Headings** | `#0D9488` | Deep Teal. Clear demarcator for low-level runbook procedures. | `h4 { color: #0D9488; }` |
| **Code Block Background** | `#F8FAFC` | Very light alabaster gray. Visually defines code boundaries without heavy ink deposit. | `div.sourceCode, pre.sourceCode { background-color: #F8FAFC !important; }` |
| **Code Block Border** | `#CBD5E1` | Slate border. Provides crisp, laser-printer-safe container edges. | `border: 1px solid #CBD5E1 !important;` |
| **Warning Callout** | `#FEF2F2` / `#DC2626` | Soft red pastel with intense dark red border and text. Immediate visual alert. | `.callout-warning` |
| **Note Callout** | `#F0F9FF` / `#0284C7` | Soft blue pastel with vivid blue border. High legibility for operational context. | `.callout-note` |
| **Tip Callout** | `#F0FDF4` / `#16A34A` | Soft green pastel with crisp green border. Architectural pro-tips. | `.callout-tip` |

#### 3.2 Typography Pairing

- **Prose:** `font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
  *Characteristics:* Clean geometric sans-serif, high x-height, optimized for both 300 DPI print and high-res displays. Line height is fixed at `1.55` with `10pt` base size.
- **Code & Configurations:** `font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;`
  *Characteristics:* Distinct character shaping (disambiguating `0`/`O` and `1`/`l`/`I`), tabular numbers, ligature support. Sized at `8.5pt` with `1.4` line height.

#### 3.3 Print Page Budget & Paging Rules (`@page`)

```css
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    background: #FFFFFF;
    @top-left {
        content: "Omni-View Business Command Centre Handbook";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
        font-weight: 500;
    }
    @top-right {
        content: "PRIVATE AND CONFIDENTIAL (P&C)";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #DC2626;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    @bottom-left {
        content: "Compile by: Harisfazillah Jamel";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
    }
    @bottom-right {
        content: "Page " counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #0F172A;
        font-weight: 600;
    }
}
```

***

### 4. The 10 Critical Engineering Hurdles Solved

#### Hurdle 1: Pandoc YAML Parser Explosions (`Unknown alias`)
- **Failure Mode:** Stitched multi-document markdowns retain individual OKF frontmatter blocks (`--- ... ---`). Pandoc attempts to parse subsequent frontmatter blocks as YAML document streams, failing with `Unknown alias` or corrupted titles.
- **Solution:** A pre-processing function (`strip_frontmatter()`) strips leading YAML frontmatter while capturing `title` and `description` to create formatted chapter metadata banners (`.chapter-meta`).

#### Hurdle 2: Nested Backtick Fence Collisions
- **Failure Mode:** Ingested markdown documents or playbook examples already contain triple backticks (```` ``` ````). If the master compiler wraps them in triple backticks, the code block prematurely terminates, leaking raw code into prose.
- **Solution:** Dynamic backtick scaling. The compiler scans the target code text; if triple backticks exist, it wraps the block in 4 backticks (```` ```` ````); if 4 exist, it scales to 5.

#### Hurdle 3: Blank Overflow Pages & Cover Fragmentation
- **Failure Mode:** Manual page breaks (`<div class="page-break"></div>`) combined with CSS `page-break-before: always;` on H1 elements generate unwanted empty pages. Furthermore, default Pandoc title headers split the cover across Pages 1 and 2.
- **Solution:**
  1. Eliminate all manual page break divs.
  2. Generate a standalone `cover.html` passed via `--include-before-body=cover.html`.
  3. Enforce `#title-block-header { display: none !important; }` and `.cover-title { break-before: avoid !important; }`.
  4. Constrain cover page padding and metadata fonts so the entire cover fits inside Page 1.

#### Hurdle 4: Mermaid 10 Syntax Bomb Graphics (HTML Escaping)
- **Failure Mode:** Pandoc automatically escapes HTML entities inside `<pre class="mermaid"><code>` (`&quot;`, `&lt;`, `&gt;`, `--&gt;`). When Mermaid.js runs, it encounters illegal characters, rendering a pink syntax error bomb icon.
- **Solution:** A dedicated post-pandoc HTML regex unescapes `&quot;`, `&lt;`, `&gt;`, `&amp;` and strips enclosing `<code>` tags before headless browser invocation.

#### Hurdle 5: Mermaid Node Collision in Multi-Diagram Handbooks
- **Failure Mode:** Different diagrams reuse common node identifiers (e.g. `NODE1`, `DB`, `CBE`, `PWP`). Mermaid's internal parser merges identical IDs into the same global SVG graph, corrupting diagram topology.
- **Solution:** **Mermaid Multi-Diagram Isolation Protocol**. Every diagram must have unique diagram-scoped namespaces prefixed to all nodes (e.g., `TB_` for Master Architecture, `PA_` for Pattern A, `PB_` for Pattern B, `PC_` for Pattern C).

#### Hurdle 6: Headless Chromium Millisecond Timestamp Collision
- **Failure Mode:** Headless Chromium renders all page scripts in milliseconds. Mermaid's default `mermaid.run()` uses `Date.now()` timestamp IDs, causing ID collisions that draw multiple diagrams inside the same container.
- **Solution:** Sequential DOM replacement. The browser script iterates over `document.querySelectorAll("pre.mermaid")` and calls `mermaid.render("diagram_svg_" + i, code)` sequentially, injecting the returned SVG directly into `el.innerHTML`.

#### Hurdle 7: Tall Vertical Flowcharts Splitting Pages
- **Failure Mode:** Long linear flowcharts (height > 600px) split mid-node across physical page breaks, causing dangling connectors and unreadable diagrams.
- **Solution:**
  1. Re-architect flowcharts into balanced 2-column grids (e.g., Phase 1 vs Phase 2).
  2. Set `pre.mermaid svg { max-width: 100% !important; height: auto !important; }`.
  3. Extract `innerHTML` rather than `textContent` in the Mermaid pre-pass to preserve `<br/>` tags and card formatting.

#### Hurdle 8: Broken Relative Links & Leaked Local Paths (`file:///`)
- **Failure Mode:** Ingested documentation contains relative links (`../how-to/deploy.md`) or absolute filesystem paths (`file:///D:/Users/...`), which break or leak workstation directories in the compiled PDF.
- **Solution:** **Soft-Path Link Resolution Mandate (3-Tier Normalisation Pipeline)**:
  1. Pre-index all chapters (`#chap-{slug}`) and code files (`#code-{slug}`) into an in-memory `link_map`.
  2. Normalize link targets across 3 tiers:
     - *Tier 1:* Exact match in `link_map`.
     - *Tier 2:* Strip `file:///`, Windows drive letters (`C:/`, `D:/`), root directory prefixes, and `build/` prefixes.
     - *Tier 3:* Basename-only fallback (`os.path.basename(target)`).
  3. Preserve `#fragment` anchor suffixes across all tiers.
  4. Run an automated post-assembly audit to verify zero absolute paths survive in PDF links.

#### Hurdle 9: Critical Safety Warnings Hidden in Code Comments
- **Failure Mode:** Production playbooks contain vital operational warnings, vendor bug workarounds, and safety dispatches hidden in `#` comments that SysAdmins miss when skimming compiled books.
- **Solution:** **Developer Commentary Extraction Protocol**:
  1. Inspect the leading `#` comment block of every playbook, script, and configuration file.
  2. Scan for warning keywords (`BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `destroy`, `destructive`, `ORA-\d+`, `crash`, `escalation`).
  3. If keywords match, generate a **⚠️ orange warning callout** (`callout-warning`, "Developer Commentary — Read Before Executing") rendered **above** the code fence.
  4. If standard comments, render a **💡 blue note callout** (`callout-note`).
  5. Preserve the original `#` comments inside the code block intact.

#### Hurdle 10: Headless Browser Print Timeouts & Compositor Stalls
- **Failure Mode:** Headless Chrome/Edge can hang indefinitely if web fonts or ESM modules fail to trigger draw completion, stalling CI/CD pipelines.
- **Solution:** Execute Chromium with strict flags:
  ```bash
  msedge.exe --headless=new --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=8000 --print-to-pdf=<out.pdf> <file_uri>
  ```
  Enforce a hard Python subprocess timeout (45–60s) to gracefully catch draw completion.

***

### 5. Multi-Format Compilation Commands

```bash
# 1. Compile Standalone Interactive HTML Ebook
pandoc build/book/master_book.md -o build/book/handbook.html \
  --standalone --toc --toc-depth=3 --number-sections \
  --include-before-body=build/book/cover.html \
  --css=build/book/terminal-theme.css \
  --highlight-style=tango \
  --metadata title="Omni-View Business Command Centre Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel" \
  --metadata date="September 2026" -V lang=en

# 2. Compile Publication-Grade PDF via Headless Chromium
msedge.exe --headless=new --disable-gpu \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=8000 \
  --print-to-pdf=build/book/handbook.pdf \
  file:///path/to/build/book/handbook.html

# 3. Compile EPUB 3 Ebook
pandoc build/book/master_book.md -o build/book/handbook.epub \
  -t epub3 --toc --toc-depth=3 \
  --css=build/book/terminal-theme.css \
  --metadata title="Omni-View Business Command Centre Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel" \
  --metadata publisher="Deep State of Mind (DSOM)"

# 4. Compile Styled OpenDocument Text (ODT) for Google Docs
pandoc build/book/master_book.md -o build/book/handbook.odt \
  --reference-doc=build/book/custom_reference.odt \
  --toc --toc-depth=3 \
  --metadata title="Omni-View Business Command Centre Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel"
```

***

### 6. Complete Embedded Skill: `dsom-technical-book-compiler`

Below is the full, unabridged operational specification of the `dsom-technical-book-compiler` skill:

```markdown
---
okf_version: "0.2"
type: "skill"
title: "Technical Ebook & Handbook Compiler (Pandoc / Print & Terminal Theme)"
timestamp: "2026-09-03T07:30:00Z"
description: "Compiles complete Diataxis documentation suites and source code repositories into publication-grade technical handbooks (PDF, standalone HTML, EPUB, ODT) using Pandoc and the Terminal & Cloud design framework."
topics: ["pandoc", "ebook", "pdf", "html", "epub", "terminal-theme"]
status: "stable"
stale_after: "2027-09-03"
sources:
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rule 11 & Rule 22)"
    path: ".agents/AGENTS.md"
name: "dsom-technical-book-compiler"
---

# Technical Ebook & Handbook Compiler

**Purpose:** Standardizes the automated compilation of complex multi-part Diátaxis documentation palaces and complete source code directories into unified, publication-grade technical handbooks (PDF, HTML, EPUB, ODT) tailored for SysAdmins, DevOps Engineers, and SREs.

## Dual-Mode "Terminal & Cloud" Design System
1. **Interactive / Screen Mode:** Optional dark slate container (#0F172A) for code and off-white (#F8FAFC) reading background.
2. **Physical Print / PDF Handbook Mode (Zero Ink Waste):**
   - **Pure White Background:** `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }` to eliminate grayish tints and toner waste.
   - **Light Code Blocks:** Code containers use `#F8FAFC` light gray with `#CBD5E1` border, dark text (`#0F172A`), and high-contrast dark syntax highlighting (Pandoc `tango`). Black or solid dark containers are strictly forbidden.
   - **Light Pastel Callouts:** Soft pastel backgrounds (`#FEF2F2` for warnings, `#F0F9FF` for notes, `#F0FDF4` for tips) with colored left borders.
   - **Full Confidentiality Statement:** Must be written as `Private And Confidential (P&C)` (uppercase `PRIVATE AND CONFIDENTIAL (P&C)` in running headers).
   - **Attribution Standard:** Compilations must be credited as `Compile by: Harisfazillah Jamel`.

## Technical Execution Constraints
1. **Footer & Frontmatter Stripping:** When assembling 100+ documents, individual OKF frontmatter and DSOM signature footers must be stripped to prevent Pandoc YAML parser collisions (`Unknown alias`).
2. **Dynamic Backtick Fence Scaling:** When wrapping source code containing triple backticks (` ``` `), the enclosing fence must scale dynamically to 4 or 5 backticks (` ```` `).
3. **Mermaid HTML Unescaping Protocol:** Pandoc automatically escapes HTML entities inside `<pre class="mermaid"><code>` (`&quot;`, `&lt;br/&gt;`, `--&gt;`). The compilation pipeline must decode these entities before browser rendering to prevent Mermaid 10 syntax error bomb graphics.
4. **Standalone Cover Body Inclusion:** Never embed raw HTML covers inside Markdown files. Generate a standalone `cover.html` passed via `--include-before-body=cover.html`. Enforce `.cover-title { break-before: avoid !important; }` and `#title-block-header { display: none !important; }` to prevent cover fragmentation.
5. **Anti-Blank Page Discipline:** Never mix manual `<div class="page-break"></div>` tags with CSS `page-break-before: always;`.
6. **Headless Browser PDF Timeout:** Headless Chromium/Edge (`--headless=new --print-to-pdf`) renders CSS `@page` layouts, vector SVGs, and web fonts. A process timeout guardrail (45–60s) must be enforced.
7. **Mermaid Multi-Diagram Isolation Protocol:**
   - *Diagram-Scoped Namespace:* Prohibit reusing identical node IDs (e.g., `NODE1`, `CBE`, `PWP`) across diagrams. Prefix all node IDs with a unique diagram namespace (e.g., `TB_`, `PA_`, `PB_`, `PC_`) to prevent global symbol collisions.
   - *Sequential Headless DOM Replacement:* Headless Chromium renders in milliseconds, causing default `mermaid.run()` timestamp IDs (`Date.now()`) to collide and nest diagrams inside one container. Mandate sequential rendering via `mermaid.render(id, code)` with unique IDs (`diagram_svg_${i}`) replacing `<pre class="mermaid">` innerHTML sequentially.
8. **Soft-Path Link Resolution Mandate (3-Tier Normalisation):** The compilation pipeline must dynamically map all chapters (`#chap-{slug}`) and ingested code blocks (`#code-{slug}`) and rewrite all markdown links via a **3-tier normalisation pipeline**: (1) *Exact match* — look up the raw target in `link_map` as-is; (2) *Normalised match* — strip `file:///`, Windows drive letters (`D:/`, `C:/`), the project root prefix, and the `build/` intermediate directory prefix, then retry; (3) *Basename-only match* — strip all directory components and retry with the filename only. Pre-index basename-only keys into `link_map` before rewriting. Preserve `#fragment` suffixes across all tiers. Run a post-compile link audit asserting zero absolute path leaks (`D:/`, `C:/`, `file:///`, `build/` prefixes) survive in any PDF/HTML link target.
9. **Full-Spectrum Code Ingestion:** Ingest all production playbooks, Jinja2 templates, inventories, host/group variables, shell scripts, and candidate staging playbooks into dedicated book chapters to produce self-contained handbooks.
10. **Developer Commentary Extraction Protocol:** For every YAML playbook, shell script, or INI file ingested, extract the leading `#` comment block (all contiguous comment lines before the first YAML key, after the `---` fence) and render it as an HTML callout div above the code fence. Classify by keyword scan: comments containing `BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `ORA-\d+`, `destroy`, `destructive`, `hard way`, or `escalation` render as `callout-warning` (⚠️ orange, label `Read Before Executing`); all others render as `callout-note` (💡 blue). Preserve original `#` lines inside the code fence unchanged. CSS must define `.callout-warning p`, `.callout-note p`, and `strong` selectors with explicit `padding: 12px 16px` and `page-break-inside: avoid` for clean print rendering.

## Execution Command
```bash
uv run python tools/build_project_book.py
```
```

***

### 7. Operational Checklist for AI Agents & Compilers

Before finalizing any compiled handbook, the AI agent must verify:
- [ ] **Pure White Audit:** No solid black terminal blocks exist in the compiled PDF.
- [ ] **Blank Page Audit:** Verified total page count has zero empty filler pages between chapters.
- [ ] **Mermaid Audit:** All diagrams render as clean vector SVGs with zero syntax error bomb icons.
- [ ] **Link Leak Audit:** Grep search the assembled HTML/PDF links for `file:///` or Windows drive letters (`D:/`, `C:/`) — result must be 0.
- [ ] **Commentary Audit:** Leading playbook dispatches are rendered as human-readable callouts above the code fences.
- [ ] **Confidentiality Audit:** Running headers state `PRIVATE AND CONFIDENTIAL (P&C)` and attribution reads `Compile by: Harisfazillah Jamel`.


# Part 2: Operational How-To Guides {.part}

<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/how-to/HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Comprehensive operational handbook and transferable AI prompt library for analyzing code repositories, synthesizing Diataxis documentation, baking native vector diagrams, and compiling publication-grade print-ready handbooks (PDF, HTML, EPUB) using Pandoc and Headless Chromium.
</div>

## How to Produce a Project Technical Handbook: The AI Prompt Engineering & Skill Adoption Blueprint

> **Classification:** Technical Standard & Transferable Knowledge Base
> **Target Audience:** Lead Architects, DevOps/SRE Engineers, and Autonomous AI Coding Assistants
> **Standard:** Terminal & Cloud Technical Book Standard (DSOM Rule 11 & Rule 22)
> **Author & Lead Consultant:** Harisfazillah Jamel (LinuxMalaysia)
> **Compiled By:** Antigravity Cognitive Digital Twin

***

### 1. Executive Overview & Transferability Mandate

Modern software, DevOps, and infrastructure projects frequently suffer from **fragmented documentation**. Architectural intent is split across READMEs, tribal chat logs, wiki pages, runbooks, and inline source code comments. When teams need to present their systems for audits, client handovers, team onboarding, or management reviews, they lack a single, authoritative, publication-grade volume.

This guide provides a **100% transferable blueprint** that enables any engineering repository—whether built on Ansible, Terraform, Kubernetes, Python, Go, or Cloud Native architectures—to synthesize its entire codebase and documentation into a cohesive, print-optimized technical book (PDF, interactive HTML, and EPUB 3).

#### What This Blueprint Provides:
1. **The Prompt Transformation Matrix:** All conversational prompts typically asked by human leads, rewritten into high-fidelity, optimized master prompts that any AI agent can execute without ambiguity.
2. **The 6-Phase Engineering Pipeline:** Discovery, visual modeling, Diataxis ingestion, narrative storytelling, print formatting, and multi-format compilation.
3. **The 17 Core Compilation Invariants:** Solutions to every major compilation hurdle (syntax crashes, dark container ink waste, missing covers, unrendered Mermaid blocks, unparsed callout alerts, and browser process timeouts).
4. **Drop-in Reusable Skill Specification:** An autonomous skill definition that can be copied directly into `skills/` of any target repository.

***

### 2. The Prompt Transformation Matrix: From Conversational Ask to Production AI Master Prompts

When humans communicate with AI assistants during technical book compilation, their initial requests are often short and intuitive. However, generic AI assistants often misinterpret these asks—generating dark code blocks, omitting cover pages, hardcoding narrative text into compiler scripts, or failing to render diagrams.

Below is the complete **Before & After Matrix**, translating conversational requests into robust, constraint-enforced AI master prompts.

***

#### Prompt 1: Project Discovery & Architectural Modeling

##### Conversational Human Ask:
> *"I need you to produce a book for this project. Start with understanding the project by understanding the ansible playbook and documents that can be related to the ansible playbook. Make sure we have diagram of flow of works and flow of how ansible work."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Principal Technical Author and Systems Architect. Your mission is to analyze this repository and assemble an authoritative, publication-grade Technical Handbook.

PHASE 1: REPOSITORY DISCOVERY & TAXONOMY
1. Scan the repository inventory, orchestration playbooks/manifests, roles, configuration templates, and documentation suites.
2. Catalog all operational components into logical tiers (e.g., Command Centres, Orchestration Bridges, Persistence Fabrics, Telemetry Ingestion Workers).
3. Map every production playbook/code file to its corresponding documentation, runbooks, and Root Cause Analysis (RCA) reports.

PHASE 2: ARCHITECTURAL VISUAL MODELING
Construct two comprehensive architectural flowcharts:
1. The End-to-End Command Highway: Visualizing the multi-tier flow of code from local development and GitOps remotes to target nodes.
2. The Orchestration Execution Engine: Visualizing how automation tasks inspect hardware, apply declarative baselines, enforce zero-trust security, and verify system state.

OUTPUT REQUIREMENTS:
- Structure the book into clear, hierarchical Parts and Chapters following the Diataxis framework.
- Ensure every code artifact has a dedicated sub-chapter accompanied by developer operational context and architectural rationale.
```

***

#### Prompt 2: Resolving Diagram Failures (Mermaid to Native SVG)

##### Conversational Human Ask:
> *"The diagram is not showing in the book."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Graphics & Headless Browser Print Specialist. The Mermaid diagrams in our compiled HTML/PDF are failing to render or displaying syntax error graphics.

ROOT CAUSE ANALYSIS:
1. Headless Chrome/Edge print engines capture DOM snapshots in milliseconds, outrunning asynchronous client-side Mermaid JavaScript CDN libraries.
2. Pandoc wraps `<pre class="mermaid">` blocks in `<code>` tags and escapes HTML arrows (`-->` becomes `--&gt;`), corrupting Mermaid syntax.

REMEDIATION MANDATE (NATIVE VECTOR SVG PRE-RENDERING):
1. Eliminate client-side Mermaid JavaScript rendering entirely for PDF production.
2. Author a standalone Python script (e.g., `tools/bake_native_svg.py`) that pre-renders or directly substitutes Mermaid code blocks with clean, styled, inline vector `<svg>` markup.
3. Ensure SVG elements include viewBox definitions, drop-shadow filters, high-contrast text labels (using 'Inter' or system sans-serif), and responsive container wrappers (`<div class="mermaid-svg-container">`).
4. Execute this transformation directly on the generated `handbook.html` prior to launching the headless browser PDF print step.
```

***

#### Prompt 3: Diátaxis Documentation Enrichment & Ingestion

##### Conversational Human Ask:
> *"Add into our books, content from md documents that is related to each of our ansible playbooks. Enrich our book."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Technical Documentation Compiler. Your task is to enrich every playbook chapter in the Technical Handbook by dynamically ingesting its accompanying operational runbooks, explanations, and incident reports.

MANDATORY INGESTION & SANITIZATION RULES:
1. Frontmatter & Signature Stripping: Parse each ingested markdown file and strip all YAML metadata fences (`--- ... ---`) and document signature footers (`*Maintained by...*`) to prevent Pandoc parser collisions (`Unknown alias`).
2. Heading Level Offsetting: Apply a dynamic heading level offset (+2 levels: `#` becomes `###`, `##` becomes `####`) to ensure ingested document headings nest cleanly beneath the parent Chapter title in the Table of Contents.
3. Markdown Horizontal Rule Sanitization: Replace all internal standalone horizontal rules (`\n---\n`) with triple asterisks (`\n***\n`) to prevent Pandoc from falsely interpreting them as YAML metadata blocks.
4. Operational Provenance Banner: Inject an audit pill above each ingested document:
   `<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>path/to/file.md</code></div>`
5. Developer Commentary Extraction: Scan the leading comment block of each code file for keywords (BUG, FIX, WARNING, CRITICAL, NEVER, escalation). Render matches as high-visibility callouts (`callout-warning` or `callout-note`) above the code fence.
```

***

#### Prompt 4: The Narrative Epic (Heart, Soul, and Sovereign Blood)

##### Conversational Human Ask:
> *"I need a chapter that's like a story, all about this project and infra from start to end, how it can be built, deployed, and operated. Highlight the use of ansible + semaphoreui + gitea as GitOps, and AIOps with human in the loop. Add about deep state of mind (DSOM) of My AI as the AI memory and brain. This chapter is not technical; it is about the heart, soul, and blood of this project."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Principal Technical Biographer and Systems Philosopher. Author an evocative, inspiring narrative chapter titled:
"# Prologue: The Story of <Project Name> — Heart, Soul, and Sovereign Blood {.unnumbered}"

NARRATIVE STRUCTURE & THEMES:
1. The Spark in the Dark (Why This Fabric Was Born):
   - Paint the operational reality: telemetry deluge, memory exhaustion, swap death spirals, and the painful loss of context when engineers step away from the terminal.
2. The Trinity of Motion (GitOps, The Control Node, and The Hand):
   - Explain how Git serves as the immutable source of truth, Semaphore UI acts as the scheduled heartbeat, and Ansible operates as the indomitable physical hand shaping the infrastructure.
3. The Mind in the Machine (Deep State of Mind & AIOps):
   - Address the fatal flaw of Large Language Models: Context Decay (cognitive amnesia).
   - Chronicle the creation of the Sovereign Markdown Palace (`.agents/brain/`, `palace_registry.md`, Start-of-Day reanimation, and End-of-Day hibernation), preserving unbroken historical context across operational shifts.
4. The Sacred Balance (AIOps with Human-in-the-Loop):
   - Reject blind, dangerous auto-remediation.
   - Embed the Sovereign AIOps Integration Loop (ASCII architectural diagram): AI proposes remediation -> Sovereign Human verifies and commits -> Ansible executes -> AI audits and records memory.
   - Articulate the Three Laws of the Twin: Advisory over Execution, Logic over Operation, and Partnership through Environmental Awareness.
5. From Raw Metal to Living Shield:
   - Walk through the 5 foundational phases from genesis virtual machine bootstrapping to hardened security baselines, rootless container pods, threat analytics, and continuous Day-2 operations.
6. The Heart, Soul, and Blood:
   - Close with the philosophical trifecta: Sovereignty, Discipline, and Human-AI Symbiosis.
```

***

#### Prompt 5: Clean Architecture Separation (Standalone Markdown Document)

##### Conversational Human Ask:
> *"I need the story to be in its own md file."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Clean Architecture and Diataxis Specialist. Refactor the narrative story chapter out of inline Python script strings into a dedicated, reusable documentation artifact.

IMPLEMENTATION STEPS:
1. Author the file `docs/explanation/THE-STORY-OF-<PROJECT>.md` with complete OKF v0.2 YAML frontmatter (`type: documentation`, `title: ...`).
2. Embed the complete narrative text, ASCII loop diagram, and formal DSOM signature footer.
3. Register the new document in `SUMMARY.md` under the `explanation` quadrant to ensure GitBook/MkDocs navigation indexing.
4. Update the book compiler script (`tools/build_project_book.py`) to dynamically ingest this document using `ingest_doc_file("docs/explanation/THE-STORY-OF-<PROJECT>.md", heading_offset=0, show_provenance=False)` directly into the book's Prologue.
```

***

#### Prompt 6: Print-Optimized Formatting Restoration (Zero Toner Waste & Cover Injection)

##### Conversational Human Ask:
> *"What happened to my book? We lost the formatting. No cover, black background? That needs to be checked again."*

##### Production-Grade AI Master Prompt:
```markdown
You are a Print Production Engineer and CSS Specialist. Diagnose and fix the visual formatting regressions in our compiled PDF and HTML handbook.

SYMPTOMS TO REMEDY:
1. Missing Cover Page: Re-inject `--include-before-body=build/book/cover.html` in the Pandoc build chain. Ensure `.cover-page` in CSS declares `break-after: page; min-height: 250mm;` so the cover fills Page 1 completely and cleanly page-breaks before the Table of Contents.
2. Black Background Code Blocks: Replace dark syntax highlighting (e.g. `--syntax-highlighting=espresso`) with `--syntax-highlighting=tango`. Ensure CSS enforces `pre, code, div.sourceCode { background-color: #F8FAFC !important; border: 1px solid #CBD5E1 !important; color: #0F172A !important; }` to eliminate toner waste.
3. External CSS Linking Failures: Prevent headless browser path resolution failures by reading `terminal-theme.css` and inlining the complete stylesheet directly into `<style>` inside `<head>` of the HTML before PDF generation.
4. Raw GitHub Alert Syntax: Detect all `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, and `> [!CAUTION]` syntax in ingested markdown files and transform them into styled pastel HTML callout cards (`<div class="callout callout-note"><strong>💡 Note</strong><p>...</p></div>`).
5. Asynchronous Process Premature Exit: When compiling via Microsoft Edge on Windows PowerShell, execute with `Start-Process -FilePath $edge -ArgumentList ... -Wait` using an isolated user profile (`--user-data-dir`) to ensure the process does not terminate before the PDF file buffer is completely written.
```

***

### 3. The 17 Non-Negotiable Technical Book Compilation Invariants

Any automated compilation pipeline must adhere to these 17 strict invariants:

| # | Invariant Name | Failure Mode Addressed | Architectural Rule |
| :--- | :--- | :--- | :--- |
| **1** | **Pure White Standard** | Dark gray backgrounds waste ink and look muddy | Force `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }`. |
| **2** | **Light Alabaster Code** | Solid black terminal containers waste ink | Code containers must use `#F8FAFC` background with `#CBD5E1` border and dark charcoal text `#0F172A`. |
| **3** | **Syntax Theme (`tango`)** | Dark themes (`espresso`, `zenburn`) force black code backgrounds | Strictly enforce `--syntax-highlighting=tango` for light-background compatibility. |
| **4** | **Standalone Cover Injection** | Raw Markdown covers break page layout and spill over | Author `cover.html` and inject via `--include-before-body=cover.html`. |
| **5** | **Cover Single-Page Fit** | Cover content spilling into Table of Contents | Enforce `.cover-page { break-after: page; min-height: 250mm; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }`. |
| **6** | **Frontmatter Stripping** | Pandoc crashes with `Unknown alias` error | Strip `--- ... ---` blocks from all ingested markdown files before concatenation. |
| **7** | **Horizontal Rule Sanitization** | `\n---\n` parsed by Pandoc as YAML start | Regex replace `\n---\n` with `\n***\n` in all ingested content. |
| **8** | **GitHub Alert Card Conversion** | `> [!NOTE]` renders as unstyled plain text | Programmatically transform into `<div class="callout callout-note"><strong>💡 Note</strong><p>...</p></div>`. |
| **9** | **Self-Contained Embedded CSS** | Headless browsers fail to resolve relative CSS links | Read `terminal-theme.css` and inject directly into `<style>` inside `<head>`. |
| **10** | **Dynamic Backtick Scaling** | Triple backticks inside code blocks close outer fence | Count max backticks in code and scale outer fence to N+1 (e.g. ` ```` `). |
| **11** | **Heading Offset (+2)** | Embedded guide titles collide with Book H1/H2 | Dynamically increment heading level (`#` to `###`, `##` to `####`). |
| **12** | **Native Vector SVG Baking** | Client-side Mermaid race conditions in headless PDF | Pre-render diagrams to `<svg>` and inject into HTML before headless PDF execution. |
| **13** | **Mermaid Namespace Isolation** | Global node ID collisions across multiple diagrams | Prefix node IDs with unique namespace prefixes (`TB_`, `AN_`, `TH_`). |
| **14** | **Pandoc Code-Tag Wrapping** | Pandoc wraps `<pre class="mermaid"><code>` and escapes HTML | SVG replacement regexes must match both standard and `<code>`-wrapped pre blocks and unescape arrows (`--&gt;`). |
| **15** | **Windows Isolated Browser Profile** | Edge crashes or hangs if user desktop instances are running | Launch Edge with `--user-data-dir="$env:TEMP/edge-pdf-$(Get-Random)"`. |
| **16** | **Synchronous Edge Execution** | PowerShell returns before Edge finishes writing PDF | Always use `Start-Process -FilePath $edge -ArgumentList ... -Wait`. |
| **17** | **Provenance Audit Banners** | Loss of traceability for ingested runbooks | Inject `<div class="doc-provenance">` detailing the repository source path. |

***

### 4. Reusable Project Book Assembler Template (`tools/build_project_book.py`)

Below is the clean, modular Python assembler that can be copied directly into any repository:

```python
#!/usr/bin/env python3
"""
Universal Technical Handbook Assembler & Multi-Format Compiler
Standard: Terminal & Cloud Standard (DSOM Rule 11 & Rule 22)
"""

import os
import re
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(".").resolve()
BUILD_DIR = ROOT_DIR / "build" / "book"
BUILD_DIR.mkdir(parents=True, exist_ok=True)

MASTER_MD = BUILD_DIR / "master_book.md"
COVER_HTML = BUILD_DIR / "cover.html"
THEME_CSS = BUILD_DIR / "terminal-theme.css"
HANDBOOK_HTML = BUILD_DIR / "handbook.html"
HANDBOOK_PDF = BUILD_DIR / "handbook.pdf"
HANDBOOK_EPUB = BUILD_DIR / "handbook.epub"

WARNING_KEYWORDS = re.compile(
    r"\b(BUG|FIX|Confirmed|live|vendor|NEVER|destroy|destructive|ORA-\d+|crash|escalation|hard way|WARNING|CAUTION|CRITICAL)\b",
    re.IGNORECASE
)

def strip_frontmatter_and_footer(content: str) -> str:
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        end_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx != -1:
            content = "\n".join(lines[end_idx+1:])
    content = re.sub(r"\n---\s*\n\*.*", "", content, flags=re.DOTALL)
    content = re.sub(r"\n---\n", "\n***\n", content)
    return content.strip()

def convert_github_alerts(text: str) -> str:
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
            clean_line = re.sub(r"^>\s?", "", line)
            lines.append(clean_line)
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
    max_ticks = 0
    matches = re.findall(r"(`{3,})", code_text)
    for m in matches:
        if len(m) > max_ticks:
            max_ticks = len(m)
    fence = "`" * max(3, max_ticks + 1)
    return fence, fence

def extract_commentary(code_text: str, lang: str = "yaml"):
    lines = code_text.splitlines()
    comment_lines = []
    start_idx = 1 if lines and lines[0].strip() == "---" else 0
    for i in range(start_idx, len(lines)):
        l = lines[i]
        stripped = l.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
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
    if not file_path.exists():
        return f"\n*File not found: {file_path}*\n"
    content = file_path.read_text(encoding="utf-8", errors="replace")
    callout = extract_commentary(content, lang)
    fence_start, fence_end = scale_backticks(content)
    md_parts = [f"\n<a id=\"{anchor}\"></a>\n### {title}\n"]
    md_parts.append(f"**Source File:** `{file_path.relative_to(ROOT_DIR).as_posix()}`\n")
    if callout:
        md_parts.append(callout)
    md_parts.append(f"{fence_start}{lang}\n{content.strip()}\n{fence_end}\n")
    return "\n".join(md_parts)

def ingest_doc_file(rel_path: str, heading_offset: int = 1, show_provenance: bool = True) -> str:
    file_path = ROOT_DIR / rel_path
    if not file_path.exists():
        return f"\n*Documentation file not found: {rel_path}*\n"
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    clean = strip_frontmatter_and_footer(raw)
    clean = convert_github_alerts(clean)

    out = []
    for line in clean.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = min(len(m.group(1)) + heading_offset, 6)
            hashes = "#" * lvl
            title = m.group(2)
            out.append(f"{hashes} {title}")
        else:
            out.append(line)

    header = f'\n<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>{rel_path}</code></div>\n' if show_provenance else "\n"
    return header + "\n".join(out) + "\n"

def build_master_book():
    print("Assembling master book markdown...")
    parts = []

    # 1. Book Executive Overview
    parts.append("""# Executive Overview {.unnumbered}
> **Classification:** Private And Confidential (P&C)
> **Compiled By:** Autonomous Cognitive Twin
> **Standard:** Terminal & Cloud Technical Handbook Standard
""")

    # 2. Prologue Story
    story_path = "docs/explanation/architecture-and-diataxis.md"
    if (ROOT_DIR / story_path).exists():
        parts.append(ingest_doc_file(story_path, heading_offset=0, show_provenance=False))

    full_text = "\n\n".join(parts)
    MASTER_MD.write_text(full_text, encoding="utf-8")
    print(f"Master markdown written: {MASTER_MD} ({len(full_text):,} bytes)")

if __name__ == "__main__":
    build_master_book()
```

***

### 5. Standalone Reusable Skill Specification (`project-technical-book-compiler`)

To adopt this capability in another repository, copy the specification below into `skills/project-technical-book-compiler/SKILL.md`:

```yaml
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
try {
    $proc = Start-Process -FilePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
      -ArgumentList "--headless=new", "--disable-gpu", "--run-all-compositor-stages-before-draw", `
      "--user-data-dir=""$tmpProfile""", "--no-pdf-header-footer", "--print-to-pdf=build/book/handbook.pdf", `
      "file:///path/to/build/book/handbook.html" -Wait -PassThru
    if ($proc.ExitCode -ne 0) { throw "Edge PDF generation failed with exit code $($proc.ExitCode)" }
    if (-not (Test-Path "build/book/handbook.pdf")) { throw "PDF file build/book/handbook.pdf was not produced" }
} finally {
    Remove-Item -Recurse -Force $tmpProfile -ErrorAction SilentlyContinue
}
```

### 5. Compile EPUB 3 Ebook
```bash
pandoc build/book/master_book.md -o build/book/handbook.epub \
  -t epub3 --toc --toc-depth=3 \
  --css=build/book/terminal-theme.css \
  --metadata title="Project Technical Handbook"
```
```

***

### 6. Operational Checklist & Quality Assurance

Before delivering any compiled handbook to stakeholders, execute this audit checklist:

- [ ] **Cover Page Audit:** Page 1 renders as a full-page bordered card with P&C badges and metadata table; breaks cleanly before Table of Contents.
- [ ] **Zero Toner Waste Audit:** All code containers have `#F8FAFC` light gray backgrounds with dark charcoal text and `tango` syntax colors. Zero black terminal boxes exist.
- [ ] **Callout Card Audit:** All operational notes, warnings, and tips render as styled pastel cards with icons (`💡 Note`, `⚠️ Warning`, `💡 Tip`). Zero raw `[!NOTE]` markdown syntax leaks survive.
- [ ] **Vector Diagram Audit:** All architecture and workflow diagrams render as crisp, scalable vector SVGs directly inline.
- [ ] **Inline CSS Audit:** CSS is embedded directly into `<style>` inside `<head>` to prevent external relative link breakage.
- [ ] **Soft-Path Link Audit:** All internal cross-references point to clean `#chap-...` or `#code-...` fragments without surviving absolute filesystem paths (`file:///` or drive letters).
- [ ] **Pagination Audit:** Verified zero empty filler pages exist between chapters.


<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/how-to/deploy-omni-view-on-render.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Step-by-step Diátaxis How-To guide for building, configuring, deploying, and troubleshooting the Omni-View Business Command Centre static site and documentation portal on Render.com.
</div>

## 🚀 Deploying Omni-View Business Command Centre on Render.com

This guide provides a comprehensive step-by-step walkthrough for deploying the **Omni-View Business Command Centre** interactive web application and documentation portal to [Render.com](https://render.com/).

***

### 🎯 Architecture & Deployment Type Recommendation

 lower-latency static site delivery is recommended for Omni-View:

1. **Frontend Web Application:** The Omni-View interface is a client-side web application composed of HTML, CSS, JavaScript, and asset management modules residing in `Web Ui/`, `js/`, `css/`, and `index.html`.
2. **Automated Documentation Engine:** During the build process, `parse_llms_txt.py --generate-all` generates machine-parseable LLM context structures (`llms-full.txt`, `llm_context.xml`) and sitemaps.
3. **Render Deployment Model:** Deployed as a **Render Static Site**, avoiding unnecessary backend web server processes (e.g. Uvicorn/FastAPI) and eliminating cold-start latency.

***

### 📋 Prerequisites & Project Structure

Ensure the repository contains the following deployment artifacts:

```text
.
├── render.yaml                             # Render Static Site Blueprint specification
├── pyproject.toml                          # Dependency & test specification
├── parse_llms_txt.py                      # Build script for generating LLM context & sitemaps
├── index.html                              # Web application landing page
└── Web Ui/                                 # Command centre dashboard views
```

***

### 🛠️ Deployment Step-by-Step Instructions

#### Method 1: Render Blueprint Deployment (Recommended)

1. Push your changes to GitHub or GitLab.
2. Log into the [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** and select **Blueprint**.
4. Connect your repository `For-Review-Omni-View-Business-Command-Centre`.
5. Render will automatically detect `render.yaml` and configure the static site with:
   - **Service Type:** `Static Site`
   - **Name:** `omni-view-command-centre`
   - **Build Command:** `python3 parse_llms_txt.py --generate-all`
   - **Publish Directory:** `./`

***

#### Method 2: Manual Static Site Setup on Render (Free Tier Compatible)

If creating the service manually in the Render Dashboard:


<div class="callout callout-note">
<strong>💡 Note</strong>

**Render Static Sites Benefits:**
- Free static site hosting on Render's Free tier, subject to standard workspace outbound-bandwidth and build-pipeline limits.
- High-availability global CDN distribution.
- Fast automated continuous deployment on every git push.
</div>


1. Log into the [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Static Site**.
3. Select **Build and deploy from a Git repository** and connect your repository.
4. Set the following explicit service parameters:
   - **Name:** `omni-view-command-centre`
   - **Branch:** `main` (or active production branch)
   - **Root Directory:** *(leave empty for repository root)*
   - **Build Command:** `python3 parse_llms_txt.py --generate-all`
   - **Publish Directory:** `./` (or `.` root directory)
5. Click **Create Static Site**. Render will run the build script and host the site immediately.

***

### 🔧 Troubleshooting Render Deploys

#### 1. Error: `ModuleNotFoundError: No module named 'src'` (Exit Status 1) or `uvicorn: command not found` (Exit Status 127)

- **Symptom:** Deployment log fails during the start/deploy phase with:

  ```text
  ==> Running 'uvicorn src.dca_service.web_app:app --host 0.0.0.0 --port $PORT'
  Traceback (most recent call last):
    ...
  ModuleNotFoundError: No module named 'src'
  ==> Exited with status 1
  ```

  or:

  ```text
  ==> Running 'uvicorn src.dca_service.web_app:app --host 0.0.0.0 --port $PORT'
  bash: line 1: uvicorn: command not found
  ==> Exited with status 127
  ```

- **Root Cause:** The Render service was misconfigured as a **Web Service** (Python runtime) with a start command (`uvicorn src.dca_service.web_app:app ...`), rather than a **Static Site**. Omni-View is a static web application and automated documentation portal that does not contain a `src` Python package or backend web server.
- **Resolution:**
  1. In the Render Dashboard, check the service type. An existing Web Service cannot be converted directly into a Static Site in-place. If configured as a Web Service, delete the Web Service and create a new **Static Site** service.
  2. Alternatively, ensure your repository root contains the correct `render.yaml` with `type: static` so Render Blueprint deploys it as a static site.
  3. Clear any leftover Start Command input in the Render service settings (Static Sites do not require a Start Command).

#### 2. Missing Generated Files or Sitemap Warnings

- **Symptom:** Deploy build log fails or missing `llms-full.txt` or `sitemap.xml`.
- **Resolution:** Verify that the build command is set to `python3 parse_llms_txt.py --generate-all`. This ensures all XML context files and sitemaps are pre-built prior to deployment publishing.

#### 3. Header and Caching Configuration

- **Symptom:** Browser caches old assets after updating HTML or CSS.
- **Resolution:** `render.yaml` configures standard headers for client caching:

  ```yaml
  headers:
    - path: /*
      name: Cache-Control
      value: max-age=3600
  ```

***

### 🌐 Endpoints & Verification

Once deployed, verify your service endpoints on Render:

- **Command Centre Portal:** `https://<your-service>.onrender.com/`
- **Dashboard Views:** `https://<your-service>.onrender.com/Web Ui/main.html`
- **LLM Text Summary:** `https://<your-service>.onrender.com/llms.txt`
- **LLM Full Context:** `https://<your-service>.onrender.com/llms-full.txt`
- **LLM XML Context:** `https://<your-service>.onrender.com/llm_context.xml`


<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/how-to/manage-inventory-and-payouts.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Practical operational guide for stock management, live streaming sales tracking, and staff payouts.
</div>

## How-To Guide: Managing Inventory, Live Sessions, and Payouts

This guide provides step-by-step procedural directions for routine operations in Omni-View.

***

### 📦 How to Manage Product Inventory

#### Adding a New Product Item

1. Navigate to **Product Management** (`http://localhost:8000/Web Ui/product.html`).
2. Click **Add Product**.
3. Fill in product details:
   - **Title**: `Premium Wireless Headset`
   - **Category**: `Electronics`
   - **Stock**: `150`
   - **Price**: `299.00`
4. Click **Save Product**.

***

### 🎥 How to Track Live Stream Performance

1. Navigate to **Live Sessions** (`http://localhost:8000/Web Ui/lives.html`).
2. Record session details upon stream completion:
   - **Employee ID**: Select employee ID/name.
   - **GMV Generated**: Enter total sales revenue.
   - **Units Sold**: Enter total quantity.
3. Save record to update the live stream leaderboard.

***

### 💰 How to Process Employee Payouts

1. Navigate to **Payout Management** (`http://localhost:8000/Web Ui/payout.html`).
2. Click **Create Payout**.
3. Select Employee, enter payout amount and payout date.
4. Set status to `Pending` or `Completed` and save.


# Part 3: Architecture & System Philosophy {.part}

<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/explanation/architecture-and-diataxis.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Conceptual explanation of decoupled web architecture and adoption rationale of Diátaxis documentation framework.
</div>

## Architectural Explanation & Diátaxis Framework Adoption

This document explains the system architecture, design decisions, and adoption of the **Diátaxis Documentation Framework** for Omni-View.

***

### 🏛 Architecture Overview

Omni-View Business Command Centre is engineered using a decoupled web architecture:

1. **Frontend Layer**:
   - Built with HTML5, CSS3, JavaScript (ES6+), and Bootstrap 5.
   - Dynamic charts powered by Chart.js.

2. **Backend & Database Layer**:
   - Built on Supabase (PostgreSQL database engine).
   - Real-time data queries managed directly through REST APIs via `supabase-js`.

3. **Role-Based Access Control (RBAC)**:
   - Client-side navigation guards (`admin_authcheck.js`, `authcheck.js`) enforce role boundaries (`administrator`, `employee`, `owner`).
   - Server-side security enforced via Supabase Row Level Security (RLS) policies.

***

### 📖 Diátaxis Framework Adoption

Documentation often mixes step-by-step tutorials, practical recipes, and technical API reference into monolithic pages. This increases cognitive load for human developers and causes hallucination in autonomous AI agents.

Omni-View solves this by adopting the **Diátaxis Documentation Framework** (https://diataxis.fr/), structuring content into four distinct quadrants based on user intent and mode:

```text
                  USER INTENT
           Learning         Practical
        +----------------+----------------+
 Acquisition|  TUTORIALS     | HOW-TO GUIDES  |
 (Study)    | (Learning-     | (Problem-      |
            |  oriented)     |  oriented)     |
        +----------------+----------------+
 Application|  EXPLANATION   |   REFERENCE    |
 (Work)     | (Concept-      | (Information-  |
            |  oriented)     |  oriented)     |
        +----------------+----------------+
```

#### Four Quadrants in Omni-View:

1. **Tutorials (`docs/tutorials/`)**:
   - **Goal**: Guided learning through execution.
   - **Scope**: Step-by-step onboarding for new users and AI agent setup.

2. **How-To Guides (`docs/how-to/`)**:
   - **Goal**: Practical directions for specific tasks.
   - **Scope**: Task-focused workflows (e.g. updating stock, processing payouts, parsing `llms.txt`).

3. **Reference (`docs/reference/`)**:
   - **Goal**: Factual descriptions and technical specifications.
   - **Scope**: File paths, API signatures, database schema, CLI options.

4. **Explanation (`docs/explanation/`)**:
   - **Goal**: Conceptual context and architectural rationale.
   - **Scope**: System design, security model, Diátaxis, and OKF 0.2 adoption.


<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>docs/explanation/okf-02-and-diataxis.md</code></div>

<div class="callout callout-note">
<strong>📌 Executive Summary</strong>

Conceptual explanation of Open Knowledge Format 0.2 and Domain-Specific Operational Model for AI agents.
</div>

## Explanation: Open Knowledge Format (OKF 0.2) & DSOM Integration Rationale

This document explains the integration of **Open Knowledge Format (OKF 0.2)** principles and **Domain-Specific Operational Model (DSOM)** within the Omni-View repository documentation system.

***

### 💡 Conceptual Background

As LLM-driven autonomous AI agents (such as Google Jules, Antigravity, and CI sub-agents) assume active roles in software engineering tasks, standard unstructured documentation causes context window overflow, redundant file reads, and degraded code generation accuracy.

To address this, Omni-View incorporates **Open Knowledge Format (OKF 0.2)** concepts and **DSOM** standards alongside the **Diátaxis Framework**.

***

### 🎯 Open Knowledge Format (OKF 0.2) Concepts

Open Knowledge Format (OKF 0.2) emphasizes machine-readable context discovery and clean knowledge framing:

1. **Explicit Entity Mapping**: Every file, utility, script, and database table has an unambiguous canonical path and type declaration in `docs/reference/file-structure-and-api.md` and `docs/reference/cli-and-tools.md`.
2. **Standardized Context Discovery (`llms.txt`)**: Following [llmstxt.org](https://llmstxt.org/), `llms.txt` maps all published documentation nodes with concise summaries. AI agents can parse this file to construct an XML context graph (`llm_context.xml`) without reading unneeded binary assets.
3. **Structured Jekyll Frontmatter Metadata**: Every Markdown file in `docs/` contains standard Jekyll YAML frontmatter (`title`, `description`, `nav_order`, `layout`), ensuring dual compatibility with both GitHub Pages (Jekyll) and GitBook parser engines while providing structured page metadata for `llms.txt` discovery.

***

### ⚡ Domain-Specific Operational Model (DSOM)

DSOM defines operational boundaries and execution constraints for autonomous agents operating in this repository:

- **Minimal Sufficient Context**: AI agents must ingest only files directly pertinent to assigned tasks.
- **Reference Anchoring**: `docs/reference/file-structure-and-api.md` serves as the single source of truth for file paths and backend schemas.
- **Deterministic Verification Contract**: Every code change must be validated by running automated unit tests (`uv run pytest`) prior to PR submission.


# Part 4: Core Implementation Source Code {.part}


<a id="code-parse-llms-txt"></a>
### LLM Parser & Sitemap Utility

**Source File:** `parse_llms_txt.py`

```python
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
    """Generate XML context from parsed `llms.txt` data, including metadata and available local document contents.

    Args:
        llms_data: Parsed `llms.txt` data containing the title, summary, sections, and documents.
        root_dir: Root directory used to resolve relative document paths.

    Returns:
        Formatted XML context document.
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

            # Embed local document content if file exists and stays within root_dir
            rel_path = item.get("url", "").lstrip("/")
            resolved_root = os.path.realpath(root_dir)
            file_path = os.path.realpath(os.path.join(root_dir, rel_path))

            if os.path.commonpath([resolved_root, file_path]) == resolved_root and os.path.isfile(file_path):
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
    """Generate the standard Markdown index for the project's documentation.

    Args:
        docs_dir: Documentation directory name retained for API compatibility.
        relative_to_docs: Whether to generate paths relative to the docs/ directory.

    Returns:
        Markdown content containing the project title, summary, and documentation links.
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
        f"- [Technical Book Design & PDF Compilation Master Prompt Guide]({p}governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md): Master prompt and blueprint for compiling publication-grade PDF handbooks.",
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
        f"- [Produce Project Technical Handbook]({p}how-to/HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK.md): AI prompt engineering and skill adoption blueprint for compiling handbooks.",
        f"- [Deploy Omni-View on Render.com]({p}how-to/deploy-omni-view-on-render.md): Step-by-step guide to deploying as a Render Static Site and troubleshooting deployment issues.",
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
    """Build a complete documentation index from available repository and documentation files.

    Args:
        docs_dir: Directory containing the documentation files.
        root_dir: Repository root used to resolve file paths.

    Returns:
        Formatted documentation text containing the contents of each available file.
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
        os.path.join(docs_dir, "governance", "TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md"),
        os.path.join(docs_dir, "explanation", "dsom-governance.md"),
        os.path.join(docs_dir, "explanation", "diataxis.md"),
        os.path.join(docs_dir, "explanation", "system-architecture.md"),
        os.path.join(docs_dir, "explanation", "architecture-and-diataxis.md"),
        os.path.join(docs_dir, "explanation", "okf-02-and-diataxis.md"),
        os.path.join(docs_dir, "tutorials", "01-getting-started.md"),
        os.path.join(docs_dir, "tutorials", "getting-started.md"),
        os.path.join(docs_dir, "tutorials", "llms-txt-setup.md"),
        os.path.join(docs_dir, "how-to", "index.md"),
        os.path.join(docs_dir, "how-to", "HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK.md"),
        os.path.join(docs_dir, "how-to", "deploy-omni-view-on-render.md"),
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
    """Generate text and XML sitemaps for the documentation site.

    Args:
        docs_dir: Documentation directory path retained for API compatibility.
        base_url: Base URL used to construct sitemap entries.

    Returns:
        Tuple containing text sitemap content and XML sitemap content.
    """
    urls = [
        f"{base_url}/",
        f"{base_url}/START-HERE",
        f"{base_url}/SOP-KNOWLEDGE-FIRST-DISCOVERY",
        f"{base_url}/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE",
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
        f"{base_url}/how-to/HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK",
        f"{base_url}/how-to/deploy-omni-view-on-render",
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
```



<a id="code-generate-summary"></a>
### Summary Table of Contents Generator

**Source File:** `tools/generate_summary.py`

```python
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
    """Extract title from YAML frontmatter or first H1 header in a Markdown file.

    Args:
        filepath: Path to the Markdown file.

    Returns:
        Extracted title string or fallback title derived from filename.
    """
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


def generate_summary_lines(is_docs_folder: bool = False) -> str:
    """Generate markdown summary lines for SUMMARY.md table of contents.

    Args:
        is_docs_folder: Boolean flag indicating if generating for docs/SUMMARY.md.

    Returns:
        Formatted summary content as a Markdown string.
    """
    prefix = ""
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


def build_summary() -> None:
    """Scan repository and build structured SUMMARY.md files in root and docs/."""
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
```
