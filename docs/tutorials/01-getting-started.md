---
title: "Quickstart Onboarding Guide"
description: "Step-by-step developer and operator onboarding walkthrough for launching and verifying Omni-View."
type: "tutorial"
id: "docs/tutorials/01-getting-started.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L1-Overview"
tags:
  - "dsom-protocol"
  - "tutorial"
  - "onboarding"
related_links:
  - "docs/tutorials/getting-started.md"
  - "docs/how-to/manage-inventory-and-payouts.md"
nav_order: 1
layout: "default"
---

# Quickstart: Onboarding Guide

Welcome to the **Omni-View Business Command Centre** onboarding tutorial. This hands-on guide gets you operational in under 5 minutes.

---

## 🎯 Step-by-Step Walkthrough

### 1. Environment Initialization
Initialize your Python virtual environment using `uv`:
```bash
uv sync
```

### 2. Verify Repository Integrity
Execute the automated test suite to ensure all frontend, schema, and documentation tests pass:
```bash
uv run pytest
```

### 3. Launch Local Application Server
Serve the application locally using Python's HTTP server:
```bash
python3 -m http.server 8000 --directory .
```
Access the application at `http://localhost:8000/Web Ui/login.html`.
