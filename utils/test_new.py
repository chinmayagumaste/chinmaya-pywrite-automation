from playwright.sync_api import Page
import time
def test_childwindowtest (page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/#")
    page.locator(".blinkingText").first.click()
    time.sleep(10)