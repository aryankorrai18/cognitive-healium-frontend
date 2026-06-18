"""
Scenario 3: Structural Change
Using brittle structural XPaths that break when the DOM structure changes.
"""

import os
from tests.conftest import print_healing_summary

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
)


def test_username_input_wrapped_playwright(page):
    """Username input is now inside .form-wrapper > .input-container. 
       Brittle XPath //div[@class='card']/input will FAIL because it's no longer a direct child."""
    page.goto(DEPLOYED_URL)

    # This XPath expects the input to be a DIRECT child of div.card. 
    # Because of the new wrappers, this is structurally broken!
    page.fill("//div[@class='card'][2]/input", "john_doe", intent="username input field")

    # FIXED: Use evaluate() to read the value without triggering Playwright's strict locator timeout
    value = page.evaluate("""() => {
        const el = document.querySelector('#username');
        return el ? el.value : '';
    }""")
    assert value == "john_doe"
    print_healing_summary(page, "test_username_input_wrapped_playwright")


def test_login_button_playwright(page):
    """Login button — testing structural XPath for the button as well."""
    page.goto(DEPLOYED_URL)

    # Same brittle structural XPath assumption
    page.fill("//div[@class='card'][2]/input", "john_doe", intent="username input field")
    page.click("//div[@class='card'][2]/button", intent="login submit button")

    # FIXED: Use evaluate() to read status text without locator timeout
    status = page.evaluate("""() => {
        const el = document.querySelector('#login-status');
        return el ? el.innerText : '';
    }""")
    assert "john_doe" in status or "Welcome" in status
    print_healing_summary(page, "test_login_button_playwright")