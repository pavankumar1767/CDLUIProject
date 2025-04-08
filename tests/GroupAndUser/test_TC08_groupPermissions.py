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
class TestTC08:
    @allure.title("Verify that user and Group Creation without filters permission")
    def test_create_group(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        group_page = GroupsPage(page)
        filter_page = FilterPage(page)

        groupName = RandomUtils.get_last_name()
        permissionsList = ["group", "user", "job", "notifications", "Settings", "System Configuration"]

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
        PropertyManager.set_property("groupName", groupName)

        userName = RandomUtils.get_user_name()
        firstName = RandomUtils.get_first_name()
        lastName = RandomUtils.get_last_name()
        email = RandomUtils.get_email()

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
        user_page.selectRoles("roles", [PropertyManager.get_property("groupName")])
        user_page.Button("Save")
        filter_page.assert_popup("User created successfully")
        PropertyManager.set_property("userName", userName)
        PropertyManager.set_property("firstName", firstName)
        PropertyManager.set_property("lastName", lastName)

    @allure.title(f"Verify user should not have filters module permission")
    def test_filter_permisssion(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(PropertyManager.get_property("userName"))
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/user-list")
        home_page.Assert_moduleInvisibility("/filter")

    @allure.title("Verify Update Group permission (remove create job) permission")
    def test_update_group(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        group_page = GroupsPage(page)
        filter_page = FilterPage(page)


        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/role-permission")
        user_page.search(PropertyManager.get_property("groupName"))
        group_page.selectIcon(PropertyManager.get_property("groupName"), "settings")

        group_page.selectReadPermission("job")
        user_page.Button("Save")
        filter_page.assert_popup("Permissions updated successfully with dependencies applied.")

    @allure.title(f"Verify user should not have create job permission")
    def test_createjob_permission(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(PropertyManager.get_property("userName"))
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/jobs")
        user_page.AssertButtonInvisibility("Create Job")

    @allure.title("delete user and group")
    def test_delete_user(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        user_page = UserPage(page)
        filter_page = FilterPage(page)
        group_page = GroupsPage(page)

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
        groupName = PropertyManager.get_property("groupName")

        home_page.select_module("/role-permission")
        user_page.search(groupName)
        group_page.selectIcon(groupName, "delete")
        user_page.Button("Delete")
        filter_page.assert_popup(f"Group '{groupName}' has been deleted successfully.")








