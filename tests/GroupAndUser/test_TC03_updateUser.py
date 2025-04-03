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
class TestTC03:
    @allure.title("update user")
    def test_update_user(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)


        email = RandomUtils.get_email()

        user = f"{PropertyManager.get_property("firstName")} {PropertyManager.get_property("lastName")}"
        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/user-list")
        user_page.search(user)
        user_page.selectUser(user, "edit")
        user_page.input("email", email)
        user_page.Button("Save")
        filter_page.assert_popup("User updated successfully.")
        assert email.lower() == user_page.getEmail(user)










