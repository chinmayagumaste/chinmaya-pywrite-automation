"""
conftest.py
-----------
Pytest fixtures live here. Fixtures are reusable setup/teardown that pytest
injects into tests automatically.

WHY FIXTURES MATTER (interview talking point):
Instead of every test opening a browser, logging in, and closing the browser,
I define that ONCE as a fixture. Each test just asks for what it needs by
naming it as an argument. This removes duplication and centralises setup.

The `page` fixture is provided by the official `pytest-playwright` plugin.
Here I build higher-level fixtures on top of it (page objects, a logged-in
session) so tests stay short and readable.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# Test credentials for the demo site (public practice app).
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def logged_in(page, login_page, inventory_page):
    """
    A composite fixture: opens the app and logs in as the standard user,
    so any test using `logged_in` starts from an authenticated state.
    This is a common way to avoid repeating login steps in every test.
    """
    login_page.load()
    login_page.login(STANDARD_USER, PASSWORD)
    assert inventory_page.is_loaded(), "Login failed - inventory page not shown"
    return page


def pytest_configure(config):
    """Register a custom marker so `@pytest.mark.smoke` doesn't warn."""
    config.addinivalue_line("markers", "smoke: quick critical-path checks")
    config.addinivalue_line("markers", "regression: fuller regression suite")
