import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_page import UserPage
from utilities.DataStore import PropertyManager
from utilities.random_utils import RandomUtils


@allure.suite("User Management")
@pytest.mark.usefixtures("setup")
class TestTC05:
    @allure.title("delete user")
    def test_delete_user(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)


        user = f"{PropertyManager.get_property("firstName")} {PropertyManager.get_property("lastName")}"
        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/user-list")
        user_page.search(user)
        user_page.selectUser(user, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"User {PropertyManager.get_property("userName")} deleted successfully")










