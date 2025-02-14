from Pages.base_page import BasePage
from typing import List


class KontaktPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @property
    def url_segment(self) -> str:
        return "/kontakt"

    def click_on_town(self, city):
        # Click on a button representing a specific city
        # The button is identified by its role ("button") and name attribute or text content (city)
        # The city parameter allows this method to be used for different towns/cities
        self.page.get_by_role("button", name=city).click()


    def does_address_exist(self, address):
        # Check if a specific address exists on the page
        # The address is expected to be in a heading element
        address_selector = self.page.get_by_role(role="heading", name=address)

        try:
            # Wait for up to 3 seconds (3000 ms) for the address to become visible
            address_selector.wait_for(timeout=3000, state="visible")
            # If the address becomes visible within the timeout, return True
            return True
        except:
            # If the address doesn't appear (timeout occurs), return False
            # This could be due to the address not existing or not being visible within 3 seconds
            return False

    def does_location_exist(self, location):
        # Check if a specific location exists on the page
        # The location is expected to be in a heading element
        location_selector = self.page.get_by_role(role="heading", name=location).first

        try:
            location_selector.wait_for(timeout=3000, state="visible")
            return True
        except:
            # If the location doesn't appear (timeout occurs), return False
            # This could be due to the location not existing or not being visible within 3 seconds
            self.take_screenshot()
            return False

    def extract_locations_from_button_texts(self) -> List[str]:
        """
        Extracts text from all buttons with class 'css-dm8w6v' within a div.

        Returns:
            List[str]: List of button texts
        """
        # Wait for the container to be present
        self.page.locator('div.css-1psz1ok').wait_for()

        # Get all buttons with the specified class
        buttons = self.page.locator('button.css-dm8w6v').all()

        # Extract text from each button
        return [button.inner_text() for button in buttons]
