import stat
from pathlib import Path

import pytest

from tools import generate_summary, install_git_guardrails


@pytest.mark.parametrize(
    ("contents", "filename", "expected"),
    [
        ('---\ntitle: "Frontmatter title"\n---\n# Ignored\n', "doc.md", "Frontmatter title"),
        ("---\ntitle: 'Title: with colon'\n---\n", "doc.md", "Title: with colon"),
        ("Introductory text\n\n# First heading\n", "doc.md", "First heading"),
        ("No frontmatter or heading\n", "fallback-name.md", "Fallback Name"),
    ],
)
def test_get_title_from_md_uses_supported_title_sources(
    tmp_path: Path, contents: str, filename: str, expected: str
):
    markdown_path = tmp_path / filename
    markdown_path.write_text(contents, encoding="utf-8")

    assert generate_summary.get_title_from_md(str(markdown_path)) == expected


def test_generate_summary_lines_groups_and_sorts_discovered_documents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    docs_dir = tmp_path / "docs"
    (docs_dir / "tutorials").mkdir(parents=True)
    (docs_dir / "how-to").mkdir()
    (docs_dir / "tutorials" / "second.md").write_text(
        "# Zebra tutorial\n", encoding="utf-8"
    )
    (docs_dir / "tutorials" / "first.md").write_text(
        "---\ntitle: Alpha tutorial\n---\n", encoding="utf-8"
    )
    (docs_dir / "how-to" / "setup.md").write_text("# Set up\n", encoding="utf-8")
    (docs_dir / "index.md").write_text("# Documentation home\n", encoding="utf-8")
    (docs_dir / "SUMMARY.md").write_text("# Must be ignored\n", encoding="utf-8")
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    summary = generate_summary.generate_summary_lines()

    assert "* [Home](README.md)" in summary
    assert "* [Set up](docs/how-to/setup.md)" in summary
    assert "* [Documentation home](docs/index.md)" in summary
    assert summary.index("## How To") < summary.index("## Tutorials")
    assert summary.index("Alpha tutorial") < summary.index("Zebra tutorial")
    assert "Must be ignored" not in summary
    assert summary.endswith("\n") and not summary.endswith("\n\n")


def test_docs_summary_uses_paths_relative_to_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    docs_dir = tmp_path / "docs" / "reference"
    docs_dir.mkdir(parents=True)
    (docs_dir / "api.md").write_text("# API\n", encoding="utf-8")
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    summary = generate_summary.generate_summary_lines(is_docs_folder=True)

    assert "* [Home](README.md)" in summary
    assert "* [API](reference/api.md)" in summary
    assert "docs/reference/api.md" not in summary


def test_build_summary_writes_root_and_docs_indexes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Documentation hub\n", encoding="utf-8")
    monkeypatch.setattr(generate_summary, "ROOT_DIR", str(tmp_path))

    generate_summary.build_summary()

    root_summary = (tmp_path / "SUMMARY.md").read_text(encoding="utf-8")
    docs_summary = (docs_dir / "SUMMARY.md").read_text(encoding="utf-8")
    assert "[Documentation hub](docs/index.md)" in root_summary
    assert "[Documentation hub](index.md)" in docs_summary
    assert "Successfully generated" in capsys.readouterr().out


def test_install_guardrails_skips_when_git_hooks_directory_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    missing_hooks_dir = tmp_path / ".git" / "hooks"
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(missing_hooks_dir))

    install_git_guardrails.install_guardrails()

    assert not missing_hooks_dir.exists()
    assert "not found. Skipping hook installation." in capsys.readouterr().out


def test_install_guardrails_creates_an_executable_hook(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    hook_path = hooks_dir / "pre-commit"
    assert hook_path.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT
    assert hook_path.stat().st_mode & stat.S_IXUSR


def test_install_guardrails_backs_up_an_unmanaged_hook_before_replacing_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook_path = hooks_dir / "pre-commit"
    original_contents = "#!/bin/sh\necho existing hook\n"
    hook_path.write_text(original_contents, encoding="utf-8")
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    assert (hooks_dir / "pre-commit.bak").read_text(encoding="utf-8") == original_contents
    assert hook_path.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT


def test_reinstalling_managed_guardrails_does_not_create_a_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook_path = hooks_dir / "pre-commit"
    hook_path.write_text(install_git_guardrails.HOOK_CONTENT, encoding="utf-8")
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    assert not (hooks_dir / "pre-commit.bak").exists()
    assert hook_path.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT
