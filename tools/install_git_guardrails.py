#!/usr/bin/env python3
"""
tools/install_git_guardrails.py

Installs git pre-commit hook to auto-run summary generation and documentation index updates
before commits. Preserves existing hooks by creating a backup if present.
"""

import os
import stat
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT_HOOKS_DIR = os.path.join(ROOT_DIR, '.git', 'hooks')

HOOK_CONTENT = """#!/bin/sh
# Git pre-commit hook for automated documentation summary and index generator
set -eu

echo "Running pre-commit documentation summary and index generator..."
python3 tools/generate_summary.py
python3 parse_llms_txt.py --generate-all

git add SUMMARY.md docs/SUMMARY.md llms.txt llms-full.txt sitemap.txt sitemap.xml docs/llms.txt docs/llms-full.txt docs/sitemap.txt docs/sitemap.xml llm_context.xml
"""


def install_guardrails():
    """Install the repository pre-commit hook that regenerates documentation files.
    
    If the Git hooks directory is unavailable, installation is skipped. An existing
    hook is backed up before being replaced when it does not already contain the
    documentation summary generator.
    """
    if not os.path.isdir(GIT_HOOKS_DIR):
        print(f"Git hooks directory {GIT_HOOKS_DIR} not found. Skipping hook installation.")
        return

    pre_commit_path = os.path.join(GIT_HOOKS_DIR, 'pre-commit')

    if os.path.exists(pre_commit_path):
        with open(pre_commit_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        if "tools/generate_summary.py" not in existing_content:
            backup_path = f"{pre_commit_path}.bak"
            shutil.copy2(pre_commit_path, backup_path)
            print(f"Existing pre-commit hook backed up to {backup_path}")

    with open(pre_commit_path, 'w', encoding='utf-8') as f:
        f.write(HOOK_CONTENT)

    # Make executable
    st = os.stat(pre_commit_path)
    os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)
    print(f"Pre-commit guardrail installed successfully at {pre_commit_path}")


if __name__ == '__main__':
    install_guardrails()
