from Pages.base_page import BasePage

class KontaktPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://knowit.se/kontakt"

    def navigate(self):
        self.page.goto(self.url)

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