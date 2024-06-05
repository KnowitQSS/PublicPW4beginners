import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://knowit.se/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Knowit"))

def test_get_om_oss_link(page: Page):
    page.goto("https://knowit.se/")

    #Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    # Click the Om oss link.
    page.get_by_role("link", name="Om oss").click()

    # Expects page to have a heading with the name Om oss
    expect(page).to_have_title(re.compile("Om oss"))


def test_search_test(page: Page):
    page.goto("https://knowit.se/")

    #Accept the cookie pop-up
    page.locator("[aria-label='Godkänn alla']").click()

    # Click the search button
    page.get_by_role("button", name="Sök").click()

    # Click on the "Sök" and write "test"
    page.get_by_role("searchbox", name="Ange ett sökord").fill("test")

    # Click Enter
    page.get_by_role("searchbox", name="Ange ett sökord").press("Enter")

    page.wait_for_timeout(3000)     #So that you have visually time to see

    # Assert that the url ends with /sok/q=test
    assert page.url.endswith("/sok/?q=test")