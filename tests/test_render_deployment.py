import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

import parse_llms_txt


ROOT_DIR = Path(__file__).resolve().parents[1]
GUIDE_PATH = Path("docs/how-to/deploy-omni-view-on-render.md")
GUIDE_TITLE = "Deploying Omni-View Business Command Centre on Render.com"


def read_repo_file(relative_path: Union[str, Path]) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def render_service_fields() -> dict[str, str]:
    """Read scalar fields from the single service in the small Render Blueprint."""
    contents = read_repo_file("render.yaml")
    services = re.findall(r"(?m)^  - type:\s*(\S+)\s*$", contents)
    assert len(services) == 1, "Render Blueprint must define exactly one service"

    fields = {"type": services[0]}
    for key, value in re.findall(r"(?m)^    ([A-Za-z][A-Za-z0-9]*):\s*([^\n]+)$", contents):
        fields[key] = value.strip()
    return fields


def markdown_links(contents: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^]]+)]\(([^)]+)\)", contents)


def render_troubleshooting_section() -> str:
    guide = read_repo_file(GUIDE_PATH)
    match = re.search(
        r"(?ms)^### 1\. Error:.*?(?=^### 2\.)",
        guide,
    )
    assert match is not None, "Render guide is missing its first troubleshooting entry"
    return match.group(0)


def test_render_blueprint_defines_the_static_site_build_contract():
    fields = render_service_fields()

    assert fields["type"] == "static"
    assert fields["name"] == "omni-view-command-centre"
    assert fields["buildCommand"] == "python3 parse_llms_txt.py --generate-all"
    assert fields["staticPublishPath"] in {".", "./"}


def test_render_blueprint_does_not_regress_to_a_web_service():
    """A static site must not acquire runtime/start fields that invoke uvicorn."""
    fields = render_service_fields()

    assert {"env", "runtime", "startCommand"}.isdisjoint(fields)
    assert "uvicorn" not in read_repo_file("render.yaml").lower()


def test_uvicorn_dependency_is_declared_in_pyproject():
    import tomllib
    pyproject_data = tomllib.loads(read_repo_file("pyproject.toml"))
    dependencies = pyproject_data.get("project", {}).get("dependencies", [])
    assert any("uvicorn>=0.30.0" in dep for dep in dependencies)


def test_render_blueprint_configures_cache_control_for_all_routes():
    contents = read_repo_file("render.yaml")
    header = re.search(
        r"(?ms)^    headers:\s*$\n"
        r"\s+- path:\s*(?P<path>\S+)\s*$\n"
        r"\s+name:\s*(?P<name>[^\n]+)\s*$\n"
        r"\s+value:\s*(?P<value>[^\n]+)\s*$",
        contents,
    )

    assert header is not None, "Render Blueprint is missing its cache header"
    assert header.groupdict() == {
        "path": "/*",
        "name": "Cache-Control",
        "value": "max-age=3600",
    }


def test_render_guide_matches_the_blueprint_and_documents_failure_recovery():
    guide = read_repo_file(GUIDE_PATH)
    fields = render_service_fields()

    assert f'**Build Command:** `{fields["buildCommand"]}`' in guide
    assert f'**Publish Directory:** `{fields["staticPublishPath"]}`' in guide
    assert "**Service Type:** `Static Site`" in guide
    assert "uvicorn: command not found" in guide
    assert "Exit Status 127" in guide
    assert "Web Service" in guide
    assert "Static Site" in guide


def test_render_guide_maps_each_web_service_failure_to_its_exit_status():
    section = render_troubleshooting_section()
    logs = re.findall(r"(?ms)^  ```text\n(.*?)^  ```", section)

    assert len(logs) == 2
    expected_failures = [
        ("ModuleNotFoundError: No module named 'src'", "Exited with status 1"),
        ("uvicorn: command not found", "Exited with status 127"),
    ]
    start_command = (
        "uvicorn src.dca_service.web_app:app --host 0.0.0.0 --port $PORT"
    )

    for log, (failure, status) in zip(logs, expected_failures):
        assert start_command in log
        assert failure in log
        assert status in log


def test_render_guide_explains_the_root_cause_and_complete_recovery():
    section = render_troubleshooting_section()

    assert "misconfigured as a **Web Service** (Python runtime)" in section
    assert "rather than a **Static Site**" in section
    assert "does not contain a `src` Python package or backend web server" in section
    assert not (ROOT_DIR / "src").exists(), "The guide's no-backend diagnosis is stale"

    recovery_steps = re.findall(r"(?m)^  \d+\. (.+)$", section)
    assert len(recovery_steps) == 3
    assert "change the service or delete it" in recovery_steps[0]
    assert "`render.yaml` with `type: static`" in recovery_steps[1]
    assert "Clear any leftover Start Command input" in recovery_steps[2]


def test_render_guide_has_deployment_specific_okf_metadata():
    guide = read_repo_file(GUIDE_PATH)
    frontmatter = guide.split("---", 2)[1]

    assert 'type: "howto"' in frontmatter
    assert 'title: "Deploying Omni-View Business Command Centre on Render.com"' in frontmatter
    assert 'description: "Step-by-step' in frontmatter
    assert 'resource: "file:///docs/how-to/deploy-omni-view-on-render.md"' in frontmatter
    for topic in ("render-com", "deployment", "static-site", "python-runtime"):
        assert f'"{topic}"' in frontmatter


def test_render_guide_is_linked_from_both_navigation_roots():
    expected_links = {
        "SUMMARY.md": GUIDE_PATH.as_posix(),
        "docs/SUMMARY.md": "how-to/deploy-omni-view-on-render.md",
    }

    for summary_path, expected_target in expected_links.items():
        links = markdown_links(read_repo_file(summary_path))
        matching_targets = [target for title, target in links if title == GUIDE_TITLE]
        assert matching_targets == [expected_target]

        resolved_target = (ROOT_DIR / Path(summary_path).parent / expected_target).resolve()
        assert resolved_target == (ROOT_DIR / GUIDE_PATH).resolve()
        assert resolved_target.is_file()


def test_render_guide_is_present_in_generated_context_artifacts():
    root_full = read_repo_file("llms-full.txt")
    docs_full = read_repo_file("docs/llms-full.txt")
    xml_root = ET.fromstring(read_repo_file("llm_context.xml"))
    xml_text = "".join(xml_root.itertext())
    expected_full = parse_llms_txt.generate_llms_full(root_dir=str(ROOT_DIR))
    parsed_index = parse_llms_txt.parse_llms_txt(str(ROOT_DIR / "llms.txt"))
    expected_xml = ET.fromstring(
        parse_llms_txt.generate_xml_context(parsed_index, root_dir=str(ROOT_DIR))
    )

    assert root_full == docs_full == expected_full
    assert ET.tostring(xml_root) == ET.tostring(expected_xml)
    for failure in (
        "ModuleNotFoundError: No module named 'src'",
        "uvicorn: command not found",
    ):
        assert failure in root_full
        assert failure in xml_text
