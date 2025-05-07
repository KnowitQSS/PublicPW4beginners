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

        # Alias role-based methods
        self.click_by_role = self.click_by_role_with_logging
        self.fill_by_role = self.fill_by_role_with_logging
        self.select_option_by_role = self.select_option_by_role_with_logging

        # Store original methods
        self.original_click = page.click
        self.original_fill = page.fill
        self.original_type = page.type
        self.original_press = page.press
        self.original_select_option = page.select_option
        self.original_check = page.check

        # Override page methods with wrapped versions
        page.click = self.click_with_logging
        page.fill = self.fill_with_logging
        page.type = self.type_with_logging
        page.press = self.press_with_logging
        page.select_option = self.select_option_with_logging
        page.check = self.check_with_logging

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

    def click_by_role_with_logging(self, role: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = self.page.get_by_role(role, name=name) if name else self.page.get_by_role(role)

            try:
                element_info = self.extract_element_info(element)
                details = f" ({', '.join(element_info)})" if element_info else ""
            except Exception:
                details = ""

            logger.info(f"Clicking element by {role_desc}{details}")

            test_context.current_selector = f"{role_desc}"
            test_context.current_action = "click_by_role"
            return element.click(**kwargs)
        except Exception as e:
            logger.error(f"Failed to click element by {role_desc}: {str(e)}")
            raise

    def fill_by_role_with_logging(self, role: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = self.page.get_by_role(role, name=name) if name else self.page.get_by_role(role)

            try:
                element_info = self.extract_element_info(element)
                details = f" ({', '.join(element_info)})" if element_info else ""
            except Exception:
                details = ""

            logger.info(f"Filling element by {role_desc}{details}")

            test_context.current_selector = f"{role_desc}"
            test_context.current_action = "fill_by_role"
            return element.fill(**kwargs)
        except Exception as e:
            logger.error(f"Failed to fill element by {role_desc}: {str(e)}")
            raise

    def select_option_by_role_with_logging(self, role: str, value: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = self.page.get_by_role(role, name=name) if name else self.page.get_by_role(role)

            try:
                element_info = self.extract_element_info(element)
                details = f" ({', '.join(element_info)})" if element_info else ""
            except Exception:
                details = ""

            logger.info(f"Selecting option '{value}' in element by {role_desc}{details}")

            test_context.current_selector = f"{role_desc}"
            test_context.current_action = "select_option_by_role"
            return element.select_option(value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to select option in element by {role_desc}: {str(e)}")
            raise

    def extract_element_info(self, element):
        """Helper function to extract common element information"""
        element_info = []

        text = element.text_content()
        if text and text.strip():
            element_info.append(f"text='{text.strip()}'")

        for attr in ['role', 'name', 'type', 'id', 'class', 'aria-label', 'title', 'data-testid', 'value',
                     'placeholder']:
            value = element.get_attribute(attr)
            if value:
                element_info.append(f"{attr}='{value}'")

        for style in ['display', 'visibility', 'pointer-events']:
            value = element.evaluate(f'el => getComputedStyle(el).{style}')
            if value and value not in ['initial', 'inherit']:
                element_info.append(f"style-{style}='{value}'")

        is_visible = element.is_visible()
        is_enabled = element.is_enabled()
        is_editable = element.is_editable()
        if not is_visible:
            element_info.append("not visible")
        if not is_enabled:
            element_info.append("disabled")
        if is_editable:
            element_info.append("editable")

        bbox = element.bounding_box()
        if bbox:
            element_info.append(f"position=(x:{bbox['x']:.0f},y:{bbox['y']:.0f})")

        return element_info

    def click_with_logging(self, selector, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Clicking on '{selector}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "click"
            return self.original_click(selector, **kwargs)
        except Exception as e:
            logger.error(f"Failed to click '{selector}': {str(e)}")
            raise

    def fill_with_logging(self, selector, value, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Filling '{selector}' with value '{value}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "fill"
            return self.original_fill(selector, value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to fill '{selector}': {str(e)}")
            raise

    def type_with_logging(self, selector, text, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Typing '{text}' into '{selector}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "type"
            return self.original_type(selector, text, **kwargs)
        except Exception as e:
            logger.error(f"Failed to type into '{selector}': {str(e)}")
            raise

    def press_with_logging(self, selector, key, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Pressing '{key}' on '{selector}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "press"
            return self.original_press(selector, key, **kwargs)
        except Exception as e:
            logger.error(f"Failed to press '{key}' on '{selector}': {str(e)}")
            raise

    def select_option_with_logging(self, selector, value, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Selecting option '{value}' in '{selector}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "select_option"
            return self.original_select_option(selector, value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to select option in '{selector}': {str(e)}")
            raise

    def check_with_logging(self, selector, **kwargs):
        try:
            element = self.page.locator(selector)
            element_info = self.extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"Checking checkbox '{selector}'{details}")

            test_context.current_selector = selector
            test_context.current_action = "check"
            return self.original_check(selector, **kwargs)
        except Exception as e:
            logger.error(f"Failed to check '{selector}': {str(e)}")
            raise

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
