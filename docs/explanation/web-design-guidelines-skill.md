---
title: "Web Design Guidelines Skill Adoption & Integration Guide"
description: "Comprehensive guide for humans and AI agents (Jules & Antigravity) to understand, operate, and extend the web-design-guidelines skill."
type: "explanation"
id: "docs/explanation/web-design-guidelines-skill.md"
dsom_governance:
  domain: "Design & UX Architecture"
  context_tier: "L2-StandardDocumentation"
tags:
  - "skills"
  - "web-design"
  - "accessibility"
  - "ui-ux"
  - "jules-agent"
  - "antigravity"
related_links:
  - "docs/explanation/web-interface-improvements.md"
  - "docs/explanation/diataxis.md"
nav_order: 10
layout: "default"
---

# Web Design Guidelines Skill Adoption & Integration Guide

This document serves as the human-readable and agent-navigable guide for adopting, operating, and extending the **Web Design Guidelines Skill** (`web-design-guidelines`) within the **Omni-View Business Command Centre** ecosystem for both **Jules** and **Antigravity** AI agent architectures.

---

## 💡 Overview & Purpose

The `web-design-guidelines` skill automates the evaluation of frontend user interfaces (HTML structures, CSS styles, JavaScript interactions, and React/framework components) against industry-standard Web Interface Guidelines.

### Key Objectives
1. **Automated UI/UX Auditing**: Instantly inspect markup and client scripts for compliance with accessibility standards (WCAG / ARIA), interactive focus states, form best practices, and performance principles.
2. **High Signal-to-Noise Reporting**: Produce terse, actionable findings in `file:line` format to facilitate rapid automated or human remediation.
3. **Agent Integration**: Provide a standardized protocol for autonomous software agents like Jules and Antigravity to run pre-flight UI checks during feature development and refactoring.

---

## 🛠️ Architecture & Skill Structure

The skill files are maintained in the repository under:

```text
skills/web-design-guidelines/
└── SKILL.md
```

### Frontmatter Metadata Specification
```yaml
---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---
```

---

## 🤖 How Jules & Antigravity Adopt & Extend This Skill

### 1. Guideline Retrieval Strategy
During a UI audit, the agent retrieves the live ruleset from the canonical remote specification URL:
```text
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```
If offline or in isolated sandbox environments, the agent falls back to the internal reference documentation located at `docs/explanation/web-interface-improvements.md`.

### 2. Execution Workflow for AI Agents
1. **Target Identification**: Specify files or patterns (e.g., `Web Ui/*.html`, `js/*.js`). If omitted, the agent automatically identifies modified or high-impact interface files.
2. **Rule Matching & AST Parsing**: Check each element against rule domains:
   - **Accessibility**: ARIA labels on icon buttons, form labels, keyboard handlers, semantic tags (`<button>`, `<a>`, `<label>`), heading hierarchy, image `alt` attributes.
   - **Focus & Interaction**: `:focus-visible` styling, absence of un-replaced `outline: none`, click target sizing, touch action definitions.
   - **Forms**: Mandatory `autocomplete` and `name` attributes, appropriate `type` and `inputmode`, non-blocking paste handlers, inline error placement.
   - **Typography**: Semantic ellipsis (`…`), curly quotes (`“` / `”`), non-breaking spaces, numeric layout formatting (`tabular-nums`).
   - **Performance & CLS**: Explicit image `width` and `height`, lazy loading for below-fold media, CSS property transition restrictions (no `transition: all`).
3. **Output Generation**: Output findings strictly using `file:line - description` formatting without conversational preamble.

---

## 🚀 Enhancements & Future Skill Tasks

To continuously improve the capability of Jules and Antigravity, the skill can be extended with the following automated tasks:

1. **Automated Playwright Screenshot Audit**:
   - Integrate with Playwright script execution to capture visual regressions and test keyboard focus navigation automatically.
2. **Automated ARIA Tree Validation**:
   - Parse HTML document trees into accessibility trees and flag broken ARIA references (e.g., `aria-labelledby` pointing to non-existent IDs).
3. **Automated Dark Mode Contrast Checker**:
   - Verify WCAG AA/AAA contrast ratios for text elements in dark and light themes using computed style rules.
4. **CI Integration Step**:
   - Include UI compliance checks as part of pre-commit hooks (`uv run pytest` / custom linting scripts).
