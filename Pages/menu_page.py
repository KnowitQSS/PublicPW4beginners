from Pages.base_page import BasePage

class MenuPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_on_menu(self):
        # Find and click the "Meny" (Menu) button
        # The button is located using a combination of CSS selectors and text content
        # It looks for an element with classes "chakra-button" and "chakra-text" that contains the text "Meny"
        self.page.locator(".chakra-button .chakra-text").get_by_text("Meny").click()


    def click_on_kontakt(self):
        # Find and click the "Kontakt" (Contact) link
        # The link is located by its role ("link") and its name attribute or text content ("Kontakt")
        self.page.get_by_role("link", name="Kontakt").click()