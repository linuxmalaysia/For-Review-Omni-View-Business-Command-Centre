---
title: "How-To: Manage Inventory, Live Sessions, and Payouts"
description: "Practical operational guide for stock management, live streaming sales tracking, and staff payouts."
nav_order: 1
layout: default
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

### Updating Product Stock Quantity

1. Locate item in product inventory table.
2. Click **Edit** action button.
3. Update stock field to target quantity (e.g., `200`).
4. Click **Update Stock**.

---

## 🎥 How to Track Live Sales Sessions

1. Navigate to **Lives** (`/Web Ui/lives.html` for Admin, `/Web Ui/Employee_Lives.html` for Staff).
2. Input live streaming operational parameters:
   - **Host Staff**: Select host user from dropdown.
   - **Duration**: Input start time (`10:00 AM`) and end time (`12:00 PM`).
   - **GMV**: Input total session gross revenue (e.g., `4500.00`).
   - **Units Sold**: Input units sold (e.g., `85`).
3. Click **Submit Live Record**.

---

## 💰 How to Process Employee Payouts

1. Navigate to **Payout** (`/Web Ui/payout.html`).
2. Select target employee account from user list.
3. Enter payout total amount (`1250.00`) and payout date (`2025-03-01`).
4. Set payout status to `Completed`.
5. Click **Record Payout**.

---

## 📄 How to Print Business Analytics Reports

1. Navigate to **Report** (`/Web Ui/report.html`).
2. Select reporting date range (`2025-01-01` to `2025-03-01`).
3. Click **Generate Report**.
4. Click **Print PDF Report** to export formatted PDF document.
