"""
Selenium self-healing test.
Shows that Healium works with Selenium too — not just Playwright.
"""

import time
import threading
import http.server
import functools
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def local_server():
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(FIXTURE_DIR)
    )
    server = http.server.HTTPServer(("127.0.0.1", 9877), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)
    yield "http://127.0.0.1:9877"
    server.shutdown()


@pytest.fixture
def h(healing_driver_factory, local_server):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts)
    healing = healing_driver_factory(driver)
    yield healing
    driver.quit()


def test_selenium_fill_heals(h, local_server):
    """Selenium — broken ID gets auto-healed."""
    h.get(f"{local_server}/test_page.html")
    time.sleep(1)

    h.find_element(By.ID, "search-input").send_keys("initial")

    # Dev changes the UI
    h.execute_script("window.BREAK_UI()")

    # Same test code — Healium auto-heals
    h.fill(By.ID, "search-input", "Selenium healed this!", intent="product search input field")

    value = h.execute_script("return document.querySelector('input').value")
    assert value == "Selenium healed this!"