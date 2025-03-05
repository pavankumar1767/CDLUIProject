import random

from playwright.sync_api import expect
from pages.base_page import BasePage


class FilterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def input_field(self, text):
        element_xpath = f"//input[@ng-reflect-name='well_name']"
        self.fill(element_xpath, text, f"{text}")

    def scroll_down(self, field_name):
        element_xpath = f"//mat-icon[normalize-space()='{field_name}']"
        self.scroll_to_element(element_xpath, field_name)

    def click_search(self, button_text):
        element_xpath = f"//mat-icon[normalize-space()='{button_text}']"
        self.click(element_xpath, f"{button_text} Button")

    def select_well(self, well_name):
        element_xpath = f"//table[@class='mat-table cdk-table mat-sort filter-well-table']//td[normalize-space()='{well_name}']/preceding-sibling::td/mat-checkbox"
        self.scroll_to_element(element_xpath, "scroll down upto well name")
        self.click(element_xpath, f"{well_name}")

    def get_wellbore_name(self, well_name):
        element_xpath = f"//table[@class='mat-table cdk-table mat-sort filter-well-table']//td[normalize-space()='{well_name}']/ancestor::tr/td[3]"
        return self.get_text(element_xpath, f"{well_name} wellbore name")

    def assert_wellname_button(self, well_name):
        element_xpath = f"//button[normalize-space()='{well_name}']"
        assert self.get_text(element_xpath, f"{well_name}") == well_name

    def select_object(self, object_name):
        element_xpath = f"//mat-panel-title[normalize-space()='{object_name}']"
        self.click(element_xpath, f"{object_name}")

    def deselect_all_logs(self):
        input_locator = self.page.locator(
            "//div[@class='select-all-log']/mat-checkbox//input"
        )
        aria_checked = input_locator.get_attribute("aria-checked")
        print(aria_checked)
        if aria_checked == "true":
            element_xpath = f"//div[@class='select-all-log']/mat-checkbox"
            self.click(element_xpath, "select all logs")
        else:
            assert False, "Test failed: 'Select All Logs' checkbox is not in the checked state."

    def select_all_logs(self):
        input_locator = self.page.locator(
            "//div[@class='select-all-log']/mat-checkbox//input"
        )
        aria_checked = input_locator.get_attribute("aria-checked")
        print(aria_checked)
        if aria_checked == "false":
            element_xpath = f"//div[@class='select-all-log']/mat-checkbox"
            self.click(element_xpath, "select all logs")
        else:
            assert False, "Test failed: 'Select All Logs' checkbox is not in the deselected state."

    def select_log(self, log_name):
        input_locator = self.page.locator(
            f"//mat-panel-title[normalize-space()='{log_name}']//../mat-checkbox//input"
        )
        aria_checked = input_locator.get_attribute("aria-checked")
        if aria_checked == "false":
            logs_xpath = f"//mat-panel-title[normalize-space()='{log_name}']//../mat-checkbox"
            self.click(logs_xpath, f"{log_name}")
        else:
            assert False, f"Test failed: '{log_name}' checkbox is not in the deselected state."


    def click_log(self, log_name):
        select_log = f"//mat-panel-title[normalize-space()='{log_name}']"
        self.click(select_log, "select log")

    def select_logcurves(self, log_name):
        # XPath pattern to select specific checkboxes by index
        select_curves_xpath_pattern = f"(//mat-panel-title[normalize-space()='{log_name}']" \
                                      f"//ancestor::mat-expansion-panel-header/following-sibling::div" \
                                      f"//h4[normalize-space()='Select Curves:']//../mat-checkbox)[{{}}]/label"
        # Locate all matching checkbox elements
        all_checkboxes_locator = f"//mat-panel-title[normalize-space()='{log_name}']" \
                                 f"//ancestor::mat-expansion-panel-header/following-sibling::div" \
                                 f"//h4[normalize-space()='Select Curves:']//../mat-checkbox"
        all_checkboxes = self.page.locator(all_checkboxes_locator)
        # Get the total count of available checkboxes
        total_checkboxes = all_checkboxes.count()
        print(f"Total checkboxes found: {total_checkboxes}")
        if total_checkboxes == 0:
            print("No checkboxes found!")
            return
        # Determine a random count of checkboxes to select (between 1 and 20% of total)
        num_to_select = random.randint(1, max(1, int(total_checkboxes * 0.2)))
        print(f"Randomly selecting {num_to_select} checkboxes.")
        # Select random indices to choose checkboxes (1-based index for XPath)
        indices_to_select = random.sample(range(1, total_checkboxes + 1), num_to_select)
        print(f"Selecting checkbox indices: {indices_to_select}")
        # Click the checkboxes at the selected indices using the dynamic XPath
        for index in indices_to_select:
            select_curves_xpath = select_curves_xpath_pattern.format(index)
            checkbox = self.page.locator(select_curves_xpath)
            expect(checkbox).to_be_visible()
            checkbox.click()
            self._capture_screenshot(f"Selected checkbox at index {index}")
        print(f"Successfully selected {num_to_select} log curves.")

    def Button(self, button_text):
        element_xpath = f"//span[contains(normalize-space(), '{button_text}')]"
        self.click(element_xpath, f"{button_text}")

    def deselectAll_objects(self, data_object):
        input_locator = self.page.locator(
            f"//mat-panel-title[normalize-space()='{data_object}']//ancestor::mat-expansion-panel/div"
            "//mat-checkbox//span[contains(normalize-space(), 'Select All')]"
            "/preceding-sibling::span//input"
        )
        aria_checked = input_locator.get_attribute("aria-checked")
        if aria_checked == "true":
            element_xpath = f"//mat-panel-title[normalize-space()='{data_object}']//ancestor::mat-expansion-panel/div//mat-checkbox//span[contains(normalize-space(), 'Select All')]"
            self.click(element_xpath, f"{data_object} select all")
        else:
            assert False, f"Test failed: '{data_object}' checkbox is not in the checked state."

    def selectAll_objects(self, data_object):
        input_locator = self.page.locator(
            f"//mat-panel-title[normalize-space()='{data_object}']//ancestor::mat-expansion-panel/div"
            "//mat-checkbox//span[contains(normalize-space(), 'Select All')]"
            "/preceding-sibling::span//input"
        )
        aria_checked = input_locator.get_attribute("aria-checked")
        if aria_checked == "false":
            element_xpath = f"//mat-panel-title[normalize-space()='{data_object}']//ancestor::mat-expansion-panel/div//mat-checkbox//span[contains(normalize-space(), 'Select All')]"
            self.click(element_xpath, f"{data_object} select all")
        else:
            assert False, f"Test failed: '{data_object}' checkbox is not in the deselected state."

    def select_objects_and_select_all(self, object_names: list):
        for object_name in object_names:
            self.select_object(object_name)
            self.deselectAll_objects(object_name)

    def select_bharuns_checkboxes(self, data_object):
        # XPath pattern to select specific checkboxes by index, excluding "Select All"
        checkbox_xpath_pattern = f"(//mat-panel-title[normalize-space()='{data_object}']" \
                                 f"//ancestor::mat-expansion-panel/div" \
                                 f"//mat-checkbox[not(.//span[contains(normalize-space(), 'Select All')])])[{{}}]/label"
        # Create a locator for all checkboxes except the "Select All" checkbox
        checkboxes_locator = self.page.locator(
            f"//mat-panel-title[normalize-space()='{data_object}']"
            f"//ancestor::mat-expansion-panel/div"
            f"//mat-checkbox[not(.//span[contains(normalize-space(), 'Select All')])]"
        )
        # Get the total count of matching checkboxes
        total_checkboxes = checkboxes_locator.count()
        print(f"Total checkboxes found (excluding 'Select All'): {total_checkboxes}")
        if total_checkboxes == 0:
            print("No checkboxes found!")
            return
        # Randomly select a count of checkboxes (between 1 and 20% of the total)
        num_to_select = random.randint(1, max(1, int(total_checkboxes * 0.2)))
        print(f"Randomly selecting {num_to_select} checkboxes.")
        # Generate random indices for selection (1-based index for XPath)
        indices_to_select = random.sample(range(1, total_checkboxes + 1), num_to_select)
        print(f"Selecting checkbox indices: {indices_to_select}")
        # Click the checkboxes at the generated indices using the dynamic XPath
        for index in indices_to_select:
            checkbox_xpath = checkbox_xpath_pattern.format(index)
            checkbox = self.page.locator(checkbox_xpath)
            try:
                expect(checkbox).to_be_visible(timeout=5000)
                checkbox.click()
                self._capture_screenshot(f"Selected checkbox at index {index}")
                print(f"Checkbox at index {index} selected.")
            except Exception as e:
                print(f"Failed to select checkbox at index {index}: {e}")
        print(f"Successfully selected {num_to_select} checkboxes.")


