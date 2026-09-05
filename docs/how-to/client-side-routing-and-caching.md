---
title: "How-To: Client-Side Routing and Session Caching"
description: "Practical guide on navigating Omni-View without full page reloads and persisting session data until the browser tab is closed."
type: "how-to"
id: "docs/how-to/client-side-routing-and-caching.md"
dsom_governance:
  domain: "Architecture"
  context_tier: "L2-OperationalGuide"
tags:
  - "dsom-protocol"
  - "how-to"
  - "router"
  - "caching"
related_links:
  - "docs/reference/file-structure-and-api.md"
  - "docs/explanation/architecture-and-diataxis.md"
nav_order: 3
layout: "default"
---

# How-To: Client-Side Routing and Session Caching

This guide explains how client-side routing and session caching work in Omni-View, allowing seamless dynamic page switching while retaining fetched data until the browser tab or session is closed.

---

## 🚀 Overview

Omni-View uses a lightweight, client-side Single Page Application (SPA) routing mechanism (`js/router.js`) paired with a session caching utility (`js/cache.js`).

### Core Benefits

- **No Full Page Reloads:** Page transitions intercept navigation link clicks and update view containers (`.app-shell` / `body`) dynamically.
- **Data Retention Across Navigation:** Data fetched from Supabase (user profiles, dashboard metrics, stock counts, payouts) is stored in browser `sessionStorage`.
- **Automatic Cache Cleanup:** Session data persists throughout the active session and is completely cleared when the user logs out or closes the browser tab.

---

## 🛠 JavaScript Modules Involved

| Script Path | Purpose |
| :--- | :--- |
| `js/cache.js` | Provides `window.SessionCache` to get, set, remove, and clear `sessionStorage` key-value entries. |
| `js/router.js` | Intercepts link navigation, fetches page views via HTML5 History API (`pushState`), and re-executes page load hooks. |
| `js/loaddata.js` | Caches logged-in profile details (`user_profile_<email>`) during the active session. |
| `js/dashboard.js` | Caches dashboard summaries (GMV, items sold, stock levels, active staff, top employees). |
| `js/logout.js` | Calls `window.SessionCache.clearAll()` upon logout prior to redirecting to `login.html`. |

---

## 📖 Usage Examples

### 1. Storing and Retrieving Cached Data

```javascript
// Reading from session cache
let cachedData = window.SessionCache.get('my_custom_key');

if (!cachedData) {
    // Fetch fresh data from backend
    cachedData = await fetchFromDatabase();

    // Store in sessionStorage
    window.SessionCache.set('my_custom_key', cachedData);
}
```

### 2. Navigating Programmatically

```javascript
// Programmatic SPA navigation without page refresh
window.AppRouter.navigateTo('product.html');
```

### 3. Evicting Caches on Logout or Mutation

```javascript
// Clear all session cache keys
window.SessionCache.clearAll();
```

---

## 🧪 Verification

To verify that routing and cache files pass structural and JavaScript syntax tests:

```bash
uv run pytest tests/test_js_files.py
```
