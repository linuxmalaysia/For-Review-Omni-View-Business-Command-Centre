import os
import glob
import re
from html.parser import HTMLParser
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        """Initialize collections for tracking parsed HTML elements and attributes."""
        super().__init__()
        self.tags = []
        self.ids = set()
        self.script_srcs = []
        self.link_hrefs = []
        self.meta_refresh = None

    def handle_starttag(self, tag, attrs):
        """
        Record an HTML start tag and its relevant attributes.
        
        Parameters:
            tag (str): The name of the HTML element.
            attrs (list[tuple[str, str]]): Attribute name-value pairs associated with the element.
        """
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

def get_html_files():
    """
    Collects the project's HTML file paths.
    
    Returns:
    	list: The root `index.html` path and any HTML files found in the `Web Ui` directory.
    """
    html_files = [os.path.join(ROOT_DIR, 'index.html')]
    web_ui_dir = os.path.join(ROOT_DIR, 'Web Ui')
    if os.path.exists(web_ui_dir):
        html_files.extend(glob.glob(os.path.join(web_ui_dir, '*.html')))
    return html_files

@pytest.mark.parametrize("filepath", get_html_files())
def test_html_file_validity(filepath):
    """Validate that an HTML file exists, contains content, and has basic document structure.
    
    Parameters:
        filepath: Path to the HTML file to validate.
    """
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
    """Verify that the main dashboard HTML contains the required DOM element IDs when the file exists."""
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
