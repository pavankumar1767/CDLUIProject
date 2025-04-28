import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from pages.setting_page import SettingPage
from pages.user_page import UserPage
from utilities.TestDataManager import TestDataManager


@allure.suite("Settings")
@pytest.mark.usefixtures("setup")
class TestTC02:
    @allure.title("Verify that invalid secret id Adding ADLS GEN2 configuration and extracting the log")
    def test_add_invalid_adlsgen_config(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        setting_page = SettingPage(page)
        user_page = UserPage(page)
        job_page = JobPage(page)

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
        setting_page.input("client_secret_id", "_ng8Q~invalidid")
        filter_page.Button("Save")
        filter_page.assert_popup("Configuration updated successfully")

        test_data = TestDataManager.get_test_data()
        well = test_data["wells"]["wellname_1"]
        log = test_data["wells"]["log_1"]
        Object_list = test_data["wells"]["objectlist"]

        home_page.select_module("/jobs")
        filter_page.Button("Create Job")
        filter_page.Button("Skip")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.select_well(well)
        wellbore_name = filter_page.get_wellbore_name(well)
        filter_page.assert_wellname_button(well)
        filter_page.select_object("Logs")
        filter_page.deselect_all_logs()
        filter_page.select_log(log)
        filter_page.click_log(log)
        filter_page.select_logcurve(log, ["TIME", "PIT01"])
        filter_page.click_log(log)
        filter_page.select_objects_and_select_all(Object_list)
        # extraction
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        time.sleep(5)

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        job_page.assert_job_failed_due_to_config(job_id)
        job_page.view_job(job_id)

        filter_page.select_object("Logs")
        job_page.assert_logs_checkbox_disabled(log)

        well_id = f"{well}_{job_id}"
        wellbore_id = f"{wellbore_name}_{job_id}"

        job_page.click_on_wellname(well_id)
        job_page.click_on_wellbore(well_id, wellbore_id)
        # need to upadte with green color coordinates
        job_page.assert_logdata_failed_intowitsml(well_id, wellbore_id, [log])
        error = job_page.get_error_msg()
        print(error)
        assert error == "Message: A data processing error occurred. Please verify the input source or configuration."

        #update ADLS GEN configuration
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

    @allure.title("Verify that an error is displayed when each mandatory field is missing in the ADLS GEN2 configuration.")
    def test_validate_mandatory_fields_in_adlsgen_config(self, setup, config):
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

        # All mandatory fields and their values
        fields = {
            "container_name": config.container_name,
            "storage_account_name": config.storage_account_name,
            "base_path": config.base_path,
            "tenant_id": config.Tenant_id,
            "client_id": config.Client_id,
            "client_secret_id": config.Client_secret_id
        }

        for field_name, field_value in fields.items():
            # Step 1: Input all fields
            for name, value in fields.items():
                setting_page.input(name, value)

            # Step 2: Clear one field
            setting_page.clear_input_text(field_name)

            # Step 3: Click Save
            filter_page.Button("Save")

            # Step 4: Assert the expected popup error
            expected_error = f"For servicePrincipal, '{field_name}' is required."
            filter_page.assert_popup(expected_error)

            # Step 5: Re-enter the cleared field to continue next iteration
            setting_page.input(field_name, field_value)





