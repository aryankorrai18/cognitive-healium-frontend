"""
Scenario 1: Locator Change (ID / Class Renamed)

The most common cause of flaky tests — developer renames an ID or class.
QA test uses the old name. Healium finds the element by role, name, or other attributes.
"""

import os
import time
from tests.conftest import print_healing_summary

# Added cache-buster
DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
) + f"?v={int(time.time())}"


def test_search_input_renamed_playwright(page):
    """QA expects #search-input. Dev changed it to #search-bar-v3."""
    page.goto(DEPLOYED_URL)
    page.fill("#search-input", "Healium healed production!", intent="product search input field")

    # FIX: page.locator("input") matches all 3 inputs on the page — strict mode violation.
    # Read back from the specific healed element using its stable placeholder.
    value = page.get_by_placeholder("Search products...").input_value()
    assert value == "Healium healed production!", f"Unexpected value: {value}"
    print_healing_summary(page, "test_search_input_renamed_playwright")


def test_search_button_works(page):
    """Verify the search button works after healing the input."""
    page.goto(DEPLOYED_URL)

    # First fill the input (this will heal #search-input)
    page.fill("#search-input", "test query", intent="product search input field")

    # The button #search-btn still exists, click it
    page.click("#search-btn", intent="search submit button")

    # Check the result div has content
    result = page.locator("#result").inner_text()
    assert result != "", f"Result div is empty"
    print_healing_summary(page, "test_search_button_works")


def test_nav_links_renamed_playwright(page):
    """Nav links have dynamic IDs like #nav-home-v2 instead of #nav-home."""
    page.goto(DEPLOYED_URL)

    page.click("#nav-home", intent="navigation home link")

    # FIX: page.url won't reliably contain the hash fragment on GitHub Pages
    # when a cache-buster query string is present. Read the hash via JS instead.
    hash_val = page.evaluate("() => window.location.hash")
    assert hash_val == "#home", f"Home link was not clicked, hash was: {hash_val!r}"

    print_healing_summary(page, "test_nav_links_renamed_playwright")