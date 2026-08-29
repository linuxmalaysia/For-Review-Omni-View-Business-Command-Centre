# Technical Reference: File Structure, Architecture & Schema

This reference document provides technical specifications for files, frontend components, JavaScript scripts, CSS stylesheets, and backend Supabase integration in Omni-View.

---

## 📂 Directory Structure

```text
.
├── index.html                   # Entry redirect page to login
├── README.md                    # Main project overview & Diátaxis navigation
├── docs/                        # Diátaxis documentation framework
│   ├── tutorials/               # Learning-oriented guides
│   ├── how-to/                  # Goal-oriented practical steps
│   ├── reference/               # Factual specifications
│   └── explanation/             # Architectural background & design decisions
├── Web Ui/                      # HTML views
│   ├── login.html               # Authentication login view
│   ├── main.html                # Administrator dashboard view
│   ├── Employee_Main.html       # Employee dashboard view
│   ├── product.html             # Product and inventory management
│   ├── lives.html               # Admin live session tracking
│   ├── Employee_Lives.html      # Employee live session tracking
│   ├── payout.html              # Payout management view
│   ├── Employee_Payout.html     # Employee payout view
│   ├── report.html              # Analytics & PDF report view
│   ├── user_management.html     # User administration view
│   ├── edit_profile.html        # Admin edit profile view
│   ├── Employee_edit_profile.html# Employee edit profile view
│   ├── profile.html             # User profile view
│   ├── employee_profile.html    # Employee profile view
│   ├── forgot-password.html     # Password recovery view
│   └── reset_password.html      # Password reset view
├── js/                          # Client-side JavaScript modules
│   ├── database.js              # Supabase client initialization & queries
│   ├── admin_authcheck.js       # Admin authentication guard
│   ├── authcheck.js             # General authentication guard
│   ├── dashboard.js             # Dashboard metrics & rendering logic
│   ├── eployee_dashboard.js     # Employee dashboard metrics & charts
│   ├── eployee_charts.js        # Employee analytics charts
│   ├── editprofile.js           # User profile updating
│   ├── employee_leaderboard.js  # Live session leaderboard logic
│   ├── live.js                  # Live session data handler
│   ├── load_employee_live.js    # Employee live session loader
│   ├── load_employee_payout.js  # Employee payout data loader
│   ├── loaddata.js              # Shared data loader utilities
│   ├── login.js                 # Authentication login logic
│   ├── logout.js                # Session teardown logic
│   ├── manage_user.js           # User administration CRUD
│   ├── payout.js                # Payout creation and list loader
│   ├── print_PDF_report.js      # PDF report renderer
│   ├── product.js               # Product management CRUD script
│   ├── report.js                # Analytics report calculator
│   └── reset_password.js        # Password reset handler
└── css/                         # System stylesheets
    ├── main.css                 # Primary system styling
    ├── login.css                # Authentication page styles
    ├── edit_profile.css         # Profile editor styles
    ├── forget.css               # Password recovery styles
    ├── leader_board.css         # Leaderboard component styles
    ├── profile.css              # Profile view styles
    ├── reset_password.css       # Password reset view styles
    └── view-transitions.css     # Navigation animation styles
```

---

## ⚡ Supabase Backend Integration

The application interacts with Supabase backend (`database.js`).

### Client Configuration

- **Supabase URL**: `https://uvmsvoyuzcwncwkghzml.supabase.co`
- **Key**: Configured in `js/database.js` using `supabaseClient`.

### Core Database Tables

- `profiles`: User IDs, roles (`administrator`, `employee`, `owner`), usernames, email addresses.
- `products`: Product ID, title, stock quantity, unit price, category.
- `lives`: Live streaming sales records, host user ID, GMV, items sold, views.
- `payouts`: Payout record ID, employee ID, amount, payout date, status.
