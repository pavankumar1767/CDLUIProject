import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage

@allure.suite("Filter and extract job")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("Filter well with single log")
    def test_filter_extract(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
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
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        assert job_status == "In Progress"