"""
Scenario 2: Attribute Removed

Developer removes the ID entirely. Only class or name attribute remains.
Healium falls back to name, class, or role-based locators.
"""

from tests.conftest import print_healing_summary


def test_email_input_no_id_playwright(page, local_server):
    """Email input has NO id — only class='email-input' and name='email'."""
    page.goto(f"{local_server}/index.html")

    # QA test uses #email-input which doesn't exist
    page.fill("#email-input", "test@example.com", intent="newsletter email input field")

    value = page.locator("input[name='email']").input_value()
    assert value == "test@example.com!", f"Unexpected value: {value}"
    print_healing_summary(page, "test_email_input_no_id_playwright")


def test_subscribe_button_no_id_playwright(page, local_server):
    """Subscribe button has no ID — only class='subscribe-btn'."""
    page.goto(f"{local_server}/index.html")

    # QA test uses #subscribe-btn which doesn't exist
    page.fill("#email-input", "test@example.com", intent="newsletter email input field")
    page.click("#subscribe-btn", intent="newsletter subscribe button")

    status = page.locator("#subscribe-status").inner_text()
    assert "test@example.com" in status
    print_healing_summary(page, "test_subscribe_button_no_id_playwright")