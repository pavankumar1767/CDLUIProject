import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.random_utils import RandomUtils


@allure.suite("Negative scenarios")
@pytest.mark.usefixtures("setup")
class TestTC05:
    @allure.title("search well without filter wells")
    def test_filter_withoutFilterWell(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.Button("Create")
        filter_page.click_search("searchicon")
        filter_page.assert_popup("Please provide at least one search criterion.")


    @allure.title("search well without selected well")
    def test_filter_withoutSelectedWell(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        well = "SND 14 23 FED COM 001 P26 225H"

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.Button("Create")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        filter_page.assert_popup("No wells selected for job creation.")


    @allure.title("search well without selected well info")
    def test_filter_withoutSelectedWellInfo(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        well = "SND 14 23 FED COM 001 P26 225H"
        Object_list = ["Logs", "BHA Run", "Trajectory", "Wellbore Geometry", "Rig"]


        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.Button("Create")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.select_well(well)
        filter_page.assert_wellname_button(well)
        filter_page.select_objects_and_select_all(Object_list)


        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        filter_page.assert_popup("No wells selected for job creation.")

    @allure.title("Filter name cannot be empty")
    def test_empty_filter_name(self, setup, config):
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
        filter_page.Button("Save and Create Job")
        filter_page.enterFilterName("")
        filter_page.AssertDisabledButton("add Save")

    @allure.title("Duplicate Filter Name")
    def test_duplicate_filter(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        filter_name = RandomUtils.get_last_name()

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
        filter_page.Button("Save and Create Job")
        filter_page.enterFilterName(filter_name)
        filter_page.clickButton("add Save")
        # filter_page.assertpopup("Filter saved successfully")

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        assert job_status == "In Progress"

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
        filter_page.assert_popup("Filter name already exists. Use another name.")







