
import time

import allure
import pytest
from playwright.sync_api import expect

from pages.filter_page import FilterPage
from pages.login_page import LoginPage


@pytest.mark.usefixtures("setup")
class TestLogin:
    @allure.title("Login_01 : Verify that a user can log in with valid credentials")
    def test_login(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")
        assert login_page.get_title(config.username) == config.username

    # @allure.title("Login_02 : Verify that an error message is displayed when incorrect credentials are entered.")
    # def test_invalid_login(self, setup, config):
    #     page = setup
    #     login_page = LoginPage(page)
    #     filter_page = FilterPage(page)
    #
    #     login_page.navigate(config.BASE_URL)
    #     login_page.enter_username("QA")
    #     login_page.enter_password("QAtest@123")
    #     login_page.click_login("Sign In")
    #     filter_page.assert_popup("User does not exist")
    #
    # @allure.title("Login_03 : Verify an appropriate error is shown when the username field is left blank.")
    # def test_login_blankUsername(self, setup, config):
    #     page = setup
    #     login_page = LoginPage(page)
    #
    #     login_page.navigate(config.BASE_URL)
    #     login_page.enter_username("")
    #     login_page.enter_password(config.password)
    #     login_page.click_login("Sign In")
    #     assert login_page.get_ErrorMsg("Username is required") == "Username is required"
    #
    # @allure.title("Login_04 : Verify an error message is displayed when the password field is left blank")
    # def test_login_blankPassword(self, setup, config):
    #     page = setup
    #     login_page = LoginPage(page)
    #
    #     login_page.navigate(config.BASE_URL)
    #     login_page.enter_username(config.username)
    #     login_page.enter_password("")
    #     login_page.click_login("Sign In")
    #     assert login_page.get_ErrorMsg("Password is required") == "Password is required"
    #
    # @allure.title("Login_05 : Verify an error message is displayed when username and password fields are left blank")
    # def test_login_blankFields(self, setup, config):
    #     page = setup
    #     login_page = LoginPage(page)
    #
    #     login_page.navigate(config.BASE_URL)
    #     login_page.enter_username("")
    #     login_page.enter_password("")
    #     login_page.click_login("Sign In")
    #     assert login_page.get_ErrorMsg("Password is required") == "Password is required"
    #     assert login_page.get_ErrorMsg("Username is required") == "Username is required"
    #
    # @allure.title("Login_06 : Verify that the password is masked by default and can be toggled")
    # def test_password_masking(self, setup, config):
    #     page = setup
    #     login_page = LoginPage(page)
    #
    #     login_page.navigate(config.BASE_URL)
    #     login_page.enter_password(config.password)
    #     login_page.toggle_password_visibility()
    #     assert login_page.page.locator(login_page.password_field).get_attribute("type") == "text"
    #
    #
