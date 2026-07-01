"""
base_page.py
------------
The BasePage is the parent class for every page object in the framework.

WHY THIS EXISTS (interview talking point):
Every page in an app shares common actions - navigating, clicking, typing,
waiting, taking a screenshot. Instead of repeating that code in every page
class, we put it once in BasePage and every page inherits from it.
This keeps the code DRY (Don't Repeat Yourself) and means a change to how we,
say, click an element only has to be made in ONE place.
"""

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        # Every page object holds a reference to the Playwright `page` object,
        # which represents a single browser tab.
        self.page = page

    def open(self, url: str):
        """Navigate to a URL."""
        self.page.goto(url)

    def click(self, locator):
        """Click an element. Playwright auto-waits for it to be actionable."""
        locator.click()

    def type_text(self, locator, text: str):
        """Fill a text field. `fill` clears the field first, then types."""
        locator.fill(text)

    def get_text(self, locator) -> str:
        """Return the visible text of an element."""
        return locator.inner_text()

    def is_visible(self, locator) -> bool:
        """Return True if the element is visible on the page."""
        return locator.is_visible()

    def wait_for_visible(self, locator, timeout: int = 10000):
        """
        Explicit wait for a specific condition.
        Playwright auto-waits on actions, but sometimes we want to assert an
        element has appeared before continuing - this is how we do it.
        """
        expect(locator).to_be_visible(timeout=timeout)

    def screenshot(self, path: str):
        """Capture a screenshot - useful evidence on failures."""
        self.page.screenshot(path=path)
