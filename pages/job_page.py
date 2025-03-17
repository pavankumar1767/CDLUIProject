import random
import time
from pages.base_page import BasePage


class JobPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def get_jobnumber(self):
        element_xpath = "//table[@class='mat-table cdk-table mat-sort jobs-table']/tbody/tr[1]/td[1]/span"
        return self.get_text(element_xpath, "job id")

    def get_job_status(self, job_number):
        element_xpath = f"//table[@class='mat-table cdk-table mat-sort jobs-table']/tbody/tr/td/span[text()='{job_number}']/ancestor::tr/td[2]"
        return self.get_text(element_xpath, f"{job_number} status")

    def assert_job_status(self, job_number):
        max_attempts = 15  # Number of times to retry (30 attempts = 30 minutes)
        for attempt in range(max_attempts):
            job_status = self.get_job_status(job_number)  # Replace with the actual method to fetch job status
            if job_status == "Completed":
                assert job_status == "Completed"
                print("Job status is completed.")
                break
            print(f"Attempt {attempt + 1}: Status is '{job_status}'. Refreshing...")
            element_xpath = "//mat-icon[normalize-space()='refresh']"
            self.click(element_xpath, "refresh")
            time.sleep(60)  # Wait for 60 seconds before the next attempt
        else:
            raise TimeoutError(f"Job status did not reach 'Completed' after {max_attempts} attempts.")


    def view_job(self, job_number):
        element_xpath = f"//table[@class='mat-table cdk-table mat-sort jobs-table']/tbody/tr/td/span[text()='{job_number}']/ancestor::tr/td[6]/button[1]"
        self.click(element_xpath, f"job {job_number} view")

    def assert_logs_checkbox_disabled(self, object_name):
        input_locator = self.page.locator(f"//mat-panel-title[normalize-space()='{object_name}']//../mat-checkbox//input")
        assert input_locator.is_disabled(), f"The input field for '{object_name}' is not disabled."
        print(f"The input field for '{object_name}' is correctly disabled.")


    def assert_objects_checkbox_disabled(self, object_name: str):
        # Locate all matching input elements for the given object name
        input_locators = self.page.locator(
            f"//mat-panel-title[normalize-space()='{object_name}']/ancestor::mat-expansion-panel//input"
        )
        # Get all input elements as a list
        elements = input_locators.element_handles()
        # Check if no elements are found
        assert elements, f"No input elements found for '{object_name}'."
        # Iterate through all elements and assert they are disabled
        for index, element in enumerate(elements, start=1):
            is_disabled = element.is_disabled()
            assert is_disabled, f"Input field {index} for '{object_name}' is not disabled."
            print(f"Input field {index} for '{object_name}' is correctly disabled.")

    def click_on_wellname(self, well_name):
        element_xpath = f"//button[contains(normalize-space(),'{well_name}')]"
        self.click(element_xpath, f"{well_name}")

    def click_on_wellbore(self, well_name, wellbore_name):
        element_xpath = f"//button[contains(normalize-space(),'{well_name}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore_name}')]"
        self.click(element_xpath, f"{wellbore_name}")

    def assert_logdata_intowitsml(self, well, wellbore, log: list):
        element_xpath = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')])[1]"
        self.click(element_xpath, "open log")
        for logs in log:
            element_xpath_log = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')]/parent::li/ul/li[contains(normalize-space(),'{logs}')]/span)[1]"
            color_dot = self.page.locator(element_xpath_log)
            background_color = color_dot.evaluate("element => getComputedStyle(element).backgroundColor")
            expected_green_color = "rgb(10, 206, 115)"  # Update this if the green color code differs
            assert background_color == expected_green_color, (
                f"Test failed: Expected green color '{expected_green_color}', "
                f"but found '{background_color}'."
        )

    def assert_data_intowitsml(self, object_name, well, wellbore):
        # Click to open the log based on well, wellbore, and object_name
        element_xpath = (
            f"//button[contains(normalize-space(),'{well}')]/parent::h2"
            f"/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]"
            f"/parent::li/ul/li/span[contains(normalize-space(),'{object_name}')]"
        )
        self.click(element_xpath, "open log")

        # XPath to locate all color dots under the specified log
        element_xpath_log = (
            f"//button[contains(normalize-space(),'{well}')]/parent::h2"
            f"/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]"
            f"/parent::li/ul/li/span[contains(normalize-space(),'{object_name}')]"
            f"/parent::li/ul/li/span"
        )
        # Locate all elements matching the XPath
        color_dots = self.page.locator(element_xpath_log)
        elements = color_dots.element_handles()  # Get all elements as a list
        # Check if elements are found
        assert elements, f"No elements found for '{object_name}' under well '{well}' and wellbore '{wellbore}'."
        expected_green_color = "rgb(10, 206, 115)"  # Expected color code (Red color in this case)
        # Loop through each element and assert the background color
        for index, element in enumerate(elements, start=1):
            background_color = element.evaluate("el => getComputedStyle(el).backgroundColor")
            assert background_color == expected_green_color, (
                f"Test failed: Element {index} expected color '{expected_green_color}', but found '{background_color}'."
            )
            print(f"Element {index} background color is correct: {background_color}")




