import http.server
import socketserver
import threading
import time

import pytest
from playwright.sync_api import sync_playwright


class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Suppress HTTP request logging."""
        pass

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def local_server():
    """
    Start a local HTTP server for the test and yield its base URL.
    
    Returns:
    	str: The server's base URL.
    """
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
    """
    Verify that key dashboard pages load successfully and become ready within 3 seconds.
    """
    dashboards = [
        ("Web Ui/login.html", "form"),
        ("Web Ui/forgot-password.html", "#forgotPasswordForm"),
        ("Web Ui/reset_password.html", "#resetPasswordForm"),
        ("Web Ui/main.html", "form, .main-content"),
        ("Web Ui/product.html", "form, .main-content"),
        ("Web Ui/payout.html", "form, .main-content"),
        ("Web Ui/report.html", "form, .main-content"),
        ("Web Ui/user_management.html", "form, .main-content"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for dashboard, readiness_selector in dashboards:
            start_time = time.perf_counter()
            response = page.goto(f"{local_server}/{dashboard}", wait_until="domcontentloaded")
            # Wait for specific landmark element visibility before measuring rendering time completion
            page.wait_for_selector(readiness_selector, state="visible", timeout=3000)
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
        page.wait_for_selector("#forgotPasswordForm", state="visible", timeout=3000)
        nav_time_ms = (time.perf_counter() - start_time) * 1000

        assert "forgot-password.html" in page.url, "Navigation to forgot-password.html failed"
        assert nav_time_ms < 3000, f"Navigation to forgot-password.html took too long: {nav_time_ms:.2f}ms"

        browser.close()
