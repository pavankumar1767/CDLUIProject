


#--------------loop

import time
import allure
import pytest
from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.DataStore import PropertyManager
from utilities.TestDataManager import TestDataManager
from utilities.random_utils import RandomUtils


@allure.suite("extract and save filter")
@pytest.mark.usefixtures("setup")
class TestTC02:
    @allure.title("Multiple filter creation")
    def test_multiple_filter(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        # Get the loop count from config, default to 1 if not specified
        loop_count = config.loopCount

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        test_data = TestDataManager.get_test_data()
        well = test_data["wells"]["wellname_1"]
        log = test_data["wells"]["log_1"]
        Object_list = test_data["wells"]["objectlist"]

        for iteration in range(1, loop_count + 1):
            with allure.step(f"Iteration {iteration} of {loop_count}"):
                # Generate unique filter name for each iteration
                filter_name = f"{RandomUtils.get_last_name()}_{iteration}"

                home_page.select_module("/filter")
                filter_page.assert_filterListPage()
                filter_page.Button("Create")
                filter_page.input_field(well)
                filter_page.click_search("searchicon")
                filter_page.select_well(well)
                wellbore_name = filter_page.get_wellbore_name(well)
                filter_page.assert_wellname_button(well)
                # filter_page.select_object("Logs")
                # filter_page.deselect_all_logs()
                # filter_page.select_log(log)
                # filter_page.click_log(log)
                # filter_page.select_logcurves(log)
                # filter_page.click_log(log)
                # filter_page.select_objects_and_select_all(Object_list)

                # extraction
                filter_page.Button("Save and Create Job")
                filter_page.enterFilterName(filter_name)
                filter_page.clickButton("add Save")
                filter_page.assert_popup("Filter saved successfully")

                # job summary
                job_id = job_page.get_jobnumber()
                job_status = job_page.get_job_status(job_id)
                # assert job_status == "In Progress"

                home_page.select_module("/filter")
                filter_page.SearchByFilter(filter_name)
                filter_page.assert_filter_visible(filter_name)

                # Store filter name with iteration suffix
                PropertyManager.set_property(f"filterName_{iteration}", filter_name)

                # Add a small delay between iterations if needed
                if iteration < loop_count:
                    time.sleep(2)  # 2-second delay between iterations