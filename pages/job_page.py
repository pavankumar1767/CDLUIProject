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
        max_attempts = 10  # Number of times to retry (30 attempts = 30 minutes)
        for attempt in range(max_attempts):
            job_status = self.get_job_status(job_number)  # Replace with the actual method to fetch job status
            if job_status == "Completed":
                assert job_status == "Completed"
                print("Job status is completed.")
                break
            elif job_status == "Failed":
                assert job_status == "Failed"  # Explicitly fail the test case
                print("Job status is 'Failed'. Test case will fail.")
                raise AssertionError(f"Job status is 'Failed'.")
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
        element_xpath = f"//button[contains(normalize-space(),'{well_name}')]/span[normalize-space()='+']"
        self.click(element_xpath, f"{well_name}")

    def click_on_wellbore(self, well_name, wellbore_name):
        element_xpath = f"//button[contains(normalize-space(),'{well_name}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore_name}')]/span[normalize-space()='+']"
        self.click(element_xpath, f"{wellbore_name}")

    def assert_logdata_intowitsml(self, well, wellbore, log: list):
        element_xpath = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')])[1]/span[normalize-space()='+']"
        self.click(element_xpath, "open log")
        for logs in log:
            element_xpath_log = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')]/parent::li/ul/li[contains(normalize-space(),'{logs}')]/span)[2]"
            color_dot = self.page.locator(element_xpath_log)
            background_color = color_dot.evaluate("element => getComputedStyle(element).backgroundColor")
            expected_green_color = "rgb(10, 206, 115)"  # Update this if the green color code differs
            assert background_color == expected_green_color, (
                f"Test failed: Expected green color '{expected_green_color}', "
                f"but found '{background_color}'."
        )

    def assert_logdata_failed_intowitsml(self, well, wellbore, log: list):
        element_xpath = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')])[1]/span[normalize-space()='+']"
        self.click(element_xpath, "open log")
        for logs in log:
            element_xpath_log = f"(//button[contains(normalize-space(),'{well}')]/parent::h2/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]/parent::li/ul/li/span[contains(normalize-space(),'Log')]/parent::li/ul/li[contains(normalize-space(),'{logs}')]/span)[2]"
            color_dot = self.page.locator(element_xpath_log)
            background_color = color_dot.evaluate("element => getComputedStyle(element).backgroundColor")
            expected_green_color = "rgb(249, 102, 102)"  # Update this if the green color code differs
            assert background_color == expected_green_color, (
                f"Test failed: Expected Red color '{expected_green_color}', "
                f"but found '{background_color}'."
        )

    def assert_data_intowitsml(self, object_name, well, wellbore):
        # Click to open the log based on well, wellbore, and object_name
        element_xpath = (
            f"//button[contains(normalize-space(),'{well}')]/parent::h2"
            f"/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]"
            f"/parent::li/ul/li/span[contains(normalize-space(),'{object_name}')]/span[normalize-space()='+']"
        )
        self.click(element_xpath, "open log")

        # XPath to locate all color dots under the specified log
        element_xpath_log = (
            f"//button[contains(normalize-space(),'{well}')]/parent::h2"
            f"/following-sibling::div//span[contains(normalize-space(),'{wellbore}')]"
            f"/parent::li/ul/li/span[contains(normalize-space(),'{object_name}')]"
            f"/parent::li/ul/li/span[2]"
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

    def job_status(self, job_number):
        max_attempts = 20  # Number of times to retry (30 attempts = 30 minutes)
        for attempt in range(max_attempts):
            job_status = self.get_job_status(job_number)  # Replace with the actual method to fetch job status
            if job_status == "Completed":
                assert job_status == "Completed"
                print("Job status is completed.")
                break
            elif job_status == "Failed":
                assert job_status == "Failed"  # Explicitly fail the test case
                print("Job status is 'Failed'. Test case will fail.")
                break
            print(f"Attempt {attempt + 1}: Status is '{job_status}'. Refreshing...")
            element_xpath = "//mat-icon[normalize-space()='refresh']"
            self.click(element_xpath, "refresh")
            time.sleep(60)  # Wait for 60 seconds before the next attempt
        else:
            raise TimeoutError(f"Job status did not reach 'Completed' after {max_attempts} attempts.")

    # def assert_job_status_notifications(self, job_number: int, expected_status: str):
    #     """
    #     Verifies if the job notification shows either success or failure based on expected status.
    #
    #     :param job_number: The job number to look for
    #     :param expected_status: Expected status, e.g., 'completed', 'completed successfully', or 'failed'
    #     """
    #     notification_xpath = (
    #         "//h3[normalize-space()='Job Notifications']/parent::div/"
    #         "following-sibling::div[@class='notified-users-table']/table/tbody/tr/td[2]"
    #     )
    #
    #     notifications = self.page.locator(notification_xpath)
    #     actual_messages = notifications.all_inner_texts()
    #     actual_messages = [msg.strip().lower() for msg in actual_messages]
    #
    #     print("📥 Notifications fetched:")
    #     for msg in actual_messages:
    #         print(f"  • {msg}")
    #
    #     job_str = f"job {job_number}".lower()
    #     expected_keywords = expected_status.lower().split()
    #
    #     for msg in actual_messages:
    #         if job_str in msg and all(word in msg for word in expected_keywords):
    #             print(f"✅ Found expected status '{expected_status}' for Job {job_number}")
    #             return
    #
    #     assert False, f"❌ No notification found for Job {job_number} with status containing: '{expected_status}'"


    # def assert_job_status_notifications(self, job_number: int, expected_partials: list):
    #     # XPath for all job-related notifications (job_number in 2nd column, actual message in 3rd)
    #     notification_xpath = "//h3[normalize-space()='Job Notifications']/parent::div/following-sibling::div[@class='notified-users-table']/table/tbody/tr/td[2]"
    #
    #     notifications = self.get_text_list(notification_xpath, "Job Notifications")
    #     for note in notifications:
    #         print(f"• {note}")
    #
    #     # Assert each expected partial is found in at least one notification
    #     for expected_text in expected_partials:
    #         if not any(expected_text.lower() in n.lower() for n in notifications):
    #             raise AssertionError(f"Expected text '{expected_text}' not found in notifications!")
    #         else:
    #             print(f"[✓] '{expected_text}' found ✅")

    def assert_job_status_notifications(self, job_number: int, expected_partials: list, require_all=True):

        # XPath for job notifications
        notification_xpath = "//h3[normalize-space()='Job Notifications']/parent::div/following-sibling::div[@class='notified-users-table']/table/tbody/tr/td[2]"

        notifications = self.get_text_list(notification_xpath, "Job Notifications")

        # Print found notifications for debugging
        print(f"\nFound {len(notifications)} notifications for job {job_number}:")
        for i, note in enumerate(notifications, 1):
            print(f"{i}. {note}")

        if require_all:
            # STRICT MODE: All expected messages must be present
            missing = [msg for msg in expected_partials
                       if not any(msg.lower() in n.lower() for n in notifications)]

            if missing:
                raise AssertionError(
                    f"Missing required notifications for job {job_number}:\n"
                    f"Expected ALL of: {expected_partials}\n"
                    f"Missing: {missing}\n"
                    f"Actual notifications: {notifications}"
                )
            print(f"[✓] All expected notifications found: {expected_partials}")
        else:
            # LENIENT MODE: At least one expected message must be present
            found = [msg for msg in expected_partials
                     if any(msg.lower() in n.lower() for n in notifications)]

            if not found:
                raise AssertionError(
                    f"No expected notifications found for job {job_number}:\n"
                    f"Expected ANY of: {expected_partials}\n"
                    f"Actual notifications: {notifications}"
                )
            print(f"[✓] Found expected notifications: {found}")

    # def status_notifications(self, job_number: int, expected_partials: list):
    #     # XPath for all job-related notifications (job_number in 2nd column, actual message in 3rd)
    #     notification_xpath = (
    #         f"//h2[normalize-space()='Notifications']/parent::div/following-sibling::div[@class='notifications-table-container']//table/tbody/tr[td[2][normalize-space() = '{job_number}']]/td[3]"
    #     )
    #
    #     notifications = self.get_text_list(notification_xpath, "Job Notifications")
    #     for note in notifications:
    #         print(f"• {note}")
    #
    #     # Assert each expected partial is found in at least one notification
    #     for expected_text in expected_partials:
    #         if not any(expected_text.lower() in n.lower() for n in notifications):
    #             raise AssertionError(f"Expected text '{expected_text}' not found in notifications!")
    #         else:
    #             print(f"[✓] '{expected_text}' found ✅")

    def status_notifications(self, job_number: int, expected_partials: list):

        # XPath for job notifications
        notification_xpath = (
            f"//h2[normalize-space()='Notifications']/parent::div/following-sibling::div"
            f"[@class='notifications-table-container']//table/tbody/"
            f"tr[td[2][normalize-space() = '{job_number}']]/td[3]"
        )

        notifications = self.get_text_list(notification_xpath, "Job Notifications")

        # Print all found notifications for debugging
        print(f"\nFound {len(notifications)} notifications for job {job_number}:")
        for i, note in enumerate(notifications, 1):
            print(f"{i}. {note}")

        # Check ALL expected texts are present in ANY notification
        missing_messages = [
            msg for msg in expected_partials
            if not any(msg.lower() in n.lower() for n in notifications)
        ]

        if missing_messages:
            raise AssertionError(
                f"Missing expected notifications:\n"
                f"Expected: {expected_partials}\n"
                f"Missing: {missing_messages}\n"
                f"Actual notifications: {notifications}"
            )

        print(f"[✓] All expected notifications found: {expected_partials}")

    def assert_added_notifyuser(self, user):

        notification_user_xpath = "//h3[normalize-space()='Notified User List']/parent::div/following-sibling::div[@class='notified-users-table']/table/tbody/tr/td[2]"
        Added_user = self.get_text(notification_user_xpath, f"{notification_user_xpath}")
        assert Added_user == user

    def search_by_job(self, text):
        element_xpath = "//input[@data-placeholder='Search by job number']"
        self.fill(element_xpath,text,f"{text}")

    def search_icon(self):
        element_xpath = "//mat-icon[normalize-space()='search']"
        self.click(element_xpath, "search icon")


    def assert_job_failed_due_to_config(self, job_number):

        max_attempts = 20  # Number of times to retry (30 attempts = 30 minutes)
        for attempt in range(max_attempts):
            job_status = self.get_job_status(job_number)  # Replace with the actual method to fetch job status
            if job_status == "Failed":
                assert job_status == "Failed"  # Explicitly fail the test case
                print("Job status is 'Failed'")
                break
            elif job_status == "Completed":
                assert job_status == "Completed"
                print("Job status is completed. Test case will fail")
                raise AssertionError(f"Job status is 'Completed'.")
            print(f"Attempt {attempt + 1}: Status is '{job_status}'. Refreshing...")
            element_xpath = "//mat-icon[normalize-space()='refresh']"
            self.click(element_xpath, "refresh")
            time.sleep(60)  # Wait for 60 seconds before the next attempt
        else:
            raise TimeoutError(f"Job status did not reach 'Failed' after {max_attempts} attempts.")

    def get_error_msg(self):
        element_xpath = "//p[@class='error-msg']"
        text = self.get_text(element_xpath, "error message")
        return text