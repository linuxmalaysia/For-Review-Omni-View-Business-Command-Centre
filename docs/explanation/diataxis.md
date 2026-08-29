---
title: "Diátaxis Structuring Framework Implementation"
description: "Architectural specification of the Diátaxis 4-quadrant documentation framework within Omni-View."
type: "architecture"
id: "docs/explanation/diataxis.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L1-Overview"
tags:
  - "dsom-protocol"
  - "diataxis"
  - "explanation"
related_links:
  - "docs/explanation/dsom-governance.md"
  - "docs/explanation/system-architecture.md"
nav_order: 2
layout: "default"
---

# Diátaxis Documentation Framework Implementation

Omni-View structures all technical documentation into four distinct functional quadrants based on user intent and mode, following the [Diátaxis Framework](https://diataxis.fr/).

---

## 🧭 Diátaxis Quadrant Matrix

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

---

## 📂 Quadrant Directory Specifications

1. **Tutorials (`docs/tutorials/`)**: Step-by-step onboarding walkthroughs for new developers and AI setup.
2. **How-To Guides (`docs/how-to/`)**: Task-oriented operational recipes for routine day-2 operations.
3. **Reference (`docs/reference/`)**: Technical specs, CLI flags, database schemas, and tool parameters.
4. **Explanation (`docs/explanation/`)**: High-level architectural reasoning, DSOM governance models, and design trade-offs.
