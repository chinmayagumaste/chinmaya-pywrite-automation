# Playwright Automation Framework (Python + Pytest + POM)

A UI and API test automation framework built with **Playwright**, **Python**, and
**Pytest**, structured using the **Page Object Model (POM)**. It automates an
end-to-end e-commerce flow: **login → add to cart → checkout → order validation**,
plus API validation, and runs in **CI via GitHub Actions**.

> This README is also my interview walkthrough. Each section is something I can
> explain and defend, because I designed it this way for a reason.

---

## How to run it

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install the browser
playwright install chromium

# 3. Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run in headed mode (watch the browser)
pytest --headed

# Run a single test
pytest tests/test_checkout.py::test_end_to_end_checkout
```

An HTML report is generated at `reports/report.html`.

---

## Project structure

```
playwright-automation/
├── pages/                  # Page Object Model - one class per page
│   ├── base_page.py        # Parent class: shared actions (click, type, wait)
│   ├── login_page.py       # Login page: locators + login() action
│   ├── inventory_page.py   # Products page: add-to-cart, cart count
│   ├── cart_page.py        # Cart page: item checks, proceed to checkout
│   └── checkout_page.py    # Checkout: customer info, finish, confirmation
├── tests/                  # Test cases (the "what to verify")
│   ├── test_login.py       # Positive + negative + data-driven login
│   ├── test_checkout.py    # End-to-end purchase journey
│   └── test_api.py         # API validation via Playwright request context
├── conftest.py             # Pytest fixtures (setup/teardown, page objects)
├── pytest.ini              # Config: markers, report, run options
├── requirements.txt        # Dependencies
└── .github/workflows/      # CI: run tests on every push/PR
    └── tests.yml
```

---

## Design decisions (the "why" - this is what interviewers probe)

### 1. Why Page Object Model?
Every page gets its own class holding **its locators and its actions**. Tests call
methods like `login_page.login(user, pw)` and never touch raw locators.

**Benefit:** if a locator changes, I update it in **one place** (that page class)
instead of hunting through every test. This is maintainability - the #1 reason POM
exists. It also makes tests readable (`cart_page.proceed_to_checkout()` reads like
plain English) and lets me reuse actions across many tests.

### 2. Why a BasePage?
All pages share common actions - click, type, navigate, wait, screenshot. I put
those once in `BasePage` and every page inherits from it. That keeps the code DRY
and means a change to *how* I click only happens in one place.

### 3. Why fixtures in conftest.py?
Setup like "open the app and log in" is needed by many tests. Instead of repeating
it, I define it once as the `logged_in` fixture. A test that needs an authenticated
session just names `logged_in` as an argument and pytest injects it. This
centralises setup/teardown and keeps tests short.

### 4. How do I handle waits?
Playwright **auto-waits** on every action - before a click or fill it waits for the
element to be attached, visible, stable, and enabled. So I rarely need manual waits,
which is why Playwright tests are less flaky than old Selenium ones. When I *do* need
to wait for a specific condition, I use an explicit `expect(locator).to_be_visible()`
(see `BasePage.wait_for_visible`). I never use hard-coded `time.sleep()` - it makes
tests slow and unreliable.

### 5. How do I choose locators?
I prefer stable, semantic locators - IDs, `data-test` attributes, and role-based
locators like `get_by_role("button", name="Add to cart")` - over brittle long
CSS/XPath chains that break the moment the UI shifts.

### 6. How do I assert?
I use Playwright's **web-first assertions** via `expect()`, which auto-retry until
the condition is met or it times out - this removes a whole class of timing flakiness
compared to a plain Python `assert` on a value read too early.

### 7. Positive AND negative testing
`test_login.py` covers the happy path *and* negative cases (locked-out user, wrong
password, empty fields) using `@pytest.mark.parametrize` - one test function, many
data rows. That's data-driven testing: broad coverage without duplicate code.

### 8. UI + API in one framework
`test_api.py` uses Playwright's `request` context to validate a REST endpoint -
status code and JSON body. So the same framework covers UI and API, which mirrors
how I did API testing manually with Postman, just automated.

### 9. CI/CD integration
`.github/workflows/tests.yml` runs the whole suite on every push and pull request,
installs the browser, runs pytest, and uploads the HTML report as an artifact. My
tests run in the pipeline, not just on my laptop - which is exactly the CI/CD
integration the role needs.

### 10. Test organisation with markers
`@pytest.mark.smoke` and `@pytest.mark.regression` let me run a fast critical-path
subset (`pytest -m smoke`) or the fuller suite (`pytest -m regression`). Smoke runs
on every commit; regression before releases.

---

## What I'd add next (shows I know the roadmap)

- **Allure reporting** for richer, historical reports.
- **Cross-browser runs** (Chromium, Firefox, WebKit) via Playwright's project config.
- **Parallel execution** with `pytest-xdist` (`pytest -n auto`) to cut run time.
- **Docker** so the suite runs in a container identically everywhere.
- **Environment config** (dev/staging URLs) driven by env variables.
- **Trace Viewer** on failures for step-by-step debugging.

---

## Honest note on my level
This is a framework I built to learn and demonstrate automation. My background is
5 years of manual, API, and SQL testing in Telecom OSS/BSS. I'm early in automation
but I understand the design principles here and can explain every decision - and I
learn fast.
