import os
from abc import abstractmethod
from datetime import datetime

from playwright.sync_api import Page
from pytest_base_url.plugin import base_url


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://knowit.se/"

    @property
    @abstractmethod
    def url_segment(self) -> str:
        """
        Each child class must implement this property to define its URL segment.
        """
        raise NotImplementedError("Child classes must implement url_segment")

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

    import os
    from datetime import datetime

    def take_screenshot(self, path=None):
        """
        Take a screenshot of the current page.

        Args:
            path (str, optional): Custom path for the screenshot.
                                   Defaults to None.

        Returns:
            str: Path where the screenshot was saved
        """
        # Create screenshots directory if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)

        # Generate a unique filename if no path is provided
        if not path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join('screenshots', f'screenshot_{self.__class__.__name__}_{timestamp}.png')

        try:
            # Ensure the directory for the path exists
            os.makedirs(os.path.dirname(path), exist_ok=True)

            # Take the screenshot
            self.page.screenshot(path=path, full_page=True)

            return path
        except Exception as e:
            # Log the error (you might want to use a proper logging framework)
            print(f"Error taking screenshot: {e}")
            return None
