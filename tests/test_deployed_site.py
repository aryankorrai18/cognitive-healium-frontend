"""
Production E2E test — runs against the live deployed site.
Looks like a normal Playwright test. Healing is invisible.
"""

import os

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium/"
)


def test_search_input(page):
    """QA expects #search-input. If dev changed it, Healium auto-heals."""
    page.goto(DEPLOYED_URL)
    page.fill("#search-input", "Healium healed production!", intent="product search input field")

    value = page.locator("input").input_value()
    assert value == "Healium healed production!"