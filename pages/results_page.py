from pages.base_page import BasePage

class ResultsPage(BasePage):
    """
    Handles search results, price filtering, and pagination.
    """
    PRODUCT_CARDS = "//div[@class='s-item__info']"
    PRICE_XPATH = ".//span[@class='s-item__price']"
    LINK_XPATH = ".//a[@class='s-item__link']"
    NEXT_BUTTON = "//a[@aria-label='Go to next search page']"

    def search_items_by_name_under_price(self, max_price: float, limit: int = 5):
        collected_urls = []
        while len(collected_urls) < limit:
            self.page.wait_for_selector(self.PRODUCT_CARDS)
            items = self.page.query_selector_all(self.PRODUCT_CARDS)

            for item in items:
                if len(collected_urls) >= limit: break
                
                price_el = item.query_selector(self.PRICE_XPATH)
                link_el = item.query_selector(self.LINK_XPATH)

                if price_el and link_el:
                    price_val = self._clean_price(price_el.inner_text())
                    # Filter items by price
                    if 0 < price_val <= max_price:
                        url = link_el.get_attribute("href")
                        if url and "itm" in url:
                            collected_urls.append(url)

            # Pagination logic
            if len(collected_urls) < limit:
                next_btn = self.page.query_selector(self.NEXT_BUTTON)
                if next_btn and next_btn.is_visible():
                    next_btn.click()
                    self.page.wait_for_load_state("networkidle")
                else:
                    break
        return collected_urls

    def _clean_price(self, text: str) -> float:
        # Handles ranges like '$10 to $20' by taking the first number
        first_part = text.split('to')[0]
        clean = "".join(c for c in first_part if c.isdigit() or c == '.')
        return float(clean) if clean else 0.0