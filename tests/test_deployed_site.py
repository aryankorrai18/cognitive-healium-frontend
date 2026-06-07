"""
Production Integration Test.
Runs against the live deployed GitHub Pages site.
Triggered automatically after deploy.yml completes.
"""

import os
import pytest
from playwright.sync_api import sync_playwright

from healium import SelfHealingPage, HealiumMemory

DEPLOYED_URL = os.getenv(
    "DEPLOYED_URL",
    "https://aryankorrai18.github.io/cognitive-healium/",
)


@pytest.mark.healium
def test_deployed_search_input():
    """QA expects #search-input. If dev changed it, the SDK heals it automatically."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        memory = HealiumMemory(tenant_id="production-ci")
        healing_page = SelfHealingPage(page, memory=memory)

        healing_page.goto(DEPLOYED_URL)

        actual_id = page.evaluate("document.querySelector('input').id")
        print(f"\n===== LIVE SITE INPUT ID: '{actual_id}' =====\n")

        healing_page.fill(
            "#search-input",
            "Healium healed production!",
            intent="product search input field",
        )

        value = page.evaluate("document.querySelector('input').value")
        assert value == "Healium healed production!", f"Unexpected value: {value}"

        if healing_page.healing_events:
            event = healing_page.healing_events[0]
            print(
                f"\n===== HEALING OCCURRED! "
                f"{event.original_locator} -> {event.healed_locator} "
                f"(conf: {event.confidence:.0%}) =====\n"
            )
        else:
            print("\n===== NO HEALING NEEDED (element found normally) =====\n")

        browser.close()
