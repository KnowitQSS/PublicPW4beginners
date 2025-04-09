class HeaderComponent:
    def __init__(self, page):
        self.page = page

    def click_logo(self):
        # Click on the logo to return to landing page
        self.page.get_by_role("button", name="Till startsidan på Knowit").click()

    def search(self, search_term):
        # Click on search button to open search box
        self.page.locator(".chakra-button .chakra-text").get_by_text("sök").click()
        # Click on the "Sök" and "Ange ett sökord" text to focus on the search box
        self.page.get_by_role("searchbox", name="Ange ett sökord").fill(search_term)
        # Click Enter
        self.page.get_by_role("searchbox", name="Ange ett sökord").press("Enter")
        # Wait for URL to be updated
        self.page.wait_for_url("**/sok/?q=*")

    def open_menu(self):
        # Click on menu button to open menu overlay
        self.page.locator(".chakra-button .chakra-text").get_by_text("Meny").click()
        # This creates and returns a new MenuPage instance which enables fluent chaining (e.g. page.header.open_mnu().click_on_kontakt())
        from Pages.menu_page import MenuPage
        return MenuPage(self.page)