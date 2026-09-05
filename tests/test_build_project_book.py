from pathlib import Path

import pytest

from tools import build_project_book


def test_extract_frontmatter_metadata_parses_flat_values_and_removes_header():
    raw = """---
title: "Operations: Handbook"
description: 'A quoted summary'
empty:
---

# Introduction
"""

    metadata, content = build_project_book.extract_frontmatter_metadata(raw)

    assert metadata == {
        "title": "Operations: Handbook",
        "description": "A quoted summary",
        "empty": "",
    }
    assert content == "# Introduction"


@pytest.mark.parametrize(
    "raw",
    [
        "# No frontmatter\n\nBody",
        "---\ntitle: Missing closing delimiter\n# Body",
    ],
)
def test_extract_frontmatter_metadata_leaves_non_frontmatter_content_unchanged(raw):
    metadata, content = build_project_book.extract_frontmatter_metadata(raw)

    assert metadata == {}
    assert content == raw.strip()


def test_strip_frontmatter_and_footer_preserves_fenced_rules_and_normalizes_rules():
    raw = '''---
description: "Runbook"
---
# Guide

---

```markdown
---
```

~~~text
---
~~~

---
*Copyright All Rights Reserved*
'''

    metadata, content = build_project_book.strip_frontmatter_and_footer(raw)

    assert metadata == {"description": "Runbook"}
    assert "\n***\n" in content
    assert "```markdown\n---\n```" in content
    assert "~~~text\n---\n~~~" in content
    assert "All Rights Reserved" not in content


def test_strip_frontmatter_and_footer_keeps_unrecognized_footer_text():
    raw = "# Guide\n\n---\n*Ordinary italic text*"

    _, content = build_project_book.strip_frontmatter_and_footer(raw)

    assert content == "# Guide\n\n***\n*Ordinary italic text*"


@pytest.mark.parametrize(
    ("alert_type", "expected_class", "expected_heading"),
    [
        ("NOTE", "callout-note", "💡 Note"),
        ("TIP", "callout-tip", "💡 Tip"),
        ("SUCCESS", "callout-tip", "✅ Success"),
        ("WARNING", "callout-warning", "⚠️ Warning"),
        ("IMPORTANT", "callout-warning", "⚠️ Important"),
        ("CAUTION", "callout-warning", "🛑 Caution"),
    ],
)
def test_convert_github_alerts_maps_supported_alerts(
    alert_type: str, expected_class: str, expected_heading: str
):
    markdown = f"> [!{alert_type}] Summary line\n> Continued detail.\n"

    converted = build_project_book.convert_github_alerts(markdown)

    assert f'class="callout {expected_class}"' in converted
    assert f"<strong>{expected_heading}</strong>" in converted
    assert "Summary line\nContinued detail." in converted


def test_convert_github_alerts_leaves_ordinary_blockquotes_unchanged():
    markdown = "> A normal quotation.\n> With another line.\n"

    assert build_project_book.convert_github_alerts(markdown) == markdown


@pytest.mark.parametrize(
    ("code", "expected_fence"),
    [
        ("print('safe')", "```"),
        ("before ``` after", "````"),
        ("```\n`````\n````", "``````"),
    ],
)
def test_scale_backticks_uses_a_fence_longer_than_embedded_runs(
    code: str, expected_fence: str
):
    assert build_project_book.scale_backticks(code) == (
        expected_fence,
        expected_fence,
    )


def test_extract_commentary_skips_shebang_and_classifies_warning_keywords():
    source = """#!/usr/bin/env python3

# Never run against live data
# without a backup.
print("safe")
"""

    commentary = build_project_book.extract_commentary(source, "python")

    assert commentary is not None
    assert "callout-warning" in commentary
    assert "Developer Commentary — Read Before Executing" in commentary
    assert "Never run against live data" in commentary
    assert "#!/usr/bin/env" not in commentary


def test_extract_commentary_returns_none_when_code_has_no_leading_comments():
    assert build_project_book.extract_commentary("value = 1\n# later") is None


def test_extract_commentary_limits_rendered_comment_lines_to_fifteen():
    source = "\n".join(f"# comment {number}" for number in range(17))

    commentary = build_project_book.extract_commentary(source)

    assert commentary is not None
    assert "> comment 14" in commentary
    assert "> comment 15" not in commentary


def test_ingest_code_file_adds_source_commentary_and_safe_fences(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = tmp_path / "src" / "example.py"
    source.parent.mkdir()
    source.write_text(
        "# Operational context\nprint('``` embedded fence')\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_project_book, "ROOT_DIR", tmp_path)

    rendered = build_project_book.ingest_code_file(
        source, "python", "Example Source", "example-source"
    )

    assert '<a id="example-source"></a>' in rendered
    assert "### Example Source" in rendered
    assert "**Source File:** `src/example.py`" in rendered
    assert "Developer Operational Context" in rendered
    assert "````python\n" in rendered
    assert rendered.rstrip().endswith("````")


def test_ingest_code_file_reports_a_missing_file(tmp_path: Path):
    missing = tmp_path / "missing.py"

    assert build_project_book.ingest_code_file(
        missing, "python", "Missing", "missing"
    ) == f"\n*File not found: {missing}*\n"


@pytest.mark.parametrize("show_provenance", [True, False])
def test_ingest_doc_file_renders_metadata_alerts_and_bounded_headings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    show_provenance: bool,
):
    document = tmp_path / "docs" / "guide.md"
    document.parent.mkdir()
    document.write_text(
        '''---
description: "Concise executive summary."
---
# Guide
###### Deep section

> [!TIP] Start here
> Continue carefully.
''',
        encoding="utf-8",
    )
    monkeypatch.setattr(build_project_book, "ROOT_DIR", tmp_path)

    rendered = build_project_book.ingest_doc_file(
        "docs/guide.md", heading_offset=2, show_provenance=show_provenance
    )

    assert ("Operational Reference Guide" in rendered) is show_provenance
    assert "📌 Executive Summary" in rendered
    assert "Concise executive summary." in rendered
    assert "### Guide" in rendered
    assert "###### Deep section" in rendered
    assert "callout-tip" in rendered
    assert "Start here\nContinue carefully." in rendered


def test_ingest_doc_file_reports_a_missing_document(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(build_project_book, "ROOT_DIR", tmp_path)

    assert build_project_book.ingest_doc_file("docs/missing.md") == (
        "\n*Documentation file not found: docs/missing.md*\n"
    )


def test_build_master_book_assembles_all_sections_in_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    output = tmp_path / "build" / "master_book.md"
    output.parent.mkdir()
    doc_calls = []
    code_calls = []

    def fake_ingest_doc_file(
        rel_path: str, heading_offset: int = 1, show_provenance: bool = True
    ) -> str:
        doc_calls.append((rel_path, heading_offset, show_provenance))
        return f"DOC:{rel_path}"

    def fake_ingest_code_file(
        file_path: Path, lang: str, title: str, anchor: str
    ) -> str:
        code_calls.append((file_path, lang, title, anchor))
        return f"CODE:{file_path.name}"

    monkeypatch.setattr(build_project_book, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(build_project_book, "MASTER_MD", output)
    monkeypatch.setattr(build_project_book, "ingest_doc_file", fake_ingest_doc_file)
    monkeypatch.setattr(build_project_book, "ingest_code_file", fake_ingest_code_file)

    build_project_book.build_master_book()

    assembled = output.read_text(encoding="utf-8")
    assert assembled.index("# Executive Overview") < assembled.index("# Part 1:")
    assert assembled.index("# Part 1:") < assembled.index("# Part 2:")
    assert assembled.index("# Part 2:") < assembled.index("# Part 3:")
    assert assembled.index("# Part 3:") < assembled.index("# Part 4:")
    assert len(doc_calls) == 6
    assert [call[0] for call in code_calls] == [
        tmp_path / "parse_llms_txt.py",
        tmp_path / "tools" / "generate_summary.py",
    ]
    assert all(call[1] == 1 for call in doc_calls)
    assert "Master markdown written" in capsys.readouterr().out
