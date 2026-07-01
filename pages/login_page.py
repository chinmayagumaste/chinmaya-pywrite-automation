"""
login_page.py
-------------
Page Object for the Login page.

DESIGN NOTE (interview talking point):
A page object holds TWO things:
  1. The LOCATORS for elements on that page (kept at the top, in one place).
  2. The ACTIONS a user can perform on that page (methods like `login`).

The test never touches a raw locator - it just calls `login_page.login(...)`.
So if a locator changes, I fix it HERE, in one place, not in every test.
"""

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        super().__init__(page)
        # --- Locators: defined once, reused everywhere ---
        # I prefer stable, semantic locators (IDs, roles, test-ids) over
        # brittle ones like long CSS/XPath chains that break when the UI shifts.
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    # --- Actions ---
    def load(self):
        """Open the login page."""
        self.open(self.URL)

    def login(self, username: str, password: str):
        """Perform a full login: type credentials and submit."""
        self.type_text(self.username_input, username)
        self.type_text(self.password_input, password)
        self.click(self.login_button)

    def get_error(self) -> str:
        """Return the error text shown on a failed login (for negative tests)."""
        return self.get_text(self.error_message)
