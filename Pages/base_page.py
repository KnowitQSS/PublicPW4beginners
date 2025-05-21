from Tests.conftest import test_context
from utils.common_imports import *
import os
from abc import abstractmethod
from datetime import datetime


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://knowit.se/"
        logger.info(f"Initializing {self.__class__.__name__}")


    @property
    @abstractmethod
    def url_segment(self) -> str:
        """
        Each child class must implement this property to define its URL segment.
        """
        raise NotImplementedError("Child classes must implement url_segment")

    def get_header(self):
        """
        Return the header component when needed.
        Import inside the method to avoid circular dependencies.
        """
        from Pages.headerComponent import HeaderComponent
        return HeaderComponent(self.page)

    def dismiss_cookies(self):
        """
        Dismiss the cookie consent popup by clicking the 'Accept all' button.

        This function finds and clicks the button with the aria-label 'Godkänn alla'
        (Swedish for 'Accept all') to dismiss the cookie consent popup.
        """
        self.page.locator("[aria-label='Godkänn alla']").click()

    def navigate_to(self):
        url = self.base_url + self.url_segment
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)



    def take_screenshot(self):
        """
        Take a screenshot of the current page.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Screenshots')

        try:
            # Ensure the directory for the path exists
            os.makedirs(screenshots_dir, exist_ok=True)
            path = os.path.join(screenshots_dir, f'{self.__class__.__name__}_{timestamp}.png')

            # Take the screenshot
            self.page.screenshot(path=path, full_page=True)
            logger.info(f"Screenshot saved to: {path}")

        except Exception as e:
            # Log the error (you might want to use a proper logging framework)
            print(f"Error taking screenshot: {e}")
