---
layout: default
title: "GitHub Pages Setup Guide"
description: "How to configure and deploy Omni View Command Centre to GitHub Pages"
---

# GitHub Pages Automated Deployment Guide

This guide details how GitHub Pages is configured for automated build and deployment upon every commit to `main`.

---

## 1. Official Workflow File

The repository uses GitHub's official Jekyll deployment action located at `.github/workflows/jekyll-gh-pages.yml`.

### Key Trigger & Permissions
```yaml
on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write
```

---

## 2. GitHub Repository Settings Configuration

To enable automated deployments:
1. Navigate to your GitHub repository: `https://github.com/linuxmalaysia/For-Review-Omni-View-Business-Command-Centre`
2. Go to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, select **GitHub Actions**.
4. Push a commit to `main`. GitHub Actions will automatically compile Jekyll and deploy to `https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre/`.

---

## 3. Dynamic Markdown Auto-Discovery

When new Markdown files are added to `docs/` or root:
- `tools/generate_summary.py` auto-discovers the file and adds it to `SUMMARY.md`.
- `parse_llms_txt.py` generates updated `llms.txt`, `llms-full.txt`, `sitemap.txt`, and `sitemap.xml`.
- Jekyll automatically renders the `.md` file using `_layouts/default.html`.
