import random
import re

import pytest
from playwright.sync_api import Page, expect

from Pages.kontakt_page import KontaktPage
from Pages.landing_page import LandingPage
from Pages.lediga_jobb_page import LedigaJobbPage
from Pages.menu_page import MenuPage


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
    page.goto("https://knowit.se/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Knowit"))

def test_get_om_oss_link(page: Page):
    """
    This test verifies the "Om oss" (About us) link on the Knowit website.

    Args:
        page (Page): The Playwright Page object representing the browser context.

    Steps:
        1. Navigate to the Knowit website (https://knowit.se/).
        2. Accept the cookie pop-up by clicking the "Godkänn alla" (Accept all) button.
        3. Click the "Om oss" (About us) link.
        4. Verify that the page title contains the text "Om oss" (About us).

    This test case simulates the user flow of navigating to the "About us" section
    of the Knowit website. It verifies that clicking the "Om oss" link navigates
    the user to the correct page, as indicated by the presence of "Om oss" in the
    page title.
    """
    page.goto("https://knowit.se/")

    #Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    # Click the Om oss link.
    page.get_by_role("link", name="Om oss").click()

    # Expects page to have a heading with the name Om oss
    expect(page).to_have_title(re.compile("Om oss"))


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
    page.goto("https://knowit.se/")

    #Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    # Click the search button
   # page.get_by_role("button", name="Sök").click()
    page.locator(".chakra-button .chakra-text").get_by_text("sök").click()

    # Click on the "Sök" and write "test"
    page.get_by_role("searchbox", name="Ange ett sökord").fill("test")

    # Click Enter
    page.get_by_role("searchbox", name="Ange ett sökord").press("Enter")

    #page.wait_for_timeout(3000)     #So that you have visually time to see
    page.pause()
    # Assert that the url ends with /sok/q=test
    assert page.url.endswith("/sok/?q=test")


def test_hitta_ditt_nya_jobb(page: Page):
    """
    This function tests the "Hitta ditt nya jobb" (Find your new job) functionality on the Knowit website.

    Args:
        page (Page): The Playwright Page object representing the browser context.

    Steps:
        1. Navigate to the Knowit website (https://knowit.se/).
        2. Accept the cookie pop-up by clicking the "Godkänn alla" (Accept all) button.
        3. Click the "Hitta ditt nya jobb här" (Find your new job here) link.
        4. Click the "ort" (location) button to open the location dropdown.
        5. From the location dropdown options, click the option with the text "Lund".
        6. Assert that the current URL ends with "/karriar/lediga-jobb/?Ort=Lund",
           which indicates that the location filter has been applied correctly.

    This test case simulates the user flow of searching for job openings in Lund on the Knowit website.
    It verifies that the user can navigate to the job search page, select a location from the dropdown,
    and that the correct URL is loaded with the selected location as a query parameter.
    """
    page.goto("https://knowit.se/")

    # Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    page.get_by_role("link", name="Hitta ditt nya jobb här").click()

    page.get_by_role("button", name="ort").click()

    # Find the option with text "Quality Assurance"
    page.locator("#Dropdown-1-options .chakra-text").get_by_text("Lund").click()

    assert page.url.endswith("/karriar/lediga-jobb/?Ort=Lund")



def test_hitta_ditt_nya_jobb_POM(page: Page):
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

def test_go_to_kontakt_page(page:Page):
    kontakt_page = KontaktPage(page)
    landing_page = LandingPage(page)
    lediga_jobb = LedigaJobbPage(page)

    kontakt_page.navigate_to()
    kontakt_page.dismiss_cookies()
    lediga_jobb.navigate_to()
    landing_page.navigate_to()
    kontakt_page.navigate_to()
    kontakt_page.take_screenshot()

@pytest.fixture(scope="function")
def setup_pet_page(page) -> Page:
    # Define the path to the local AddPet HTML file
    add_pet_file_path = "file:///C:/Users/magwal/projects/PlayWrightForBeginners/petstore/AddPet.html"

    # Generate a random Pet ID between 2000 and 3000
    pet_id = random.randint(2000, 3000)
    # Generate a random Pet Name
    # pet_name = f"Pet{random.randint(1000, 9999)}"
    pet_name = "Magnus"
    # Define the Photo URL
    photo_url = "https://images.dog.ceo/breeds/corgi-cardigan/n02113186_11035.jpg"

    # Print the Pet ID to the console
    print(f"Generated Pet ID: {pet_id}")

    # Open the AddPet page
    page.goto(add_pet_file_path)
    # Fill in the Pet ID, Pet Name, and Photo URL
    page.fill("#petId", str(pet_id))
    page.fill("#petName", pet_name)
    page.fill("#photoUrl", photo_url)
    # Click the PostPet button
    page.click("#postPetButton")

    # Wait for a success message or some indication that the pet was added
    page.wait_for_selector("text=Pet added successfully")
    yield {"page": page, "pet_id": pet_id, "pet_name": pet_name, "photo_url": photo_url}
    delete_button = page.get_by_role(role="button", name="Delete Pet")

    delete_button.wait_for(timeout=3000, state="visible")
    delete_button.click()
    page.get_by_text("Pet deleted successfully.").wait_for(timeout=3000, state="visible")

def test_add_and_get_pet(setup_pet_page):

    pet_data = setup_pet_page
    page = pet_data['page']
    # Define the path to the local GetPet HTML file
    get_pet_file_path = "file:///C:/Users/magwal/projects/PlayWrightForBeginners/petstore/GetPet.html"

    # Construct the URL with the PetID parameter for the GetPet page
    get_pet_url = f"{get_pet_file_path}?petid={pet_data['pet_id']}"
    # Open the GetPet page
    page.goto(get_pet_url)
    # Wait for either the image or the message to be visible
    page.wait_for_selector('img, .message', state='visible')

    # Add assertions or further interactions as needed
    assert page.locator('img').is_visible() or page.locator('.message').is_visible()
    if page.locator('img').is_visible():
        assert page.locator('img').get_attribute('src') == pet_data['photo_url']

    assert page.locator('#pet-name').inner_text().endswith("Magnus")


