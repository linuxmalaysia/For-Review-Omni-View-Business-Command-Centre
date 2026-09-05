import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse_llms_txt


def test_parse_llms_txt_string():
    sample_text = """# Test Title

> Test Summary Line

## Section One

- [Doc One](docs/doc1.md): Description for doc one
- [Doc Two](docs/doc2.md)
"""
    data = parse_llms_txt.parse_llms_txt(sample_text)
    assert data["title"] == "Test Title"
    assert data["summary"] == "Test Summary Line"
    assert len(data["sections"]) == 1
    assert data["sections"][0]["title"] == "Section One"
    assert len(data["sections"][0]["items"]) == 2
    assert data["sections"][0]["items"][0]["title"] == "Doc One"
    assert data["sections"][0]["items"][0]["description"] == "Description for doc one"


def test_generate_xml_context():
    sample_data = {
        "title": "XML Test",
        "summary": "XML Summary",
        "sections": [
            {
                "title": "Tutorials",
                "items": [
                    {
                        "title": "Getting Started",
                        "url": "docs/tutorials/getting-started.md",
                        "description": "Getting started guide"
                    }
                ]
            }
        ]
    }
    xml_str = parse_llms_txt.generate_xml_context(sample_data)
    assert 'title="XML Test"' in xml_str
    assert "<summary>XML Summary</summary>" in xml_str
    assert 'name="Tutorials"' in xml_str
    assert "<title>Getting Started</title>" in xml_str


def test_generate_llms_txt_and_full():
    llms_txt = parse_llms_txt.generate_llms_txt()
    assert "# Omni-View Business Command Centre" in llms_txt
    assert "getting-started.md" in llms_txt

    llms_full = parse_llms_txt.generate_llms_full()
    assert "llms-full.txt" in llms_full
    assert "FILE:" in llms_full
    assert llms_full.endswith("\n")
    assert not llms_full.endswith("\n\n")


def test_generate_llms_txt_links_documentation_hub_from_each_output_location():
    root_index = parse_llms_txt.generate_llms_txt(relative_to_docs=False)
    docs_index = parse_llms_txt.generate_llms_txt(relative_to_docs=True)

    assert "- [Documentation Hub](docs/index.md):" in root_index
    assert "- [Documentation Hub](index.md):" in docs_index
    assert "- [Documentation Hub](docs/index.md):" not in docs_index


def test_generate_llms_full_embeds_documentation_hub(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    hub_content = "# Distinct documentation hub\n\nHub body.\n"
    (docs_dir / "index.md").write_text(hub_content, encoding="utf-8")

    generated = parse_llms_txt.generate_llms_full(root_dir=str(tmp_path))

    assert "--- FILE: docs/index.md ---" in generated
    assert hub_content.rstrip() in generated


def test_generate_sitemaps():
    stxt, sxml = parse_llms_txt.generate_sitemaps()
    target_base = "https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre"
    obsolete_base = "https://linuxmalaysia.github.io/openwiki"

    assert target_base in stxt
    assert target_base in sxml
    assert obsolete_base not in stxt
    assert obsolete_base not in sxml
    assert "<urlset" in sxml
    assert "<loc>" in sxml
