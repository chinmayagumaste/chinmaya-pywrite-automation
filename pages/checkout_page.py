"""
checkout_page.py
----------------
Page Object for the Checkout flow (customer info -> overview -> finish).
This is where we validate the order completed successfully.
"""

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Step 1: customer information
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        # Step 2: overview
        self.finish_button = page.locator("#finish")
        self.total_label = page.locator(".summary_total_label")
        # Step 3: confirmation
        self.confirmation_header = page.locator(".complete-header")

    def fill_customer_info(self, first: str, last: str, postal: str):
        self.type_text(self.first_name, first)
        self.type_text(self.last_name, last)
        self.type_text(self.postal_code, postal)
        self.click(self.continue_button)

    def get_total_text(self) -> str:
        """Return the order total summary text (e.g. 'Total: $58.29')."""
        return self.get_text(self.total_label)

    def finish_order(self):
        self.click(self.finish_button)

    def get_confirmation_message(self) -> str:
        """Return the post-order confirmation header ('Thank you for your order!')."""
        return self.get_text(self.confirmation_header)
