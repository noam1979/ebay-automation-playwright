import pytest
import os
import csv
from playwright.sync_api import sync_playwright
from utils.data_parser import get_test_data
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.item_page import ItemPage
from pages.cart_page import CartPage

def test_ebay_purchase_flow():
    """
    Main E2E test execution flow using Page Object Model (POM).
    Steps:
    1. Load configuration from CSV (Data-Driven).
    2. Initialize browser with persistent authentication state to bypass bot detection.
    3. Navigate to search results and filter by price.
    4. Save found items to a local CSV report.
    5. Add selected items to cart.
    6. Final cart total validation.
    """
    
    # 1. Load Data-Driven inputs from CSV
    data = get_test_data()
    max_p = float(data['max_price'])
    limit = int(data['items_limit'])
    query = data['search_query']

    # Path to the saved authentication state
    session_path = "auth/state.json"

    with sync_playwright() as p:
        # 2. Setup: Launch browser
        # Headless=False allows visual tracking of the execution
        browser = p.chromium.launch(headless=False, slow_mo=500)
        
        # Define modern headers for browser robustness
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

        # Check if an authentication session exists
        if os.path.exists(session_path):
            # Launch context with saved session (Bypasses Login and CAPTCHA)
            context = browser.new_context(
                storage_state=session_path,
                user_agent=user_agent
            )
            print(f"Using existing session from {session_path}")
        else:
            # Fallback to guest context if no session is found
            print("Warning: No session file found. Running as Guest.")
            context = browser.new_context(user_agent=user_agent)
            
            # Inject US-based Cookie for Guest mode robustness
            context.add_cookies([{
                'name': 'regPrms',
                'value': 'un_prm%3D%26location%3D10001%26',
                'domain': '.ebay.com',
                'path': '/'
            }])

        page = context.new_page()

        # Initialize Page Objects (POM)
        results = ResultsPage(page)
        item_p = ItemPage(page)
        cart = CartPage(page)

        # 3. Execution Flow
        
        # Step A: Direct Navigation to Search Results (Optimized URL)
        search_url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
        page.goto(search_url)
        
        # Human emulation: Scroll to trigger lazy-loaded elements
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(2000)
        print(f"Navigated to: {search_url}")

        # Step B: Filter and collect items based on business requirements
        urls = results.search_items_by_name_under_price(max_p, limit)
        print(f"Collected {len(urls)} items under the price of {max_p}")

        # --- NEW: SAVE COLLECTED ITEMS TO CSV REPORT ---
        report_file = "collected_items_report.csv"
        if urls:
            # Writing the found URLs to a CSV for auditing and verification
            with open(report_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Index", "Product URL"]) # CSV Header
                for i, url in enumerate(urls, start=1):
                    writer.writerow([i, url])
            print(f"REPORT GENERATED: {report_file}")
        # -----------------------------------------------

        # Step C: Process each found item[cite: 1]
        if urls:
            item_p.add_items_to_cart(urls)
        else:
            # Fail the test if no items meet the criteria
            pytest.fail("No items found under the specified price. Check search query or selectors.")

        # Step D: Final Cart Validation
        # Verify the total cart price matches the sum of individual price limits
        cart.assert_cart_total_not_exceeds(max_p, len(urls))

        # 4. Teardown
        context.close()
        browser.close()