import os
import glob
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_js_files():
    """
    Find all JavaScript files in the project's `js` directory.
    
    Returns:
    	list[str]: Paths to the JavaScript files found.
    """
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

    # Token-aware cleaning of comments, string literals, template strings, and regex literals
    token_pattern = r'/\*[\s\S]*?\*/|//.*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`|/(?![/*])(?:\\/|[^/\n])+/[gimsuy]*'

    def strip_token(match):
        tok = match.group(0)
        if tok.startswith('//') or tok.startswith('/*'):
            return ''
        return '""'

    clean_content = re.sub(token_pattern, strip_token, content)

    for char in clean_content:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            assert len(stack) > 0 and stack[-1] == pairs[char], (
                f"Unmatched closing bracket '{char}' in JS file: {os.path.basename(filepath)}"
            )
            stack.pop()

    assert len(stack) == 0, f"Unclosed open bracket in JS file: {os.path.basename(filepath)}"

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
    assert os.path.exists(dashboard_js_path), "js/dashboard.js missing"
    with open(dashboard_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Assert concrete consumer-contract identifiers
    assert 'loaddailyGMV' in content, "Missing function loaddailyGMV in dashboard.js"
    assert 'daily-gmv' in content, "Missing DOM element binding 'daily-gmv' in dashboard.js"
    assert 'supabaseClient' in content, "Missing supabaseClient invocation in dashboard.js"
