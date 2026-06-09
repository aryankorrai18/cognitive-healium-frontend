"""
Scenario 5: Cross-Framework Memory

A healing learned by Playwright is instantly available to Selenium
because they share the same ChromaDB collection.

Run this after test_locator_change to see the RAG memory in action.
"""

import time
from selenium.webdriver.common.by import By
from tests.conftest import print_healing_summary

DEPLOYED_URL = "https://aryankorrai18.github.io/cognitive-healium/"


def test_selenium_uses_playwright_memory(h, local_server):
    """
    If Playwright already healed #search-input → getByRole('searchbox'),
    Selenium should heal the SAME locator instantly via RAG (no LLM call needed).
    """
    h.get(f"{local_server}/index.html")
    time.sleep(1)

    # Same broken locator that Playwright already healed
    h.fill(By.ID, "search-input", "Cross-framework healing!", intent="product search input field")

    value = h.execute_script("return document.querySelector('input').value")
    assert value == "Cross-framework healing!"
    print_healing_summary(h, "test_selenium_uses_playwright_memory")