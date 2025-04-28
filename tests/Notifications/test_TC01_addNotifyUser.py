import time

import allure
import pytest

from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.TestDataManager import TestDataManager
from utilities.random_utils import RandomUtils


@allure.suite("Notifications")
@pytest.mark.usefixtures("setup")
class TestTC01:
    @allure.title("Verify that Adding Notify User list and In-App notifications are received.")
    def test_add_notify_user(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        notifyUser = RandomUtils.get_email()

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")



        test_data = TestDataManager.get_test_data()
        well = test_data["wells"]["wellname_1"]
        Object_list = test_data["wells"]["RigObjectlist"]
        data_Object = "Rig"

        home_page.select_module("/jobs")
        filter_page.Button("Create Job")
        filter_page.Button("Skip")
        filter_page.input_field(well)
        filter_page.click_search("searchicon")
        filter_page.select_well(well)
        wellbore_name = filter_page.get_wellbore_name(well)
        filter_page.assert_wellname_button(well)
        filter_page.select_object(data_Object)
        filter_page.deselectAll_objects(data_Object)
        filter_page.select_ObjectCheckbox(data_Object, ["PATTERSON_257"])
        filter_page.select_object(data_Object)
        filter_page.select_objects_and_select_all(Object_list)

        # notify user
        filter_page.enterNotifyUser([notifyUser])

        # extraction
        filter_page.Button("Extract and Create Job")
        filter_page.Button("Yes")
        time.sleep(5)

        # job summary
        job_id = job_page.get_jobnumber()
        job_page.job_status(job_id)
        job_status = job_page.get_job_status(job_id)


        job_page.view_job(job_id)

        filter_page.select_object(data_Object)
        job_page.assert_objects_checkbox_disabled(data_Object)



        if job_status == "Completed":
            expected_partials = ["completed successfully", f"New job {job_id} started"]
            job_page.assert_job_status_notifications(job_id, expected_partials)
        elif job_status == "Failed":
            expected_partials = ["failed", f"New job {job_id} started"]
            job_page.assert_job_status_notifications(job_id, expected_partials)
        else:
            print(f"⏳ Job {job_id} is still in progress... Current status: '{job_status}'")
            raise Exception(f"Job {job_id} has not yet completed or failed. Current status: '{job_status}'")

        job_page.assert_added_notifyuser(notifyUser)

        # Notifications
        home_page.select_module("/notifications")
        job_page.search_by_job(str(job_id))
        job_page.search_icon()
        if job_status == "Completed":
            expected_partials = ["completed successfully", f"New job {job_id} started"]
            job_page.status_notifications(job_id, expected_partials)
        elif job_status == "Failed":
            expected_partials = ["failed", f"New job {job_id} started"]
            job_page.status_notifications(job_id, expected_partials)















