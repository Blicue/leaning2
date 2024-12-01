import pytest
from playwright.sync_api import Playwright, sync_playwright
import sys
import os


print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    
