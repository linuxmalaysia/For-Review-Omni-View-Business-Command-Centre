---
title: "Tutorial: Getting Started with Omni-View"
description: "Step-by-step onboarding tutorial for navigating and using Omni-View Business Command Centre."
type: "tutorial"
id: "docs/tutorials/getting-started.md"
dsom_governance:
  domain: "Automation"
  context_tier: "L1-Overview"
tags:
  - "dsom-protocol"
  - "tutorial"
  - "onboarding"
related_links:
  - "docs/tutorials/01-getting-started.md"
  - "docs/tutorials/llms-txt-setup.md"
nav_order: 1
layout: "default"
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
- Local Python runtime for serving application files (`python3 -m http.server 8000`).

---

## 🚀 Step 1: Launch the Application

1. Open your terminal in the project root directory.
2. Start the local server:
   ```bash
   python3 -m http.server 8000 --directory .
   ```
3. Open `http://localhost:8000/Web Ui/login.html` in your web browser.

---

## 🔐 Step 2: User Authentication

- **Administrator Access**: Enter admin credentials to access `main.html` (Administrator Command Dashboard).
- **Staff Access**: Enter employee credentials to access `Employee_Main.html` (Staff Member Dashboard).

---

## 📊 Step 3: Explore Core Quadrants

- **Products (`product.html`)**: Manage product inventory items, stock levels, and prices.
- **Live Streams (`lives.html` / `Employee_Lives.html`)**: Monitor live streaming session performance, GMV, and units sold.
- **Payouts (`payout.html` / `Employee_Payout.html`)**: Process and review employee payout allocations.
- **Reports (`report.html`)**: Export analytics and generate PDF performance reports.
