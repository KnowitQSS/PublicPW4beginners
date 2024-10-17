from playwright.sync_api import Page
from pytest_base_url.plugin import base_url


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://knowit.se/"

    @property
    def url_segment(self):
        return ""  # Base implementation returns an empty string


    def dismiss_cookies(self):
        """
        Dismiss the cookie consent popup by clicking the 'Accept all' button.

        This function finds and clicks the button with the aria-label 'Godkänn alla'
        (Swedish for 'Accept all') to dismiss the cookie consent popup.
        """
        self.page.locator("[aria-label='Godkänn alla']").click()


    def navigate_to(self):
        url = self.base_url + self.url_segment
        self.page.goto(url)