import os
import glob
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_css_files():
    css_dir = os.path.join(ROOT_DIR, 'css')
    assert os.path.exists(css_dir), "css directory missing"
    return glob.glob(os.path.join(css_dir, '*.css'))

@pytest.mark.parametrize("filepath", get_css_files())
def test_css_file_validity(filepath):
    assert os.path.isfile(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0, f"CSS file is empty: {filepath}"

    # Strip comments
    clean_css = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Strip quoted strings to ignore braces inside quoted CSS values
    clean_css = re.sub(r'(["\'])(?:(?=(\\?))\2[\s\S])*?\1', '""', clean_css)

    # Stack-based token-aware scan for braces
    stack = []
    for char in clean_css:
        if char == '{':
            stack.append('{')
        elif char == '}':
            assert len(stack) > 0, f"Unmatched closing brace '}}' in CSS file: {os.path.basename(filepath)}"
            stack.pop()

    assert len(stack) == 0, f"Unclosed open brace '{{' in CSS file: {os.path.basename(filepath)}"

def test_main_css_theme_variables():
    main_css_path = os.path.join(ROOT_DIR, 'css', 'main.css')
    assert os.path.exists(main_css_path)
    with open(main_css_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0, "main.css is empty"

    required_variables = [
        '--ink',
        '--paper',
        '--surface',
        '--border',
        '--text',
        '--gold',
        '--navy',
        '--success',
        '--danger',
    ]

    for var in required_variables:
        assert var in content, f"Required theme variable '{var}' missing in main.css"
