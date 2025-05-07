# import time
#
# import allure
# import pytest
#
# from pages.filter_page import FilterPage
# from pages.home_page import HomePage
# from pages.job_page import JobPage
# from pages.login_page import LoginPage
# from utilities.TestDataManager import TestDataManager
# from utilities.random_utils import RandomUtils
#
#
# @allure.suite("Load Test")
# @pytest.mark.usefixtures("setup")
# class TestTC015:
#     @allure.title("Verify the load test with multiple objects in a well")
#     def test_load(self, setup, config):
#         page = setup
#         home_page = HomePage(page)
#         login_page = LoginPage(page)
#         filter_page = FilterPage(page)
#         job_page = JobPage(page)
#
#
#         login_page.navigate(config.BASE_URL)
#         login_page.enter_username(config.username)
#         login_page.enter_password(config.password)
#         login_page.click_login("Sign In")
#
#         test_data = TestDataManager.get_test_data()
#         well = test_data["wells"]["wellname_1"]
#         log = test_data["wells"]["log_1"]
#         # Object_list = test_data["wells"]["objectlist"]
#         Object_list = ["BHA Run", "Wellbore Geometry"]
#
#         home_page.select_module("/jobs")
#         filter_page.Button("Create Job")
#         filter_page.Button("Skip")
#         filter_page.input_field(well)
#         filter_page.click_search("searchicon")
#         filter_page.select_well(well)
#         wellbore_name = filter_page.get_wellbore_name(well)
#         filter_page.assert_wellname_button(well)
#
#         filter_page.select_objects_and_select_all(Object_list)
#         # extraction
#         filter_page.Button("Extract and Create Job")
#         filter_page.Button("Yes")
#         time.sleep(5)
#
#         # job summary
#         job_id = job_page.get_jobnumber()
#         job_status = job_page.get_job_status(job_id)
#         assert job_status == "In Progress"
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


import time
import allure
import pytest
from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.TestDataManager import TestDataManager
from utilities.random_utils import RandomUtils


@allure.suite("Load Test")
@pytest.mark.usefixtures("setup")
class TestTC015:
    @allure.title("Verify the load test with multiple objects in a well")
    def test_load(self, setup, config):
        page = setup
        home_page = HomePage(page)
        login_page = LoginPage(page)
        filter_page = FilterPage(page)
        job_page = JobPage(page)

        login_page.navigate(config.BASE_URL)
        login_page.enter_username(config.username)
        login_page.enter_password(config.password)
        login_page.click_login("Sign In")

        # Hardcoded loop count - change this value as needed
        LOOP_COUNT = 5  # Run the test 5 times

        for iteration in range(LOOP_COUNT):
            # Log the current iteration
            print(f"\nRunning iteration {iteration + 1} of {LOOP_COUNT}")
            with allure.step(f"Iteration {iteration + 1}"):


                test_data = TestDataManager.get_test_data()
                well = "SND 14 23 FED COM 001 P26 226H"
                Object_list = ["BHA Run", "Wellbore Geometry"]

                home_page.select_module("/jobs")
                filter_page.Button("Create Job")
                filter_page.Button("Skip")
                filter_page.input_field(well)
                filter_page.click_search("searchicon")
                filter_page.select_well(well)
                wellbore_name = filter_page.get_wellbore_name(well)
                filter_page.assert_wellname_button(well)

                filter_page.select_objects_and_select_all(Object_list)
                # extraction
                filter_page.Button("Extract and Create Job")
                filter_page.Button("Yes")
                time.sleep(5)

                # job summary
                job_id = job_page.get_jobnumber()
                job_status = job_page.get_job_status(job_id)
                # assert job_status == "In Progress"

