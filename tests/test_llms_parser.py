import os
import sys
import tempfile
import xml.etree.ElementTree as ET

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


def test_generate_sitemaps():
    stxt, sxml = parse_llms_txt.generate_sitemaps()
    assert "https://linuxmalaysia.github.io/For-Review-Omni-View-Business-Command-Centre/" in stxt
    assert "<urlset" in sxml
    assert "<loc>" in sxml
