import time

import allure

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

    def toggle_password_visibility(self):
        eye_icon = "//mat-icon[text()='visibility']"
        self.click(eye_icon, "password masking")

    def logout(self):
        element_xpath = "//mat-icon[normalize-space()='account_circle']"
        self.click(element_xpath, "profile icon")
        second_element_xpath = "//mat-icon[normalize-space()='logout']"
        self.click(second_element_xpath, "logout")


    def profile(self):
        element_xpath = "//mat-icon[normalize-space()='account_circle']"
        self.click(element_xpath, "profile icon")
        second_element_xpath = "//mat-icon[normalize-space()='person']"
        self.click(second_element_xpath, "profile")

    import time


    def assert_group_token(self):
        time.sleep(5)

        # Log message for the assertion step
        log_message = "Asserting that the group input is disabled and WITSML Server Access Token input is readonly and disabled."
        allure.attach(log_message, name="Assertion Log", attachment_type=allure.attachment_type.TEXT)

        # Locate the input element for the group
        group_input = self.page.locator("//input[@formcontrolname='groups']")
        with allure.step("Assert Group Input is Disabled"):
            assert group_input.is_disabled(), "❌ Group input box should be disabled but it is editable."
            allure.attach("Group input is disabled.", name="Group Input Status",
                          attachment_type=allure.attachment_type.TEXT)

        # Locate the input element for WITSML Server Access Token
        access_token_input = self.page.locator("//input[@formcontrolname='rp_pass']")

        with allure.step("Check 'readonly' attribute for WITSML Server Access Token"):
            # Check if the 'readonly' attribute is set for the input
            readonly_attr = access_token_input.get_attribute("readonly")
            assert readonly_attr is not None, "❌ WITSML Server Access Token input is editable but should be readonly."
            allure.attach(f"Readonly attribute: {readonly_attr}", name="Readonly Attribute Status",
                          attachment_type=allure.attachment_type.TEXT)