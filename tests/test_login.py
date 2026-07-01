"""
test_login.py
-------------
Login tests - shows POSITIVE and NEGATIVE cases, and data-driven testing
with @pytest.mark.parametrize.
"""

import pytest


@pytest.mark.smoke
def test_valid_login(login_page, inventory_page):
    """Positive: a valid user lands on the inventory page."""
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()


@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong_password", "do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
)
def test_invalid_login(login_page, username, password, expected_error):
    """
    Negative + data-driven: one test function, four sets of bad inputs.
    parametrize runs this test once per row - clean way to cover many cases.
    """
    login_page.load()
    login_page.login(username, password)
    assert expected_error.lower() in login_page.get_error().lower()
