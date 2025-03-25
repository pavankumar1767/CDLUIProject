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
class TestTC09:
    @allure.title("Verify user is assigned to multiple group, Then user will have superior role access")
    def test_crate_group(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        group_page = GroupsPage(page)
        filter_page = FilterPage(page)

        groupName = RandomUtils.get_last_name()
        second_groupName = RandomUtils.get_last_name()
        userName = RandomUtils.get_user_name()
        firstName = RandomUtils.get_first_name()
        lastName = RandomUtils.get_last_name()
        email = RandomUtils.get_email()

        permissionsList = ["job"]
        permissionsList_2 = ["filter"]


        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/role-permission")
        user_page.Button("Add Group")
        user_page.input("group_name", groupName)
        group_page.Button_2("Add")
        filter_page.assert_popup("Group created successfully.")
        user_page.search(groupName)
        group_page.selectIcon(groupName, "settings")
        group_page.selectAllObjectsList(permissionsList)
        user_page.Button("Save")
        filter_page.assert_popup("Permissions updated successfully with dependencies applied.")

        home_page.select_module("/role-permission")
        user_page.Button("Add Group")
        user_page.input("group_name", second_groupName)
        group_page.Button_2("Add")
        filter_page.assert_popup("Group created successfully.")
        user_page.search(second_groupName)
        group_page.selectIcon(second_groupName, "settings")
        group_page.selectAllObjectsList(permissionsList_2)
        user_page.Button("Save")
        filter_page.assert_popup("Permissions updated successfully with dependencies applied.")

        home_page.select_module("/user-list")
        user_page.Button("Add User")
        user_page.input("username", userName)
        user_page.input("password", config.setpassword)
        user_page.input("fname", firstName)
        user_page.input("sname", lastName)
        user_page.input("disp_name", firstName)
        user_page.input("company", "CDS")
        user_page.input("email", email)
        user_page.input("mobile", RandomUtils.get_mobile_number())
        user_page.selectRoles("roles", [groupName, second_groupName])
        user_page.Button("Save")
        filter_page.assert_popup("User created successfully")
        login_page.logout()

        login_page.enter_username(userName)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")
        home_page.Assert_moduleVisibility("/filter")
        home_page.Assert_moduleVisibility("/jobs")
        home_page.select_module("/jobs")
        user_page.AssertButtonVisibility("Create Job")
        home_page.select_module("/filter")
        user_page.AssertButtonVisibility("Create")
        login_page.logout()

        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")
        home_page.select_module("/user-list")
        user_page.search(f"{firstName} {lastName}")
        user_page.selectUser(f"{firstName} {lastName}", "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"User {userName} deleted successfully")

        home_page.select_module("/role-permission")
        user_page.search(groupName)
        group_page.selectIcon(groupName, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"Group '{groupName}' has been deleted successfully.")
        user_page.search(second_groupName)
        group_page.selectIcon(second_groupName, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"Group '{second_groupName}' has been deleted successfully.")

