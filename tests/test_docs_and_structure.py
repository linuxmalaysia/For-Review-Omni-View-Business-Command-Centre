import os
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_diataxis_directories_exist():
    docs_dir = os.path.join(ROOT_DIR, 'docs')
    assert os.path.isdir(docs_dir), "docs/ directory does not exist"

    expected_subdirs = ['tutorials', 'how-to', 'reference', 'explanation']
    for subdir in expected_subdirs:
        subdir_path = os.path.join(docs_dir, subdir)
        assert os.path.isdir(subdir_path), f"Diataxis directory docs/{subdir} missing"

def test_diataxis_documents_exist():
    expected_files = [
        os.path.join(ROOT_DIR, 'docs', 'tutorials', 'getting-started.md'),
        os.path.join(ROOT_DIR, 'docs', 'how-to', 'manage-inventory-and-payouts.md'),
        os.path.join(ROOT_DIR, 'docs', 'reference', 'file-structure-and-api.md'),
        os.path.join(ROOT_DIR, 'docs', 'explanation', 'architecture-and-diataxis.md'),
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected documentation file missing: {filepath}"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        assert len(content.strip()) > 100, f"Documentation file {filepath} content is too short"

def test_readme_references_diataxis():
    readme_path = os.path.join(ROOT_DIR, 'README.md')
    assert os.path.isfile(readme_path)
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'Diátaxis' in content or 'diataxis' in content
    assert 'tutorials' in content.lower()
    assert 'how-to' in content.lower()
    assert 'reference' in content.lower()
    assert 'explanation' in content.lower()

def test_all_repository_files_accounted_for():
    # Enumerate all key directories and verify non-empty files
    for folder in ['Web Ui', 'js', 'css', 'proposal']:
        dir_path = os.path.join(ROOT_DIR, folder)
        assert os.path.isdir(dir_path), f"Required directory {folder} missing"

        entries = os.listdir(dir_path)
        regular_files = [f for f in entries if os.path.isfile(os.path.join(dir_path, f))]
        assert len(regular_files) > 0, f"Directory {folder} contains no regular files"
