eBay E2E Automation Project
Overview
This project implements an End-to-End (E2E) automated test for eBay using Python and Playwright. The test follows the Page Object Model (POM) design pattern and utilizes a Data-Driven approach.

How to Run
Prerequisites
Python 3.10+

Virtual Environment (Recommended)

Setup & Execution
Clone the repository to your local machine.

Install dependencies:
pip install -r requirements.txt

Install Playwright browsers:
playwright install chromium

Run the test:
pytest tests/test_ebay_e2e.py

Architecture
The project is structured to ensure maintainability and scalability:

Page Object Model (POM): Every page (Home, Results, Item, Cart) is represented by a class in the pages/ directory. This separates the UI selectors from the test logic.

Data-Driven Testing: Test inputs like search_query and max_price are managed via data/test_data.csv.

Utilities: A dedicated utils/ folder handles data parsing (CSV).

Robustness Layer: Custom headers (User-Agent) and Cookie injection are used to stabilize the test environment.

Limitations & Assumptions
Guest Flow: Following the examiner's approval, the project implements the flow as a Guest (No Login). This bypasses automated login blocks and security challenges (CAPTCHA) enforced by Google/eBay on automated browsers.

Geo-blocking Workaround: To ensure consistent product availability and pricing, a US-based Zip Code cookie (10001) is injected during setup.

Environment Constraints: Since this is a live environment, eBay's anti-bot mechanisms may occasionally lead to TimeoutErrors. The code is designed to handle these using explicit waits, but local network conditions or IP-based blocking may affect results.

Currency: All price validations assume USD ($) as the primary currency based on the US zip code setting.

Task 2: Bug Analysis (AI Code Review)
Implicit vs Explicit Waits: The original AI code used time.sleep(), which is inefficient. This was replaced with Playwright’s dynamic wait_for_selector().

Context Management: Fixed the issue where clicking items opens new tabs; the current architecture supports multi-page context handling.

Selector Stability: Replaced fragile text-based selectors with robust XPaths to prevent failures during eBay UI updates.