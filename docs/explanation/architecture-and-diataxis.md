---
title: "Explanation: Architecture & Diátaxis Framework Adoption"
description: "Conceptual explanation of decoupled web architecture and adoption rationale of Diátaxis documentation framework."
type: "architecture"
id: "docs/explanation/architecture-and-diataxis.md"
dsom_governance:
  domain: "Infrastructure"
  context_tier: "L1-Overview"
tags:
  - "dsom-protocol"
  - "architecture"
  - "diataxis"
related_links:
  - "docs/explanation/dsom-governance.md"
  - "docs/explanation/diataxis.md"
nav_order: 1
layout: "default"
---

# Architectural Explanation & Diátaxis Framework Adoption

This document explains the system architecture, design decisions, and adoption of the **Diátaxis Documentation Framework** for Omni-View.

---

## 🏛 Architecture Overview

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

---

## 📖 Diátaxis Framework Adoption

Documentation often mixes step-by-step tutorials, practical recipes, and technical API reference into monolithic pages. This increases cognitive load for human developers and causes hallucination in autonomous AI agents.

Omni-View solves this by adopting the **Diátaxis Documentation Framework** (<https://diataxis.fr/>), structuring content into four distinct quadrants based on user intent and mode:

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

### Four Quadrants in Omni-View

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
