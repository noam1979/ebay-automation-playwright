import pytest
from playwright.sync_api import sync_playwright
from utils.data_parser import get_test_data
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.item_page import ItemPage
from pages.cart_page import CartPage

def test_ebay_purchase_flow():
    """
    Main E2E test execution flow.
    Steps:
    1. Load data from CSV.
    2. Navigate to search results directly (to bypass home-page blocking).
    3. Filter and collect item URLs under max price.
    4. Add items to cart with random variants and screenshots.
    5. Validate total cart price.
    """
    
    # 1. Load Data-Driven inputs from CSV
    data = get_test_data()
    max_p = float(data['max_price'])
    limit = int(data['items_limit'])
    query = data['search_query']

    with sync_playwright() as p:
        # 2. Setup: Launch browser with specific configurations to bypass bot detection
        #browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        # Using a modern User-Agent is crucial for Robustness
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        # --- ROBUSTNESS FIX: Set US-based Cookie ---
        # This helps bypass regional shipping blocks (Geo-blocking)
        context.add_cookies([{
            'name': 'regPrms',
            'value': 'un_prm%3D%26location%3D10001%26', # Zip Code 10001 (New York)
            'domain': '.ebay.com',
            'path': '/'
        }])

        page = context.new_page()

        # Initialize Page Objects (POM)
        home = HomePage(page)
        results = ResultsPage(page)
        item_p = ItemPage(page)
        cart = CartPage(page)

        # 3. Execution Flow
        
        # Step A: Direct Navigation to Search Results
        # Replacing spaces with '+' for the URL format
        search_url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
        page.goto(search_url)
        print(f"Navigated to: {search_url}")

        # Step B: Search and collect links (Handles Paging if necessary)
        # Requirement: Filter items by price <= maxPrice
        urls = results.search_items_by_name_under_price(max_p, limit)
        print(f"Collected {len(urls)} items under the price of {max_p}")

        # Step C: Process each item
        # Requirement: Add to cart, select random variants, and take screenshots
        if urls:
            item_p.add_items_to_cart(urls)
        else:
            pytest.fail("No items found under the specified price. Check search query or selectors.")

        # Step D: Final Cart Validation
        # Requirement: budgetPerItem * itemsCount
        cart.assert_cart_total_not_exceeds(max_p, len(urls))

        # 4. Teardown
        browser.close()