import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.DataStore import PropertyManager
from utilities.config import Config
from utilities.random_utils import RandomUtils


@allure.suite("extract and save filter")
@pytest.mark.usefixtures("setup")
class TestTC02:
    @allure.title("Filter well with single log and save the filter")
    def test_filter_extract_save(self, setup):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        filter_name = RandomUtils.get_last_name()

        login_page.navigate(Config.BASE_URL)
        login_page.enter_username(Config.username)
        login_page.enter_password(Config.password)
        login_page.click_login("Sign In")

        well = "SND 14 23 FED COM 001 P26 225H"
        log = "CALC_ATA"
        Object_list = ["BHA Run", "Trajectory", "Wellbore Geometry"]

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.Button("Create")
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
        filter_page.Button("Save and Create Job")
        filter_page.enterFilterName(filter_name)
        filter_page.clickButton("add Save")
        # filter_page.assertpopup("Filter saved successfully")
        home_page.select_module("/jobs")
        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        # assert job_status == "In Progress"

        home_page.select_module("/filter")
        filter_page.assert_filter_visible(filter_name)

        PropertyManager.set_property("filterName", filter_name)

