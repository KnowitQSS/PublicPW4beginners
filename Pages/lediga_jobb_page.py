from Pages.base_page import BasePage

class LedigaJobbPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @property
    def url_segment(self):
        return "/karriar/lediga-jobb"

    def filter_jobs_for_city(self, city):
        """
        Filter job listings by city.

        This function applies a city filter to the job listings:
        1. It opens the 'Ort' (Location) dropdown menu.
        2. It then selects the specified city from the dropdown options.

        Args:
            city (str): The name of the city to filter by.
        """
        # Click on dropdown "Ort" to be able to filter
        #self.page.locator(".chakra-button .chakra-text").get_by_text("Ort").click()
        self.page.get_by_role("button", name="ort").click()

        # Select "city" in the dropdown
        self.page.locator("#Dropdown-1-options .chakra-text").get_by_text(city).click()