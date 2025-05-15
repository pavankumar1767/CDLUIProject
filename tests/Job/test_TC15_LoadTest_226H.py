import time
import allure
import pytest
from pages.filter_page import FilterPage
from pages.home_page import HomePage
from pages.job_page import JobPage
from pages.login_page import LoginPage
from utilities.TestDataManager import TestDataManager


@allure.suite("Load Test")
@pytest.mark.usefixtures("setup")
class TestTC015:
    @allure.title("Verify the load test with multiple objects in a well")
    @pytest.mark.repeat(3)  # This will run the test 5 times
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

        filter_name = "Load_SND_2261"

        home_page.select_module("/jobs")
        filter_page.Button("Create Job")
        job_page.select_filter(filter_name)


        # extraction
        filter_page.Button("Save and Create Job")
        filter_page.Button("Yes")
        time.sleep(1)

        # job summary
        job_id = job_page.get_jobnumber()
        job_status = job_page.get_job_status(job_id)
        # assert job_status == "In Progress"