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


@allure.suite("Group Permissions")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("create Group")
    def test_crate_group(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        group_page = GroupsPage(page)
        filter_page = FilterPage(page)

        groupName = RandomUtils.get_last_name()
        permissionsList = ["group", "user", "filter", "job", "notifications", "Settings", "System Configuration"]


        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/role-permission")
        user_page.Button("Add Group")
        user_page.input("group_name", groupName)
        group_page.Button_2("Add")
        filter_page.assert_popup("Group created successfully.")
        group_page.selectIcon(groupName, "settings")
        group_page.selectAllObjectsList(permissionsList)
        user_page.Button("Save")
        filter_page.assert_popup("Permissions updated successfully with dependencies applied.")

        PropertyManager.set_property("groupName", groupName)








