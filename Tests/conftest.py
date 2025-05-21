import os
import pytest
import time
from datetime import datetime, timedelta
from playwright.sync_api import Playwright, Browser, Page, BrowserContext, sync_playwright
from utils.logger_config import TestLogger

# Global variables to track the current context
class TestContext:
    current_page = None
    current_selector = None
    current_action = None
test_context = TestContext()

# Configuration for log retention
LOG_RETENTION_DAYS = 30  # Change this value as needed

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    logger = TestLogger().get_logger()
    logger.info("Starting new browser session")
    browser = playwright.chromium.launch(headless=False)
    yield browser
    logger.info("Closing browser session")
    browser.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    logger = TestLogger().get_logger()
    logger.info("Creating new page")
    page = context.new_page()
    # Store the page in our global context
    test_context.current_page = page

    # Override certain methods to track selectors
    original_click = page.click
    original_fill = page.fill
    original_type = page.type
    original_press = page.press
    original_select_option = page.select_option
    original_check = page.check

    def click_with_logging(selector, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Clicking", selector, element, logger, **kwargs)

            test_context.current_selector = selector
            test_context.current_action = "click"
            return original_click(selector, **kwargs)
        except Exception as e:
            logger.error(f"Failed to click '{selector}': {str(e)}")
            raise
    page.click = click_with_logging

    def fill_with_logging(selector, value, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Filling", selector, element, logger, **kwargs)

            test_context.current_selector = selector
            test_context.current_action = "fill"
            return original_fill(selector, value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to fill '{selector}' with value '{value}': {str(e)}")
            raise
    page.fill = fill_with_logging

    def type_with_logging(selector, text, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Typing", selector, element, logger, **kwargs)
            test_context.current_selector = selector
            test_context.current_action = "type"
            return original_type(selector, text, **kwargs)
        except Exception as e:
            logger.error(f"Failed to type into '{selector}': {str(e)}")
            raise
    page.type = type_with_logging

    def press_with_logging(selector, key, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Pressing", selector, element, logger, **kwargs)
            test_context.current_selector = selector
            test_context.current_action = "press"
            return original_press(selector, key, **kwargs)
        except Exception as e:
            logger.error(f"Failed to press '{key}' on '{selector}': {str(e)}")
            raise
    page.press = press_with_logging

    def select_option_with_logging(selector, value, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Selecting option", selector, element, logger, **kwargs)
            test_context.current_selector = selector
            test_context.current_action = "select_option"
            return original_select_option(selector, value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to select option in '{selector}': {str(e)}")
            raise
    page.select_option = select_option_with_logging

    def check_with_logging(selector, **kwargs):
        try:
            element = page.locator(selector)
            log_element_details("Checkking", selector, element, logger, **kwargs)
            test_context.current_selector = selector
            test_context.current_action = "check"
            return original_check(selector, **kwargs)
        except Exception as e:
            logger.error(f"Failed to check '{selector}': {str(e)}")
            raise
    page.check = check_with_logging

    def click_by_role_with_logging(role: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = page.get_by_role(role, name=name) if name else page.get_by_role(role)

            try:
                element_info = extract_element_info(element)
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
    page.click_by_role = click_by_role_with_logging

    def fill_by_role_with_logging(self, role: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = page.get_by_role(role, name=name) if name else page.get_by_role(role)

            try:
                element_info = extract_element_info(element)
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
    page.fill_by_role = fill_by_role_with_logging

    def select_option_by_role_with_logging(self, role: str, value: str, name: str = None, **kwargs):
        role_desc = f"role='{role}'"
        if name:
            role_desc += f", name='{name}'"

        try:
            element = page.get_by_role(role, name=name) if name else page.get_by_role(role)

            try:
                element_info = extract_element_info(element)
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
    page.select_option = select_option_by_role_with_logging

    def log_element_details(action, selector, element, logger, **kwargs):
        try:
            element_info = extract_element_info(element)
            details = f" ({', '.join(element_info)})" if element_info else ""
            logger.info(f"{action} on '{selector}'{details}")
        except Exception as e:
            logger.warning(f"Failed to log details for '{selector}': {str(e)}")

    yield page
    logger.info("Closing page")
    page.close()
    test_context.current_page = None

def extract_element_info(element):
        """Helper function to extract common element information"""
        element_info = []

        # Get element text content
        text = element.text_content()
        if text and text.strip():
            element_info.append(f"text='{text.strip()}'")

        # Get common HTML attributes
        for attr in ['role', 'name', 'type', 'id', 'class', 'aria-label', 'title', 'data-testid', 'value', 'placeholder']:
            value = element.get_attribute(attr)
            if value:
                element_info.append(f"{attr}='{value}'")

        # Get computed styles
        for style in ['display', 'visibility', 'pointer-events']:
            value = element.evaluate(f'el => getComputedStyle(el)["{style}"]')
            if value and value not in ['initial', 'inherit']:
                element_info.append(f"style-{style}='{value}'")

        # Check element state
        is_visible = element.is_visible()
        if not is_visible:
            element_info.append("not visible")

        # Log element position
        bbox = element.bounding_box()
        if bbox:
            element_info.append(f"position=(x:{bbox['x']:.0f},y:{bbox['y']:.0f})")

        return element_info

def delete_old_files(directory, retention_days):
    """Delete files in the specified directory older than the retention period."""
    if not os.path.exists(directory):
        return

    now = time.time()
    cutoff = now - (retention_days * 86400)  # Convert days to seconds

    for filename in os.listdir(directory):
        if filename == ".gitkeep":
            continue  # Skip the .gitkeep file

        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                try:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

def pytest_sessionstart(session):
    """Hook to clean up old files at the start of a test session."""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Directories to clean
    directories_to_clean = [
        os.path.join(base_dir, 'logs'),
        os.path.join(base_dir, 'screenshots'),
        os.path.join(base_dir, 'traces'),
        os.path.join(base_dir, 'page_dumps'),
    ]

    for directory in directories_to_clean:
        delete_old_files(directory, LOG_RETENTION_DAYS)

def pytest_runtest_logstart(nodeid, location):
    logger = TestLogger().get_logger()
    logger.info(f"Test '{nodeid}' started")

# Hook that runs when a test fails
@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    logger = TestLogger().get_logger()
    logger.error(f"Test failed: {node.name}")

    if test_context.current_page:
        try:
            url = test_context.current_page.url
            logger.error(f"Current page URL: {url}")

            if test_context.current_selector:
                logger.error(f"Last used selector: {test_context.current_selector}")
            if test_context.current_action:
                logger.error(f"Last action performed: {test_context.current_action}")

            # Capture a screenshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)

            screenshot_path = os.path.join(screenshots_dir, f"failure_{node.name}_{timestamp}.png")
            test_context.current_page.screenshot(path=screenshot_path)
            logger.error(f"Screenshot saved to: {screenshot_path}")

            # Capture page HTML
            html_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'page_dumps')
            os.makedirs(html_dir, exist_ok=True)

            html_path = os.path.join(html_dir, f"failure_{node.name}_{timestamp}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(test_context.current_page.content())
            logger.error(f"Page HTML saved to: {html_path}")

        except Exception as e:
            logger.error(f"Failed to capture diagnostic information: {str(e)}")
    else:
        logger.warning("No current page available to capture diagnostics.")

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "trace: mark test to enable Playwright tracing")


@pytest.fixture(scope="function")
def context(browser: Browser, request):
    """Create a new browser context with tracing configured based on marker."""
    context = browser.new_context()

    # Check if test is marked for tracing
    if request.node.get_closest_marker("trace"):
        # Create traces directory if it doesn't exist
        traces_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'traces')
        os.makedirs(traces_dir, exist_ok=True)

        # Generate trace file name based on test name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_file = os.path.join(traces_dir, f"{request.node.name}_{timestamp}.zip")

        # Start tracing
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

    yield context

    # Stop and save trace if enabled
    if request.node.get_closest_marker("trace"):
        context.tracing.stop(path=trace_file)

    context.close()

