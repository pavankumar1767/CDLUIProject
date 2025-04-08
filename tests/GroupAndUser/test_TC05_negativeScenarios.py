import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.groups_page import GroupsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.user_page import UserPage
from utilities.DataStore import PropertyManager


@allure.suite("Negative Scenarios GroupAndUser Management")
@pytest.mark.usefixtures("setup")
class TestTC05:
    @allure.title("Verify user should be able to delete Group associated to user")
    def test_delete_AssignedGroup(self, setup, config):
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
        user_page.search(groupName)
        group_page.selectIcon(groupName, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"Group '{groupName}' is assigned to users and cannot be deleted.")

    @allure.title("Verify user should not able to create Duplicate Group")
    def test_crate_duplicate_group(self, setup, config):
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
        user_page.Button("Add Group")
        user_page.input("group_name", groupName)
        group_page.Button_2("Add")
        filter_page.assert_popup(f"A group with the name '{groupName}' already exists.")








