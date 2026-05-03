from playwright.sync_api import Page

class BasePage:
    """
    Parent class for all Page Objects.
    Contains common browser interactions.
    """
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def click_element(self, selector: str):
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    def fill_text(self, selector: str, text: str):
        self.page.wait_for_selector(selector, state="visible")
        self.page.fill(selector, text)