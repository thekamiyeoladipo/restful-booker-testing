import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.set_default_timeout(15000)
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.fixture(scope="session")
def api_context():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=os.getenv("BASE_URL")
        )
        yield request_context
        request_context.dispose()