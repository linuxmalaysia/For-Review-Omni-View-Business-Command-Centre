---
title: "Tutorial: Getting Started with Omni-View"
description: "Step-by-step onboarding tutorial for navigating and using Omni-View Business Command Centre."
nav_order: 1
layout: default
---

# Tutorial: Getting Started with Omni-View Command Centre

Welcome to **Omni-View Business Command Centre**! This tutorial guides you step-by-step through setting up and navigating the platform.

---

## 🎯 Learning Objectives

By completing this tutorial, you will:
- Launch the application interface locally.
- Authenticate using administrator or staff credentials.
- Navigate core operational modules: Dashboard, Products, Lives, and Payouts.

---

## 📋 Prerequisites

- Modern web browser (Chrome, Edge, or Firefox).
- Python 3.9+ with `uv` package manager installed.
- Internet connectivity for Supabase REST API access.

---

## 🚀 Step 1: Initialize Local Workspace

Run the following shell commands to start the local application server:

```bash
uv sync
python3 -m http.server 8000 --directory .
```

Open `http://localhost:8000` in your web browser. The entry point (`index.html`) automatically routes to `./Web Ui/login.html`.

---

## 🔐 Step 2: Authenticate and Sign In

1. Open the sign-in page at `http://localhost:8000/Web Ui/login.html`.
2. Input target credentials:
   - **Administrator Login**: Enter admin email and password.
   - **Employee Login**: Enter staff email and password.
3. Click **Login**.
4. System redirects based on user role:
   - **Administrators**: Navigated to `main.html` (Admin Command Dashboard).
   - **Employees**: Navigated to `Employee_Main.html` (Staff Dashboard).

---

## 📊 Step 3: Explore Operational Metrics

1. Review key performance indicators at the top:
   - **Daily GMV**: Real-time gross merchandise value.
   - **Items Sold Today**: Total merchandise units processed.
   - **Active Staff Count**: Active host staff on shift.
2. Inspect the **Inventory Summary** table and live sales bar charts.
3. Check **Top Employees This Month** and recent payout records.

---

## 🎓 Next Steps

Now that you have completed basic setup:
- Learn procedural workflows in [Managing Inventory & Payouts](../how-to/manage-inventory-and-payouts.md).
- Learn LLM context generation in [LLMs.txt Setup Guide](llms-txt-setup.md).
