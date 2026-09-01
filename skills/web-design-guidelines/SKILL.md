---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below. If WebFetch cannot reach the source URL, fall back to the local reference guidelines in `docs/explanation/web-interface-improvements.md`.
2. Read the specified files (or prompt user for files/pattern, or automatically identify modified interface files).
3. Check against all rules in the fetched or fallback guidelines.
4. Output findings in the terse `file:line` format.

## Guidelines Source

Fetch fresh guidelines before each review:

```text
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. When fetching, use a reviewed immutable commit reference when required, and authenticate/verify the fetched content against expected checksum before applying rules. If WebFetch fails or environment is offline, fall back to `docs/explanation/web-interface-improvements.md`.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above (or local fallback).
2. Read the specified files.
3. Apply all rules from the guidelines.
4. Output findings using the format specified in the guidelines.

If no files specified, prompt the user for files/pattern or automatically identify modified interface files.
