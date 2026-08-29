# Architectural Explanation & Diátaxis Framework Adoption

This document details the software architecture, design decisions, and adoption of the **Diátaxis Documentation Framework** for the Omni-View project.

---

## 🏛 Architecture Overview

Omni-View Business Command Centre is built using a modern decoupled web architecture:

1. **Frontend Layer**:
   - Built with HTML5, CSS3, JavaScript (ES6+), and Bootstrap 5.
   - Responsive layout designed for operational efficiency across devices.
   - Dynamic UI charts powered by Chart.js.

2. **Backend & Database Layer**:
   - Built on Supabase (PostgreSQL engine).
   - Real-time queries and authentication managed directly through standard REST APIs via `supabase-js`.

3. **Role-Based Access Control (RBAC)**:
   - System distinguishes between `administrator`, `employee`, and `owner` roles.
   - Client-side navigation script guards (`admin_authcheck.js`, `authcheck.js`) check user sessions to provide seamless page redirects and UI navigation control.
   - Data security and API authorization for direct Supabase requests are strictly enforced server-side via Supabase Row Level Security (RLS) policies and PostgreSQL database rules for administrator, employee, and owner roles.

---

## 📖 Diátaxis Framework Adoption

Documentation in complex business systems often mixes practical tutorials with technical API details and high-level architectural explanations. This creates confusion and inflates cognitive load for both human developers and AI coding agents.

To solve this, Omni-View adopts the **Diátaxis Documentation Framework** (https://diataxis.fr/), structuring documentation into four distinct quadrants based on user intent and intent type:

```
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

### Quadrants Structure in Omni-View:

1. **Tutorials (`docs/tutorials/`)**:
   - **Focus**: Learning-oriented, step-by-step onboarding for new users and developers.
   - **Example**: `getting-started.md`

2. **How-To Guides (`docs/how-to/`)**:
   - **Focus**: Problem-oriented practical guides to complete specific tasks.
   - **Example**: `manage-inventory-and-payouts.md`

3. **Reference (`docs/reference/`)**:
   - **Focus**: Information-oriented, factual description of code, file layout, and API schema.
   - **Example**: `file-structure-and-api.md`

4. **Explanation (`docs/explanation/`)**:
   - **Focus**: Concept-oriented architectural discussions and design rationale.
   - **Example**: `architecture-and-diataxis.md`
