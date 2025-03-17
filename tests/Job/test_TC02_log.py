import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage

@allure.suite("data extraction multiple logs")
@pytest.mark.usefixtures("setup")
class TestTC02:
    @allure.title("Filter well with multiple logs")
    def test_filter_multiple_log(self, setup, config):
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
        second_log = "CALC_MSE_DEPTH"
        Object_list = ["BHA Run", "Trajectory", "Wellbore Geometry"]

        home_page.select_module("/filter")
        filter_page.Button("Create")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.select_well(well)
        wellbore_name = filter_page.get_wellbore_name(well)
        filter_page.assert_wellname_button(well)
        filter_page.select_object("Logs")
        filter_page.deselect_all_logs()
        # first log
        filter_page.select_log(log)
        filter_page.click_log(log)
        filter_page.select_logcurves(log)
        filter_page.click_log(log)
        # second log
        filter_page.select_log(second_log)
        filter_page.click_log(second_log)
        filter_page.select_logcurves(second_log)
        filter_page.click_log(second_log)
        # uncheck remaining objects
        filter_page.select_objects_and_select_all(Object_list)
        # extraction
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        time.sleep(5)
        home_page.select_module("/jobs")

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        job_page.assert_job_status(job_id)
        job_page.view_job(job_id)

        filter_page.select_object("Logs")
        job_page.assert_logs_checkbox_disabled(log)
        job_page.assert_logs_checkbox_disabled(second_log)


        well_id = f"{well}_{job_id}"
        wellbore_id = f"{wellbore_name}_{job_id}"

        job_page.click_on_wellname(well_id)
        job_page.click_on_wellbore(well_id, wellbore_id)
        # need to upadte with green color coordinates
        job_page.assert_logdata_intowitsml(well_id, wellbore_id, [log, second_log])



















