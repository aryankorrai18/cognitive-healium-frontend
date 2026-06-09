"""
Scenario 1: Locator Change (ID / Class Renamed)
Using XPaths instead of IDs to demonstrate healing brittle selectors.
"""

import os
from tests.conftest import print_healing_summary

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
)


def test_search_input_renamed_playwright(page):
    """QA expects XPath //input[@id='search-input']. Dev changed the ID to search-bar-v3."""
    page.goto(DEPLOYED_URL)
    
    # Using an XPath that relies on the old ID
    page.fill("//input[@id='search-input']", "Healium healed production!", intent="product search input field")

    value = page.locator("input").input_value()
    assert value == "Healium healed production!", f"Unexpected value: {value}"
    print_healing_summary(page, "test_search_input_renamed_playwright")


def test_search_button_works(page):
    """Verify the search button works after healing the input."""
    page.goto(DEPLOYED_URL)
    
    # Heal the input first using XPath
    page.fill("//input[@id='search-input']", "test query", intent="product search input field")
    
    # Click the button using XPath (This one isn't broken, but shows mixed usage)
    page.click("//button[@id='search-btn']", intent="search submit button")
    
    result = page.locator("#result").inner_text()
    assert result != "", f"Result div is empty"
    print_healing_summary(page, "test_search_button_works")


def test_nav_links_renamed_playwright(page):
    """Nav links have dynamic IDs like #nav-home-v2 instead of #nav-home."""
    page.goto(DEPLOYED_URL)

    # Using XPath targeting the old ID
    page.click("//a[@id='nav-home']", intent="navigation home link")
    print_healing_summary(page, "test_nav_links_renamed_playwright")