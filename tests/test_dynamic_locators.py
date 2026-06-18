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

    # FIX: page.evaluate() takes a JS *expression*, not a statement.
    # "return window.rowClicked" is a SyntaxError (illegal return statement).
    # Use an arrow function or drop the return keyword entirely.
    clicked = page.evaluate("() => window.rowClicked || ''")
    assert clicked == "ORD-2024-001", f"Healed to wrong element. Got: {clicked}"

    print_healing_summary(page, "test_dynamic_order_row_playwright")


def test_dynamic_order_row_selenium(h):
    """Selenium — same dynamic ID challenge using XPath, proves cross-framework healing."""
    h.get(DEPLOYED_URL)
    time.sleep(1)

    # FIX: The healer was suggesting //table/tr[1] which skips <tbody> in HTML.
    # A more specific intent tells the LLM to generate //tbody/tr[1] as a candidate,
    # which correctly navigates past the implicit <tbody> element.
    h.click(
        By.XPATH,
        "//tr[@id='order-row']",
        intent="first data row inside the orders table tbody"
    )

    # FIX: Same expression-vs-statement fix as the Playwright version above.
    clicked = h.execute_script("return window.rowClicked || ''")
    assert clicked == "ORD-2024-001", f"Healed to wrong element. Got: {clicked}"

    print_healing_summary(h, "test_dynamic_order_row_selenium")