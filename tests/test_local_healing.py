"""
Local Playwright test — simulates a UI change mid-test.
"""

import time
import threading
import http.server
import functools
import pytest
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def local_server():
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(FIXTURE_DIR)
    )
    server = http.server.HTTPServer(("127.0.0.1", 9876), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)
    yield "http://127.0.0.1:9876"
    server.shutdown()


def test_fill_heals_broken_input(page, local_server):
    """Element ID changes mid-test — Healium heals the broken locator."""
    page.goto(f"{local_server}/test_page.html")
    page.fill("#search-input", "initial test")

    # Dev renames the element — ID is gone
    page.evaluate("window.BREAK_UI()")

    # Same test code still works — Healium auto-heals
    page.fill("#search-input", "Healium healed this!", intent="product search input field")

    value = page.locator("input").input_value()
    assert value == "Healium healed this!"