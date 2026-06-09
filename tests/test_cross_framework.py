"""
Scenario 5: Cross-Framework Memory
A healing learned by Playwright is instantly available to Selenium.
"""

import os
import time
from selenium.webdriver.common.by import By
from tests.conftest import print_healing_summary

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
)


def test_selenium_uses_playwright_memory(h):
    """
    If Playwright already healed the XPath //input[@id='search-input'],
    Selenium should heal the SAME broken XPath instantly via RAG memory.
    """
    h.get(DEPLOYED_URL)
    time.sleep(1)

    # Selenium uses By.XPATH to hit the same broken locator
    h.fill(By.XPATH, "//input[@id='search-input']", "Cross-framework healing!", intent="product search input field")

    value = h.execute_script("return document.querySelector('input').value")
    assert value == "Cross-framework healing!"
    print_healing_summary(h, "test_selenium_uses_playwright_memory")