import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def demoqa_base_url():
    return os.getenv("DEMOQA_BASE_URL")

@pytest.fixture(scope="session")
def demoqa_username():
    return os.getenv("DEMOQA_USERNAME")

@pytest.fixture(scope="session")
def demoqa_password():
    return os.getenv("DEMOQA_PASSWORD")

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.set_default_timeout(60000)  # Increase to 60 seconds
        page = context.new_page()
        page.set_default_navigation_timeout(60000)  # Navigation timeout too
        yield page
        context.close()
        browser.close()

@pytest.fixture(scope="session")
def demoqa_user_id():
    return os.getenv("DEMOQA_USER_ID")