class BookingPage:
    def __init__(self, page):
        self.page = page

        # Locators
        self.booking_table = page.locator("#bookings")
        self.booking_rows = page.locator("#bookings tbody tr")
        self.firstname_input = page.locator("#firstname")
        self.lastname_input = page.locator("#lastname")
        self.totalprice_input = page.locator("#totalprice")
        self.depositpaid_select = page.locator("#depositpaid")
        self.checkin_input = page.locator("#checkin")
        self.checkout_input = page.locator("#checkout")
        self.save_button = page.locator("#saveBooking")

    def navigate(self):
        self.page.goto("https://automationintesting.online")
        self.page.wait_for_load_state("networkidle")

    def get_booking_count(self):
        try:
            self.booking_rows.first.wait_for(state="visible", timeout=8000)
        except:
            pass
        return self.booking_rows.count()

    def is_booking_visible(self, firstname, lastname):
        rows = self.booking_rows
        count = rows.count()
        for i in range(count):
            row_text = rows.nth(i).inner_text()
            if firstname in row_text and lastname in row_text:
                return True
        return False

    def create_booking_via_ui(self, firstname, lastname, price, checkin, checkout):
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.totalprice_input.fill(str(price))
        self.depositpaid_select.select_option("true")
        self.checkin_input.fill(checkin)
        self.checkout_input.fill(checkout)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")