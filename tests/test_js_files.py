import os
import glob
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_js_files():
    js_dir = os.path.join(ROOT_DIR, 'js')
    assert os.path.exists(js_dir), "js directory missing"
    return glob.glob(os.path.join(js_dir, '*.js'))

def sanitize_js_for_bracket_scan(content):
    """
    Context-aware stateful tokenizer/scanner for JavaScript:
    - Distinguishes division operators from regular-expression literals
    - Preserves bracket content inside ${...} template interpolations
    - Handles character classes such as /[/]/ in regexes
    - Strips comments, string literals, and regex contents
    """
    i = 0
    n = len(content)
    result = []

    state = 'NORMAL'  # NORMAL, SL_COMMENT, ML_COMMENT, S_STRING, D_STRING, TEMPLATE, REGEX
    template_stack = []
    in_char_class = False
    escaped = False

    REGEX_PREV_TOKENS = {
        '(', ',', '=', ':', '?', '[', '{', ';', '!', '&', '|', '+', '-', '*', '/', '%',
        '^', '~', '<', '>', 'return', 'case', 'typeof', 'void', 'delete', 'await', 'yield', 'in', 'instanceof'
    }

    def get_last_non_space_token():
        s = ''.join(result).rstrip()
        if not s:
            return ''
        m = re.search(r'([a-zA-Z0-9_$]+|[^a-zA-Z0-9_\s$])$', s)
        return m.group(1) if m else ''

    while i < n:
        ch = content[i]
        nxt = content[i + 1] if i + 1 < n else ''

        if state == 'SL_COMMENT':
            if ch == '\n':
                state = 'NORMAL'
                result.append('\n')
            i += 1
            continue

        if state == 'ML_COMMENT':
            if ch == '*' and nxt == '/':
                state = 'NORMAL'
                i += 2
            else:
                i += 1
            continue

        if state == 'S_STRING':
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == "'":
                state = 'NORMAL'
            i += 1
            continue

        if state == 'D_STRING':
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                state = 'NORMAL'
            i += 1
            continue

        if state == 'TEMPLATE':
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '$' and nxt == '{':
                template_stack.append(1)
                result.append('${')
                state = 'NORMAL'
                i += 2
                continue
            elif ch == '`':
                state = 'NORMAL'
            i += 1
            continue

        if state == 'REGEX':
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif in_char_class:
                if ch == ']':
                    in_char_class = False
            else:
                if ch == '[':
                    in_char_class = True
                elif ch == '/':
                    state = 'NORMAL'
            i += 1
            continue

        # NORMAL state
        if ch == '/' and nxt == '/':
            state = 'SL_COMMENT'
            i += 2
            continue

        if ch == '/' and nxt == '*':
            state = 'ML_COMMENT'
            i += 2
            continue

        if ch == "'":
            state = 'S_STRING'
            escaped = False
            i += 1
            continue

        if ch == '"':
            state = 'D_STRING'
            escaped = False
            i += 1
            continue

        if ch == '`':
            state = 'TEMPLATE'
            escaped = False
            i += 1
            continue

        if ch == '/':
            prev = get_last_non_space_token()
            if prev in REGEX_PREV_TOKENS or not prev:
                state = 'REGEX'
                escaped = False
                in_char_class = False
                i += 1
                continue

        if template_stack:
            if ch == '{':
                template_stack[-1] += 1
            elif ch == '}':
                template_stack[-1] -= 1
                if template_stack[-1] == 0:
                    template_stack.pop()
                    state = 'TEMPLATE'
                    escaped = False
                    result.append('}')
                    i += 1
                    continue

        result.append(ch)
        i += 1

    return ''.join(result)

@pytest.mark.parametrize("filepath", get_js_files())
def test_js_file_syntax_and_structure(filepath):
    assert os.path.isfile(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0, f"JS file is empty: {filepath}"

    # Basic brackets / parentheses balancing check
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    clean_content = sanitize_js_for_bracket_scan(content)

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

    assert 'loaddailyGMV' in content, "Missing function loaddailyGMV in dashboard.js"
    assert 'daily-gmv' in content, "Missing DOM element binding 'daily-gmv' in dashboard.js"
    assert 'supabaseClient' in content, "Missing supabaseClient invocation in dashboard.js"

def test_router_and_cache_js_files():
    router_path = os.path.join(ROOT_DIR, 'js', 'router.js')
    cache_path = os.path.join(ROOT_DIR, 'js', 'cache.js')
    assert os.path.exists(router_path), "js/router.js missing"
    assert os.path.exists(cache_path), "js/cache.js missing"

    with open(router_path, 'r', encoding='utf-8') as f:
        router_content = f.read()
    assert 'AppRouter' in router_content
    assert 'navigateTo' in router_content

    with open(cache_path, 'r', encoding='utf-8') as f:
        cache_content = f.read()
    assert 'SessionCache' in cache_content
    assert 'sessionStorage' in cache_content
