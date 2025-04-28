import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.setting_page import SettingPage
from pages.user_page import UserPage



@allure.suite("Settings")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("Verify that Adding RockPegion Witsml store configuration")
    def test_add_witsml_config(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        setting_page = SettingPage(page)



        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")


        home_page.select_module("/config-setting")
        setting_page.select_tab("RockPigeon WITSML Store")
        setting_page.input_url(config.WITSML_URL)
        filter_page.Button("Save")
        filter_page.assert_popup("Data updated successfully")

    @allure.title("Verify that Adding ADLS GEN2 configuration")
    def test_add_adls_gen_config(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        setting_page = SettingPage(page)
        user_page = UserPage(page)


        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/config-setting")
        setting_page.select_tab("ADLS GEN 2")
        user_page.selectRoles("config_type", [config.Config_Type])
        setting_page.input("container_name", config.container_name)
        setting_page.input("storage_account_name", config.storage_account_name)
        setting_page.input("base_path", config.base_path)
        setting_page.input("tenant_id", config.Tenant_id)
        setting_page.input("client_id", config.Client_id)
        setting_page.input("client_secret_id", config.Client_secret_id)
        filter_page.Button("Save")
        filter_page.assert_popup("Configuration updated successfully")

    @allure.title("Verify that Adding Notification configuration")
    def test_add_notification_config(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        setting_page = SettingPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/config-setting")
        setting_page.select_tab("Notification")

        setting_page.select_checkbox("notify_email")
        setting_page.input("email_address", config.Email_address)
        setting_page.input("email_token", config.Email_token)
        setting_page.select_checkbox("notify_teams")
        setting_page.input("teams_url", config.Teams_webhook_url)
        filter_page.Button("Save")
        filter_page.assert_popup("Notification settings updated successfully.")

















