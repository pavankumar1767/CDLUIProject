import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.DataStore import PropertyManager
from utilities.random_utils import RandomUtils


@allure.suite("edit and extract filter")
@pytest.mark.usefixtures("setup")
class TestTC04:
    @allure.title("Filter well with single log edit and extract the filter")
    def test_filter_edit_extract(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        filter_name = PropertyManager.get_property("filterName")
        well = "SND 14 23 FED COM 001 P26 225H"
        data_Object = "Trajectory"

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        home_page.select_module("/filter")
        filter_page.assert_filterListPage()
        filter_page.edit_filter(filter_name)
        filter_page.assert_wellname_button(well)
        filter_page.select_object(data_Object)
        # filter_page.deselectAll_objects(data_Object)
        filter_page.select_object_checkboxes(data_Object)
        filter_page.select_object(data_Object)
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        assert job_status == "In Progress"
        # job_page.assert_job_status(job_id)
        job_page.view_job(job_id)

        filter_page.select_object(data_Object)
        job_page.assert_objects_checkbox_disabled(data_Object)


