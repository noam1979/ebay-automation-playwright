import random
from pages.base_page import BasePage

class ItemPage(BasePage):
    """
    Handles item details and adding to cart with random variants.
    """
    VARIANT_DROPDOWNS = "//select[contains(@class, 'msku-sel')]"
    ADD_TO_CART_BTN = "//a[@id='atcRedesignId_btn']"

    def add_items_to_cart(self, urls: list):
        for i, url in enumerate(urls):
            self.navigate(url)
            self._select_random_variants()
            # Requirement: Save screenshot for each item added
            self.page.screenshot(path=f"screenshots/item_{i+1}.png")
            self.click_element(self.ADD_TO_CART_BTN)
            self.page.wait_for_load_state("networkidle")

    def _select_random_variants(self):
        dropdowns = self.page.query_selector_all(self.VARIANT_DROPDOWNS)
        for d in dropdowns:
            options = [o.get_attribute("value") for o in d.query_selector_all("option") 
                       if o.get_attribute("value") and o.get_attribute("value") != "-1"]
            if options:
                d.select_option(value=random.choice(options))
                self.page.wait_for_timeout(500)