import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def test_github_pages_workflow_uses_safe_pinned_deployment_action():
    workflow = _read(".github/workflows/jekyll-gh-pages.yml")

    deploy_ref = re.search(r"uses:\s*actions/deploy-pages@([^\s]+)", workflow)
    assert deploy_ref, "The workflow must deploy with actions/deploy-pages"
    assert re.fullmatch(r"[0-9a-f]{40}", deploy_ref.group(1)), (
        "The deployment action must be pinned to an immutable commit SHA"
    )
    assert "pages: write" in workflow
    assert "id-token: write" in workflow
    assert "cancel-in-progress: false" in workflow


def test_jekyll_config_targets_the_repository_pages_subpath():
    config = _read("_config.yml")

    assert 'url: "https://linuxmalaysia.github.io"' in config
    assert 'baseurl: "/For-Review-Omni-View-Business-Command-Centre"' in config
    assert "  - docs" in config
    assert "  - assets" in config
    assert "  - tests" in config


def test_read_the_docs_configuration_points_to_sphinx_dependencies():
    read_the_docs = _read(".readthedocs.yaml")
    sphinx_config = _read("docs/conf.py")
    requirements = _read("docs/requirements.txt")

    assert "configuration: docs/conf.py" in read_the_docs
    assert "requirements: docs/requirements.txt" in read_the_docs
    assert "master_doc = 'SUMMARY'" in sphinx_config
    assert "'myst_parser'" in sphinx_config
    assert "html_theme = 'sphinx_rtd_theme'" in sphinx_config
    assert "myst-parser" in requirements
    assert "sphinx-rtd-theme" in requirements


def test_gitbook_uses_docs_navigation_files():
    config = _read(".gitbook.yaml")

    assert re.search(r"(?m)^root:\s*\./docs\s*$", config)
    assert re.search(r"(?m)^\s+summary:\s*SUMMARY\.md\s*$", config)
    assert re.search(r"(?m)^\s+readme:\s*README\.md\s*$", config)


def test_alternate_hosts_publish_generated_static_content():
    gitlab = _read(".gitlab-ci.yml")
    render = _read("render.yaml")

    assert "jekyll build -d public" in gitlab
    assert re.search(r"(?m)^\s+- main\s*$", gitlab)
    assert "buildCommand: python3 parse_llms_txt.py --generate-all" in render
    assert "staticPublishPath: ./" in render
