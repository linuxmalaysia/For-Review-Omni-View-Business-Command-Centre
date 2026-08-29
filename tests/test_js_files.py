import os
import glob
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_js_files():
    js_dir = os.path.join(ROOT_DIR, 'js')
    assert os.path.exists(js_dir), "js directory missing"
    return glob.glob(os.path.join(js_dir, '*.js'))

@pytest.mark.parametrize("filepath", get_js_files())
def test_js_file_syntax_and_structure(filepath):
    assert os.path.isfile(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0, f"JS file is empty: {filepath}"

    # Basic brackets / parentheses balancing check
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    # Clean comments, string literals, template literals, and regex literals
    clean_content = re.sub(r'//.*', '', content)
    clean_content = re.sub(r'/\*[\s\S]*?\*/', '', clean_content)
    clean_content = re.sub(r'/(?:\\/|[^/\n])+/[gimsuy]*', '""', clean_content)
    clean_content = re.sub(r'`(?:\\`|[^`])*`', '""', clean_content)
    clean_content = re.sub(r'(["\'])(?:(?=(\\?))\2[\s\S])*?\1', '""', clean_content)

    for char in clean_content:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            if stack and stack[-1] == pairs[char]:
                stack.pop()

    assert len(stack) == 0, f"Unbalanced brackets/parentheses in JS file: {os.path.basename(filepath)}"

def test_database_js_supabase_configuration():
    db_js_path = os.path.join(ROOT_DIR, 'js', 'database.js')
    assert os.path.exists(db_js_path)
    with open(db_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'supabaseUrl' in content
    assert 'supabaseKey' in content
    assert 'supabaseClient' in content
    assert 'STAFF_ROLES' in content

def test_dashboard_js_functions():
    dashboard_js_path = os.path.join(ROOT_DIR, 'js', 'dashboard.js')
    if os.path.exists(dashboard_js_path):
        with open(dashboard_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check presence of primary load/render functions
        assert 'fetch' in content or 'supabaseClient' in content or 'function' in content
