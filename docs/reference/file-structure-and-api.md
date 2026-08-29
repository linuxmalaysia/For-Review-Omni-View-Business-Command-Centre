---
title: "Technical Reference: File Structure, Architecture & Schema"
description: "Factual specification of files, HTML UI views, JavaScript modules, CSS stylesheets, and Supabase database schema."
nav_order: 1
layout: default
---

# Technical Reference: File Structure, Architecture & Database Schema

This document provides factual specifications for repository organization, JavaScript modules, CSS stylesheets, and Supabase integration.

---

## 📂 Directory Map

```text
.
├── index.html                   # Redirect entry point to login page
├── parse_llms_txt.py            # LLM text parser, XML generator, and sitemap builder
├── llms.txt                     # Standard LLM discovery index file
├── llms-full.txt                # Consolidated markdown documentation file
├── sitemap.txt                  # Plaintext documentation URL sitemap
├── sitemap.xml                  # Standard XML sitemap
├── START-HERE.md                # Dual-audience onboarding specification
├── README.md                    # Primary project landing page
├── docs/                        # Diátaxis documentation system
│   ├── README.md                # Documentation hub home page
│   ├── SUMMARY.md               # GitBook table of contents
│   ├── tutorials/               # Guided learning lessons
│   ├── how-to/                  # Practical operational guides
│   ├── reference/               # Factual technical specifications
│   └── explanation/             # Design rationale and background
├── Web Ui/                      # HTML5 interface views
│   ├── login.html               # Authentication login view
│   ├── main.html                # Administrator command dashboard
│   ├── Employee_Main.html       # Staff member dashboard
│   ├── product.html             # Inventory CRUD interface
│   ├── lives.html               # Admin live session tracker
│   ├── Employee_Lives.html      # Staff live session tracker
│   ├── payout.html              # Payout processing interface
│   ├── Employee_Payout.html     # Staff payout view
│   ├── report.html              # Analytics & PDF export view
│   ├── user_management.html     # User administration view
│   ├── edit_profile.html        # Admin profile editor
│   ├── Employee_edit_profile.html # Staff profile editor
│   ├── profile.html             # Profile details view
│   ├── employee_profile.html    # Staff profile details view
│   ├── forgot-password.html     # Password recovery view
│   └── reset_password.html      # Password reset view
├── js/                          # Client-side JavaScript modules
│   ├── database.js              # Supabase client initialization
│   ├── admin_authcheck.js       # Admin session RBAC guard
│   ├── authcheck.js             # General session guard
│   ├── dashboard.js             # Admin dashboard data loader
│   ├── eployee_dashboard.js     # Employee dashboard data loader
│   ├── eployee_charts.js        # Analytics chart renderer
│   ├── editprofile.js           # Profile update handler
│   ├── employee_leaderboard.js  # Live session leaderboard logic
│   ├── live.js                  # Live streaming session CRUD
│   ├── load_employee_live.js    # Staff live streaming view loader
│   ├── load_employee_payout.js  # Staff payout view loader
│   ├── loaddata.js              # Shared DOM data utilities
│   ├── login.js                 # Authentication handler
│   ├── logout.js                # Session teardown handler
│   ├── manage_user.js           # User administration logic
│   ├── payout.js                # Payout creation logic
│   ├── print_PDF_report.js      # PDF report exporter
│   ├── product.js               # Product CRUD logic
│   ├── report.js                # Report analytics engine
│   └── reset_password.js        # Password reset engine
└── css/                         # Application CSS stylesheets
    ├── main.css                 # Global system styling
    ├── login.css                # Authentication view styling
    ├── edit_profile.css         # Profile view styling
    ├── forget.css               # Password recovery styling
    ├── leader_board.css         # Leaderboard component styling
    ├── profile.css              # Profile view styling
    ├── reset_password.css       # Password reset styling
    └── view-transitions.css     # Navigation transitions styling
```

---

## ⚡ Supabase Database Schema

Client configuration initialized in `js/database.js`.

### Table Specifications

1. **`profiles`**: User account credentials and roles.
   - `id` (uuid, primary key)
   - `username` (text)
   - `email` (text)
   - `role` (text: `administrator`, `employee`, `owner`)

2. **`products`**: Inventory items catalog.
   - `id` (uuid, primary key)
   - `title` (text)
   - `category` (text)
   - `stock` (integer)
   - `price` (numeric)

3. **`lives`**: Live stream session records.
   - `id` (uuid, primary key)
   - `user_id` (uuid, foreign key -> profiles.id)
   - `gmv` (numeric)
   - `units_sold` (integer)
   - `session_date` (timestamp)

4. **`payouts`**: Employee compensation records.
   - `id` (uuid, primary key)
   - `employee_id` (uuid, foreign key -> profiles.id)
   - `amount` (numeric)
   - `payout_date` (date)
   - `status` (text: `Completed`, `Pending`)
