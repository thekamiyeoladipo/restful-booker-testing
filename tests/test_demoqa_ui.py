import os
from dotenv import load_dotenv
from pages.demoqa_page import DemoQAPage
from utils.demoqa_helpers import (
    get_demoqa_token,
    get_all_books,
    add_book_to_user,
    delete_book_from_user
)

load_dotenv()

USERNAME = os.getenv("DEMOQA_USERNAME")
PASSWORD = os.getenv("DEMOQA_PASSWORD")
USER_ID = os.getenv("DEMOQA_USER_ID")


class TestDemoQAUI:

    def test_bookstore_page_loads(self, page):
        demoqa = DemoQAPage(page)
        demoqa.navigate_to_bookstore()
        assert "demoqa" in page.url, "Should be on demoqa books page"

    def test_books_are_displayed(self, page):
        demoqa = DemoQAPage(page)
        demoqa.navigate_to_bookstore()
        assert demoqa.get_visible_book_count() > 0, "Bookstore should display books"

    def test_search_filters_books(self, page):
        demoqa = DemoQAPage(page)
        demoqa.navigate_to_bookstore()
        demoqa.search_book("Git")
        assert demoqa.is_book_visible("Git"), "Search should show Git book"

    def test_login_with_valid_credentials(self, page):
        demoqa = DemoQAPage(page)
        demoqa.navigate_to_login()
        demoqa.login(USERNAME, PASSWORD)
        assert demoqa.is_logged_in(), "User should be logged in with valid credentials"

    def test_api_added_book_appears_in_profile(self, page):
        token = get_demoqa_token(USERNAME, PASSWORD)
        books_response = get_all_books()
        first_book = books_response.json()["books"][0]
        isbn = first_book["isbn"]
        title = first_book["title"]

        # Cleanup first in case book already exists from previous run
        delete_book_from_user(USER_ID, isbn, token)

        # Step 1 — Add book via API
        add_response = add_book_to_user(USER_ID, isbn, token)
        assert add_response.status_code in [200, 201], \
            f"Book should be added via API, got {add_response.status_code}: {add_response.text}"

        # Step 2 — Login via UI
        demoqa = DemoQAPage(page)
        demoqa.navigate_to_login()
        demoqa.login(USERNAME, PASSWORD)
        assert demoqa.is_logged_in(), "User should be logged in"

        # Step 3 — Navigate to profile and verify book appears
        demoqa.navigate_to_profile()
        assert demoqa.is_book_visible(title), \
            f"Book '{title}' added via API should appear in UI profile"

        # Step 4 — Cleanup
        delete_book_from_user(USER_ID, isbn, token)