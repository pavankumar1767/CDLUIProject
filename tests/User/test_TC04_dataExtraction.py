import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.DataStore import PropertyManager
from utilities.TestDataManager import TestDataManager


@allure.suite("data extraction with created user for single log")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("Filter well with created user for single log")
    def test_filter_single_log(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(PropertyManager.get_property("userName"))
        login_page.enter_password(config.setpassword)
        login_page.click_login("Sign In")

        test_data = TestDataManager.get_test_data()
        well = test_data["wells"]["wellname_1"]
        log = test_data["wells"]["log_1"]
        Object_list = test_data["wells"]["objectlist"]

        home_page.select_module("/jobs")
        filter_page.Button("Create Job")
        # filter_page.Button("Skip")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.select_well(well)
        wellbore_name = filter_page.get_wellbore_name(well)
        filter_page.assert_wellname_button(well)
        filter_page.select_object("Logs")
        filter_page.deselect_all_logs()
        filter_page.select_log(log)
        filter_page.click_log(log)
        filter_page.select_logcurves(log)
        filter_page.click_log(log)
        filter_page.select_objects_and_select_all(Object_list)
        # extraction
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        time.sleep(5)

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        # job_page.assert_job_status(job_id)
        job_page.view_job(job_id)

        filter_page.select_object("Logs")
        job_page.assert_logs_checkbox_disabled(log)

        well_id = f"{well}_{job_id}"
        wellbore_id = f"{wellbore_name}_{job_id}"

        job_page.click_on_wellname(well_id)
        job_page.click_on_wellbore(well_id, wellbore_id)
        # need to upadte with green color coordinates
        job_page.assert_logdata_intowitsml(well_id, wellbore_id, [log])















