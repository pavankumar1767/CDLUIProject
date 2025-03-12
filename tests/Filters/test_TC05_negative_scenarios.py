import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.config import Config

@allure.suite("Negative scenarios")
@pytest.mark.usefixtures("setup")
class TestTC05:
    @allure.title("search well without filter wells")
    def test_filter_withoutFilterWell(self, setup):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        login_page.navigate(Config.BASE_URL)
        login_page.enter_username(Config.username)
        login_page.enter_password(Config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.Button("Create")
        filter_page.click_search("searchicon")
        filter_page.assert_popup("Please provide at least one search criterion.")


    @allure.title("search well without selected well")
    def test_filter_withoutSelectedWell(self, setup):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        well = "SND 14 23 FED COM 001 P26 225H"

        login_page.navigate(Config.BASE_URL)
        login_page.enter_username(Config.username)
        login_page.enter_password(Config.password)
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
    def test_filter_withoutSelectedWellInfo(self, setup):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)

        well = "SND 14 23 FED COM 001 P26 225H"
        Object_list = ["Logs", "BHA Run", "Trajectory", "Wellbore Geometry", "Rig"]


        login_page.navigate(Config.BASE_URL)
        login_page.enter_username(Config.username)
        login_page.enter_password(Config.password)
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




