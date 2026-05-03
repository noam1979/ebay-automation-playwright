from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Validates the final cart total.
    """
    CART_URL = "https://cart.ebay.com"
    TOTAL_PRICE_SELECTOR = "//div[@data-test-id='SUBTOTAL']//span"

    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int):
        self.navigate(self.CART_URL)
        # Requirement: Save screenshot of the final cart
        self.page.screenshot(path="screenshots/final_cart.png")
        
        self.page.wait_for_selector(self.TOTAL_PRICE_SELECTOR)
        actual_total = self._clean_price(self.page.inner_text(self.TOTAL_PRICE_SELECTOR))
        allowed_threshold = budget_per_item * items_count
        
        # Final validation
        assert actual_total <= allowed_threshold, f"Total {actual_total} exceeds budget {allowed_threshold}"

    def _clean_price(self, text: str) -> float:
        clean = "".join(c for c in text if c.isdigit() or c == '.')
        return float(clean) if clean else 0.0