import re

from playwright.sync_api import Page, expect
from Pages.landing_page import LandingPage


def test_has_title(page: Page):
    """
    This test verifies the title of the Knowit website.

    Args:
        page (Page): The Playwright Page object representing the browser context.

    Steps:
        1. Navigate to the Knowit website (https://knowit.se/).
        2. Verify that the page title contains the substring "Knowit".

    This test case checks if the title of the Knowit website homepage contains
    the expected text "Knowit". The test passes if the page title contains the
    substring "Knowit", regardless of the rest of the title text.
    """

    landing_page = LandingPage(page)
    # Navigate to the landing page
    landing_page.navigate_to()
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Knowit"))


def test_search_test(page: Page):
    """
    This test verifies the search functionality on the Knowit website.

    Args:
        page (Page): The Playwright Page object representing the browser context.

    Steps:
        1. Navigate to the Knowit website (https://knowit.se/).
        2. Accept the cookie pop-up by clicking the "Godkänn alla" (Accept all) button.
        3. Click the "sök" (search) button.
        4. Enter the search term "test" in the search box.
        5. Press the "Enter" key to submit the search.
        6. Wait for 3 seconds to visually observe the search results.
        7. Assert that the current URL ends with "/sok/?q=test", indicating that
           the search was performed correctly.

    This test case simulates the user flow of performing a search on the Knowit website.
    It verifies that the user can enter a search term, submit the search, and that the
    correct URL with the search query parameter is loaded.
    """
    landing_page = LandingPage(page)
    # Navigate to the landing page
    landing_page.navigate_to()
    # Dismiss any cookie consent dialogs
    landing_page.dismiss_cookies()

    # Get the header component (can be done from any page)
    header = landing_page.get_header()

    header.search("test")

    # Assert that the url ends with /sok/q=test
    assert page.url.endswith("/sok/?q=test")



