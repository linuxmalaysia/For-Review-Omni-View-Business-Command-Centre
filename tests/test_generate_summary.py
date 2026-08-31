from pathlib import Path

import pytest

from tools import generate_summary


@pytest.mark.parametrize(
    ("content", "filename", "expected"),
    [
        ('---\ntitle: "Frontmatter title"\n---\n# Ignored\n', "page.md", "Frontmatter title"),
        ("---\ntitle: 'Single-quoted title'\n---\n", "page.md", "Single-quoted title"),
        ("Some introduction\n\n# First heading\n\n# Second heading\n", "page.md", "First heading"),
        ("No metadata or heading\n", "release-notes.md", "Release Notes"),
        ("---\ndescription: Missing closing delimiter\n", "plain-name.md", "Plain Name"),
    ],
)
def test_get_title_from_md_uses_supported_fallbacks(tmp_path, content, filename, expected):
    markdown_file = tmp_path / filename
    markdown_file.write_text(content, encoding="utf-8")

    assert generate_summary.get_title_from_md(str(markdown_file)) == expected


def _write_markdown(path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\ntitle: {title}\n---\n\nContent\n", encoding="utf-8")


def test_generate_summary_lines_discovers_groups_and_sorts_recursive_docs(tmp_path, monkeypatch):
    _write_markdown(tmp_path / "docs" / "tutorials" / "z-last.md", "Alpha by title")
    _write_markdown(tmp_path / "docs" / "tutorials" / "nested" / "first.md", "Nested guide")
    _write_markdown(tmp_path / "docs" / "how-to" / "task.md", "Perform a task")
    _write_markdown(tmp_path / "docs" / "overview.md", "Overview")
    _write_markdown(tmp_path / "docs" / "SUMMARY.md", "Must not be listed")
    _write_markdown(tmp_path / "docs" / "tutorials" / "SUMMARY.md", "Also excluded")
    (tmp_path / "docs" / "tutorials" / "ignored.txt").write_text("ignored", encoding="utf-8")
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    summary = generate_summary.generate_summary_lines()

    assert summary.startswith("---\nlayout: default\n")
    assert summary.endswith("\n")
    assert "## How To\n\n* [Perform a task](docs/how-to/task.md)" in summary
    assert "## Tutorials\n\n* [Alpha by title](docs/tutorials/z-last.md)" in summary
    assert "* [Nested guide](docs/tutorials/nested/first.md)" in summary
    assert "## Additional Documentation\n\n* [Overview](docs/overview.md)" in summary
    assert "Must not be listed" not in summary
    assert "Also excluded" not in summary
    assert "ignored.txt" not in summary
    assert summary.index("## How To") < summary.index("## Tutorials")
    assert summary.index("Alpha by title") < summary.index("Nested guide")


def test_docs_summary_uses_paths_relative_to_docs(tmp_path, monkeypatch):
    _write_markdown(tmp_path / "docs" / "reference" / "api.md", "API")
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    summary = generate_summary.generate_summary_lines(is_docs_folder=True)

    assert "* [Home](../README.md)" in summary
    assert "* [Getting Started](../START-HERE.md)" in summary
    assert "* [API](reference/api.md)" in summary
    assert "docs/reference/api.md" not in summary


def test_generate_summary_lines_handles_missing_docs_directory(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    summary = generate_summary.generate_summary_lines()

    assert "# Summary" in summary
    assert "* [Home](README.md)" in summary
    assert not any(line.startswith("## ") for line in summary.splitlines())


def test_build_summary_writes_both_variants_and_creates_docs_directory(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    generate_summary.build_summary()

    root_summary = (tmp_path / "SUMMARY.md").read_text(encoding="utf-8")
    docs_summary = (tmp_path / "docs" / "SUMMARY.md").read_text(encoding="utf-8")
    assert "* [Home](README.md)" in root_summary
    assert "* [Home](../README.md)" in docs_summary
    assert str(tmp_path / "SUMMARY.md") in capsys.readouterr().out
