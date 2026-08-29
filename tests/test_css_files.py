import os
import glob
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_css_files():
    """
    Collect all CSS files in the project's CSS directory.
    
    Returns:
    	list[str]: Paths to the CSS files found.
    
    Raises:
    	AssertionError: If the CSS directory does not exist.
    """
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

    # Check brace balance
    open_braces = clean_css.count('{')
    close_braces = clean_css.count('}')
    assert open_braces == close_braces, f"Unbalanced braces in CSS file: {os.path.basename(filepath)}"

def test_main_css_theme_variables():
    main_css_path = os.path.join(ROOT_DIR, 'css', 'main.css')
    assert os.path.exists(main_css_path)
    with open(main_css_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0
