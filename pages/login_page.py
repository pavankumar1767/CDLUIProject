from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = "//input[@ng-reflect-name='username']"
        self.password_field = "//input[@ng-reflect-name='password']"

    def enter_username(self, username):
        self.fill(self.username_field, username, "username")

    def enter_password(self, password):
        self.fill(self.password_field, password, "password")

    def click_login(self, button_text):
        login_button_xpath = f"//button[@type='submit']/span[normalize-space()='{button_text}']"
        self.click(login_button_xpath, f"{button_text} Button")

    def get_title(self, text_content):
        element_xpath = f"//span[normalize-space()='{text_content}']"
        return self.get_text(element_xpath, f"user {text_content}")

    def get_ErrorMsg(self, text_content):
        element_xpath = f"//mat-error[normalize-space()='{text_content}']"
        return self.get_text(element_xpath, f"Error Message: {text_content}")

    def get_invalidUserError(self):
        element_xpath = "//div[normalize-space()='User does not exist']"
        return self.get_text(element_xpath, "invalid user error message")