"""
test_checkout.py
----------------
The end-to-end test that mirrors my real shopping-cart scenario:
login -> add product to cart -> verify cart -> checkout -> validate order.

This is the test I walk interviewers through, because it shows a complete
user journey and combines UI validation with an order-confirmation check.
"""

import pytest


@pytest.mark.smoke
def test_add_to_cart_updates_badge(logged_in, inventory_page):
    """Adding an item increments the cart badge count."""
    assert inventory_page.get_cart_count() == 0
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == 1


@pytest.mark.regression
def test_end_to_end_checkout(logged_in, inventory_page, cart_page, checkout_page):
    """
    Full happy-path purchase.
    Each step asserts state before moving on, so a failure points to the
    exact stage that broke.
    """
    # 1. Add a product and confirm the badge updates
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == 1

    # 2. Go to the cart and confirm the item is there
    inventory_page.go_to_cart()
    assert cart_page.get_item_count() == 1
    assert cart_page.has_item("Sauce Labs Backpack")

    # 3. Checkout: fill customer info
    cart_page.proceed_to_checkout()
    checkout_page.fill_customer_info("Chinmaya", "Gumaste", "560001")

    # 4. Confirm an order total is displayed on the overview
    assert "Total" in checkout_page.get_total_text()

    # 5. Finish and validate the order confirmation
    checkout_page.finish_order()
    assert "Thank you for your order" in checkout_page.get_confirmation_message()


@pytest.mark.regression
def test_two_items_in_cart(logged_in, inventory_page, cart_page):
    """Add multiple items and confirm both reach the cart."""
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    assert inventory_page.get_cart_count() == 2

    inventory_page.go_to_cart()
    assert cart_page.get_item_count() == 2
