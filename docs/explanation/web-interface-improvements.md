---
title: "Web Interface Audit & Code Improvement Plan"
description: "Detailed UI audit findings, design guidelines, and code modification plan for Omni-View Business Command Centre."
type: "explanation"
id: "docs/explanation/web-interface-improvements.md"
dsom_governance:
  domain: "Design & UX Architecture"
  context_tier: "L2-StandardDocumentation"
tags:
  - "web-interface"
  - "ui-ux"
  - "accessibility"
  - "design-system"
  - "code-improvements"
related_links:
  - "docs/explanation/web-design-guidelines-skill.md"
  - "docs/explanation/system-architecture.md"
nav_order: 11
layout: "default"
---

# Web Interface Audit & Code Improvement Plan

This document outlines the design audit standards, identified compliance gaps, and targeted code improvements for the **Omni-View Business Command Centre** web interface (`Web Ui/*.html` and `js/*.js`).

---

## 🎨 UI Design Guidelines & Standards

The project follows the Web Interface Guidelines established by Vercel and extended for enterprise command centers. Key standard domains include:

### 1. Accessibility (a11y)

- **Form Controls**: Every input control must have a visible `<label>` bound via `for`/`id` or an explicit `aria-label`.
- **Icon Buttons**: Icon-only controls (such as password visibility toggles and modal close icons) must include `aria-label`.
- **Decorative Elements**: Non-informational icons must be hidden from screen readers using `aria-hidden="true"`.
- **Semantic Tags**: Interactive actions use `<button>`, navigation uses `<a>`, avoiding `<div onClick>`.

### 2. Form Experience & Autocomplete

- **Autocomplete Hints**: Authentication and profile inputs must supply valid `autocomplete` hints (e.g., `email`, `current-password`, `new-password`, `username`).
- **Meaningful Names**: Every form input must have a descriptive `name` attribute for browser and password manager integration.
- **Unblocked Input**: Pasting must never be intercepted or blocked (`onPaste` with `preventDefault` is strictly prohibited).

### 3. Typography & Microcopy

- **Ellipsis**: Literal triple periods (`...`) in labels, placeholders, and dynamic status updates must be replaced with the unicode character (`…`).
- **Loading States**: Dynamic button feedback must indicate progress with trailing ellipsis (e.g., `Logging in…`, `Saving…`).

### 4. Performance & Layout Stability

- **Explicit Image Dimensions**: All static `<img>` elements must specify `width` and `height` attributes to prevent Cumulative Layout Shift (CLS).

---

## 🔍 Code Audit Findings & Modification Plan

### Target Files Audit Summary

| Target File | Identified Gaps | Planned Remediation |
| :--- | :--- | :--- |
| `Web Ui/login.html` | Missing `name` & `autocomplete` on `#email` & `#password`; logo `<img>` missing dimensions. | Add `name="email"` `autocomplete="email"`, `name="password"` `autocomplete="current-password"`, and `width="100"` `height="100"`. |
| `Web Ui/forgot-password.html` | Missing `name` & `autocomplete` on `#email` input. | Add `name="email"` and `autocomplete="email"`. |
| `Web Ui/reset_password.html` | Missing `name` & `autocomplete` on password inputs. | Add `name="password"` `autocomplete="new-password"` and `name="confirm-password"` `autocomplete="new-password"`. |
| `Web Ui/edit_profile.html` | Missing `name` & `autocomplete` on username and email inputs. | Add `name="username"` `autocomplete="username"` and `name="email"` `autocomplete="email"`. |
| `Web Ui/Employee_edit_profile.html` | Missing `name` & `autocomplete` on inputs. | Add `name="username"` `autocomplete="username"` and `name="email"` `autocomplete="email"`. |
| `js/login.js`, `js/payout.js`, `js/live.js`, `js/reset_password.js`, `js/manage_user.js` | Literal triple dots (`...`) used in loading indicators and toasts. | Replace `...` with semantic ellipsis `…`. |

---

## 🚀 Implementation Matrix

All modifications are applied directly to source template and script files in the codebase, ensuring full adherence to accessibility and design guidelines.
