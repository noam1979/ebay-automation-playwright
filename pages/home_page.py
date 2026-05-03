from pages.base_page import BasePage

class HomePage(BasePage):
    """
    Handles the landing page and initial search.
    """
    SEARCH_INPUT = "//input[@id='gh-ac']"
    SEARCH_BUTTON = "//input[@id='gh-btn']"
    # Using a secondary page to avoid geo-blocking on the main home page
    URL = "https://www.ebay.com/n/all-categories"

    def open(self):
        self.navigate(self.URL)

    def search_for_product(self, product_name: str):
        self.page.wait_for_selector(self.SEARCH_INPUT, state="visible")
        self.fill_text(self.SEARCH_INPUT, product_name)
        self.click_element(self.SEARCH_BUTTON)