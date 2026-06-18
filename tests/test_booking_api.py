import pytest
from utils.api_helpers import (
    get_auth_token,
    create_booking,
    get_booking,
    update_booking,
    delete_booking
)


class TestBookingAPI:

    def test_create_booking(self):
        response = create_booking()

        assert response.status_code == 200, "Should return 200 on successful booking creation"

        data = response.json()
        assert "bookingid" in data, "Response should contain a booking ID"
        assert data["booking"]["firstname"] == "Kamiye", "First name should match"
        assert data["booking"]["lastname"] == "Oladipo", "Last name should match"
        assert data["booking"]["totalprice"] == 150, "Total price should match"
        assert data["booking"]["depositpaid"] == True, "Deposit paid should be True"

    def test_get_booking(self):
        # First create a booking so we have an ID to fetch
        create_response = create_booking()
        booking_id = create_response.json()["bookingid"]

        # Now fetch it
        response = get_booking(booking_id)

        assert response.status_code == 200, "Should return 200 for existing booking"

        data = response.json()
        assert data["firstname"] == "Kamiye", "First name should match"
        assert data["lastname"] == "Oladipo", "Last name should match"

    def test_get_all_bookings(self):
        import requests
        response = requests.get("https://restful-booker.herokuapp.com/booking")

        assert response.status_code == 200, "Should return 200 for all bookings"
        assert isinstance(response.json(), list), "Response should be a list"
        assert len(response.json()) > 0, "Bookings list should not be empty"

    def test_update_booking(self):
        # Create a booking first
        create_response = create_booking()
        booking_id = create_response.json()["bookingid"]
        token = get_auth_token()

        updated_payload = {
            "firstname": "Updated",
            "lastname": "Name",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-08-01",
                "checkout": "2026-08-10"
            },
            "additionalneeds": "Lunch"
        }

        response = update_booking(booking_id, updated_payload, token)

        assert response.status_code == 200, "Should return 200 on successful update"

        data = response.json()
        assert data["firstname"] == "Updated", "First name should be updated"
        assert data["lastname"] == "Name", "Last name should be updated"
        assert data["totalprice"] == 200, "Total price should be updated"

    def test_delete_booking(self):
        # Create a booking to delete
        create_response = create_booking()
        booking_id = create_response.json()["bookingid"]
        token = get_auth_token()

        # Delete it
        delete_response = delete_booking(booking_id, token)
        assert delete_response.status_code == 201, "Should return 201 on successful deletion"

        # Verify it's gone
        get_response = get_booking(booking_id)
        assert get_response.status_code == 404, "Deleted booking should return 404"

    def test_get_nonexistent_booking(self):
        response = get_booking(999999)
        assert response.status_code == 404, "Non-existent booking should return 404"

    def test_create_booking_missing_required_fields(self):
        import requests
        response = requests.post(
            "https://restful-booker.herokuapp.com/booking",
            json={
                "firstname": "Kamiye"
                # Missing all other required fields
            }
        )
        assert response.status_code == 500, "Missing required fields should return 500"

    def test_update_booking_without_token(self):
        import requests
        create_response = create_booking()
        booking_id = create_response.json()["bookingid"]

        response = requests.put(
            f"https://restful-booker.herokuapp.com/booking/{booking_id}",
            json={
                "firstname": "Hacker",
                "lastname": "Attempt",
                "totalprice": 0,
                "depositpaid": False,
                "bookingdates": {
                    "checkin": "2026-01-01",
                    "checkout": "2026-01-02"
                }
            }
        )
        assert response.status_code == 403, "Update without token should return 403 Forbidden"