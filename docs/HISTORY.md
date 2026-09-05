---
layout: default
title: "HISTORY"
description: "Project history and lineage"
---

# Project History

## Origins & Evolution

 Omni View Business Command Centre began as a lightweight executive dashboard designed to aggregate business metrics, inventory status, and payout management into a clean visual interface.

### Phase 1: Prototype & Client-Side UI
- Initial release featuring responsive HTML/CSS/JS interfaces.
- Client-side navigation, interactive charts, and local session cache.

### Phase 2: Documentation & AI Context Standardization
- Integrated OKF 0.2 (Ontological Knowledge Frame) standards.
- Added `parse_llms_txt.py` tool to automate generation of `llms.txt`, `llms-full.txt`, and XML context files for LLM agents.
- Adopted the Diátaxis framework for documentation under `docs/`.

### Phase 3: Multi-Platform Publishing & Laboratory UI
- Adapted site structure for Jekyll and GitHub Pages automated deployment.
- Integrated `cmsfornerd2` Laboratory design language with Light/Dark theme switcher.
- Configured multi-platform hosting support for GitHub Pages, GitLab Pages, GitBook, ReadTheDocs, and Render.com.

### Phase 4: Technical Book Design & Autonomous Skill Compilation
- Added Technical Book Design & PDF Compilation Master Prompt Guide and How-To blueprint.
- Defined reusable agent skills (`dsom-technical-book-compiler` and `project-technical-book-compiler`).
- Implemented universal book assembler `tools/build_project_book.py` with Terminal & Cloud print standards.
