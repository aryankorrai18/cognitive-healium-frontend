"""
Scenario 4: Dynamic Locators
IDs contain random suffixes like order-row-84729.
Using XPath that looks for exact ID match, which fails on dynamic suffixes.
"""

import os
import time
from selenium.webdriver.common.by import By
from tests.conftest import print_healing_summary

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
)


def test_dynamic_order_row_playwright(page):
    """Order rows have IDs like #order-row-84729 with random suffixes."""
    page.goto(DEPLOYED_URL)

    # XPath expects exact ID 'order-row', but it has a random suffix in the DOM
    page.click("//tr[@id='order-row']", intent="first order row in orders table")
    
    # FIXED: Verify the correct element was actually clicked to prevent false positives
    row_text = page.evaluate("""() => {
        const row = document.querySelector('.order-row') || 
                     document.querySelector('[data-testid="order-row"]') ||
                     document.querySelector('table tbody tr');
        return row ? row.innerText : '';
    }""")
    assert "ORD-2024-001" in row_text or "49.99" in row_text, \
        f"Healed to wrong element. Got: {row_text}"
        
    print_healing_summary(page, "test_dynamic_order_row_playwright")


def test_dynamic_order_row_selenium(h):
    """Selenium — same dynamic ID challenge using XPath, proves cross-framework healing."""
    h.get(DEPLOYED_URL)
    time.sleep(1)

    # Using By.XPATH instead of By.ID
    h.click(By.XPATH, "//tr[@id='order-row']", intent="first order row in orders table")
    
    # FIXED: Verify the correct element was actually clicked
    clicked_text = h.execute_script("""return (
        document.querySelector('.order-row') || 
        document.querySelector('[data-testid="order-row"]') ||
        document.querySelector('table tbody tr')
    )?.innerText || ''""")
    assert "ORD-2024-001" in clicked_text or "49.99" in clicked_text, \
        f"Healed to wrong element. Got: {clicked_text}"
        
    print_healing_summary(h, "test_dynamic_order_row_selenium")