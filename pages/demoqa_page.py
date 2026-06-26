class DemoQAPage:
    def __init__(self, page):
        self.page = page

        # Locators
        self.login_button = page.locator("button#login")
        self.username_input = page.locator("input#userName")
        self.password_input = page.locator("input#password")
        self.login_submit = page.locator("button#login")
        self.logged_in_username = page.locator("#userName-value")
        self.search_input = page.locator("input#searchBox")
        self.book_rows = page.locator(".rt-tr-group")
        self.profile_books = page.locator(".rt-tr-group")

    def navigate_to_bookstore(self):
        self.page.goto("https://demoqa.com/books")
        self.page.wait_for_load_state("networkidle")

    def navigate_to_login(self):
        self.page.goto("https://demoqa.com/login")
        self.page.wait_for_load_state("networkidle")

    def navigate_to_profile(self):
        self.page.goto("https://demoqa.com/profile")
        self.page.wait_for_load_state("networkidle")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_submit.click()
        self.page.wait_for_load_state("networkidle")

    def is_logged_in(self):
        try:
            self.logged_in_username.wait_for(state="visible", timeout=8000)
            return True
        except:
            return False

    def search_book(self, title):
        self.search_input.fill(title)
        self.page.wait_for_timeout(1000)

    def get_visible_book_count(self):
        try:
            self.book_rows.first.wait_for(state="visible", timeout=8000)
        except:
            pass
        return self.book_rows.count()

    def is_book_visible(self, title):
        rows = self.book_rows
        count = rows.count()
        for i in range(count):
            row_text = rows.nth(i).inner_text()
            if title in row_text:
                return True
        return False