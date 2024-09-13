from Pages.base_page import BasePage

class LandingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://knowit.se/"

    def navigate(self):
        self.page.goto(self.url)

    def dismiss_cookies(self):
        """
        Dismiss the cookie consent popup by clicking the 'Accept all' button.

        This function finds and clicks the button with the aria-label 'Godkänn alla'
        (Swedish for 'Accept all') to dismiss the cookie consent popup.
        """
        self.page.locator("[aria-label='Godkänn alla']").click()

    def find_new_job(self):
        """
        Navigate to the job search page.

        This function finds and clicks the link with the text 'Hitta ditt nya jobb här'
        (Swedish for 'Find your new job here') to navigate to the job search page.
        """
        self.page.get_by_role("link", name="Hitta ditt nya jobb här").click()