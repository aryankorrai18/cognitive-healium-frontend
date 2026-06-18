"""
Scenario 4: Dynamic Locators
IDs contain random suffixes like order-row-84729.
Using XPath that looks for exact ID match, which fails on dynamic suffixes.
"""

import os
import time
from selenium.webdriver.common.by import By
from tests.conftest import print_healing_summary

# Added cache-buster
DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
) + f"?v={int(time.time())}"


def test_dynamic_order_row_playwright(page):
    """Order rows have IDs like #order-row-84729 with random suffixes."""
    page.goto(DEPLOYED_URL)

    page.click("//tr[@id='order-row']", intent="first order row in orders table")
    
    # FIXED: Verify via global JS variable that the correct row was clicked
    clicked = page.evaluate("return window.rowClicked || ''")
    assert clicked == "ORD-2024-001", f"Healed to wrong element. Got: {clicked}"
        
    print_healing_summary(page, "test_dynamic_order_row_playwright")


def test_dynamic_order_row_selenium(h):
    """Selenium — same dynamic ID challenge using XPath, proves cross-framework healing."""
    h.get(DEPLOYED_URL)
    time.sleep(1)

    h.click(By.XPATH, "//tr[@id='order-row']", intent="first order row in orders table")
    
    # FIXED: Verify via global JS variable
    clicked = h.execute_script("return window.rowClicked || ''")
    assert clicked == "ORD-2024-001", f"Healed to wrong element. Got: {clicked}"
        
    print_healing_summary(h, "test_dynamic_order_row_selenium")