import pytest
from playwright.sync_api import Playwright, Browser, Page, sync_playwright

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    page = browser.new_page()
    yield page
    page.close()