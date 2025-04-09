from utils.common_imports import *
from Pages.kontakt_page import KontaktPage
from Pages.landing_page import LandingPage
from Pages.lediga_jobb_page import LedigaJobbPage
from utils.logger_config import TestLogger

@pytest.fixture(scope="function")
def kontakt_page_fixture(page: Page):
    logger = TestLogger().get_logger()
    logger.info("Initializing KontaktPage")
    kontakt_page = KontaktPage(page)
    logger.info("Navigating to contact page")
    kontakt_page.navigate_to()
    logger.info("Dismissing cookies")
    kontakt_page.dismiss_cookies()
    yield kontakt_page
    logger.info("Finished with KontaktPage")

def test_go_to_kontakt_page(page:Page):
    kontakt_page = KontaktPage(page)
    landing_page = LandingPage(page)
    lediga_jobb = LedigaJobbPage(page)

    kontakt_page.navigate_to()
    kontakt_page.dismiss_cookies()
    lediga_jobb.navigate_to()
    landing_page.navigate_to()
    kontakt_page.navigate_to()


def test_does_address_exist(page: Page):
    # Initialize page objects for different sections of the website
    landing_page = LandingPage(page)
    kontakt_page = KontaktPage(page)

    # Navigate to the landing page
    landing_page.navigate_to()
    # Dismiss any cookie consent dialogs
    landing_page.dismiss_cookies()

    # Get the header component (can be done from any page)
    header = landing_page.get_header()

    # Navigate to the contact page through the menu
    menu_page = header.open_menu()
    menu_page.click_on_kontakt()

    # On the contact page, select the town "Lund"
    kontakt_page.click_on_town("Lund")
    # Assert that the address "Mobilvägen 10" exists for Lund
    assert kontakt_page.does_address_exist("Mobilvägen 10")

@pytest.mark.trace
def test_all_locations_exist(page: Page, kontakt_page_fixture):

    logger.info("Starting test_all_locations_exist")
    # Get a list of all the locations from location buttons
    locations_list = kontakt_page_fixture.extract_locations_from_button_texts()

    # Loop through the list, click on each button and assert that the name of the location shows up on page
    for location in locations_list:
        logger.info(f"Checking if location '{location}' exists on the page")
        kontakt_page_fixture.click_on_town(location)
        assert kontakt_page_fixture.does_location_exist(location)

    # And now let the test fail so that we also can test the screenshot functionality
    assert kontakt_page_fixture.does_location_exist("Zanzibar")
