# Onboarding Standard & Operational Index

> "Engineers and autonomous AI agents do not need to ingest this entire repository to begin contributing effectively. In fact, doing so degrades performance and focus. The optimal path to mastery is immediate execution of small, deterministic, high-impact tasks."
> — *Adapted from the Diátaxis Foundational Principle*

---

## 1. Epigraph & Onboarding Philosophy

This document serves as the primary operational entry point for the **Omni-View Business Command Centre** repository. It implements a dual-interface architecture engineered to satisfy two distinct operational paradigms:

1. **Human Operator Readability:** Providing clear, unambiguous navigation pathways for rapid bootstrapping, local development, code review, and collaborative contribution workflows.
2. **Autonomous Agent Determinism:** Providing strict, machine-parseable contextual anchors, API/CLI invocation patterns, and structural constraints for autonomous Large Language Model (LLM) agent runtimes (such as Jules, Google Antigravity, and CI/CD sub-agents).

Both human engineers and autonomous agents must adhere to the principle of **Minimal Sufficient Context**: do not ingest unneeded repository artefacts upfront. Identify the task, isolate the relevant subsystem, execute the minimal viable operation, and verify results against test suites.

---

## 2. Dual-Audience Entry Matrix (Diátaxis Navigation Grid)

The repository documentation is structured according to the Diátaxis framework across four distinct functional quadrants. Use the matrix below to route your execution path based on entity type and task requirements.

| Quadrant | Purpose | Human Pathway | Autonomous Agent Pathway |
| :--- | :--- | :--- | :--- |
| **Tutorials** | Learning-oriented onboarding & initial platform setup | Read [`docs/tutorials/getting-started.md`](docs/tutorials/getting-started.md) for step-by-step UI login and dashboard navigation. | Parse `docs/tutorials/getting-started.md` for user roles (`administrator`, `employee`), login entry points, and baseline user flows. |
| **How-To Guides** | Problem-oriented practical procedures for target workflows | Consult [`docs/how-to/manage-inventory-and-payouts.md`](docs/how-to/manage-inventory-and-payouts.md) for operational inventory and payout tasks. | Extract discrete procedural steps and DOM manipulation dependencies for automated integration tests. |
| **Reference** | Information-oriented factual specifications and schemas | Inspect [`docs/reference/file-structure-and-api.md`](docs/reference/file-structure-and-api.md) for file maps, database schemas, and JS modules. | Query file location indexes, API schemas, Supabase table definitions, and CSS module bindings. |
| **Explanation** | Concept-oriented architectural background and rationale | Review [`docs/explanation/architecture-and-diataxis.md`](docs/explanation/architecture-and-diataxis.md) for design decisions and security models. | Anchor operational boundaries against Role-Based Access Control (RBAC) rules and decoupled architecture constraints. |

---

## 3. Immediate Action: The Smallest Viable Task

### 3.1. Human Pathway (3-Step Quickstart)

To establish a verified local workspace, execute the following command chain:

1. **Environment Initialization:**
   Ensure Python 3.12+ and `uv` are installed. Synchronise the virtual environment:

   ```bash
   uv sync
   ```

2. **Repository Integrity Validation:**
   Run the test suite to confirm all structural, HTML, JS, and CSS assertions pass:

   ```bash
   uv run pytest
   ```

3. **Local Application Execution:**
   Serve the application locally via HTTP or open `index.html` in a web browser (which automatically routes to `Web Ui/login.html`):

   ```bash
   python3 -m http.server 8000 --directory .
   ```

---

## 3.2. Agent Pathway (Standardised Task Ingestion Protocol)

Autonomous agents MUST execute the following four-phase ingestion protocol prior to modifying code:

```text
+-------------------+     +---------------------+     +--------------------+     +--------------------+
| 1. State Parsing  | --> | 2. Context Isolation| --> | 3. Deterministic   | --> | 4. Structured Diff |
| (Repo Discovery)  |     | (Target Subsystem)  |     |    Verification    |     |    Submission      |
+-------------------+     +---------------------+     +--------------------+     +--------------------+
```

1. **State Parsing:**
   - Execute directory listing (`list_files`) to index existing modules in `Web Ui/`, `js/`, `css/`, `docs/`, and `tests/`.
   - Read `pyproject.toml` and `README.md` to establish project metadata and dependency constraints.

2. **Context Isolation:**
   - Locate relevant specifications in `docs/reference/file-structure-and-api.md`.
   - Read ONLY the target source files and matching tests associated with the assigned task. Avoid reading unreferenced binary or large asset files.

3. **Deterministic Verification:**
   - Run localized or full test suites via CLI (`uv run pytest`).
   - Confirm zero regression on structural and schema validation assertions.

4. **Structured Diff Submission:**
   - Format proposed code modifications using standard Git merge diff blocks or unified patches.
   - Run verification checks prior to finalizing commits.

---

## 4. Agent Context Governance (DSOM & OKF Integration)

To optimize context window usage and prevent hallucination, agent runtimes must adhere to **Domain-Specific Operational Model (DSOM)** and **Ontological Knowledge Frame (OKF)** guidelines.

### 4.1. Context Window Boundaries

- **Strict Scope Isolation:** Agents must read only files directly pertinent to the task ticket. Do NOT load full repository snapshots into memory.
- **Reference Anchoring:** Use `docs/reference/file-structure-and-api.md` as the canonical source of truth for file paths and backend integration schemas.
- **No Direct Artifact Editing:** Never modify generated build outputs or external vendor scripts directly. Always modify source code in `js/`, `css/`, or `Web Ui/`.

### 4.2. Multi-Agent Interoperability (Jules, Google Antigravity, & CI/CD Pipelines)

- **Shared State via Version Control:** Communication between agents (e.g. Jules performing feature implementation and Google Antigravity/CI agents performing automated verification) must occur deterministically through Git commits, standard branch names, and PR review comments.
- **Machine-Parseable Output Standards:** Agent execution output, test results, and status updates must follow standard Markdown structures or JSON payloads where applicable.
- **Automated Verification Contract:** Any pull request generated by an agent must pass `uv run pytest` cleanly in CI/CD pipelines before merge approval.
