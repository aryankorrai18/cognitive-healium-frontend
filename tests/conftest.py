"""
conftest.py — Shared fixtures for all test scripts.

Makes self-healing invisible:
  pytest --healium-enabled  → page.fill() auto-heals broken locators
  pytest                   → page is a normal Playwright page
"""

import pytest

@pytest.fixture
def page(context, _healium_enabled, healium_memory, healium_providers):
    """Override pytest-playwright's page fixture with SelfHealingPage."""
    raw_page = context.new_page()

    if not _healium_enabled or healium_memory is None:
        yield raw_page
    else:
        from healium.healing_agent import SelfHealingPage
        cache, storage, event_store = healium_providers
        hp = SelfHealingPage(
            page=raw_page,
            memory=healium_memory,
            tenant_id=healium_memory.tenant_id,
            cache_provider=cache,
            storage_provider=storage,
            event_store=event_store,
        )
        yield hp

    raw_page.close()


@pytest.fixture
def h(healing_driver_factory):
    """Self-healing Selenium driver — ready to use."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts)
    healing = healing_driver_factory(driver)
    yield healing
    driver.quit()


def print_healing_summary(page_or_driver, test_name: str):
    """Print a clear summary of what the agent healed — visible in CI logs."""
    healed = hasattr(page_or_driver, 'healing_events') and len(page_or_driver.healing_events) > 0
    if healed:
        for event in page_or_driver.healing_events:
            print(f"\n{'='*60}")
            print(f"  SELF-HEALING ACTIVATED in {test_name}")
            print(f"  Broken locator : {event.original_locator}")
            print(f"  Healed to       : {event.healed_locator}")
            print(f"  Confidence      : {event.confidence:.0%}")
            print(f"  Source          : {event.source}")
            print(f"  AI Reasoning    : {event.reasoning}")
            print(f"{'='*60}\n")
    else:
        print(f"\n  [{test_name}] Element found normally (no healing needed)\n")
    return healed