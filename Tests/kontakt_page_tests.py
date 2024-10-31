from playwright.sync_api import Page
from Pages.kontakt_page import KontaktPage
from Pages.landing_page import LandingPage
from Pages.menu_page import MenuPage


def test_does_address_exist(page: Page):
    # Initialize page objects for different sections of the website
    landing_page = LandingPage(page)
    menu_page = MenuPage(page)
    kontakt_page = KontaktPage(page)

    # Navigate to the landing page
    landing_page.navigate_to()
    # Dismiss any cookie consent dialogs
    landing_page.dismiss_cookies()

    # Navigate to the contact page through the menu
    menu_page.navigate_to()
    menu_page.click_on_kontakt()

    # On the contact page, select the town "Lund"
    kontakt_page.click_on_town("Lund")
    # Assert that the address "Mobilvägen 10" exists for Lund
    assert kontakt_page.does_address_exist("Mobilvägen 10")


def test_all_locations_exist(page: Page):
    # Initialize page object for kontakt page
    kontakt_page = KontaktPage(page)

    # Navigate to the contact page
    kontakt_page.navigate_to()
    kontakt_page.dismiss_cookies()

    # Get a list of all the locations from location buttons
    locations_list = kontakt_page.extract_locations_from_button_texts()

    # Loop through the list, click on each button and assert that the name of the location shows up on page
    for location in locations_list:
        kontakt_page.click_on_town(location)
        assert kontakt_page.does_location_exist(location)
