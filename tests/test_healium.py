"""
Cognitive Healium — Self-Healing Tests

QA test uses #search-input. Dev changed it to #search-bar-v3.
Healium auto-heals. Test code never changes.
"""

import os
import time
import pytest
from selenium.webdriver.common.by import By

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium/"
)


# ── PLAYWRIGHT: Local ────────────────────────────────

def test_playwright_local(page, local_server):
    """Playwright against local HTML — Healium auto-heals broken locator."""
    page.goto(f"{local_server}/index.html")
    page.fill("#search-input", "Healium healed this!", intent="product search input field")

    value = page.locator("input").input_value()
    assert value == "Healium healed this!"


# ── PLAYWRIGHT: Production (GitHub Pages) ────────────

def test_playwright_production(page):
    """Playwright against live deployed site — Healium auto-heals broken locator."""
    page.goto(DEPLOYED_URL)
    page.fill("#search-input", "Healium healed production!", intent="product search input field")

    value = page.locator("input").input_value()
    assert value == "Healium healed production!"


# ── SELENIUM: Local ──────────────────────────────────

def test_selenium_local(h, local_server):
    """Selenium against local HTML — Healium auto-heals broken locator."""
    h.get(f"{local_server}/index.html")
    time.sleep(1)

    h.fill(By.ID, "search-input", "Selenium healed this!", intent="product search input field")

    value = h.execute_script("return document.querySelector('input').value")
    assert value == "Selenium healed this!"