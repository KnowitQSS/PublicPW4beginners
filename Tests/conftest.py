import pytest
from playwright.sync_api import Playwright, Browser, Page, sync_playwright

from Pages.kontakt_page import KontaktPage


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


@pytest.fixture(scope="function")
def kontakt_page_fixture(page: Page):
    kontakt_page = KontaktPage(page)
    # Navigate to the contact page
    kontakt_page.navigate_to()
    kontakt_page.dismiss_cookies()
    yield kontakt_page