from Pages.base_page import BasePage

class MenuPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def click_on_kontakt(self):
        # Find and click the "Kontakt" (Contact) link
        # The link is located by its role ("link") and its name attribute or text content ("Kontakt")
        self.page.get_by_role("link", name="Kontakt").click()