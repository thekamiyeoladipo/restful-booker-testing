import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def get_auth_token():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": "admin",
            "password": "password123"
        }
    )
    return response.json().get("token")

def create_booking(payload=None):
    if payload is None:
        payload = {
            "firstname": "Kamiye",
            "lastname": "Oladipo",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-07-01",
                "checkout": "2026-07-10"
            },
            "additionalneeds": "Breakfast"
        }
    response = requests.post(
        f"{BASE_URL}/booking",
        json=payload
    )
    return response

def get_booking(booking_id):
    response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    return response

def update_booking(booking_id, payload, token):
    response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=payload,
        headers={
            "Cookie": f"token={token}",
            "Content-Type": "application/json"
        }
    )
    return response

def delete_booking(booking_id, token):
    response = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"}
    )
    return response