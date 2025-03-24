import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_page import UserPage
from utilities.DataStore import PropertyManager
from utilities.random_utils import RandomUtils


@allure.suite("GroupAndUser Management")
@pytest.mark.usefixtures("setup")
class TestTC02:
    @allure.title("create user")
    def test_create_user(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)

        userName = RandomUtils.get_user_name()
        firstName = RandomUtils.get_first_name()
        lastName = RandomUtils.get_last_name()
        email = RandomUtils.get_email()

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/user-list")
        user_page.Button("Add GroupAndUser")
        user_page.input("username", userName)
        user_page.input("password", config.setpassword)
        user_page.input("fname", firstName)
        user_page.input("sname", lastName)
        user_page.input("disp_name", firstName)
        user_page.input("company", "CDS")
        user_page.input("email", email)
        user_page.input("mobile", RandomUtils.get_mobile_number())
        user_page.selectRoles("roles", [PropertyManager.get_property("groupName")])
        user_page.Button("Save")
        filter_page.assert_popup("GroupAndUser created successfully")

        PropertyManager.set_property("userName", userName)
        PropertyManager.set_property("firstName", firstName)
        PropertyManager.set_property("lastName", lastName)






