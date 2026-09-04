---
okf_version: "0.2"
type: "howto"
title: "Deploying Omni-View Business Command Centre on Render.com"
timestamp: "2026-09-02T00:00:00Z"
topics: ["render-com", "deployment", "static-site", "python-runtime", "troubleshooting", "omni-view"]
description: "Step-by-step Diátaxis How-To guide for building, configuring, deploying, and troubleshooting the Omni-View Business Command Centre static site and documentation portal on Render.com."
resource: "file:///docs/how-to/deploy-omni-view-on-render.md"
sources: [
  "https://render.com/docs/static-sites",
  "https://render.com/docs/troubleshooting-deploys",
  "render.yaml",
  "pyproject.toml"
]
dsom_governance:
  domain: "Automation"
  context_tier: "L2-Operational"
tags:
  - "render-com"
  - "deployment"
  - "how-to"
related_links:
  - "docs/multi-platform-hosting.md"
  - "docs/how-to/index.md"
  - "docs/how-to/generate-llms-context.md"
nav_order: 5
layout: "default"
generated: "jules"
verified: true
status: "approved"
stale_after: "2027-09-02T00:00:00Z"
language: "en-GB"
---

# 🚀 Deploying Omni-View Business Command Centre on Render.com

This guide provides a comprehensive step-by-step walkthrough for deploying the **Omni-View Business Command Centre** interactive web application and documentation portal to [Render.com](https://render.com/).

---

## 🎯 Architecture & Deployment Type Recommendation

 lower-latency static site delivery is recommended for Omni-View:

1. **Frontend Web Application:** The Omni-View interface is a client-side web application composed of HTML, CSS, JavaScript, and asset management modules residing in `Web Ui/`, `js/`, `css/`, and `index.html`.
2. **Automated Documentation Engine:** During the build process, `parse_llms_txt.py --generate-all` generates machine-parseable LLM context structures (`llms-full.txt`, `llm_context.xml`) and sitemaps.
3. **Render Deployment Model:** Deployed as a **Render Static Site**, avoiding unnecessary backend web server processes (e.g. Uvicorn/FastAPI) and eliminating cold-start latency.

---

## 📋 Prerequisites & Project Structure

Ensure the repository contains the following deployment artifacts:

```text
.
├── render.yaml                             # Render Static Site Blueprint specification
├── pyproject.toml                          # Dependency & test specification
├── parse_llms_txt.py                      # Build script for generating LLM context & sitemaps
├── index.html                              # Web application landing page
└── Web Ui/                                 # Command centre dashboard views
```

---

## 🛠️ Deployment Step-by-Step Instructions

### Method 1: Render Blueprint Deployment (Recommended)

1. Push your changes to GitHub or GitLab.
2. Log into the [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** and select **Blueprint**.
4. Connect your repository `For-Review-Omni-View-Business-Command-Centre`.
5. Render will automatically detect `render.yaml` and configure the static site with:
   - **Service Type:** `Static Site`
   - **Name:** `omni-view-command-centre`
   - **Build Command:** `python3 parse_llms_txt.py --generate-all`
   - **Publish Directory:** `./`

---

### Method 2: Manual Static Site Setup on Render (Free Tier Compatible)

If creating the service manually in the Render Dashboard:

> [!NOTE]
> **Render Static Sites Benefits:**
>
> - Free static site hosting on Render's Free tier, subject to standard workspace outbound-bandwidth and build-pipeline limits.
> - High-availability global CDN distribution.
> - Fast automated continuous deployment on every git push.

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

---

## 🔧 Troubleshooting Render Deploys

### 1. Error: `ModuleNotFoundError: No module named 'src'` (Exit Status 1) or `uvicorn: command not found` (Exit Status 127)

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

### 2. Missing Generated Files or Sitemap Warnings

- **Symptom:** Deploy build log fails or missing `llms-full.txt` or `sitemap.xml`.
- **Resolution:** Verify that the build command is set to `python3 parse_llms_txt.py --generate-all`. This ensures all XML context files and sitemaps are pre-built prior to deployment publishing.

### 3. Header and Caching Configuration

- **Symptom:** Browser caches old assets after updating HTML or CSS.
- **Resolution:** `render.yaml` configures standard headers for client caching:

  ```yaml
  headers:
    - path: /*
      name: Cache-Control
      value: max-age=3600
  ```

---

## 🌐 Endpoints & Verification

Once deployed, verify your service endpoints on Render:

- **Command Centre Portal:** `https://<your-service>.onrender.com/`
- **Dashboard Views:** `https://<your-service>.onrender.com/Web Ui/main.html`
- **LLM Text Summary:** `https://<your-service>.onrender.com/llms.txt`
- **LLM Full Context:** `https://<your-service>.onrender.com/llms-full.txt`
- **LLM XML Context:** `https://<your-service>.onrender.com/llm_context.xml`
