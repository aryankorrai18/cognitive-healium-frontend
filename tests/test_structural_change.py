"""
Scenario 3: Structural Change

Element is wrapped in new containers by the developer.
The element itself hasn't changed, but its position in the DOM is different.
Healium finds it by its stable attributes regardless of DOM depth.
"""

from tests.conftest import print_healing_summary


def test_username_input_wrapped_playwright(page, local_server):
    """Username input is now inside .form-wrapper > .input-container."""
    page.goto(f"{local_server}/index.html")

    # QA test uses a simple selector — element is nested deeper now
    page.fill("#username", "john_doe", intent="username input field")

    value = page.locator("#username").input_value()
    assert value == "john_doe"
    print_healing_summary(page, "test_username_input_wrapped_playwright")


def test_login_button_playwright(page, local_server):
    """Login button — same ID, but now inside a nested card structure."""
    page.goto(f"{local_server}/index.html")

    page.fill("#username", "john_doe", intent="username input field")
    page.click("#login-btn", intent="login submit button")

    status = page.locator("#login-status").inner_text()
    assert "john_doe" in status or "Welcome" in status
    print_healing_summary(page, "test_login_button_playwright")