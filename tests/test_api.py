"""
test_api.py
-----------
A small API test using Playwright's built-in `request` fixture.

INTERVIEW TALKING POINT:
Playwright isn't only for UI - it has an APIRequestContext for hitting REST
endpoints directly. That means I can validate an API response in the same
framework as my UI tests. Here I check status code and JSON body, which maps
to how I did API testing manually with Postman - just automated.

(Uses a public test API so it runs anywhere.)
"""

import pytest


@pytest.mark.regression
def test_get_user_status_and_body(playwright):
    request_context = playwright.request.new_context()
    response = request_context.get("https://reqres.in/api/users/2")

    # 1. Validate the status code
    assert response.status == 200

    # 2. Validate the response body / schema
    body = response.json()
    assert "data" in body
    assert body["data"]["id"] == 2
    assert "email" in body["data"]

    request_context.dispose()
