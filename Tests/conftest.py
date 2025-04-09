import os
import pytest
from datetime import datetime
from playwright.sync_api import Playwright, Browser, Page, BrowserContext, sync_playwright
from utils.logger_config import TestLogger


# Global variables to track the current context
class TestContext:
    current_page = None
    current_selector = None
    current_action = None
test_context = TestContext()


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

    def click_with_logging(selector, **kwargs):
        logger.info(f"Clicking on selector: {selector}")
        test_context.current_selector = selector
        test_context.current_action = "click"
        return original_click(selector, **kwargs)

    page.click = click_with_logging

    original_fill = page.fill

    def fill_with_logging(selector, value, **kwargs):
        logger.info(f"Filling selector: {selector}")
        test_context.current_selector = selector
        test_context.current_action = "fill"
        return original_fill(selector, value, **kwargs)

    page.fill = fill_with_logging

    yield page
    logger.info("Closing page")
    page.close()
    test_context.current_page = None





# Hook that runs when a test fails
@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    logger = TestLogger().get_logger()
    logger.error(f"Test failed: {node.name}")

    # Get error details
    excinfo = call.excinfo
    if excinfo:
        logger.error(f"Exception type: {excinfo.typename}")
        logger.error(f"Exception message: {excinfo.value}")

    # Log the current context information
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

