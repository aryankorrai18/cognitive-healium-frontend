"""
Scenario 4: Dynamic Locators

IDs contain random suffixes like order-row-84729.
Healium avoids the random part and uses stable attributes or text content.
"""

import time
from selenium.webdriver.common.by import By
from tests.conftest import print_healing_summary


def test_dynamic_order_row_playwright(page, local_server):
    """Order rows have IDs like #order-row-84729 with random suffixes."""
    page.goto(f"{local_server}/index.html")

    # QA test uses a partial ID that doesn't match the dynamic pattern
    page.click("#order-row", intent="first order row in orders table")
    print_healing_summary(page, "test_dynamic_order_row_playwright")


def test_dynamic_order_row_selenium(h, local_server):
    """Selenium — same dynamic ID challenge, proves cross-framework healing."""
    h.get(f"{local_server}/index.html")
    time.sleep(1)

    # QA uses partial ID — agent finds by stable attributes or XPath contains()
    h.fill(By.ID, "order-row", "test", intent="order row element")
    print_healing_summary(h, "test_dynamic_order_row_selenium")