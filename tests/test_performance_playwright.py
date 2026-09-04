import http.server
import socketserver
import threading
import time

import pytest
from playwright.sync_api import sync_playwright


class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def local_server():
    handler = QuietHTTPRequestHandler
    httpd = ReusableTCPServer(("127.0.0.1", 0), handler)
    host, port = httpd.server_address
    base_url = f"http://{host}:{port}"
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.2)
    yield base_url
    httpd.shutdown()
    httpd.server_close()

def test_dashboard_rendering_performance(local_server):
    """Smoke test to measure initial page load and rendering times for key dashboards in Web Ui/."""
    dashboards = [
        "Web Ui/login.html",
        "Web Ui/forgot-password.html",
        "Web Ui/reset_password.html",
        "Web Ui/main.html",
        "Web Ui/product.html",
        "Web Ui/payout.html",
        "Web Ui/report.html",
        "Web Ui/user_management.html",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for dashboard in dashboards:
            start_time = time.perf_counter()
            response = page.goto(f"{local_server}/{dashboard}", wait_until="domcontentloaded")
            render_time_ms = (time.perf_counter() - start_time) * 1000

            assert response.status == 200, f"Failed to load {dashboard}"
            # Enforce that rendering completes well within performance budget (< 3000ms)
            assert render_time_ms < 3000, f"Dashboard {dashboard} rendering took too long: {render_time_ms:.2f}ms"

        browser.close()

def test_client_side_navigation_performance(local_server):
    """Smoke test to measure client-side navigation performance across views in Web Ui/."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(f"{local_server}/Web%20Ui/login.html", wait_until="domcontentloaded")

        start_time = time.perf_counter()
        page.click('a[href="forgot-password.html"]')
        page.wait_for_selector("form", timeout=3000)
        nav_time_ms = (time.perf_counter() - start_time) * 1000

        assert "forgot-password.html" in page.url, "Navigation to forgot-password.html failed"
        assert nav_time_ms < 3000, f"Navigation to forgot-password.html took too long: {nav_time_ms:.2f}ms"

        browser.close()
