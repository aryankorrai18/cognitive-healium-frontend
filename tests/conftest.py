"""
conftest.py — Makes self-healing invisible.

When you run:  pytest --healium-enabled
  → page.fill() and page.click() auto-heal broken locators

When you run:  pytest
  → page is a normal Playwright page (no healing)
"""

import pytest


@pytest.fixture
def page(context, _healium_enabled, healium_memory, healium_providers):
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