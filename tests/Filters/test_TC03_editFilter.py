import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.DataStore import PropertyManager
from utilities.random_utils import RandomUtils


@allure.suite("edit and save filter")
@pytest.mark.usefixtures("setup")
class TestTC03:
    @allure.title("Filter well with single log edit and save the filter")
    def test_filter_edit_save(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        filter_name = PropertyManager.get_property("filterName")
        New_filter_name = RandomUtils.get_last_name()
        well = "SND 14 23 FED COM 001 P26 225H"
        second_log = "CALC_MSE_DEPTH"

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.edit_filter(filter_name)
        filter_page.assert_wellname_button(well)
        filter_page.select_object("Logs")
        filter_page.select_log(second_log)
        filter_page.click_log(second_log)
        filter_page.select_logcurves(second_log)
        filter_page.click_log(second_log)
        filter_page.Button("Save and Create Job")
        filter_page.enterFilterName(New_filter_name)
        filter_page.clickButton("add Save")
        filter_page.assert_popup("Filter saved successfully")

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        assert job_status == "In Progress"

        home_page.select_module("/filter")
        filter_page.assert_filter_visible(New_filter_name)

