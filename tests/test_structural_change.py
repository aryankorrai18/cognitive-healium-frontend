"""
Scenario 3: Structural Change
Using brittle structural XPaths that break when the DOM structure changes.
"""

import os
import time
from tests.conftest import print_healing_summary

# Added cache-buster ?v=timestamp to bypass GitHub Pages CDN caching
DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium-frontend/"
) + f"?v={int(time.time())}"


def test_username_input_wrapped_playwright(page):
    """Username input is now inside .form-wrapper > .input-container. 
       Brittle XPath //div[@class='card']/input will FAIL because it's no longer a direct child."""
    page.goto(DEPLOYED_URL)

    # FIXED: Changed card[2] to card[3] to target the Login card (3rd card on page)
    page.fill("//div[@class='card'][3]/input", "john_doe", intent="username input field")

    value = page.evaluate("""() => {
        const el = document.querySelector('#username');
        return el ? el.value : '';
    }""")
    assert value == "john_doe"
    print_healing_summary(page, "test_username_input_wrapped_playwright")


def test_login_button_playwright(page):
    """Login button — testing structural XPath for the button as well."""
    page.goto(DEPLOYED_URL)

    # FIXED: Changed card[2] to card[3]
    page.fill("//div[@class='card'][3]/input", "john_doe", intent="username input field")
    page.click("//div[@class='card'][3]/button", intent="login submit button")

    status = page.evaluate("""() => {
        const el = document.querySelector('#login-status');
        return el ? el.innerText : '';
    }""")
    assert "john_doe" in status or "Welcome" in status
    print_healing_summary(page, "test_login_button_playwright")