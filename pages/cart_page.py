"""
cart_page.py
------------
Page Object for the shopping Cart page.
"""

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")

    def get_item_count(self) -> int:
        """Count how many line items are in the cart."""
        return self.cart_items.count()

    def has_item(self, item_name: str) -> bool:
        """Check a specific product is present in the cart."""
        return self.page.locator(".cart_item", has_text=item_name).is_visible()

    def proceed_to_checkout(self):
        self.click(self.checkout_button)
