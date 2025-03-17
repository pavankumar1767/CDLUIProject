import time

import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.mark.usefixtures("setup")
class TestLogin:
    @allure.title("Login with valid credentials")
    def test_login(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")
        assert login_page.get_title(config.username) == "sigmastream"


    @allure.title("Login with invalid credentials")
    def test_invalid_login(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username("QA")
        login_page.enter_password("QAtest@123")
        login_page.click_login("Sign In")
        assert login_page.get_invalidUserError() == "User does not exist"

    @allure.title("Login with blank username")
    def test_login_blankUsername(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username("")
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")
        assert login_page.get_ErrorMsg("Username is required") == "Username is required"


    @allure.title("Login with blank password")
    def test_login_blankPassword(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password("")
        login_page.click_login("Sign In")
        assert login_page.get_ErrorMsg("Password is required") == "Password is required"


    @allure.title("Login with blank fields")
    def test_login_blankFields(self, setup, config):
        page = setup
        login_page = LoginPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username("")
        login_page.enter_password("")
        login_page.click_login("Sign In")
        assert login_page.get_ErrorMsg("Password is required") == "Password is required"
        assert login_page.get_ErrorMsg("Username is required") == "Username is required"
