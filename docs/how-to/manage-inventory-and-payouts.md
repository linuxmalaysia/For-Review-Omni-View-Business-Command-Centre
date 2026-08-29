---
title: "How-To: Manage Inventory, Live Sessions, and Payouts"
description: "Practical operational guide for stock management, live streaming sales tracking, and staff payouts."
type: "guide"
id: "docs/how-to/manage-inventory-and-payouts.md"
dsom_governance:
  domain: "Infrastructure"
  context_tier: "L2-Operational"
tags:
  - "dsom-protocol"
  - "how-to"
  - "operations"
related_links:
  - "docs/how-to/index.md"
  - "docs/reference/file-structure-and-api.md"
nav_order: 1
layout: "default"
---

# How-To Guide: Managing Inventory, Live Sessions, and Payouts

This guide provides step-by-step procedural directions for routine operations in Omni-View.

---

## 📦 How to Manage Product Inventory

### Adding a New Product Item

1. Navigate to **Product Management** (`http://localhost:8000/Web Ui/product.html`).
2. Click **Add Product**.
3. Fill in product details:
   - **Title**: `Premium Wireless Headset`
   - **Category**: `Electronics`
   - **Stock**: `150`
   - **Price**: `299.00`
4. Click **Save Product**.

---

## 🎥 How to Track Live Stream Performance

1. Navigate to **Live Sessions** (`http://localhost:8000/Web Ui/lives.html`).
2. Record session details upon stream completion:
   - **Host User**: Select employee ID/name.
   - **GMV Generated**: Enter total sales revenue.
   - **Units Sold**: Enter total quantity.
3. Save record to update the live stream leaderboard.

---

## 💰 How to Process Employee Payouts

1. Navigate to **Payout Management** (`http://localhost:8000/Web Ui/payout.html`).
2. Click **Create Payout**.
3. Select Employee, enter payout amount and payout date.
4. Set status to `Pending` or `Completed` and save.
