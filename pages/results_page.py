from pages.base_page import BasePage
import re

class ResultsPage(BasePage):
    """
    Final ultimate fallback version. 
    Targets item links directly to bypass container naming issues.
    """
    
    # eBay product links always contain '/itm/'
    ANY_ITEM_LINK = "a[href*='/itm/']"

    def search_items_by_name_under_price(self, max_price: float, limit: int = 5):
        collected_urls = []
        
        # Give it a moment to settle
        self.page.wait_for_timeout(3000)
        
        # Get all links that look like products
        links = self.page.query_selector_all(self.ANY_ITEM_LINK)
        print(f"DEBUG: Found {len(links)} potential product links.")

        for link in links:
            if len(collected_urls) >= limit:
                break
            
            url = link.get_attribute("href")
            if not url or "clkid" in url: # Skip ads/tracking links
                continue
                
            clean_url = url.split('?')[0]
            if clean_url in collected_urls:
                continue

            # Look for price text near this link (in the parent or sibling)
            # We search for currency symbols or 'ILS' nearby
            parent = link.evaluate_handle("el => el.closest('li, div.s-item__wrapper, div.s-item__info')")
            if parent:
                price_text = parent.as_element().inner_text()
                price_val = self._clean_price(price_text)
                
                if 0 < price_val <= max_price:
                    collected_urls.append(clean_url)
                    print(f"!!! MATCH !!! Found Price: {price_val} | URL: {clean_url}")

        return list(set(collected_urls)) # Return unique URLs

    def _clean_price(self, text: str) -> float:
        """
        Extracts the numeric value from a block of text.
        """
        try:
            # Cleanup common non-numeric chars
            clean_text = text.replace(',', '').replace('₪', '').replace('ILS', '').replace('$', '')
            # Find all numbers with decimals
            matches = re.findall(r"(\d+\.\d+|\d+)", clean_text)
            
            # We look for numbers that look like prices (usually the first or second one)
            for num in matches:
                val = float(num)
                if 1 < val < 10000: # Filter out weird small/huge numbers that aren't prices
                    return val
            return 0.0
        except:
            return 0.0