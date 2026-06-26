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
        # Get token and user ID
        token = get_demoqa_token(USERNAME, PASSWORD)
        response = requests.post(
            "https://demoqa.com/Account/v1/Authorized",
            json={"userName": USERNAME, "password": PASSWORD}
        )

        # Get user ID
        user_response = requests.get(
            f"https://demoqa.com/Account/v1/User",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Get first book ISBN
        books_response = get_all_books()
        isbn = books_response.json()["books"][0]["isbn"]

        # Get user ID from token call
        token_response = requests.post(
            "https://demoqa.com/Account/v1/GenerateToken",
            json={"userName": USERNAME, "password": PASSWORD}
        )
        user_id_response = requests.get(
            "https://demoqa.com/Account/v1/User",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Add book
        add_response = requests.post(
            "https://demoqa.com/BookStore/v1/Books",
            json={
                "userId": user_id_response.json().get("userId"),
                "collectionOfIsbns": [{"isbn": isbn}]
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert add_response.status_code in [200, 201], "Book should be added successfully"

    def test_invalid_credentials_return_error(self):
        response = requests.post(
            "https://demoqa.com/Account/v1/GenerateToken",
            json={
                "userName": "wronguser",
                "password": "wrongpassword"
            }
        )
        data = response.json()
        assert data.get("status") == "Failed", "Invalid credentials should return Failed status"