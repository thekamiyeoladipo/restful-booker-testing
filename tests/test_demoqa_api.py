import requests
import os
from dotenv import load_dotenv
from utils.demoqa_helpers import (
    get_demoqa_token,
    get_all_books,
    add_book_to_user,
    get_user_books,
    delete_book_from_user
)

load_dotenv()

USERNAME = os.getenv("DEMOQA_USERNAME")
PASSWORD = os.getenv("DEMOQA_PASSWORD")
USER_ID = os.getenv("DEMOQA_USER_ID")


class TestDemoQAAPI:

    def test_generate_token(self):
        token = get_demoqa_token(USERNAME, PASSWORD)
        assert token is not None, "Token should not be None"
        assert isinstance(token, str), "Token should be a string"
        assert len(token) > 0, "Token should not be empty"

    def test_get_all_books(self):
        response = get_all_books()
        assert response.status_code == 200, "Should return 200"
        books = response.json().get("books", [])
        assert len(books) > 0, "Bookstore should have books"

    def test_add_book_to_user(self):
        token = get_demoqa_token(USERNAME, PASSWORD)

        # Get first available book ISBN
        books_response = get_all_books()
        isbn = books_response.json()["books"][0]["isbn"]

        # Cleanup first in case book already exists from a previous run
        delete_book_from_user(USER_ID, isbn, token)

        # Add book to user
        add_response = add_book_to_user(USER_ID, isbn, token)
        assert add_response.status_code in [200, 201], \
            f"Book should be added successfully, got {add_response.status_code}: {add_response.text}"

        # Verify book appears in user profile
        user_books = get_user_books(USER_ID, token)
        assert user_books.status_code == 200, "Should fetch user profile successfully"

        books_in_profile = user_books.json().get("books", [])
        assert any(b["isbn"] == isbn for b in books_in_profile), \
            "Added book should appear in user profile"

        # Cleanup
        delete_book_from_user(USER_ID, isbn, token)

    def test_invalid_credentials_return_error(self):
        response = requests.post(
            "https://demoqa.com/Account/v1/GenerateToken",
            json={
                "userName": "wronguser",
                "password": "wrongpassword"
            }
        )
        data = response.json()
        assert data.get("status") == "Failed", \
            "Invalid credentials should return Failed status"