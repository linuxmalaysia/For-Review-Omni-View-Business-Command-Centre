---
layout: default
title: "CHANGELOG"
description: "Project version history and release logs"
---

# Changelog

All notable changes to the Omni View Business Command Centre project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Technical Book Design & PDF Compilation Master Prompt Guide (`docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md`) and How-To blueprint (`docs/how-to/HOW-TO-PRODUCE-PROJECT-TECHNICAL-HANDBOOK.md`).
- Autonomous agent skills `dsom-technical-book-compiler` and `project-technical-book-compiler` under `skills/` and `.agents/skills/`.
- Universal project handbook compiler script (`tools/build_project_book.py`).
- GitHub Pages official workflow (`.github/workflows/jekyll-gh-pages.yml`) for automated site builds and deployment on push to `main`.
- Laboratory design template matching `cmsfornerd2` with dynamic Light / Dark / Auto mode toggle.
- Root documentation files (`CHANGELOG.md`, `HISTORY.md`, `SUMMARY.md`, `README.md`) and structured `docs/` tree following Diátaxis framework.
- Multi-platform deployment configurations for GitLab Pages (`.gitlab-ci.yml`), GitBook (`.gitbook.yaml`), ReadTheDocs (`.readthedocs.yaml`), and Render.com (`render.yaml`).
- Auto-discovery tooling (`tools/generate_summary.py` and `tools/install_git_guardrails.py`) to automatically update `SUMMARY.md` whenever new Markdown files are created.
