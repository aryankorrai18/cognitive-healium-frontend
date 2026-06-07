"""
conftest.py -- Makes self-healing invisible.

pytest --healium-enabled   -> page.fill() and page.click() auto-heal
pytest                     -> page is a normal Playwright page
"""

import time
import threading
import http.server
import functools
import pytest
from pathlib import Path

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@pytest.fixture(scope="session")
def local_server():
    """Serve frontend/ on localhost so local tests don't need the internet."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(FRONTEND_DIR)
    )
    server = http.server.HTTPServer(("127.0.0.1", 9876), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)
    yield "http://127.0.0.1:9876"
    server.shutdown()


@pytest.fixture
def page(context, _healium_enabled, healium_memory, healium_providers):
    raw_page = context.new_page()

    if not _healium_enabled or healium_memory is None:
        yield raw_page
    else:
        from healium.healing_agent import SelfHealingPage
        cache, storage, event_store = healium_providers
        hp = SelfHealingPage(
            page=raw_page,
            memory=healium_memory,
            tenant_id=healium_memory.tenant_id,
            cache_provider=cache,
            storage_provider=storage,
            event_store=event_store,
        )
        yield hp

    raw_page.close()


@pytest.fixture
def h(healing_driver_factory):
    """Self-healing Selenium driver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts)
    healing = healing_driver_factory(driver)
    yield healing
    driver.quit()