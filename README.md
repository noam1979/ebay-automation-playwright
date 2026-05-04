eBay E2E Automation Project

Overview
This project implements an End to End automated test for eBay using Python and Playwright. The test follows the Page Object Model design pattern and utilizes a Data Driven approach.

How to Run

Prerequisites
Python 3.10 plus
Virtual Environment Recommended

Setup and Execution
Clone the repository to your local machine.

Install dependencies:
pip install -r requirements.txt

Install Playwright browsers:
playwright install chromium

Run the test:
pytest tests/test_ebay_e2e.py

Authentication and Session Management save session script
To bypass eBays CAPTCHA and bot detection we use a persistent authentication state. This allows the automation to run as a logged in user without entering credentials every time.

How to use:
1. Run the session saver script:
python scripts/save_session.py
2. A browser window will open. Manually log in to your eBay account.
3. Once you are logged in and see your homepage the script will automatically save your cookies and storage state to auth/state.json and close the browser.
4. The main test test_ebay_e2e.py will now use this file to authenticate automatically.

Test Outputs and Reports

collected items report csv
After every successful test execution the system generates a data report.
Location: Root directory of the project[cite: 1, 2].
Content: A list of all product URLs that matched your search query and price filters[cite: 2].
Usage: You can open this file in Excel or any text editor to verify which items were selected by the bot before they were added to the cart[cite: 1, 2].

Architecture
The project is structured to ensure maintainability and scalability:

Page Object Model POM: Every page like Home, Results, Item, and Cart is represented by a class in the pages directory. This separates the UI selectors from the test logic.

Data Driven Testing: Test inputs like search query and max price are managed via data/test data csv.

Utilities: A dedicated utils folder handles data parsing.

Robustness Layer: Custom headers and Cookie injection are used to stabilize the test environment.

Limitations and Assumptions

Guest Flow: Following the examiners approval the project implements the flow as a Guest if no session file is found. This bypasses automated login blocks and security challenges enforced by eBay on automated browsers.

Geo blocking Workaround: To ensure consistent product availability and pricing a US based Zip Code cookie 10001 is injected during setup.

Environment Constraints: Since this is a live environment eBays anti bot mechanisms may occasionally lead to TimeoutErrors. The code is designed to handle these using explicit waits and robust selectors but local network conditions may affect results.

Currency: All price validations assume USD or ILS based on the location and search results provided by the live site.

Task 2 Bug Analysis AI Code Review

Implicit vs Explicit Waits: The original AI code used time sleep which is inefficient. This was replaced with Playwrights dynamic wait for selector and robust Locators to handle lazy loading.

Variation Handling: Added logic to handle item variations like size and color which often block the add to cart button[cite: 1].

Selector Stability: Replaced fragile selectors with flexible XPath and parent container searches to prevent failures during eBay UI updates[cite: 1, 2].