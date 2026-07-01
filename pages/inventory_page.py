"""
inventory_page.py
-----------------
Page Object for the Products (inventory) page - where we add items to the cart.
"""

from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Container that only appears once we're logged in - a good "we're here" check.
        self.inventory_container = page.locator(".inventory_list")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def is_loaded(self) -> bool:
        """Confirm the inventory page loaded (used to verify login succeeded)."""
        return self.is_visible(self.inventory_container)

    def add_item_to_cart(self, item_name: str):
        """
        Add a product to the cart by its visible name.
        We build the locator dynamically from the item name - this is a common
        pattern when elements are generated from data.
        """
        # Find the product card whose text matches, then its Add-to-cart button.
        product = self.page.locator(".inventory_item", has_text=item_name)
        product.get_by_role("button", name="Add to cart").click()

    def get_cart_count(self) -> int:
        """Return the number shown on the cart badge (0 if the badge is absent)."""
        if self.is_visible(self.cart_badge):
            return int(self.get_text(self.cart_badge))
        return 0

    def go_to_cart(self):
        self.click(self.cart_link)
