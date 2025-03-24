import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.groups_page import GroupsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_page import UserPage
from utilities.DataStore import PropertyManager
from utilities.random_utils import RandomUtils


@allure.suite("GroupAndUser Management")
@pytest.mark.usefixtures("setup")
class TestTC06:
    @allure.title("delete Group")
    def test_delete_group(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        group_page = GroupsPage(page)
        filter_page = FilterPage(page)

        groupName = PropertyManager.get_property("groupName")

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/role-permission")
        group_page.selectIcon(groupName, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"Group '{groupName}' has been deleted successfully.")










