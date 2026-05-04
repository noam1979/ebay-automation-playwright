import os
from playwright.sync_api import sync_playwright

def save_session():
    """
    Utility script to manually log into eBay and save the authentication state.
    This bypasses CAPTCHA and bot detection by reusing a valid user session.
    """
    with sync_playwright() as p:
        # Launch browser in headed mode so you can interact with it
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to eBay login page
        page.goto("https://www.ebay.com/signin")
        
        print("ACTION REQUIRED: Please log in manually in the opened browser.")
        print("The script will wait for 60 seconds to allow you to finish login...")
        
        # Wait for the user to complete the login process manually
        page.wait_for_timeout(60000) 
        
        # Create 'auth' directory if it doesn't exist
        if not os.path.exists("auth"):
            os.makedirs("auth")
            
        # Save cookies and local storage to a JSON file
        context.storage_state(path="auth/state.json")
        print("SUCCESS: Session saved to auth/state.json")
        
        browser.close()

if __name__ == "__main__":
    save_session()