import os
import glob
import re
from html.parser import HTMLParser
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.script_srcs = []
        self.link_hrefs = []
        self.meta_refresh = None

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attr_dict = dict(attrs)
        if 'id' in attr_dict:
            self.ids.add(attr_dict['id'])
        if tag == 'script' and 'src' in attr_dict:
            self.script_srcs.append(attr_dict['src'])
        if tag == 'link' and 'href' in attr_dict:
            self.link_hrefs.append(attr_dict['href'])
        if tag == 'meta' and attr_dict.get('http-equiv', '').lower() == 'refresh':
            self.meta_refresh = attr_dict.get('content', '')


class FormMarkupParser(HTMLParser):
    """Collect form-control, label, and image attributes by their stable identifiers."""

    def __init__(self):
        super().__init__()
        self.controls = {}
        self.labels = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag in {'input', 'select', 'textarea'} and attr_dict.get('id'):
            self.controls[attr_dict['id']] = attr_dict
        elif tag == 'label':
            self.labels.append(attr_dict)
        elif tag == 'img':
            self.images.append(attr_dict)


def parse_form_markup(relative_path):
    filepath = os.path.join(ROOT_DIR, relative_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = FormMarkupParser()
    parser.feed(content)
    return parser, content

def get_html_files():
    html_files = [os.path.join(ROOT_DIR, 'index.html')]
    web_ui_dir = os.path.join(ROOT_DIR, 'Web Ui')
    if os.path.exists(web_ui_dir):
        html_files.extend(glob.glob(os.path.join(web_ui_dir, '*.html')))
    return html_files

@pytest.mark.parametrize("filepath", get_html_files())
def test_html_file_validity(filepath):
    assert os.path.isfile(filepath), f"HTML file does not exist: {filepath}"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert len(content.strip()) > 0, f"HTML file is empty: {filepath}"

    parser = SimpleHTMLValidator()
    parser.feed(content)

    # Check basic HTML structure
    assert 'html' in parser.tags, f"Missing <html> tag in {filepath}"
    assert 'head' in parser.tags or 'body' in parser.tags, f"Missing head/body tag in {filepath}"

def test_index_html_redirect():
    index_path = os.path.join(ROOT_DIR, 'index.html')
    assert os.path.isfile(index_path), "index.html missing"
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = SimpleHTMLValidator()
    parser.feed(content)

    # Validate exact meta refresh redirect target or window.location.replace expression
    assert parser.meta_refresh is not None, "Missing meta refresh header in index.html"
    assert re.search(r'url=\.?/?[Ww]eb%20[Uu]i/login\.html', parser.meta_refresh), (
        f"meta refresh content '{parser.meta_refresh}' does not target Web Ui/login.html"
    )
    assert re.search(r'window\.location\.replace\(["\']\.?/?Web%20Ui/login\.html["\']\)', content), (
        "window.location.replace script does not target Web Ui/login.html"
    )

def test_web_ui_critical_elements():
    main_html_path = os.path.join(ROOT_DIR, 'Web Ui', 'main.html')
    assert os.path.isfile(main_html_path), f"Required dashboard template main.html missing at {main_html_path}"

    with open(main_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = SimpleHTMLValidator()
    parser.feed(content)

    # Verify required key DOM IDs for dashboard JS calculations
    expected_ids = {'daily-gmv', 'daily-item-sold', 'active_staff', 'top-employee', 'stockChart'}
    for elem_id in expected_ids:
        assert elem_id in parser.ids, f"Missing critical DOM ID '{elem_id}' in main.html"


@pytest.mark.parametrize(
    ("relative_path", "control_id", "expected_type", "expected_name", "expected_autocomplete"),
    [
        ('Web Ui/login.html', 'email', 'email', 'email', 'email'),
        ('Web Ui/login.html', 'password', 'password', 'password', 'current-password'),
        ('Web Ui/forgot-password.html', 'email', 'email', 'email', 'email'),
        ('Web Ui/reset_password.html', 'newPassword', 'password', 'password', 'new-password'),
        ('Web Ui/reset_password.html', 'confirmPassword', 'password', 'confirm-password', 'new-password'),
        ('Web Ui/edit_profile.html', 'update_name', 'text', 'name', 'name'),
        ('Web Ui/edit_profile.html', 'update_phone', 'tel', 'tel', 'tel'),
        ('Web Ui/Employee_edit_profile.html', 'update_name', 'text', 'name', 'name'),
        ('Web Ui/Employee_edit_profile.html', 'update_phone', 'tel', 'tel', 'tel'),
    ],
)
def test_changed_form_controls_expose_autofill_metadata(
    relative_path, control_id, expected_type, expected_name, expected_autocomplete
):
    parser, _ = parse_form_markup(relative_path)

    assert control_id in parser.controls, f"Missing #{control_id} in {relative_path}"
    control = parser.controls[control_id]
    assert control.get('type') == expected_type
    assert control.get('name') == expected_name
    assert control.get('autocomplete') == expected_autocomplete
    assert 'required' in control


@pytest.mark.parametrize(
    ("relative_path", "control_ids"),
    [
        ('Web Ui/login.html', ('email', 'password')),
        ('Web Ui/forgot-password.html', ('email',)),
        ('Web Ui/reset_password.html', ('newPassword', 'confirmPassword')),
        ('Web Ui/edit_profile.html', ('update_name', 'update_phone')),
        ('Web Ui/Employee_edit_profile.html', ('update_name', 'update_phone')),
    ],
)
def test_changed_form_controls_have_matching_labels(relative_path, control_ids):
    parser, _ = parse_form_markup(relative_path)
    label_targets = {label.get('for') for label in parser.labels}

    assert set(control_ids) <= label_targets


def test_login_logo_has_stable_dimensions_and_accessible_alternative_text():
    parser, _ = parse_form_markup('Web Ui/login.html')
    logo = next(image for image in parser.images if image.get('class', '').split().count('logo'))

    assert logo.get('width') == '100'
    assert logo.get('height') == '100'
    assert logo.get('alt', '').strip()


@pytest.mark.parametrize(
    ("relative_path", "old_copy", "new_copy"),
    [
        ('Web Ui/Employee_Main.html', 'Loading leaderboard...', 'Loading leaderboard…'),
        ('Web Ui/lives.html', 'Loading employees...', 'Loading employees…'),
        ('Web Ui/main.html', 'Loading activities...', 'Loading activities…'),
        ('Web Ui/payout.html', 'Loading employees...', 'Loading employees…'),
        ('js/live.js', 'Loading employees...', 'Loading employees…'),
        ('js/login.js', 'Logging in...', 'Logging in…'),
        ('js/login.js', 'Login successful. Redirecting...', 'Login successful. Redirecting…'),
        ('js/manage_user.js', 'Adding...', 'Adding…'),
        ('js/payout.js', 'Loading employees...', 'Loading employees…'),
        ('js/reset_password.js', 'Resetting...', 'Resetting…'),
    ],
)
def test_changed_status_copy_uses_a_single_ellipsis_character(relative_path, old_copy, new_copy):
    filepath = os.path.join(ROOT_DIR, relative_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert new_copy in content
    assert old_copy not in content
