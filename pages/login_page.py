from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = "//input[@id='Email']"
        self.password_field = "//input[@id='Password']"
        self.login_button = "//button[text()='Log in']"

    def enter_username(self, username):
        self.fill(self.username_field, username, "username")

    def enter_password(self, password):
        self.fill(self.password_field, password, "password")

    def click_login(self):
        self.click(self.login_button,"Login")