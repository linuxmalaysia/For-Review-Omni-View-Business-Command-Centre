import os
import re

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
        os.path.join(ROOT_DIR, 'docs', 'github-pages-setup.md'),
        os.path.join(ROOT_DIR, 'docs', 'multi-platform-hosting.md'),
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
        if target.startswith(("http://", "https://", "#")):
            continue

        target_path = os.path.normpath(os.path.join(docs_root, target))
        assert os.path.isfile(target_path), f"SUMMARY.md link [{label}]({target}) resolves to missing file: {target_path}"


def test_root_markdown_files_exist():
    """Verify that required root markdown files exist and have valid content."""
    root_md_files = ['README.md', 'CHANGELOG.md', 'HISTORY.md', 'SUMMARY.md', 'START-HERE.md']
    for filename in root_md_files:
        filepath = os.path.join(ROOT_DIR, filename)
        assert os.path.isfile(filepath), f"Root Markdown file {filename} missing"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        assert len(content.strip()) > 50, f"Root Markdown file {filename} content is too short"


def test_jekyll_config_and_layouts():
    """Verify Jekyll configuration and layout files exist."""
    config_path = os.path.join(ROOT_DIR, '_config.yml')
    assert os.path.isfile(config_path), "_config.yml missing at root"
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'title:' in content
    assert 'markdown:' in content

    layout_path = os.path.join(ROOT_DIR, '_layouts', 'default.html')
    assert os.path.isfile(layout_path), "_layouts/default.html missing"

    for partial in ['header.html', 'sidebar.html', 'footer.html']:
        partial_path = os.path.join(ROOT_DIR, '_includes', partial)
        assert os.path.isfile(partial_path), f"_includes/{partial} missing"


def test_multi_platform_descriptors():
    """Verify multi-platform configuration files exist."""
    platform_files = ['.gitlab-ci.yml', '.gitbook.yaml', '.readthedocs.yaml', 'render.yaml']
    for filename in platform_files:
        filepath = os.path.join(ROOT_DIR, filename)
        assert os.path.isfile(filepath), f"Multi-platform file {filename} missing"


def test_tools_scripts_exist():
    """Verify generator and guardrails tools exist."""
    tools = [
        os.path.join(ROOT_DIR, 'tools', 'generate_summary.py'),
        os.path.join(ROOT_DIR, 'tools', 'install_git_guardrails.py')
    ]
    for script_path in tools:
        assert os.path.isfile(script_path), f"Tool script {script_path} missing"


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


def test_okf_02_frontmatter_standard_across_all_md():
    """Verify that documentation and governance Markdown files conform to OKF 0.2 YAML frontmatter standards."""
    target_dirs = [
        os.path.join(ROOT_DIR, 'docs'),
        os.path.join(ROOT_DIR, '.agents')
    ]
    checked_files = 0
    for tdir in target_dirs:
        if not os.path.exists(tdir):
            continue
        for root, _, files in os.walk(tdir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    assert content.startswith("---"), f"OKF 0.2 compliance failure: File {filepath} does not open with line-based YAML frontmatter '---'"
                    metadata = parse_yaml_frontmatter(content)
                    assert "title" in metadata and len(metadata["title"]) > 0, f"OKF 0.2 compliance failure: File {filepath} missing non-empty 'title' in frontmatter"
                    assert "description" in metadata and len(metadata["description"]) > 0, f"OKF 0.2 compliance failure: File {filepath} missing non-empty 'description' in frontmatter"
                    assert "type" in metadata or "layout" in metadata, f"OKF 0.2 compliance failure: File {filepath} missing 'type' or 'layout' in frontmatter"
                    checked_files += 1

    assert checked_files >= 10, f"Expected at least 10 OKF-checked files across docs/ and .agents/, found {checked_files}"


def test_agents_and_brain_governance():
    """Verify that AGENTS.md, .agents/AGENTS.md, and .agents/brain/ structure exist with required rules."""
    root_agents = os.path.join(ROOT_DIR, 'AGENTS.md')
    agents_constitution = os.path.join(ROOT_DIR, '.agents', 'AGENTS.md')
    palace_registry = os.path.join(ROOT_DIR, '.agents', 'brain', 'palace_registry.md')
    sop_discovery = os.path.join(ROOT_DIR, 'docs', 'SOP-KNOWLEDGE-FIRST-DISCOVERY.md')

    assert os.path.isfile(root_agents), "Root AGENTS.md missing"
    assert os.path.isfile(agents_constitution), ".agents/AGENTS.md missing"
    assert os.path.isfile(palace_registry), ".agents/brain/palace_registry.md missing"
    assert os.path.isfile(sop_discovery), "docs/SOP-KNOWLEDGE-FIRST-DISCOVERY.md missing"

    with open(agents_constitution, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Local Knowledge-First & Metadata Discovery Mandate" in content
    assert "Sovereign Markdown Palace" in content

    with open(sop_discovery, 'r', encoding='utf-8') as f:
        sop_content = f.read()
    metadata = parse_yaml_frontmatter(sop_content)
    assert "title" in metadata, "SOP-KNOWLEDGE-FIRST-DISCOVERY.md missing frontmatter title"
    assert "SOP: Knowledge-First Discovery" in metadata["title"]


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
