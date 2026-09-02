import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from packaging.requirements import Requirement
from packaging.version import Version

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.9/3.10
    import tomli as tomllib


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


def read_toml(relative_path: Union[str, Path]) -> dict:
    with (ROOT_DIR / relative_path).open("rb") as toml_file:
        return tomllib.load(toml_file)


def uvicorn_requirement() -> Requirement:
    dependencies = read_toml("pyproject.toml")["project"]["dependencies"]
    requirements = [
        Requirement(dependency)
        for dependency in dependencies
        if Requirement(dependency).name.lower() == "uvicorn"
    ]
    assert len(requirements) == 1, "uvicorn must be declared exactly once"
    return requirements[0]


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
    requirement = uvicorn_requirement()

    assert str(requirement.specifier) == ">=0.30.0"
    assert not requirement.extras
    assert requirement.marker is None
    assert requirement.url is None


def test_uvicorn_minimum_version_boundary_is_enforced():
    specifier = uvicorn_requirement().specifier

    assert Version("0.30.0") in specifier
    assert Version("0.29.999") not in specifier


def test_uvicorn_lock_entries_match_the_project_requirement():
    lock = read_toml("uv.lock")
    project = read_toml("pyproject.toml")["project"]
    project_package = next(
        package for package in lock["package"] if package["name"] == project["name"]
    )
    requirement = uvicorn_requirement()

    assert lock["requires-python"] == project["requires-python"]
    assert project_package["metadata"]["requires-dist"] == [
        {"name": "uvicorn", "specifier": str(requirement.specifier)}
    ]

    locked_uvicorn = {
        (package["version"], package["source"]["registry"])
        for package in lock["package"]
        if package["name"] == "uvicorn"
    }
    root_uvicorn = [
        dependency
        for dependency in project_package["dependencies"]
        if dependency["name"] == "uvicorn"
    ]

    assert root_uvicorn, "The root package must resolve uvicorn as a runtime dependency"
    assert all(
        (dependency["version"], dependency["source"]["registry"])
        in locked_uvicorn
        for dependency in root_uvicorn
    )
    assert all(
        Version(version) in requirement.specifier for version, _ in locked_uvicorn
    )


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
    guide_reference = "deploy-omni-view-on-render.md"

    assert root_full == docs_full
    assert guide_reference in root_full
    assert guide_reference in xml_text
