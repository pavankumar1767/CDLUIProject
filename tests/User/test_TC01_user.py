import time

import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_page import UserPage
from utilities.config import Config
from utilities.random_utils import RandomUtils


@allure.suite("User Management")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("create user")
    def test_crate_user(self, setup):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)

        userName = RandomUtils.get_user_name()
        firstName = RandomUtils.get_first_name()
        lastName = RandomUtils.get_last_name()
        email = RandomUtils.get_email()

        login_page.navigate(Config.BASE_URL)
        login_page.enter_username(Config.username)
        login_page.enter_password(Config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/user-list")
        user_page.Button("Add User")
        user_page.input("username", userName)
        user_page.input("password", Config.setpassword)
        user_page.input("fname", firstName)
        user_page.input("sname", lastName)
        user_page.input("disp_name", firstName)
        user_page.input("company", "CDS")
        user_page.input("email", email)
        user_page.input("mobile", RandomUtils.get_mobile_number())
        user_page.select_multiple_mat_options("roles", ["Admin", "Test"])
        user_page.Button("Save")
        time.sleep(10)



