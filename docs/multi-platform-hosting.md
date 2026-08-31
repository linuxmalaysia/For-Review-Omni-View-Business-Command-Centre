---
layout: default
title: "Multi-Platform Hosting Guide"
description: "Deploying Omni View Command Centre to GitLab Pages, GitBook, ReadTheDocs, and Render.com"
---

# Multi-Platform Hosting Guide

Omni View Command Centre supports multi-platform publishing across modern documentation and hosting platforms.

---

## Supported Hosting Targets

### 1. GitHub Pages
- **Configuration**: `.github/workflows/jekyll-gh-pages.yml` and `_config.yml`
- **Deployment**: Automatic on push to `main`.

### 2. GitLab Pages
- **Configuration**: `.gitlab-ci.yml`
- **Deployment**: Uses Ruby Jekyll image to compile site into `public/`.

### 3. GitBook
- **Configuration**: `.gitbook.yaml`
- **Root directory**: `docs/`
- **Summary file**: `SUMMARY.md`

### 4. ReadTheDocs (v2)
- **Configuration**: `.readthedocs.yaml`
- **Build engine**: Ubuntu 22.04 with Python 3.12.

### 5. Render.com
- **Configuration**: `render.yaml`
- **Type**: Static site service running `python3 parse_llms_txt.py --generate-all`.
