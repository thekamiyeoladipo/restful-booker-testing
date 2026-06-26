import requests

DEMOQA_BASE_URL = "https://demoqa.com"

def get_demoqa_token(username, password):
    response = requests.post(
        f"{DEMOQA_BASE_URL}/Account/v1/GenerateToken",
        json={
            "userName": username,
            "password": password
        }
    )
    return response.json().get("token")

def get_all_books():
    response = requests.get(f"{DEMOQA_BASE_URL}/BookStore/v1/Books")
    return response

def add_book_to_user(user_id, isbn, token):
    response = requests.post(
        f"{DEMOQA_BASE_URL}/BookStore/v1/Books",
        json={
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": isbn}]
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    return response

def get_user_books(user_id, token):
    response = requests.get(
        f"{DEMOQA_BASE_URL}/Account/v1/User/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response

def delete_book_from_user(user_id, isbn, token):
    response = requests.delete(
        f"{DEMOQA_BASE_URL}/BookStore/v1/Book",
        json={
            "userId": user_id,
            "isbn": isbn
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    return response