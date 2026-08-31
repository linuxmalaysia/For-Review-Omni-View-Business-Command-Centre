import stat

from tools import install_git_guardrails


def test_install_guardrails_skips_when_hooks_directory_is_missing(tmp_path, monkeypatch, capsys):
    hooks_dir = tmp_path / ".git" / "hooks"
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    assert not hooks_dir.exists()
    assert "not found. Skipping" in capsys.readouterr().out


def test_install_guardrails_creates_executable_hook(tmp_path, monkeypatch):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    hook = hooks_dir / "pre-commit"
    assert hook.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT
    assert hook.stat().st_mode & stat.S_IXUSR
    assert "set -eu" in hook.read_text(encoding="utf-8")
    assert "parse_llms_txt.py --generate-all" in hook.read_text(encoding="utf-8")


def test_install_guardrails_backs_up_an_unmanaged_hook(tmp_path, monkeypatch, capsys):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook = hooks_dir / "pre-commit"
    original_content = "#!/bin/sh\necho custom hook\n"
    hook.write_text(original_content, encoding="utf-8")
    hook.chmod(0o750)
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    backup = hooks_dir / "pre-commit.bak"
    assert backup.read_text(encoding="utf-8") == original_content
    assert stat.S_IMODE(backup.stat().st_mode) == 0o750
    assert hook.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT
    assert str(backup) in capsys.readouterr().out


def test_install_guardrails_does_not_back_up_a_managed_hook(tmp_path, monkeypatch):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook = hooks_dir / "pre-commit"
    hook.write_text(
        "#!/bin/sh\npython3 tools/generate_summary.py\n# locally customized\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(install_git_guardrails, "GIT_HOOKS_DIR", str(hooks_dir))

    install_git_guardrails.install_guardrails()

    assert not (hooks_dir / "pre-commit.bak").exists()
    assert hook.read_text(encoding="utf-8") == install_git_guardrails.HOOK_CONTENT
