from pages.base_page import BasePage

class ItemPage(BasePage):
    """
    Handles interaction with individual product pages.
    Integrated with robust selectors and variation handling.
    """
    
    # List of common 'Add to Cart' selectors on eBay (different regions/layouts)
    ADD_TO_CART_SELECTORS = [
        "#atcRedesignId_btn",          # New design
        "#isCartBtn_btn",              # Classic design
        "text='Add to cart'",          # Text-based fallback
        "[data-testid='x-atc-action']" # Modern test-id
    ]

    def add_items_to_cart(self, urls: list):
        """
        Iterates through the collected URLs and attempts to add each to the cart.
        """
        for url in urls:
            print(f"DEBUG: Navigating to Item Page: {url}")
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                
                # 1. Handle Variations (Size, Color, etc.)
                # Many items (especially shoes) block 'Add to Cart' until a size is picked.
                self._handle_variations()

                # 2. Try to click the 'Add to cart' button
                added = False
                for selector in self.ADD_TO_CART_SELECTORS:
                    try:
                        # We use a short timeout (3s) for each selector to keep the test moving
                        btn = self.page.wait_for_selector(selector, timeout=3000, state="visible")
                        if btn:
                            # Use 'force=True' if eBay tries to overlap the button with banners
                            btn.click(force=True)
                            print(f"SUCCESS: Added to cart using selector: {selector}")
                            added = True
                            break
                    except Exception:
                        continue
                
                if not added:
                    print(f"WARNING: Could not find 'Add to Cart' for {url}. It might be out of stock or requires login.")
                
                # Wait for the mini-cart or confirmation to appear
                self.page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"ERROR: Failed to process URL {url}: {str(e)}")

    def _handle_variations(self):
        """
        Finds dropdown menus (select tags) and picks the first available option.
        This is crucial for footwear automation on eBay.
        """
        try:
            # Look for all select elements on the page
            dropdowns = self.page.query_selector_all("select")
            for dropdown in dropdowns:
                if dropdown.is_visible():
                    # Option index 0 is usually "- Select -", index 1 is the first real choice.
                    try:
                        dropdown.select_option(index=1)
                        print("DEBUG: Automatically selected a variation option.")
                        self.page.wait_for_timeout(500)
                    except:
                        continue
        except Exception:
            # If no dropdowns found, we just move on
            pass