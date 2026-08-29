---
title: "Omni-View System Architecture & Topology"
description: "Detailed system architecture diagram, subsystem topologies, and integration points for Omni-View."
type: "architecture"
id: "docs/explanation/system-architecture.md"
dsom_governance:
  domain: "Infrastructure"
  context_tier: "L1-Overview"
tags:
  - "dsom-protocol"
  - "architecture"
  - "explanation"
related_links:
  - "docs/explanation/dsom-governance.md"
  - "docs/reference/file-structure-and-api.md"
nav_order: 3
layout: "default"
---

# System Architecture & Component Topology

Omni-View Business Command Centre is structured as a decoupled web application backed by Supabase PostgreSQL database service.

---

## 🏗 Subsystem Topologies

```mermaid
graph LR
    SubGraph1[Frontend Web UI] -->|REST / JS SDK| SubGraph2[Supabase Backend Engine]
    SubGraph1 -->|Chart.js| Analytics[Dashboard Analytics]
    SubGraph2 --> PostgreSQL[(PostgreSQL DB)]
    SubGraph2 --> RLS[Row Level Security]
```

### Components:

- **Client Presentation Layer (`Web Ui/`, `js/`, `css/`)**: Static HTML5 interface enhanced with Bootstrap 5 and Chart.js. Client authentication guards enforce RBAC rules.
- **Backend Infrastructure Layer (Supabase)**: Houses core tables (`profiles`, `products`, `lives`, `payouts`) secured via PostgreSQL Row Level Security (RLS).
- **Automation & LLM Context Layer (`parse_llms_txt.py`)**: Utility pipeline generating XML context maps and sitemaps for AI systems.
