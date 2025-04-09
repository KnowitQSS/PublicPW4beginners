from playwright.sync_api import Page, expect


def test_get_om_oss_link(page: Page):
    """
    This test verifies the "Om oss" (About us) link on the Knowit website.

    Args:
        page (Page): The Playwright Page object representing the browser context.

    Steps:
        1. Navigate to the Knowit website (https://knowit.se/).
        2. Accept the cookie pop-up by clicking the "Godkänn alla" (Accept all) button.
        3. Click the "Om oss" (About us) link.
        4. Verify that the page title contains the text "Om oss" (About us).

    This test case simulates the user flow of navigating to the "About us" section
    of the Knowit website. It verifies that clicking the "Om oss" link navigates
    the user to the correct page, as indicated by the presence of "Om oss" in the
    page title.
    """
    page.goto("https://knowit.se/")

    #Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    # Click the Om oss link.
    page.get_by_role("link", name="Om oss").click()

    # Expects page to have a heading with the name Om oss
    expect(page.get_by_role("heading", name="Om oss")).to_be_visible()
