from pages.booking_page import BookingPage
from utils.api_helpers import create_booking, get_auth_token, delete_booking


class TestBookingUI:

    def test_booking_page_loads(self, page):
        booking = BookingPage(page)
        booking.navigate()
        assert "Restful" in page.title(), "Page title should contain Restful Booker"

    def test_bookings_are_displayed(self, page):
        booking = BookingPage(page)
        booking.navigate()
        assert booking.get_booking_count() > 0, "Bookings table should display bookings"

    def test_api_created_booking_appears_on_ui(self, page):
        # Step 1 — Create booking via API
        response = create_booking({
            "firstname": "Hybrid",
            "lastname": "Test",
            "totalprice": 300,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-01",
                "checkout": "2026-09-05"
            },
            "additionalneeds": "Dinner"
        })
        assert response.status_code == 200, "Booking should be created successfully via API"
        booking_id = response.json()["bookingid"]

        # Step 2 — Open browser and verify it shows up on UI
        booking = BookingPage(page)
        booking.navigate()

        assert booking.is_booking_visible("Hybrid", "Test"), \
            "Booking created via API should appear on the UI"

        # Step 3 — Cleanup via API
        token = get_auth_token()
        delete_booking(booking_id, token)

    def test_booking_count_increases_after_api_create(self, page):
        booking = BookingPage(page)
        booking.navigate()

        # Get initial count
        initial_count = booking.get_booking_count()

        # Create a new booking via API
        response = create_booking()
        assert response.status_code == 200
        booking_id = response.json()["bookingid"]

        # Refresh and check count increased
        booking.navigate()
        new_count = booking.get_booking_count()

        assert new_count > initial_count, \
            "Booking count should increase after creating via API"

        # Cleanup
        token = get_auth_token()
        delete_booking(booking_id, token)