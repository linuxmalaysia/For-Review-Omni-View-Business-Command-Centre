import os
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_yaml_frontmatter(content: str) -> dict:
    """
    Parses simple YAML frontmatter bounded by opening and closing '---' delimiters.
    """
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    frontmatter_raw = parts[1].strip()
    metadata = {}
    for line in frontmatter_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")

    return metadata


def test_diataxis_directories_exist():
    docs_dir = os.path.join(ROOT_DIR, 'docs')
    assert os.path.isdir(docs_dir), "docs/ directory does not exist"

    expected_subdirs = ['tutorials', 'how-to', 'reference', 'explanation']
    for subdir in expected_subdirs:
        subdir_path = os.path.join(docs_dir, subdir)
        assert os.path.isdir(subdir_path), f"Diataxis directory docs/{subdir} missing"


def test_diataxis_documents_exist():
    expected_files = [
        os.path.join(ROOT_DIR, 'docs', 'tutorials', 'getting-started.md'),
        os.path.join(ROOT_DIR, 'docs', 'tutorials', 'llms-txt-setup.md'),
        os.path.join(ROOT_DIR, 'docs', 'how-to', 'manage-inventory-and-payouts.md'),
        os.path.join(ROOT_DIR, 'docs', 'how-to', 'generate-llms-context.md'),
        os.path.join(ROOT_DIR, 'docs', 'reference', 'file-structure-and-api.md'),
        os.path.join(ROOT_DIR, 'docs', 'reference', 'cli-and-tools.md'),
        os.path.join(ROOT_DIR, 'docs', 'explanation', 'architecture-and-diataxis.md'),
        os.path.join(ROOT_DIR, 'docs', 'explanation', 'okf-02-and-diataxis.md'),
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected documentation file missing: {filepath}"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        assert len(content.strip()) > 100, f"Documentation file {filepath} content is too short"

        metadata = parse_yaml_frontmatter(content)
        assert "title" in metadata, f"Documentation file {filepath} missing parsed title in frontmatter"
        assert len(metadata["title"]) > 0, f"Documentation file {filepath} has empty title in frontmatter"


def test_summary_and_navigation_files():
    """Verify that the documentation summary file exists and links to all Diátaxis sections."""
    summary_path = os.path.join(ROOT_DIR, 'docs', 'SUMMARY.md')
    assert os.path.isfile(summary_path), "docs/SUMMARY.md missing"
    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "# Summary" in content

    # Extract actual Markdown links [label](target)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    assert len(links) > 0, "docs/SUMMARY.md contains no Markdown links"

    docs_root = os.path.join(ROOT_DIR, 'docs')
    for label, target in links:
        # Ignore external URLs or anchors
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue

        target_path = os.path.normpath(os.path.join(docs_root, target))
        assert os.path.isfile(target_path), f"SUMMARY.md link [{label}]({target}) resolves to missing file: {target_path}"


def test_llm_index_files_exist():
    """
    Verify that required LLM index and sitemap files exist at the repository root and in the documentation directory.
    """
    required_index_files = [
        'llms.txt', 'llms-full.txt', 'sitemap.txt', 'sitemap.xml',
        os.path.join('docs', 'llms.txt'),
        os.path.join('docs', 'llms-full.txt'),
        os.path.join('docs', 'sitemap.txt'),
        os.path.join('docs', 'sitemap.xml'),
    ]
    for filename in required_index_files:
        filepath = os.path.join(ROOT_DIR, filename)
        assert os.path.isfile(filepath), f"Required index file {filename} missing"


def test_start_here_document_exists():
    start_here_path = os.path.join(ROOT_DIR, 'START-HERE.md')
    assert os.path.isfile(start_here_path), "START-HERE.md missing at root"
    with open(start_here_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert len(content.strip()) > 500, "START-HERE.md content is too short"
    assert "Epigraph & Onboarding Philosophy" in content
    assert "Dual-Audience Entry Matrix" in content
    assert "Immediate Action" in content
    assert "Agent Context Governance" in content


def test_readme_references_diataxis():
    readme_path = os.path.join(ROOT_DIR, 'README.md')
    assert os.path.isfile(readme_path)
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'Diátaxis' in content or 'diataxis' in content
    assert 'tutorials' in content.lower()
    assert 'how-to' in content.lower()
    assert 'reference' in content.lower()
    assert 'explanation' in content.lower()


def test_all_repository_files_accounted_for():
    # Enumerate all key directories and verify non-empty files
    for folder in ['Web Ui', 'js', 'css', 'proposal']:
        dir_path = os.path.join(ROOT_DIR, folder)
        assert os.path.isdir(dir_path), f"Required directory {folder} missing"

        entries = os.listdir(dir_path)
        regular_files = [f for f in entries if os.path.isfile(os.path.join(dir_path, f))]
        assert len(regular_files) > 0, f"Directory {folder} contains no regular files"
