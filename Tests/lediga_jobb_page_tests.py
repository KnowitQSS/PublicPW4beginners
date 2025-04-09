from playwright.sync_api import Page
from Pages.landing_page import LandingPage
from Pages.lediga_jobb_page import LedigaJobbPage


def test_hitta_ditt_nya_jobb(page: Page):
    """
        This test verifies the find new job in a specific city on the Knowit website. This time using a POM structure

        Args:
            page (Page): The Playwright Page object representing the browser context.

        Steps:
            1. Navigate to the Knowit website (https://knowit.se/).
            2. Accept the cookie pop-up by clicking the "Godkänn alla" (Accept all) button.
            3. Click the "Hitta ditt nya jobb här" link.
            4. Click on dropdown "Ort" to be able to filter
            5. Select "Lund" in the dropdown
            6. Assert that the current URL ends with ""lediga-jobb/?Ort=Lund"", indicating that
               the search was performed correctly.

        This test case simulates the user flow of navigating to the find new job on the Knowit website.
        It verifies that the user can use the city filter, select a city i the dropdown, and that the
        correct URL with the filter query parameter is loaded.
        """

    landing_page = LandingPage(page)
    lediga_jobb_page = LedigaJobbPage(page)

    #Steps 1-3:
    landing_page.navigate_to()
    landing_page.dismiss_cookies()
    landing_page.find_new_job()

    #Steps 4-6
    lediga_jobb_page.filter_jobs_for_city("Lund")

    # Assert that the url ends with "lediga-jobb/?Ort=Lund"
    assert page.url.endswith("/karriar/lediga-jobb/?Ort=Lund")
