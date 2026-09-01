import re
import runpy
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def read_repo_file(relative_path: str) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def yaml_list(contents: str, key: str) -> list[str]:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*\n((?:^[ \t]+- .*(?:\n|$))+)", contents)
    assert match is not None, f"Missing YAML list: {key}"
    return [line.split("-", 1)[1].strip() for line in match.group(1).splitlines()]


def test_documentation_hub_has_frontmatter_and_resolvable_navigation():
    contents = read_repo_file("docs/index.md")
    frontmatter = contents.split("---", 2)[1]

    assert "layout: default" in frontmatter
    assert "title:" in frontmatter
    assert "description:" in frontmatter

    links = re.findall(r"\[[^]]+\]\(([^)]+)\)", contents)
    assert links, "Documentation hub should provide navigation links"
    for target in links:
        if target.startswith(("http://", "https://", "#")):
            continue
        assert (ROOT_DIR / "docs" / target).resolve().is_file(), (
            f"Documentation hub link points to a missing file: {target}"
        )

    expected_quadrants = {"tutorials", "how-to", "reference", "explanation"}
    linked_quadrants = {Path(target).parts[0] for target in links}
    assert expected_quadrants <= linked_quadrants


def test_jekyll_build_uses_docs_hub_without_overwriting_application_index():
    config = read_repo_file("_config.yml")
    workflow = read_repo_file(".github/workflows/jekyll-gh-pages.yml")

    assert "docs" in yaml_list(config, "include")
    assert "index.html" in yaml_list(config, "exclude")
    assert "index.html" not in yaml_list(config, "include")
    assert (ROOT_DIR / "index.html").is_file(), "Application redirect entry point must remain"

    build_step = re.search(
        r"(?ms)^\s+- name: Build with Jekyll\s*$\n(?P<body>.*?)(?=^\s+- name:|\Z)",
        workflow,
    )
    assert build_step is not None, "GitHub Pages workflow is missing its Jekyll build step"
    assert re.search(r"(?m)^\s+source:\s*\./docs\s*$", build_step.group("body"))
    assert not re.search(r"(?m)^\s+source:\s*\./\s*$", build_step.group("body"))


def test_default_layout_wires_shared_chrome_and_theme_assets():
    layout = read_repo_file("_layouts/default.html")

    for include in ("header.html", "sidebar.html", "footer.html"):
        assert f"{{% include {include} %}}" in layout
        assert (ROOT_DIR / "_includes" / include).is_file()
    assert "'/assets/css/style.css' | relative_url" in layout
    assert "'/assets/js/theme-toggle.js' | relative_url" in layout


def test_multi_platform_descriptors_reference_existing_documentation_inputs():
    gitbook = read_repo_file(".gitbook.yaml")
    assert "root: ./docs" in gitbook
    assert "summary: SUMMARY.md" in gitbook
    assert (ROOT_DIR / "docs" / "SUMMARY.md").is_file()
    assert (ROOT_DIR / "docs" / "README.md").is_file()

    readthedocs = read_repo_file(".readthedocs.yaml")
    assert "configuration: docs/conf.py" in readthedocs
    assert "requirements: docs/requirements.txt" in readthedocs
    assert (ROOT_DIR / "docs" / "conf.py").is_file()
    assert (ROOT_DIR / "docs" / "requirements.txt").is_file()


def test_sphinx_configuration_uses_markdown_summary_as_master_document():
    config = runpy.run_path(str(ROOT_DIR / "docs" / "conf.py"))

    assert config["master_doc"] == "SUMMARY"
    assert config["source_suffix"][".md"] == "markdown"
    assert "myst_parser" in config["extensions"]
    assert (ROOT_DIR / "docs" / f'{config["master_doc"]}.md').is_file()


def test_github_pages_deployment_action_is_pinned_to_a_commit():
    workflow = read_repo_file(".github/workflows/jekyll-gh-pages.yml")
    deployment_action = re.search(r"uses:\s*actions/deploy-pages@([^\s]+)", workflow)

    assert deployment_action is not None
    assert re.fullmatch(r"[0-9a-f]{40}", deployment_action.group(1))
